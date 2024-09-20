import json
import os
import boto3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Define S3 bucket
        bucket_name = 'aws-sam-cli-managed-default-samclisourcebucket-kdvjqzoec6pg'
        prefix = 'pdf_templates/'

        # Log the incoming event for debugging
        logger.info("Received event: %s", json.dumps(event))

        # List objects in the specified S3 bucket and folder
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        templates = [obj['Key'].split('/')[-1] for obj in response.get('Contents', []) if obj['Key'].endswith('.pdf')]

        # Return the list of templates
        return {
            'statusCode': 200,
            'body': json.dumps({'templates': templates}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        # Log the exception details
        logger.error("Error occurred: %s", str(e), exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Internal server error',
                'error': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }