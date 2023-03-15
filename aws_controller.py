from flask import request,jsonify
import boto3
import json
import os
import re

dynamo_client = boto3.client('dynamodb')
#table name
table_name = 'file_and_content'
lambda_client = boto3.client('lambda')
# Lambda function to convert the file to csv
function_name = 'convert-file-to-csv-and-upload-it-to-s3'
#s3 input bucket
s3 = boto3.client('s3')


def upload_file(request):
    try:
        file = request.files['file']
        fileBaseName, extension = os.path.splitext(file.filename)
        filename = re.sub(r"[^\w\d_]", "_", fileBaseName)
        s3.upload_fileobj(file, 'input-bucket-for-lambda', filename+extension)
        return jsonify({'status': 'success', 'message': 'File uploaded successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


#get row from ddb with help of a key
def get_item(fileName):
    return dynamo_client.get_item(
        TableName=table_name,
        Key={
            'file_name': {'S': fileName}
        })

#get all items from ddb
def get_fileNames():

    response = dynamo_client.scan(TableName='file_and_content',ProjectionExpression="file_name")
    items=[]
    while 'LastEvaluatedKey' in response:
        items += response['Items']
        # process items
        response = dynamo_client.scan(TableName='file_and_content',ProjectionExpression="file_name",ExclusiveStartKey=response['LastEvaluatedKey'])
    items += response['Items']
    return items



def get_file_url(fileName):

    payload = {
        "file_name": fileName
    }
    # Invoke the Lambda function
    response = lambda_client.invoke(FunctionName=function_name, Payload=json.dumps(payload))
    return response
    
