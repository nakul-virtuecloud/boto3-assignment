import boto3
import json

sns = boto3.client('sns')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))

    topic_arn = "arn:aws:sns:ap-south-1:010928211412:s3-upload-alerts"

    for record in event['Records']:
        s3_info = record['s3']
        bucket = s3_info['bucket']['name']
        key = s3_info['object']['key']

        message = f" New file uploaded: s3://{bucket}/{key}"
        subject = " S3 Upload Alert"

        sns.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Notification Sent!')
    }
