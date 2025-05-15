import boto3

r1 = boto3.resource('iam')
for role in r1.roles.all():
    print(role)