import json
import boto3
import os

sfn = boto3.client('stepfunctions')

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    #Read Env variables
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
    STATE_MACHINE_ARN = os.environ.get("STATE_MACHINE_ARN")
    DDB_TABLE_NAME = os.environ.get("DDB_TABLE_NAME")

    if not S3_BUCKET_NAME:
        raise Exception("S3_BUCKET_NAME not defined")
    
    if not STATE_MACHINE_ARN:
        raise Exception("STATE_MACHINE_ARN not defined")
    

    for record in event.get("Records" ,[]):
        body = record.get("body")  

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            print(f"Invalid JSON in message body: {body}")
            payload = {"rawbody" : body}

        payload["bucket" ] = S3_BUCKET_NAME

        exec_name = payload.get("upload_id")

        kwargs = {
            "stateMachineArn": STATE_MACHINE_ARN,
            "name": exec_name,
            "input": json.dumps(payload)
        }

        sfn.start_execution(**kwargs)

        #Add code to update DynamoDB record
        table = dynamodb.Table(DDB_TABLE_NAME)

        response = table.update_item(
            Key={
                'upload_id': exec_name
                },
                UpdateExpression='SET #Status = :Status',
                ExpressionAttributeNames={
                    '#Status': 'Status'
                    },
                ExpressionAttributeValues={
                    ':Status': "PROCESSING_STARTED"
                    }
                )
        
        print(response)

        return{"statusCode" : 200, "body" : "Image Workflow Started"}