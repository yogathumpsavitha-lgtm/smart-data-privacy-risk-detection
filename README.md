# 🔐 Smart Data Privacy Risk Detection for Documents

## Project Overview

Smart Data Privacy Risk Detection is a Python-based web application that identifies potential sensitive information in documents and helps users review findings before sharing them.

The application uses pattern-based detection to identify email addresses, phone numbers, and configured identifiers. It provides a dashboard for reviewing findings and generating a redacted text copy.

## Objectives

* Identify potential sensitive information in documents.
* Classify detected findings by category and risk level.
* Provide a simple interface for reviewing findings.
* Allow users to approve findings for redaction.
* Generate a separate redacted text file.
* Provide an audit summary without including detected raw values.

## Features

* **Document Upload:** Supports TXT, PDF, and DOCX files.
* **Text Extraction:** Extracts available text from supported documents.
* **Sensitive Information Detection:** Detects configured email, phone number, and employee ID patterns.
* **Risk Dashboard:** Displays total findings and risk-level counts.
* **Human Review:** Allows users to approve individual findings for redaction.
* **Redaction Preview:** Displays a text copy with approved findings masked.
* **Download:** Allows users to download the redacted text and audit summary.
* **Automated Tests:** Includes pytest tests for detection and document processing.

## Technologies Used

* Python
* Streamlit
* PyMuPDF
* python-docx
* Regular Expressions
* pytest
* Git and GitHub

## Project Structure

```text
Smart-Data-Privacy-Risk-Detection/
│
├── app.py
├── detector.py
├── document_processor.py
├── redactor.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── sample_documents/
│   └── sample.txt
│
└── tests/
    ├── test_detector.py
    ├── test_document_processor.py
    └── test_privacy_scan.py
```

## Installation

### Prerequisites

* Python 3.11 or a compatible Python version
* Visual Studio Code or another Python editor
* Git (for version control)

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Smart-Data-Privacy-Risk-Detection
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

Open the local address displayed in the terminal, usually:

`http://localhost:8501`

## How to Use

1. Start the application.
2. Upload an authorized TXT, PDF, or DOCX document.
3. Click **Scan Document**.
4. Review the detected information and risk categories.
5. Approve the findings that should be redacted.
6. Inspect the redaction preview.
7. Download the redacted text copy and audit summary.

## Running Tests

Run the automated tests using:

```bash
python -m pytest -q
```

## Security and Privacy Considerations

* Process only documents you are authorized to use.
* Use synthetic data for demonstrations and testing.
* Do not commit confidential documents or personal information to GitHub.
* Do not store credentials or secrets in source code.
* Review findings before redaction.
* Keep the original document unchanged.

## Current Limitations

* Detection relies on configured patterns and may miss sensitive information.
* False positives are possible.
* Scanned PDFs containing images may require OCR.
* The current redaction workflow exports a redacted text copy rather than a format-preserving PDF or DOCX.
* Risk levels are configurable prototype classifications, not a formal compliance assessment.
* The application is a prototype and has not been independently security-audited.

## Future Enhancements

* Format-preserving PDF and DOCX redaction.
* OCR support for scanned documents.
* Configurable detection policies.
* More comprehensive test coverage.
* Improved access controls and retention management.

## Conclusion

This project demonstrates a practical approach to document privacy risk detection through pattern matching, risk classification, human review, and redacted text export.

It is intended as an educational prototype and should not be treated as a guarantee that a document contains no sensitive information.
