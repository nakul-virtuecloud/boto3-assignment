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

#Attach Policy to IAM User (like 'AmazonS3ReadOnlyAccess')
def attach_policy(user_name, policy_arn):
    try:
        iam.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
        print(f" Attached policy '{policy_arn}' to user '{user_name}'.")
    except ClientError as e:
        print(" Error attaching policy:", e)

#  List IAM Users
def list_iam_users():
    try:
        response = iam.list_users()
        print(" IAM Users:")
        for user in response['Users']:
            print(" -", user['UserName'])
    except ClientError as e:
        print(" Error listing IAM users:", e)

# Test script
if __name__ == "__main__":
    user = "nakul-boto3-user"
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"

    create_iam_user(user)
    list_iam_users()

    confirm = input(f"Attach S3 read-only policy to '{user}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        attach_policy(user, policy_arn)