import fitz  # PyMuPDF
import os
import csv
from docx import Document


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from various document types while preserving
    page boundaries and cleaning unnecessary whitespace where applicable.
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        extracted_pages = []

        with fitz.open(file_path) as document:
            for page in document:
                page_text = page.get_text("text").strip()

                if page_text:
                    extracted_pages.append(page_text)

        return "\n\n".join(extracted_pages)

    elif extension == ".docx":
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n\n".join(paragraphs)

    elif extension in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read()

    elif extension == ".csv":
        rows = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(" | ".join(row))
        return "\n".join(rows)

    else:
        raise ValueError(f"Unsupported file type: {extension}")