# PDF Form Field Discovery with AWS Lambda

This project contains an AWS Lambda function that dynamically extracts form field names from a PDF template stored in an S3 bucket. The extracted fields are returned in a structured JSON format, making it easy to understand what fields are available for further operations like populating or modifying the PDF.

## Features

- **Discover PDF Form Fields**: Automatically scans and extracts all the form fields (e.g., text fields, checkboxes) from a PDF.
- **S3 Integration**: Retrieves the PDF template from an S3 bucket.
- **JSON Response**: Returns the form field names in a JSON format, ready for further processing or validation.
  
## How it Works

1. The Lambda function receives an API request containing the name of a PDF template stored in an S3 bucket.
2. The function downloads the PDF template from the S3 bucket to the Lambda environment.
3. It reads through the PDF and extracts any form fields (e.g., text fields, checkboxes) available.
4. The function returns a JSON response containing the names of the discovered fields.

## Technologies Used

- **AWS Lambda**: The serverless function that extracts form fields from a PDF.
- **AWS S3**: Stores the PDF templates used for field discovery.
- **PyPDF**: Python library used to read and extract form data from PDF files.
- **Boto3**: AWS SDK for Python, used to interact with S3.
- **Python 3.12**: The runtime environment for the Lambda function.

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

The API expects a GET request with the following structure:

- **Query Parameters**:
  - `templateName`: The name of the PDF template stored in the S3 bucket.

#### Example Request

```http
GET /pdf-form-discovery?templateName=sample_template.pdf HTTP/1.1
Host: your-api-gateway-url
```

### Response

- **Status Code**: `200 OK`
- **Response Body**: A JSON object containing the names of the form fields found in the PDF template.
- **Headers**:
  - `Content-Type`: `application/json`

#### Example Response

```json
{
    "formData": {
        "fname_input": "",
        "lname_input": "",
        "email_input": "",
        "checkbox_human": ""
    }
}
```

### Error Responses

- **Status Code**: `400 Bad Request`
  - Occurs when the `templateName` query parameter is missing.
  
- **Status Code**: `500 Internal Server Error`
  - Occurs when something goes wrong during the PDF processing or S3 download.

#### Example Error Response

```json
{
    "message": "Internal server error",
    "error": "An error occurred (403) when calling the HeadObject operation: Forbidden"
}
```

## S3 Bucket Structure

Your S3 bucket should contain the PDF templates that will be used for field discovery.

### Example Structure:

```plaintext
S3 Bucket: aws-sam-cli-managed-default-samclisourcebucket-kdvjqzoec6pg
└── pdf_templates/
    ├── sample_template.pdf
    └── another_template.pdf
```

## Lambda Code

Here’s the core code for the Lambda function:

```python
import json
import boto3
from pypdf import PdfReader

s3 = boto3.client('s3')

def discover_pdf_fields(pdf_path):
    """Discover form fields in a given PDF."""
    pdf_reader = PdfReader(pdf_path)
    fields = {}

    for page in pdf_reader.pages:
        if '/Annots' in page:
            for annotation in page['/Annots']:
                field = annotation.get_object()
                field_name = field.get('/T')
                if field_name:
                    field_name = field_name.strip('()')
                    fields[field_name] = ""

    return fields

def lambda_handler(event, context):
    try:
        # Get template name from query parameters
        template_name = event.get('queryStringParameters', {}).get('templateName')
        if not template_name:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'templateName parameter is required'}),
                'headers': {'Content-Type': 'application/json'}
            }

        # Define S3 bucket and template path
        bucket_name = 'aws-sam-cli-managed-default-samclisourcebucket-kdvjqzoec6pg'
        pdf_template_s3_key = f'pdf_templates/{template_name}'

        # Paths in Lambda's tmp directory
        pdf_template_path = f'/tmp/{template_name}'

        # Download the template PDF from S3
        s3.download_file(bucket_name, pdf_template_s3_key, pdf_template_path)

        # Discover form fields from the template
        discovered_fields = discover_pdf_fields(pdf_template_path)

        # Return the form fields
        return {
            'statusCode': 200,
            'body': json.dumps({'formData': discovered_fields}),
            'headers': {'Content-Type': 'application/json'}
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Internal server error',
                'error': str(e)
            }),
            'headers': {'Content-Type': 'application/json'}
        }
```

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
curl -X GET "https://your-api-url/pdf-form-discovery?templateName=sample_template.pdf"
```

### Expected Response:
```json
{
    "formData": {
        "fname_input": "",
        "lname_input": "",
        "checkbox_human": ""
    }
}
```

## Error Handling

The function returns the following error codes:

- **400 Bad Request**: When the `templateName` query parameter is missing.
- **500 Internal Server Error**: When something goes wrong during PDF processing or S3 download.

### Example Error Cases:
- **Missing templateName Parameter**:
  ```json
  {
      "message": "templateName parameter is required"
  }
  ```

- **S3 Access Error (403 Forbidden)**:
  ```json
  {
      "message": "Internal server error",
      "error": "An error occurred (403) when calling the HeadObject operation: Forbidden"
  }
  ```

## Future Improvements

- **PDF Field Types**: Currently, only field names are extracted. Future versions could extract field types (e.g., text, checkbox) as well.
- **Multi-page PDFs**: Improve the handling of multi-page PDFs to ensure form fields from all pages are accurately captured.
- **Improved Error Handling**: Add more detailed error handling and logging for easier troubleshooting.
