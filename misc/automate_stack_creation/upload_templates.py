import sys, boto3
from pathlib import Path

# python upload_templates.py <s3-bucket-name>

s3BucketName = sys.argv[1]
s3BucketURL = f'https://{s3BucketName}.s3.amazonaws.com/'
ymlFiles = Path('./templates').glob('*.yml')
s3Client = boto3.client('s3')

def s3_upload(filename):
    saveFile = filename[10:]
    response = s3Client.upload_file(filename, s3BucketName, saveFile)

for i in ymlFiles:
    s3_upload(str(i))
