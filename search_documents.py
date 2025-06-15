import os
import fitz  # PyMuPDF
import docx

DOCS_FOLDER = "documents"

def search_pdf(path, keyword):
    results = []
    try:
        doc = fitz.open(path)
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            if keyword.lower() in text.lower():
                # 🔶 حدد كل الأماكن التي يظهر فيها النص
                highlights = page.search_for(keyword, quads=False)
                for inst in highlights:
                    page.add_highlight_annot(inst)
                # 🔶 جمع الأسطر التي تحتوي على الكلمة
                lines = text.split('\n')
                for line in lines:
                    if keyword.lower() in line.lower():
                        results.append((page_num, line.strip()))
        # 🔐 حفظ التغييرات داخل نفس الملف
        doc.save(path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
        doc.close()
    except Exception as e:
        print(f"[!] Error reading {path}: {e}")
    return results

def search_docx(path, keyword):
    results = []
    try:
        doc = docx.Document(path)
        for para in doc.paragraphs:
            if keyword.lower() in para.text.lower():
                results.append(para.text.strip())
    except Exception as e:
        print(f"[!] Error reading {path}: {e}")
    return results

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
