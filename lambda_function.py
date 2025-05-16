import json
import boto3

#The code Lambda runs in AWS
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    obj_metadata = s3.head_object(Bucket=bucket_name, Key=object_key)
    size = obj_metadata['ContentLength']
    created_time = obj_metadata['LastModified']

    message = f"📦 New object uploaded:\n\nBucket: {bucket_name}\nKey: {object_key}\nSize: {size} bytes\nUploaded at: {created_time}"

    sns.publish(
        TopicArn='arn:aws:sns:ap-south-1:010928211412:s3-upload-alerts',  # replace later
        Message=message,
        Subject="🆕 New S3 Upload Notification"
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent!')
    }