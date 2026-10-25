from pathlib import Path
import pymupdf
from docx import Document


SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def extract_text(file_path):
    """
    Extract text from a supported document.

    Returns a dictionary containing extracted text
    and processing status.
    """
    path = Path(file_path)

    if not path.is_file():
        return {
            "text": "",
            "status": "error",
            "message": "File not found.",
        }

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return {
            "text": "",
            "status": "error",
            "message": "Unsupported file format.",
        }

    try:
        if path.suffix.lower() == ".txt":
            text = path.read_text(encoding="utf-8")

        elif path.suffix.lower() == ".pdf":
            with pymupdf.open(path) as pdf:
                text = "\n".join(
                    page.get_text()
                    for page in pdf
                )

        elif path.suffix.lower() == ".docx":
            document = Document(path)

            paragraphs = [
                paragraph.text
                for paragraph in document.paragraphs
            ]

            text = "\n".join(paragraphs)

        return {
            "text": text,
            "status": "success" if text.strip() else "empty",
            "message": (
                "Text extracted successfully."
                if text.strip()
                else "No extractable text found. "
                     "Scanned content may require OCR."
            ),
        }

    except Exception:
        return {
            "text": "",
            "status": "error",
            "message": "Could not process this document.",
        }