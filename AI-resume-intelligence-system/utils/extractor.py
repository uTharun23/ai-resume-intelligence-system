from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file_path):
    text = ""
    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = []

    for para in doc.paragraphs:
        if para.text.strip():
            text.append(para.text.strip())

    return "\n".join(text)


def extract_resume_text(file_path, filename):
    filename = filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        return ""