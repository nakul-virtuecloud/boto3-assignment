import boto3
import json
import time

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

# Call the function
topic_arn = create_sns_topic("s3-upload-alerts", "nakul.desai@virtuecloud.io")



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
        print(f"✅ IAM Role '{role_name}' created.")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"ℹ️ IAM Role '{role_name}' already exists.")
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

role_arn = create_lambda_iam_role("s3-upload-lambda-role")
create_lambda_function("s3-upload-alert", role_arn)
