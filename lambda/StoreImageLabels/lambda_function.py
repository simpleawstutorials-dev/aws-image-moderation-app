import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

def simplify_labels(labels):
    simple_labels = []
    for label in labels:
        simple_labels.append({
            'Name': label.get('Name'),
            'Confidence': Decimal(str(label.get('Confidence'))),
            'Categories' : label.get('Categories', [])
        })
    
    return simple_labels

def lambda_handler(event, context):
    DDB_TABLE_NAME = os.environ.get("DDB_TABLE_NAME")
    table = dynamodb.Table(DDB_TABLE_NAME)

    upload_id = event.get('upload_id')
    labels = event.get('labels')

    simplified_labels = simplify_labels(labels)

    table.update_item(
        Key={
            'upload_id': upload_id
        },
        UpdateExpression="SET labels = :labels, #Status = :Status",
        ExpressionAttributeNames={
            '#Status': 'Status'
        },
        ExpressionAttributeValues={
            ':labels': simplified_labels,
            ':Status': 'LABELS_STORED'
        }
    )

    return event
