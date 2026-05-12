import json
import boto3
import os
import uuid
import re

s3 = boto3.client("s3")
ddb = boto3.client("dynamodb")



ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN")
UPLOAD_BUCKET = os.environ.get("UPLOAD_BUCKET")
UPLOAD_PREFIX = os.environ.get("UPLOAD_PREFIX")
URL_EXPIRATION_SECONDS = os.environ.get("URL_EXPIRATION_SECONDS")
DDB_TABLE_NAME = os.environ.get("DDB_TABLE_NAME")

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/jpg"
}

def sanitize_filename(filename):
    filename = filename.split("/")[-1].split("\\")[-1]
    #replace the characters that are not allowed in the filename
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    return filename


def response(status_code, body):
    return {
        "statusCode" : status_code,
        "headers" : {
            "Access-Control-Allow-Origin" : ALLOWED_ORIGIN,
            "Access-Control-Allow-Credentials" : True,
            "Content-Type" : "application/json",
            "Access-Control-Allow-Methods" : "OPTIONS,POST,GET"
        },
        "body" : json.dumps(body)
    }

def lambda_handler(event, context):
    try:
        #Code to genereate presigned URL
        body = json.loads(event["body"])

        user_name = body.get("userName")
        user_email = body.get("userEmail")
        file_name = body.get("fileName")
        content_type = body.get("contentType")
        content_length = body.get("contentLength")

        if not file_name:
            return {"statusCode" : 400, "body": json.dumps({"error": "File name is required"})}
        
        if content_type not in ALLOWED_CONTENT_TYPES:
            return {"statusCode": 400, "body": json.dumps({"error": "Content type not allowed"})}

        if content_length is None or int(content_length) > 5 * 1024 * 1024:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid file size"})}

        safe_file_name = sanitize_filename(file_name)
        upload_id = str(uuid.uuid4())

        object_key = f"{UPLOAD_PREFIX}/{upload_id}_{safe_file_name}"

        #Generate the presigned URL
        presigned_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": UPLOAD_BUCKET,
                "Key": object_key,
                "ContentType": content_type,
                "Metadata": {
                    "user-name": user_name,
                    "user-email": user_email,
                }
            },
            ExpiresIn=int(URL_EXPIRATION_SECONDS),
        )

        # Insert into DDB
        try:
            ddb.put_item(
                TableName=DDB_TABLE_NAME,
                Item={
                    "upload_id": {"S": upload_id},
                    "UserName": {"S": user_name},
                    "UserEmail": {"S": user_email},
                    "FileName": {"S": file_name},
                    "ContentType": {"S": content_type},
                    "ContentLength": {"N": str(content_length)},
                    "ObjectKey": {"S": object_key},
                    "Status": {"S": "UPLOAD_URL_CREATED"}
                }
            )
        except Exception as e:
            print(str(e))
            return {"statusCode": 500, "body": json.dumps({"error": "Failed to insert into Dynamo db table."})}

        return {
            "statusCode" : 200,
            "headers" : {
                "Access-Control-Allow-Origin" : ALLOWED_ORIGIN,
                "Access-Control-Allow-Credentials": True,
                "Content-Type" : "application/json",
                "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods" : "OPTIONS,POST,GET"
            },
            "body" : json.dumps({
                "presignedUrl" : presigned_url,
                "objectKey" : object_key,
                "uploadId" : upload_id,
                "bucket" : UPLOAD_BUCKET
            })
        }


    except Exception as e:
        print(str(e))   
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({
                "error": str(e)
            }),
        }