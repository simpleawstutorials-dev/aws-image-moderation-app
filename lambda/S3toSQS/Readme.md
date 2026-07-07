# S3toSQS Lambda

This Lambda function is triggered whenever a new object is created in the S3 bucket under the configured upload prefix.
The function sends a message to an Amazon SQS queue containing image-upload metadata, such as the S3 bucket name, object key, upload ID, filename, and user details. The downstream image-processing workflow can then consume this message asynchronously.

## Trigger

S3:ObjectCreated event

## Environment Variables

| Variable | Description |
|---|---|
| SQS_URL | URL of the Amazon SQS queue that receives image-upload messages.|
| DDB_TABLE | DynamoDB table for upload records |
| UPLOAD_PREFIX | S3 prefix under which newly uploaded images are stored. Only objects in this prefix are processed. |



## Required IAM Permissions

- sqs:SendMessage
- dynamodb:GetItem
- dynamodb:UpdateItem

