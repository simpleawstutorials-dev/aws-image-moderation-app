import json
import boto3

rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    print(event)

    #{'UserName': 'Michael Scott', 'UserEmail': 'mscott@gmail.com', 
    #'S3ObjectKey': 'uploads/b35d3e66-c8bd-41a0-905b-16df7c0b4fb5_NYC.jpeg', 
    #'S3FileName': 'b35d3e66-c8bd-41a0-905b-16df7c0b4fb5_NYC.jpeg', 'upload_id': 'b35d3e66-c8bd-41a0-905b-16df7c0b4fb5', 'bucket': 'uploadedimages12356'}

    bucket = event["bucket"]
    key = event["S3ObjectKey"]

    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        MaxLabels=10
    )

    print(response)

    labels = response.get("Labels", [])

    return{
        "bucket": bucket,
        "S3ObjectKey": key,
        "labels": labels,
        "UserName" : event["UserName"],
        "UserEmail" : event["UserEmail"],
        "S3FileName" : event["S3FileName"],
        "upload_id" : event["upload_id"]
    }

