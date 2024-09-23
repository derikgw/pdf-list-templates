# template_list_service.py
import boto3
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize the S3 client
s3 = boto3.client('s3')


def list_pdf_templates(bucket_or_path, prefix='pdf_templates/'):
    """
    List PDF templates from S3 or a local directory.

    :param bucket_or_path: The name of the S3 bucket or local directory path
    :param prefix: The folder path to list PDFs in S3 or local directory
    :return: A list of PDF template names
    """
    if bucket_or_path.startswith("s3://"):
        # Extract bucket name and key from the S3 path
        bucket_name = bucket_or_path.split('/')[2]
        prefix = '/'.join(bucket_or_path.split('/')[3:])

        try:
            logger.info(f"Listing PDF templates from S3 bucket: {bucket_name}, prefix: {prefix}")
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            templates = [obj['Key'].split('/')[-1] for obj in response.get('Contents', []) if obj['Key'].endswith('.pdf')]
            logger.info(f"Discovered PDF templates: {templates}")
            return templates
        except Exception as e:
            logger.error(f"Error listing templates from S3: {str(e)}", exc_info=True)
            raise e
    else:
        # Local file path listing
        logger.info(f"Listing PDF templates from local directory: {bucket_or_path}/{prefix}")
        full_path = os.path.join(bucket_or_path, prefix)
        templates = [f for f in os.listdir(full_path) if f.endswith('.pdf')]
        logger.info(f"Discovered PDF templates: {templates}")
        return templates
