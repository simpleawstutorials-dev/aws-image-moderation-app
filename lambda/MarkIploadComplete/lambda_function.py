import json
import boto3
import os
from datetime import datetime,timezone

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    DDL_TABLE_NAME = os.environ.get('DDL_TABLE_NAME')

    table = dynamodb.Table(DDL_TABLE_NAME)

    upload_id = event.get('upload_id')
    finalS3Key = event.get('finalS3Key')
    imageAssessmentReason = event.get('imageAssessmentReason')
    sendToReview = event.get('sendToReview')
    
    completed_at = datetime.now(timezone.utc).isoformat()

    table.update_item(
        Key = {
            'upload_id': upload_id
        },
        UpdateExpression='SET finalS3Key=:finalS3Key, imageAssessmentReason=:imageAssessmentReason, sendToReview=:sendToReview, completed_at=:completed_at, #Status=:Status',
        ExpressionAttributeNames={
            '#Status': 'Status'
        },
        ExpressionAttributeValues={
            ':finalS3Key': finalS3Key,
            ':imageAssessmentReason': imageAssessmentReason,
            ':sendToReview': sendToReview,
            ':completed_at': completed_at,
            ':Status': 'COMPLETE'
        }
    )