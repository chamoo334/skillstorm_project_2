import boto3
import json
import logging
from decimal import Decimal

# logging.basicConfig(level=logging.DEBUG)

# DynamoDB Connectivity
dbTableName = 'AWSomeTable'
dynamoDB = boto3.resource('dynamodb')
dbTable = dynamoDB.Table(dbTableName)

# API Gateway Resource: method, path
healthURL = ['GET', '/health']
readURL = ['GET', '/messages']
signURL = ['POST', '/sign']
removeURL = ['DELETE', '/remove']


# https://stackoverflow.com/questions/63278737/object-of-type-decimal-is-not-json-serializable
class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

# API response
def responseMessage(statusCode, body):
    return {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origion': '*' # required for cross region access
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }

# Get all messages
def readMessages():
    try:
        dbResponse = dbTable.scan()
        data = dbResponse['Items']

        while 'LastEvaluatedKey' in dbResponse:
            dbResponse = dbTable.scan(ExclusiveStartKey=dbResponse['LastEvaluatedKey'])
            data.extend(dbResponse['Items'])

        return responseMessage(200, { 'messages': data })
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return responseMessage(500, { 'Error': 'Unable to read messages' })

# Create a message
def createMessage(message_data):
    try:
        dbTable.put_item(Item=message_data)
        
        return responseMessage(
            200, 
            {
                'Save_Status': 'Success',
                'Item': message_data
            }
        )
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return responseMessage(500, { 'Save_Status': 'Fail' })

# Delete a message
def removeMessage(messageId):
    try:
        dbResponse = dbTable.delete_item(
            Key={ 'id': messageId },
            ReturnValues='ALL_OLD'
        )

        return responseMessage( 200, { 'Delete_Status': 'Success' } )
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return responseMessage(500, { 'Delete_Status': 'Fail' } )

# lambda function entrypoint
def lambda_handler(event, context):
    httpMethod = event['httpMethod']
    path = event['path']

    # health check
    if httpMethod == healthURL[0] and path == healthURL[1]:
        response = responseMessage(200, 'Healthy!')
    # get all messages
    elif httpMethod == readURL[0] and path == readURL[1]:
        response = readMessages()

    # create message - requires json {"id": "ex123", "header": "Example", "message": "Some message!", "signature": "user-signature"}
    elif httpMethod == signURL[0] and path == signURL[1]:
        response = createMessage(json.loads(event['body']))

    # delete message - requires json {"id": "ex123"}
    elif httpMethod == removeURL[0] and path == removeURL[1]:
        response = removeMessage(json.loads(event['body'])['id'])

    else:
        response = responseMessage(404, 'Not Found: Check http method and path')

    return response
    
    

