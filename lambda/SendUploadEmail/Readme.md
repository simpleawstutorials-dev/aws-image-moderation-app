# SendUploadEmail Lambda

This Lambda function sends email notifications based on the image moderation decision made by the `MoveImageToPrefix` Lambda function.

If the image does not contain restricted categories, the function sends an approval email to the user.

If the image contains one or more restricted categories, the function sends an email to the user and also sends a notification email to the administrator.

## Trigger

Step Functions task state in the `ImageModerationWorkflow` state machine.

## Environment Variables

| Variable          | Description                                                                                                        |
| ----------------- | ------------------------------------------------------------------------------------------------------------------ |
| `SES_ADMIN_EMAIL` | Administrator email address that receives a notification when an image contains one or more restricted categories. |
| `SES_FROM_EMAIL`  | Verified sender email address used by Amazon Simple Email Service (SES).                                           |

## Required IAM Permissions

- `ses:SendEmail`
