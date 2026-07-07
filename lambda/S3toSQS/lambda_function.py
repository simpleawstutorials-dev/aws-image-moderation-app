import json
import boto3
import os

sqs = boto3.client('sqs')
dynamo = boto3.resource('dynamodb')


def lambda_handler(event, context):


    #event {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2026-05-15T15:07:03.845Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AEOKNJHYMHGF3'}, 
    #'requestParameters': {'sourceIPAddress': '74.104.183.94'}, 'responseElements': {'x-amz-request-id': '1KX7C11ZPY4XBJMS', 'x-amz-id-2': '1yOIv/TnS0F5qLY6qgavWZ8YfyIdQKkWPmsr25kgKEmk+yrppru/o3rU9mmp83IMWIEyuGb38Tg07l10w6gHnJHSoGLS0rKR'}, 
    #'s3': {'s3SchemaVersion': '1.0', 'configurationId': 'ImageUploaded', 'bucket': {'name': 'uploadedimages12356', 'ownerIdentity': {'principalId': 'AEOKNJHYMHGF3'}, 'arn': 'arn:aws:s3:::uploadedimages12356'}, 
    #'object': {'key': 'uploads/52e05ba1-b74b-409b-a906-c2770592c2b8_ducati-panigale-v4-1200x630-2-1920w.jpeg', 'size': 31788, 'eTag': '6810cdf9ed628cf5d5227bd32418b858', 'sequencer': '006A073697CB7CDE2A'}}}]}

    # Read env variables
    DDB_TABLE = os.environ.get('DDB_TABLE')
    SQS_URL = os.environ.get('SQS_URL')
    UPLOAD_PREFIX = os.environ.get('UPLOAD_PREFIX')

    for record in event.get('Records', [] ):
        s3_info = record.get('s3')
        bucket = s3_info.get('bucket').get('name')
        object_key = s3_info.get('object').get('key')

        if not bucket or not object_key.startswith(UPLOAD_PREFIX):
            print("Invalid bucket name or object key")
            continue

        file_name = object_key[len(UPLOAD_PREFIX):] #oject key - uuid_filename.. so read everything on the right side of uuid
        upload_id = file_name.split('_')[0]

        #Fetch information about the image upload from DDB
        table = dynamo.Table(DDB_TABLE)
        database_resp = table.get_item(Key={'upload_id': upload_id})

        #print("DynamoDB Information", database_resp)
        item = database_resp.get('Item')

        if not item:
            print ("No matching upload_id in the database table")
            continue
        
        message= {
            "UserName" : item.get('UserName'),
            "UserEmail" : item.get('UserEmail'),
            "S3ObjectKey" : object_key,
            "S3FileName" : file_name,
            "upload_id" : upload_id
        }

        sqs.send_message(QueueUrl=SQS_URL, MessageBody=json.dumps(message))

        table.update_item(Key={'upload_id': upload_id},
            UpdateExpression='SET #s= :newStatus',
            ExpressionAttributeNames={'#s': 'Status'},
            ExpressionAttributeValues={':newStatus': "IMAGE_UPLOADED"}
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Image uplaoded and ready to process')
    }
