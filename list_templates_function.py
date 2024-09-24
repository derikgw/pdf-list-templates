# list_templates_function.py
import json
import logging
from template_list_service import list_pdf_templates  # Import the function from the new module

# Set up logging
if logging.getLogger().hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

def lambda_handler(event, context):
    try:
        # Define S3 bucket and prefix
        bucket_name = 's3://aws-sam-cli-managed-default-samclisourcebucket-kdvjqzoec6pg'

        prefix = 'pdf_templates/'

        # Log the incoming event for debugging
        logger.info("Received event: %s", json.dumps(event))

        # Call the module to list PDF templates
        templates = list_pdf_templates(bucket_name, prefix)

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
