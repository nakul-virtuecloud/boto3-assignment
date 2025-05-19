#start and stop ec2 using cron job 
#1. Create IAM Role for Lambda
#2. Create Lambda Function to start and stop ec2
#4. Create EventBridge Rule to Start EC2
#5. Create EventBridge Rule to Stop EC2
#EC2 starts → runs for ~3 mins → stops → off for ~3 mins → repeats

import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='ap-south-1')  # change region
    instance_id = 'i-0abc123def456ghij'  # replace with your instance ID
    action = event.get('action', 'stop')  # default to stop

    if action == 'start':
        ec2.start_instances(InstanceIds=[instance_id])
        return f"Started instance {instance_id}"
    elif action == 'stop':
        ec2.stop_instances(InstanceIds=[instance_id])
        return f"Stopped instance {instance_id}"
    else:
        return "Invalid action"
