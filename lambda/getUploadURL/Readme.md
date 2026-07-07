# getUploadUrl Lambda

This Lambda function generates a pre-signed S3 upload URL and creates an initial upload record in DynamoDB.

## Trigger

API Gateway REST endpoint.

## Environment Variables

| Variable | Description |
|---|---|
| UPLOAD_BUCKET | S3 bucket where images are uploaded |
| DDB_TABLE_NAME | DynamoDB table for upload records |
| URL_EXPIRATION_SECONDS | Pre-signed URL expiration time |
| ALLOWED_ORIGIN | The URL of image moderation website |
| UPLOAD_PREFIX | The prefix under which all uploaded images will be stored in the S3 bucket |



## Required IAM Permissions

- s3:PutObject
- dynamodb:PutItem
