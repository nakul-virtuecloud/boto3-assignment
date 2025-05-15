# testing bucket
# import boto3

# s3 = boto3.resource('s3')

# for bucket in s3.buckets.all():
#     print(bucket.name)

#===============start=====================


import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region=None):
    """
    Create an S3 bucket if it doesn't already exist.
    """
    s3_client = boto3.client('s3', region_name=region or 'us-east-1')
    try:
        # Check if the bucket already exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists. Skipping creation.")
        return False

    except ClientError as e:
        error_code = int(e.response['Error']['Code'])

        # If the bucket doesn't exist (404), then create it
        if error_code == 404:
            try:
                if region is None or region == 'us-east-1':
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    location = {'LocationConstraint': region}
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration=location
                    )
                print(f" Bucket '{bucket_name}' created successfully in region '{region or 'us-east-1'}'")
                return True
            except ClientError as create_error:
                print(" Error creating bucket:", create_error)
                return False
        else:
            print(" Unexpected error checking bucket:", e)
            return False


def s3_list():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    print(" Available S3 Buckets:")
    for bucket in response['Buckets']:
        print(" -", bucket['Name'])

def upload(bucket_name, file_name, object_name):
    try:
        s3 = boto3.client('s3')
        s3.upload_file(file_name, bucket_name, object_name)
        print(f" Uploaded '{file_name}' to bucket '{bucket_name}' as '{object_name}'")
    except ClientError as e:
        print(" Error uploading file:", e)

def delete_object(bucket_name, object_name):
    try:
        s3 = boto3.client('s3')
        s3.delete_object(Bucket=bucket_name, Key=object_name)
        print(f" Deleted object '{object_name}' from bucket '{bucket_name}'")
    except ClientError as e:
        print(" Error deleting object:", e)

def delete_bucket(bucket_name):
    try:
        s3 = boto3.client('s3')
        
        # Must first delete all objects before deleting bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f" Deleted object '{obj['Key']}'")

        s3.delete_bucket(Bucket=bucket_name)
        print(f" Bucket '{bucket_name}' deleted successfully")
    except ClientError as e:
        print(" Error deleting bucket:", e)

# 🧪 Example usage with user confirmation
if __name__ == "__main__":
    bucket = "nakul-boto3-bucket-9795"
    region = "ap-south-1"
    local_file = "testfile.txt"
    object_name = "uploaded_testfile.txt"

    # Create test file
    with open(local_file, "w") as f:
        f.write("Hello from Nakul!")

    # 1. Create Bucket
    create_bucket(bucket, region)

    # 2. List Buckets
    s3_list()

    # 3. Upload File
    upload(bucket, local_file, object_name)

    # 4. Wait for user input before deleting object
    confirm = input(f"\n👀 Confirm deletion of object '{object_name}' from bucket '{bucket}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        delete_object(bucket, object_name)
    else:
        print(" Skipping object deletion.")

    # 5. Wait for user input before deleting bucket
    confirm = input(f"\n👀 Confirm deletion of bucket '{bucket}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        delete_bucket(bucket)
    else:
        print(" Skipping bucket deletion.")




#===============END=====================


# import boto3
# from botocore.exceptions import ClientError

# def create_bucket(bucket_name, region=None):
#     """
#     Create an S3 bucket in the specified region.

#     :param bucket_name: Name of the bucket (must be globally unique)
#     :param region: AWS region (e.g., 'ap-south-1'). Defaults to us-east-1.
#     :return: True if bucket created successfully, else False
#     """
#     try:
#         if region is None:
#             # Default region: us-east-1
#             s3_client = boto3.client('s3')
#             s3_client.create_bucket(Bucket=bucket_name)
#         else:
#             # Custom region
#             s3_client = boto3.client('s3', region_name=region)
#             location = {'LocationConstraint': region}
#             s3_client.create_bucket(
#                 Bucket=bucket_name,
#                 CreateBucketConfiguration=location
#             )
#         print(f"✅ Bucket '{bucket_name}' created successfully in region '{region or 'us-east-1'}'")
#         return True

#     except ClientError as e:
#         print("❌ Error creating bucket:", e)
#         return False

# def s3_list():
#     """
#     List all S3 buckets in the account.
#     """
#     s3 = boto3.client('s3')
#     response = s3.list_buckets()
#     print("📦 Available S3 Buckets:")
#     for bucket in response['Buckets']:
#         print(" -", bucket['Name'])
#     return None

# def upload(bucket_name, file_name, object_name):
#     """
#     Upload a file to a specific S3 bucket.

#     :param bucket_name: Target S3 bucket
#     :param file_name: Local file to upload
#     :param object_name: S3 object name (key)
#     """
#     try:
#         s3 = boto3.client('s3')
#         s3.upload_file(file_name, bucket_name, object_name)
#         print(f"📤 Uploaded '{file_name}' to bucket '{bucket_name}' as '{object_name}'")
#     except ClientError as e:
#         print("❌ Error uploading file:", e)
#     return None

# # 🧪 Example usage
# if __name__ == "__main__":
#     bucket = "nakul-boto3-bucket-9795"
#     region = "ap-south-1"

#     create_bucket(bucket, region)
#     s3_list()
#     upload(bucket, "testfile.txt", "uploaded_testfile.txt")


