import boto3
import json
import time
import os

def create_sns_topic(topic_name, email):
    sns = boto3.client('sns')
    
    # Create SNS topic
    topic_response = sns.create_topic(Name=topic_name)
    topic_arn = topic_response['TopicArn']
    print(f"SNS Topic Created: {topic_arn}")

    # Subscribe your email
    sub_response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',  # use 'sms' for phone alerts
        Endpoint=email
    )
    print(f" Subscription initiated. Please confirm from your inbox: {email}")

    return topic_arn





def create_lambda_iam_role(role_name):
    iam = boto3.client('iam')

    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }

    try:
        role = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy)
        )
        print(f" IAM Role '{role_name}' created.")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f" IAM Role '{role_name}' already exists.")
        role = iam.get_role(RoleName=role_name)

    # Attach Policies
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    )
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
    )
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn='arn:aws:iam::aws:policy/AmazonSNSFullAccess'
    )

    print(" Policies attached.")

    # Wait for role to propagate
    time.sleep(10)
    return role['Role']['Arn']

#The script you run locally to create/upload that Lambda
def create_lambda_function(function_name, role_arn):
    lambda_client = boto3.client('lambda')

    if not os.path.exists("function.zip"):
        print("ERROR: 'function.zip' not found. Please run: zip function.zip lambda_function.py")
        return

    with open("function.zip", 'rb') as f:
        zipped_code = f.read()

    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.12',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zipped_code},
            Timeout=10,
            MemorySize=128,
            Publish=True
        )
        print(f" Lambda function '{function_name}' created.")
    except lambda_client.exceptions.ResourceConflictException:
        print(f" Lambda function '{function_name}' already exists.")

def add_lambda_permission(bucket_name, function_name):
    lambda_client = boto3.client('lambda')
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()["Account"]

    statement_id = 's3invoke'
    try:
        response = lambda_client.add_permission(
            FunctionName=function_name,
            StatementId=statement_id,
            Action='lambda:InvokeFunction',
            Principal='s3.amazonaws.com',
            SourceArn=f'arn:aws:s3:::{bucket_name}',
            SourceAccount=account_id
        )
        print(f" Added permission for S3 to invoke Lambda: {response['Statement']}")
    except lambda_client.exceptions.ResourceConflictException:
        print(" Lambda permission already exists. Skipping...")




def add_s3_event_notification(bucket_name, function_arn):
    s3 = boto3.client('s3')

    notification_config = {
        'LambdaFunctionConfigurations': [
            {
                'LambdaFunctionArn': function_arn,
                'Events': ['s3:ObjectCreated:*']
            }
        ]
    }

    s3.put_bucket_notification_configuration(
        Bucket=bucket_name,
        NotificationConfiguration=notification_config
    )
    print(f"✅ S3 bucket '{bucket_name}' is now triggering Lambda on upload.")


if __name__ == "__main__":
    bucket_name = "sns-virtuecloud"
    function_name = "s3-upload-alert"

    # Call the function
    topic_arn = create_sns_topic("s3-upload-alerts", "nakul.desai@virtuecloud.io")
    role_arn = create_lambda_iam_role("lambda-s3-role")
    create_lambda_function(function_name, role_arn)

    add_lambda_permission(bucket_name, function_name)
    time.sleep(10)

    lambda_client = boto3.client('lambda')
    function_arn = lambda_client.get_function(FunctionName=function_name)['Configuration']['FunctionArn']

    add_s3_event_notification(bucket_name, function_arn)
