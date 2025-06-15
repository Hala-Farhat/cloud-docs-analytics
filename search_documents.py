import os
import fitz  # PyMuPDF
import docx
from docx.shared import RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOCS_FOLDER = "documents"

# 🔶 تمييز الكلمة داخل PDF
def search_pdf(path, keyword):
    results = []
    try:
        doc = fitz.open(path)
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            if keyword.lower() in text.lower():
                highlights = page.search_for(keyword)
                for inst in highlights:
                    page.add_highlight_annot(inst)
                lines = text.split('\n')
                for line in lines:
                    if keyword.lower() in line.lower():
                        results.append((page_num, line.strip()))
        doc.save(path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
        doc.close()
    except Exception as e:
        print(f"[!] Error reading {path}: {e}")
    return results

# 🔶 تمييز الكلمة داخل Word docx
def highlight_word_in_docx(paragraph, keyword):
    for run in paragraph.runs:
        if keyword.lower() in run.text.lower():
            run.font.highlight_color = 7  # Yellow

def search_docx(path, keyword):
    results = []
    try:
        doc = docx.Document(path)
        changed = False
        for para in doc.paragraphs:
            if keyword.lower() in para.text.lower():
                results.append(para.text.strip())
                highlight_word_in_docx(para, keyword)
                changed = True
        if changed:
            doc.save(path)
    except Exception as e:
        print(f"[!] Error reading {path}: {e}")
    return results

# 🔶 تابع Streamlit لاستخدامه مع واجهة المستخدم
def search_documents(keyword):
    result_dict = {}
    for filename in os.listdir(DOCS_FOLDER):
        full_path = os.path.join(DOCS_FOLDER, filename)
        matches = []
        if filename.lower().endswith(".pdf"):
            matches = search_pdf(full_path, keyword)
            if matches:
                lines = [f"Page {p}: {line}" for p, line in matches]
                result_dict[filename] = lines
        elif filename.lower().endswith(".docx"):
            matches = search_docx(full_path, keyword)
            if matches:
                result_dict[filename] = matches
    return result_dict
