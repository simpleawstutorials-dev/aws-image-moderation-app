import json
import boto3
import os

ses = boto3.client('ses', region_name='us-east-1')

def lambda_handler(event, context):
    SES_ADMIN_EMAIL = os.environ.get('SES_ADMIN_EMAIL')
    SES_FROM_EMAIL = os.environ.get('SES_FROM_EMAIL')

    recepient_email = event['UserEmail']
    recepient_name = event['UserName']

    image_decision = event['sendToReview']
    image_decision_reason = event['imageAssessmentReason']
    final_s3_key = event ['finalS3Key']

    if image_decision == False:
        email_subject = "Congratulations! Your photo submission is now live!"
        email_body = f"""
        <html>
            <body>
                <h2>Congratulations {recepient_name}!</h2>
                <p>Your photo has been approved and is now live on our website.</p>
            </body>
        </html>
        """

        ses.send_email(
            Source=SES_FROM_EMAIL,
            Destination={
                'ToAddresses': [
                    recepient_email,
                ]
            },
            Message={
                'Subject': {
                    'Data': email_subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {
                        'Data': email_body,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
    else:
        email_subject_user = "Your photo submission is under review."
        email_body_user = f"""
        <html>
            <body>
                <h2>Hi {recepient_name}</h2>
                <p>Thank you for submitting your photo. Your submission is under review. We will provide an update in next 48hrs.</p>
            </body>
        </html>
        """

        ses.send_email(
            Source=SES_FROM_EMAIL,
            Destination={
                'ToAddresses': [
                    recepient_email,
                ]
            },
            Message={
                'Subject': {
                    'Data': email_subject_user,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {
                        'Data': email_body_user,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )

        email_subject_admin = "Photo submission needs your review"
        email_body_admin = f"""
        <html>
            <body>
                <h2>Hi Admin</h2>
                <p>A new photo submission requires human review.</p>
                <ul>
                    <li><strong>Submitted by:</strong> {recepient_name}</li>
                    <li><strong>Email:</strong> {recepient_email}</li>
                    <li><strong>Reason for review:</strong> {image_decision_reason}</li>
                    <li><strong>S3 Key:</strong> {final_s3_key}</li>
                </ul>
            </body>
        </html>
        """

        ses.send_email(
           Source=SES_FROM_EMAIL,
            Destination={
                'ToAddresses': [
                    SES_ADMIN_EMAIL,
                ]
            },
            Message={
                'Subject': {
                    'Data': email_subject_admin,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {
                        'Data': email_body_admin,
                        'Charset': 'UTF-8'
                    }
                }
            } 
        )

    return event
    

    
