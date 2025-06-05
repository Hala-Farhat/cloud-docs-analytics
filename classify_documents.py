import os
import fitz
import docx

DOCS_FOLDER = "documents"

classification_keywords = {
    "Education": ["student", "school", "exam", "university", "lecture", "homework", "course"],
    "Technology": ["software", "technology", "innovation", "data center", "network", "infrastructure"],
    "Business": ["salary", "employee", "company", "market", "management", "finance", "business"],
    "Health": ["health", "disease", "treatment", "patient", "medical", "symptom", "virus", "hospital"],
    "Security": ["hacking", "cyber", "malware", "breach", "firewall", "encryption", "attack", "phishing"],
    "Math": ["equation", "math", "calculation", "variance", "mean", "probability", "algebra", "statistics"],
    "Computer Science": ["algorithm", "data structure", "linked list", "stack", "queue", "recursion"],
    "Programming": ["python", "java", "code", "function", "variable", "loop", "object-oriented"],
    "AI": ["machine learning", "neural network", "deep learning", "AI", "model", "training", "classifier"],
    "Communication": ["transmission", "data packet", "modulation", "signal", "protocol"],
    "Writing": ["writing", "paragraph", "task", "IELTS", "composition", "grammar"],
    "General": ["general", "misc", "overview", "notes", "info", "information"],
    "Templates": ["template", "form", "application", "format", "structure"],
    "Reports": ["report", "summary", "document", "feedback", "findings"]
}



def extract_pdf_text(path):
    try:
        with fitz.open(path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text.lower()
    except:
        return ""


def extract_docx_text(path):
    try:
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs]).lower()
    except:
        return ""


def classify_document(text):
    scores = {label: 0 for label in classification_keywords}
    for label, keywords in classification_keywords.items():
        for word in keywords:
            scores[label] += text.count(word)
    return max(scores, key=scores.get) if any(scores.values()) else "Uncategorized"


print("Document Classification:\n")
for filename in os.listdir(DOCS_FOLDER):
    full_path = os.path.join(DOCS_FOLDER, filename)
    if filename.endswith(".pdf"):
        text = extract_pdf_text(full_path)
    elif filename.endswith(".docx"):
        text = extract_docx_text(full_path)
    else:
        continue
    label = classify_document(text)
    print(f"{filename} → {label}")

def classify_documents():
    results = {}
    for filename in os.listdir(DOCS_FOLDER):
        full_path = os.path.join(DOCS_FOLDER, filename)
        if filename.endswith(".pdf"):
            text = extract_pdf_text(full_path)
        elif filename.endswith(".docx"):
            text = extract_docx_text(full_path)
        else:
            continue
        label = classify_document(text)
        results[filename] = label
    return results
