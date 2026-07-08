# StartImageWorkflow Lambda

This Lambda function is invoked by Amazon SQS when messages are available in the queue. For each message, it starts an execution of the image moderation Step Functions workflow.
The Lambda also updates the related upload record in DynamoDB to reflect that the workflow has started.

## Trigger

SQS Lambda Trigger

## Environment Variables

| Variable | Description |
|---|---|
| S3_BUCKET_NAME | Name of the S3 bucket where the user uploaded images are stored.|
| DDB_TABLE_NAME | DynamoDB table for upload records |
| STATE_MACHINE_ARN | ARN of the state machine that is used to orchestrate the image moderation workflow |



## Required IAM Permissions

- sqs:DeleteMessage
- sqs:ChangeMessageVisibility
- sqs:ReceiveMessage
- sqs:GetQueueAttributes
- states:StartExecution
- dynamodb:UpdateItem

