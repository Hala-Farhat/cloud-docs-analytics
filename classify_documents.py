import os
import fitz  # PyMuPDF
import docx

DOCS_FOLDER = "documents"

classification_tree = {
    "Technology": {
        "Programming": {
            "Python": ["python", "pandas", "numpy", "django", "flask"],
            "Java": ["java", "spring", "jvm", "inheritance", "oop"],
            "Web": ["html", "css", "javascript", "react", "angular", "frontend"]
        },
        "Artificial Intelligence": {
            "Machine Learning": ["machine learning", "supervised", "unsupervised", "regression"],
            "Deep Learning": ["neural network", "deep learning", "cnn", "rnn"],
            "NLP": ["natural language processing", "bert", "tokenization", "nlp"]
        },
        "Networking": {
            "Protocols": ["http", "tcp", "udp", "ip", "protocol", "transmission"],
            "Security": ["firewall", "encryption", "vpn", "tls", "ssl", "cyber", "attack", "malware"]
        }
    },
    "Health": {
        "Medicine": {
            "Diseases": ["cancer", "diabetes", "covid", "flu"],
            "Treatment": ["therapy", "surgery", "vaccine", "antibiotic", "treatment"]
        },
        "Nutrition": {
            "Diet": ["diet", "calories", "protein", "carbohydrate", "nutrition", "food"],
            "Supplements": ["vitamin", "omega", "zinc", "magnesium", "supplement"]
        }
    },
    "Education": {
        "Higher Education": {
            "University": ["university", "college", "campus", "faculty"],
            "Courses": ["lecture", "course", "exam", "credit", "syllabus", "schedule"],
            "Assignments": ["assignment", "task", "homework", "question", "problem", "solution"]
        },
        "School": {
            "Subjects": ["math", "science", "history", "language", "english", "biology", "physics"],
            "Activities": ["project", "activity", "worksheet", "presentation"]
        }
    },
    "Math": {
        "Discrete Math": {
            "Set Theory": ["set", "subset", "intersection", "union", "venn", "relation", "element"],
            "Logic": ["boolean", "truth table", "implication", "proposition", "proof", "induction"]
        }
    }
}


def extract_pdf_text(path):
    try:
        with fitz.open(path) as doc:
            return "\n".join([page.get_text() for page in doc]).lower()
    except Exception as e:
        print(f"[!] Error reading PDF '{path}': {e}")
        return ""


def extract_docx_text(path):
    try:
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs]).lower()
    except Exception as e:
        print(f"[!] Error reading DOCX '{path}': {e}")
        return ""


def classify_document(text):
    best_score = 0
    best_path = "Uncategorized"

    def recursive_score(node, path=""):
        nonlocal best_score, best_path
        for key, val in node.items():
            current_path = f"{path} > {key}" if path else key
            if isinstance(val, dict):
                recursive_score(val, current_path)
            elif isinstance(val, list):
                score = sum(text.count(word) for word in val)
                if score > best_score:
                    best_score = score
                    best_path = current_path

    recursive_score(classification_tree)
    return best_path


def classify_documents():
    results = {}
    for filename in os.listdir(DOCS_FOLDER):
        full_path = os.path.join(DOCS_FOLDER, filename)
        if filename.lower().endswith(".pdf"):
            text = extract_pdf_text(full_path)
        elif filename.lower().endswith(".docx"):
            text = extract_docx_text(full_path)
        else:
            continue
        label = classify_document(text)
        results[filename] = label
    return results
