import boto3
from botocore.exceptions import ClientError

iam = boto3.client('iam')


def create_iam_user(user_name):
    try:
        iam.create_user(UserName=user_name)
        print(f" IAM user '{user_name}' created.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f" IAM user '{user_name}' already exists.")
        else:
            raise e


def create_iam_group(group_name):
    try:
        iam.create_group(GroupName=group_name)
        print(f" IAM group '{group_name}' created.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f" IAM group '{group_name}' already exists.")
        else:
            raise e


def attach_policy_to_group(group_name, policy_arn):
    try:
        iam.attach_group_policy(
            GroupName=group_name,
            PolicyArn=policy_arn
        )
        print(f" Policy '{policy_arn}' attached to group '{group_name}'.")
    except ClientError as e:
        print(f" Failed to attach policy: {e}")


def add_user_to_group(user_name, group_name):
    try:
        iam.add_user_to_group(
            GroupName=group_name,
            UserName=user_name
        )
        print(f" User '{user_name}' added to group '{group_name}'.")
    except ClientError as e:
        print(f" Failed to add user to group: {e}")


if __name__ == "__main__":
    user_name = "nakul-group-user"
    group_name = "S3FullAccessGroup"
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"

    create_iam_user(user_name)
    create_iam_group(group_name)
    attach_policy_to_group(group_name, policy_arn)
    add_user_to_group(user_name, group_name)
