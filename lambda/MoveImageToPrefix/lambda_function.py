import json
import os
import boto3

s3 = boto3.client('s3') 

def lambda_handler(event, context):
    RESTRICTED_CATEGORIES = os.environ.get('RESTRICTED_CATEGORIES', [])
    CONFIDENCE_THRESHOLD = os.environ.get('CONFIDENCE_THRESHOLD')

    try:
        restricted_labels = json.loads(RESTRICTED_CATEGORIES)
    except json.JSONDecodeError:
        raise RuntimeError ('Restricted categories must be a valid JSON')
    

    labels = event.get('labels', [])
    bucket = event.get('bucket')
    s3ObjectKey = event.get('S3ObjectKey')

    new_prefix = ''

    file_name = s3ObjectKey.split('/')[-1]

    send_to_review = False
    matched_category = None

    for label in labels:
        name = label.get('Name')
        confidence = label.get('Confidence')
        
        if name.lower() in restricted_labels and confidence >= float(CONFIDENCE_THRESHOLD):
            send_to_review = True
            matched_category = name
            break
    
    if send_to_review:
        # Send to review workflow
        print(f'Image required review. Image contains restricted category: {matched_category} with confidence rating of {confidence}, which exceeds the confidence threshold of {CONFIDENCE_THRESHOLD}')
        new_prefix = 'review/'
        image_assessment_reason = f'Image required review. Image contains restricted category: {matched_category} with confidence rating of {confidence}, which exceeds the confidence threshold of {CONFIDENCE_THRESHOLD}'
    else:
        print(f'Image does not require review. No restricted categories found above the confidence threshold of {CONFIDENCE_THRESHOLD}')
        new_prefix = 'approved/'
        image_assessment_reason = f'Image does not require review. No restricted categories found above the confidence threshold of {CONFIDENCE_THRESHOLD}'

    target_key = f"{new_prefix}{file_name}"

    s3.copy_object(
        Bucket=bucket,
        CopySource={'Bucket': bucket, 'Key': s3ObjectKey},
        Key=target_key)
    
    s3.delete_object(
        Bucket=bucket,
        Key=s3ObjectKey)

    event["finalS3Key"] = target_key
    event["sendToReview"] = send_to_review
    event["imageAssessmentReason"] = image_assessment_reason

    return event
