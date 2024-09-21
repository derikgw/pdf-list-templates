# PDF Template Listing with AWS Lambda

This AWS Lambda function lists all PDF templates stored in a specific folder within an S3 bucket. The function returns a JSON response containing the names of all available PDF templates, making it easy for users to see which templates are available for further operations.

## Features

- **List PDF Templates**: Automatically retrieves a list of all `.pdf` files in the designated folder of an S3 bucket.
- **S3 Integration**: The function interacts with an S3 bucket to fetch the template names.
- **Logging**: Logs important events and errors using the `logging` module for easy debugging.
- **JSON Response**: Returns the list of PDF templates in a structured JSON format.

## How it Works

1. The Lambda function receives an API request.
2. It connects to the specified S3 bucket and lists all objects (files) in the `pdf_templates/` folder.
3. It filters the files to include only `.pdf` files.
4. The function returns the list of PDF filenames as a JSON response.

## Technologies Used

- **AWS Lambda**: Serverless function that lists available PDF templates.
- **AWS S3**: Stores the PDF templates, and the function queries S3 to retrieve the list of files.
- **Boto3**: AWS SDK for Python, used to interact with S3.
- **Python 3.12**: The runtime environment for the Lambda function.
- **Logging**: Python's `logging` module is used for debugging and error tracking.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [API Overview](#api-overview)
3. [S3 Bucket Structure](#s3-bucket-structure)
4. [Lambda Code](#lambda-code)
5. [Deploying the Lambda Function](#deploying-the-lambda-function)
6. [Testing the API](#testing-the-api)
7. [Error Handling](#error-handling)
8. [Future Improvements](#future-improvements)

---

## Prerequisites

Before deploying or testing the Lambda function, ensure you have the following:

- **AWS Account**: You need an AWS account to create the Lambda function and S3 bucket.
- **AWS CLI**: Installed and configured on your machine. [AWS CLI Installation](https://aws.amazon.com/cli/)
- **SAM CLI (Serverless Application Model)**: For deploying the Lambda function. [Install SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- **Python 3.12 or higher**: The Lambda function uses Python 3.12.

## API Overview

### Request Format

The API expects a simple GET request to retrieve the list of available PDF templates.

#### Example Request

```http
GET /pdf-template-list HTTP/1.1
Host: your-api-gateway-url
```

### Response

- **Status Code**: `200 OK`
- **Response Body**: A JSON object containing the list of PDF templates available in the S3 bucket.
- **Headers**:
  - `Content-Type`: `application/json`

#### Example Response

```json
{
    "templates": [
        "sample_template.pdf",
        "contract_template.pdf",
        "invoice_template.pdf"
    ]
}
```

### Error Responses

- **Status Code**: `500 Internal Server Error`
  - Occurs when something goes wrong during the S3 interaction or PDF listing process.

#### Example Error Response

```json
{
    "message": "Internal server error",
    "error": "An error occurred (403) when calling the ListObjectsV2 operation: Forbidden"
}
```

## S3 Bucket Structure

Your S3 bucket should contain PDF templates stored in a specific folder. The function will list only `.pdf` files from this folder.

### Example Structure:

```plaintext
S3 Bucket: aws-sam-cli-managed-default-samclisourcebucket-kdvjqzoec6pg
└── pdf_templates/
    ├── sample_template.pdf
    ├── contract_template.pdf
    └── invoice_template.pdf
```

## Lambda Code

Here’s the core code for the Lambda function:

```python
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
```

### Key Functionality:

1. **Logging**: The function logs incoming events and any exceptions that occur, making debugging easier via AWS CloudWatch.
2. **S3 PDF Listing**: The function lists all `.pdf` files in the `pdf_templates/` folder of the specified S3 bucket and returns them as a list.
3. **Error Handling**: If any error occurs during the S3 interaction, the function logs the error and returns an appropriate response.

## Deploying the Lambda Function

You can deploy this Lambda function using AWS SAM. Here's a general overview of the deployment process:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build the Lambda Function**:
   ```bash
   sam build
   ```

3. **Deploy the Lambda Function**:
   ```bash
   sam deploy --guided
   ```

   During deployment, SAM will ask you to provide various parameters, including the stack name and the S3 bucket name.

4. **Test the API** using the API Gateway URL provided after deployment.

## Testing the API

You can test the API using tools like **Postman** or **cURL**. Example:

```bash
curl -X GET https://your-api-url/pdf-template-list
```

### Expected Response:
```json
{
    "templates": [
        "sample_template.pdf",
        "contract_template.pdf",
        "invoice_template.pdf"
    ]
}
```

## Error Handling

The function returns the following error codes:

- **500 Internal Server Error**: When something goes wrong during S3 interaction or template listing.

### Example Error Case:
- **S3 Access Error (403 Forbidden)**:
  ```json
  {
      "message": "Internal server error",
      "error": "An error occurred (403) when calling the ListObjectsV2 operation: Forbidden"
  }
  ```

## Future Improvements

- **Pagination**: If the S3 bucket contains a large number of files, consider adding pagination using `list_objects_v2`'s `ContinuationToken`.
- **File Type Filtering**: Currently, only `.pdf` files are listed. You could extend this to support other file types if needed.
- **Improved Error Handling**: Add more specific error codes (e.g., `404 Not Found` for an empty folder).
