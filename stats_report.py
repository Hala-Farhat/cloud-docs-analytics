import os
import time
import fitz
import docx

DOCS_FOLDER = "documents"

def get_file_size(path):
    return os.path.getsize(path) / 1024  # KB

def count_documents():
    return [f for f in os.listdir(DOCS_FOLDER) if f.endswith(('.pdf', '.docx'))]

def simulate_sorting(documents):
    start = time.time()
    titles = []
    for filename in documents:
        path = os.path.join(DOCS_FOLDER, filename)
        title = None
        if filename.endswith('.pdf'):
            try:
                with fitz.open(path) as doc:
                    for page in doc:
                        text = page.get_text().strip()
                        if text:
                            title = text.split('\n')[0]
                            break
            except:
                pass
        elif filename.endswith('.docx'):
            try:
                doc = docx.Document(path)
                for para in doc.paragraphs:
                    text = para.text.strip()
                    if text:
                        title = text
                        break
            except:
                pass
        if not title:
            title = "Unknown Title"
        titles.append((title, filename))
    titles.sort(key=lambda x: x[0].lower())
    end = time.time()
    return end - start

def simulate_search(documents, keyword="data"):
    start = time.time()
    for filename in documents:
        path = os.path.join(DOCS_FOLDER, filename)
        try:
            if filename.endswith('.pdf'):
                with fitz.open(path) as doc:
                    for page in doc:
                        _ = keyword.lower() in page.get_text().lower()
            elif filename.endswith('.docx'):
                doc = docx.Document(path)
                for para in doc.paragraphs:
                    _ = keyword.lower() in para.text.lower()
        except:
            continue
    end = time.time()
    return end - start

def simulate_classification(documents):
    start = time.time()
    for filename in documents:
        path = os.path.join(DOCS_FOLDER, filename)
        try:
            if filename.endswith('.pdf'):
                with fitz.open(path) as doc:
                    text = ''.join(page.get_text() for page in doc).lower()
            elif filename.endswith('.docx'):
                doc = docx.Document(path)
                text = "\n".join(para.text for para in doc.paragraphs).lower()
        except:
            continue
    end = time.time()
    return end - start

docs = count_documents()
file_count = len(docs)
total_size = sum(get_file_size(os.path.join(DOCS_FOLDER, f)) for f in docs)

sort_time = simulate_sorting(docs)
search_time = simulate_search(docs)
classify_time = simulate_classification(docs)

print("📊 Project Statistics:")
print(f"- Total number of documents: {file_count}")
print(f"- Total size: {total_size:.2f} KB")
print(f"- Time to sort documents: {sort_time:.2f} sec")
print(f"- Time to search documents: {search_time:.2f} sec")
print(f"- Time to classify documents: {classify_time:.2f} sec")

def generate_stats_report():
    report = []
    report.append(f"📊 Project Statistics:")
    report.append(f"- Total number of documents: {file_count}")
    report.append(f"- Total size: {total_size:.2f} KB")
    report.append(f"- Time to sort documents: {sort_time:.2f} sec")
    report.append(f"- Time to search documents: {search_time:.2f} sec")
    report.append(f"- Time to classify documents: {classify_time:.2f} sec")
    return report
