# AWS Image Moderation App

This repository contains the source code for the AWS Image Moderation App built in the Simple AWS Tutorials YouTube series.

## Project Overview

This project demonstrates how to build a real-world image moderation application using AWS services.

Users upload images through a static website. The image is uploaded directly to Amazon S3 using a pre-signed URL. The backend workflow uses Lambda, SQS, Step Functions, Rekognition, DynamoDB, and SES to analyze the image, store metadata, and notify the user and the admins.

## AWS Services Used

- Amazon S3
- Amazon CloudFront
- Amazon API Gateway
- AWS Lambda
- Amazon SQS
- AWS Step Functions
- Amazon Rekognition
- Amazon DynamoDB
- Amazon SES
- Amazon Route 53
- AWS Certificate Manager

## Folder Structure

```text
website/   - HTML, CSS, and JavaScript files
lambda/    - AWS Lambda function code
docs/      - Architecture diagrams and supporting files
