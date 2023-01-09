import sys, boto3, yaml, json
# from ruamel.yaml import YAML
from pathlib import Path

# python s3_upload.py <s3-bucket-name>

def create_bucket(bucketName):
    s3Client = boto3.client('s3')
    resCreate = s3Client.create_bucket(Bucket = bucketName)
    resPublic = s3Client.put_public_access_block(
        Bucket = bucketName,
        PublicAccessBlockConfiguration = {
            'BlockPublicPolicy': True
        }
    )
    s3Client.close()

def s3_upload(filename, bucketName, botoClient):
    saveFile = filename[10:]
    response = botoClient.upload_file(filename, bucketName, saveFile)

def uploade_templates(tempDir, fileExt, bucketName):
    ymlFiles = Path(tempDir).glob('*.yml')
    s3Client = boto3.client('s3')
    for i in ymlFiles:
        s3_upload(str(i), bucketName, s3Client)
    s3Client.close()

def deploy_cfn_stack():
    pass


def deploy_cfn(template, stackName, bucketName):

    usedCFNBuiltins = [u'!Ref', u'!GetAtt', u'!Sub']


    # with open(template, 'r') as yamlFile:
    #     content = yaml.safe_load(yamlFile)

    # print(content)

    # content['AWSTemplateFormatVersion'] = content['AWSTemplateFormatVersion'].strftime('%Y-%m-%d')
    # cfnTemplate = json.dumps(content)

    # cfnClient = boto3.client('cloudformation')
    # resCfn = cfnClient.create_stack(
    #     StackName = stackName,
    #     TemplateBody = cfnTemplate,
    #     Parameters = [
    #         {
    #             'ParameterKey': 'S3BucketName',
    #             'ParameterValue': bucketName,
    #         }
    #     ],
    #     Capabilities=[
    #         'CAPABILITY_IAM',
    #         'CAPABILITY_NAMED_IAM',
    #         'CAPABILITY_AUTO_EXPAND'
    #     ],

    # )

    # cfnClient.close()


if __name__ == '__main__':
    s3BucketName = sys.argv[1]
    # cfnYaml = sys.argv[2]
    # cfnStackName = sys.argv[3]
    
    create_bucket(s3BucketName)

    uploade_templates('./templates', '*.yml', s3BucketName)

    # deploy_cfn(cfnYaml, cfnStackName, s3BucketName)


