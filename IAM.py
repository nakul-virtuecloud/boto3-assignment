# import boto3

# r1 = boto3.resource('iam')
# for role in r1.roles.all():
#     print(role)

import boto3
from botocore.exceptions import ClientError

iam = boto3.client('iam')

# Create IAM User
def create_iam_user(user_name):
    try:
        iam.create_user(UserName=user_name)
        print(f"IAM user '{user_name}' created successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f"User '{user_name}' already exists. Skipping creation.")
        else:
            print(" Error creating IAM user:", e)

# 🧪 Test script
if __name__ == "__main__":
    user = "nakul-boto3-user"
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"

    create_iam_user(user)