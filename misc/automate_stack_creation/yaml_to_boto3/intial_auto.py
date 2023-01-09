import boto3, yaml, json
from pathlib import Path

s3BucketFile = 'AWSomeS3Bucket.yml'

def create_stack(ymlFile):
    with open(ymlFile, 'r') as content:
        template = yaml.safe_load(content)
    jsonTemplate = json.dumps(template)

    client = boto3.client('cloudformation')

    res = client.create_stack(
        StackName = 'AWSomeS3BucketStack',
        TemplateBody = 'read s3YmlFile',
        Parameters = [
            {
                'ParameterKey': 'BucketNamePrefix',
                'ParameterValue': 'awsome-test-python-1',
            }
        ]
    )

    print(res)


# Create S3 bucket using CloudFormation
create_stack(s3BucketFile)

# Load files to s3 bucket
ymlFiles = Path('./templates').glob('*.yml')

for i in ymlFiles:
    print(i)