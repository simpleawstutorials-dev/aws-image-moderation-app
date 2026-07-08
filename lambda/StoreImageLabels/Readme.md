# StoreImageLabels Lambda

This Lambda function updates the image upload record in the DynamoDB table with the labels returned by Amazon Rekognition.
The function receives the upload identifier and Rekognition label results from the Step Functions workflow, then stores the labels against the corresponding upload record.

## Trigger

Step Functions task state in the ImageModerationWorkflow state machine.

## Environment Variables

| Variable | Description |
|---|---|
| DDB_TABLE_NAME | DynamoDB table for upload records |



## Required IAM Permissions

- dynamodb:UpdateItem

