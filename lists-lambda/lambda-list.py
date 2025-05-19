#listing lambda functions by extracting .json
import boto3
import json
import os

# Define the path to the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the JSON file in the same folder
json_file_path = os.path.join(script_dir, 'lambda_functions.json')

# Initialize Lambda client
lambda_client = boto3.client('lambda', region_name='us-east-1')

# List all Lambda functions
def list_lambda_functions():
    functions = []
    paginator = lambda_client.get_paginator('list_functions')
    for page in paginator.paginate():
        for function in page['Functions']:
            functions.append({
                'FunctionName': function['FunctionName'],
                'Runtime': function['Runtime'],
                'Handler': function['Handler'],
                'LastModified': function['LastModified'],
                'MemorySize': function['MemorySize'],
                'Timeout': function['Timeout'],
                'Role': function['Role'],
                'Description': function.get('Description', '')
            })
    return functions

# Get the Lambda list
lambda_functions = list_lambda_functions()
print(json.dumps(lambda_functions, indent=2))

# Write the list to lambda_functions.json in the same folder
with open(json_file_path, 'w') as f:
    json.dump(lambda_functions, f, indent=2)



# import boto3
# lambda_client = boto3.client('lambda')
# response = lambda_client.list_functions()
# functions = response['Functions']
# for function in functions:
#     print(function['FunctionName'])
#     # if function == None:
#     #     print(function['FunctionName'])
#     # else:
#     #     print("No function found")