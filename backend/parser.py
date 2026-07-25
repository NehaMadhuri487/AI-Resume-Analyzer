import io
from pypdf import PdfReader
from docx import Document

def extract_text_from_pdf(file_bytes: io.BytesIO) -> str:
    """Extract text from PDF bytes using PyPDF."""
    try:
        reader = PdfReader(file_bytes)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error parsing PDF file: {str(e)}")

def extract_text_from_docx(file_bytes: io.BytesIO) -> str:
    """Extract text from DOCX file."""
    try:
        doc = Document(file_bytes)
        text = [para.text for para in doc.paragraphs]
        return "\n".join(text).strip()
    except Exception as e:
        raise ValueError(f"Error parsing Word document: {str(e)}")

def extract_text(file_obj, filename: str) -> str:
    """
    Determines file type from extension and extracts text.
    file_obj can be a file path, bytes, or a file-like object (BytesIO).
    """
    ext = filename.split(".")[-1].lower()

    # Normalize to BytesIO
    if hasattr(file_obj, "read"):  # Streamlit UploadedFile
        file_bytes = io.BytesIO(file_obj.read())
        file_obj.seek(0)
    elif isinstance(file_obj, bytes):
        file_bytes = io.BytesIO(file_obj)
    elif isinstance(file_obj, str):  # File path
        with open(file_obj, "rb") as f:
            file_bytes = io.BytesIO(f.read())
    else:
        raise ValueError("Invalid file object type provided to parser.")

    if ext == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif ext in ["docx", "doc"]:
        return extract_text_from_docx(file_bytes)
    elif ext in ["txt", "md"]:
        return file_bytes.getvalue().decode("utf-8", errors="ignore").strip()
    else:
        raise ValueError(f"Unsupported file format: .{ext}. Please upload a PDF, DOCX, or TXT file.")

def clean_text(text: str) -> str:
    """Basic cleaning: normalize whitespace and remove empty lines."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)
