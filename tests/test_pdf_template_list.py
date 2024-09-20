import os

import requests

# Define the API URL and API key
API_URL = "https://q22xmlxuyd.execute-api.us-east-1.amazonaws.com/Prod/pdfTemplateList"  # Replace with your actual API URL
# API Key (retrieve from environment variable)
API_KEY = os.getenv("PDF_TEMPLATE_LIST_API_KEY")

def test_pdf_template_list():
    headers = {
        "x-api-key": API_KEY
    }

    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Print the response details
        print("Status Code:", response.status_code)
        print("Response Body:", response.json())
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)

if __name__ == "__main__":
    test_pdf_template_list()