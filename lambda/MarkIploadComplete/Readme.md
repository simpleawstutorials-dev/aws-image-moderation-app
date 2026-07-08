# MarkUploadComplete Lambda

This is the final Lambda function in the image moderation workflow.

The function updates the image upload record in the DynamoDB table to indicate that processing is complete. It also stores the timestamp when the workflow completed processing the image.

## Trigger

Step Functions task state in the `ImageModerationWorkflow` state machine.

## Environment Variables

| Variable         | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| `DDB_TABLE_NAME` | Name of the DynamoDB table that stores image upload records. |

## Required IAM Permissions

- `dynamodb:UpdateItem`
