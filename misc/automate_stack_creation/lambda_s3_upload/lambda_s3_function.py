import boto3
import logging

def upload_file(data, fileName):
    try:
        s3Client = boto3.client('s3')
        s3Bucket = s3Client.Bucket('AWSomeStackBucketProject2')
        s3Bucket.upload_file(f'tmp/{fileName}', fileName)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        
def lambda_handler(event, context):
    uploadData = event
    # upload_file(uploadData, fileName)