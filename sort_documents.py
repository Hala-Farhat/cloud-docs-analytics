import os
import fitz  # PyMuPDF
import docx

DOCS_FOLDER = "documents"


def get_pdf_title(path):
    try:
        with fitz.open(path) as doc:
            for page in doc:
                text = page.get_text().strip()
                if text:
                    return text.split('\n')[0]
    except Exception as e:
        print(f"[!] Error reading PDF '{path}': {e}")
    return None


def get_docx_title(path):
    try:
        doc = docx.Document(path)
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                return text
    except Exception as e:
        print(f"[!] Error reading DOCX '{path}': {e}")
    return None


def sort_documents():
    titles = []
    for filename in os.listdir(DOCS_FOLDER):
        full_path = os.path.join(DOCS_FOLDER, filename)


        if filename.lower().endswith(".pdf"):
            title = get_pdf_title(full_path)
        elif filename.lower().endswith(".docx"):
            title = get_docx_title(full_path)
        else:
            continue


        if not title:
            title = "Unknown Title"

        titles.append((title, filename))

    # ✅ الترتيب حسب العنوان الأبجدي (غير حساس لحالة الحرف)
    titles.sort(key=lambda x: x[0].lower())
    return titles
