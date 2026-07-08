# AnalyzeImageLabels Lambda

This Lambda function uses Amazon Rekognition to analyze the uploaded image and detect labels, objects, scenes, and other visual content.
The function receives the image bucket and object key from the Step Functions workflow, calls Amazon Rekognition DetectLabels, and stores the analysis results for the upload record.

## Trigger

Step Functions task state in the ImageModerationWorkflow state machine.



## Required IAM Permissions

- rekognition:DetectLabels
- s3:GetObject

