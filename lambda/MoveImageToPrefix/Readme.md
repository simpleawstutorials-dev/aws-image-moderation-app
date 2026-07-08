# MoveImageToPrefix Lambda

This Lambda function checks the labels returned by Amazon Rekognition against a list of restricted categories.

If one or more restricted labels are found with a confidence score greater than the configured threshold, the function moves the image to the `review/` prefix in the S3 bucket.

If no restricted labels are found above the configured threshold, the function moves the image to the `approved/` prefix.

In Amazon S3, moving an object is handled by copying the object to the new prefix and then deleting the original object.

## Trigger

Step Functions task state in the `ImageModerationWorkflow` state machine.

## Environment Variables

| Variable                | Description                                                                                         |
| ----------------------- | --------------------------------------------------------------------------------------------------- |
| `CONFIDENCE_THRESHOLD`  | Minimum confidence score required for a restricted label to send the image to the `review/` prefix. |
| `RESTRICTED_CATEGORIES` | List of restricted labels or categories used to evaluate the uploaded image.                        |

## Required IAM Permissions

- `s3:GetObject`
- `s3:PutObject`
- `s3:DeleteObject`


