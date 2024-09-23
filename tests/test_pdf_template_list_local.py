# test_pdf_template_list_local.py
import os
from template_list_service import list_pdf_templates  # Relative import within the package

def test_list_pdf_templates():
    template_dir = os.path.expanduser("~")  # Use local directory or S3 path
    templates = list_pdf_templates(template_dir)
    print("Discovered templates:", templates)

if __name__ == "__main__":
    test_list_pdf_templates()
