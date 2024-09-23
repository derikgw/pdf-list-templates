# template_list_service.py
import boto3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

s3 = boto3.client('s3')


def list_pdf_templates(bucket_name, prefix='pdf_templates/'):
    """
    List all PDF templates in the specified S3 bucket and prefix.

    :param bucket_name: The name of the S3 bucket
    :param prefix: The prefix path in the S3 bucket where the PDFs are located
    :return: A list of PDF filenames
    :raises Exception: If there is an issue listing the objects in the S3 bucket
    """
    try:
        logger.info(f"Listing objects in bucket: {bucket_name} with prefix: {prefix}")

        # List objects in the specified S3 bucket and folder
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        # Filter and return only PDF files
        templates = [obj['Key'].split('/')[-1] for obj in response.get('Contents', []) if obj['Key'].endswith('.pdf')]

        return templates

    except Exception as e:
        logger.error(f"Error occurred while listing templates: {str(e)}", exc_info=True)
        raise e
