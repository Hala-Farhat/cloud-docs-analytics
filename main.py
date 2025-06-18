import os
import base64
import streamlit as st
import streamlit.components.v1 as components

from sort_documents import sort_documents
from search_documents import search_documents
from classify_documents import classify_documents
from stats_report import generate_stats_report
from gdrive_utils import download_from_drive, upload_to_drive


FOLDER_ID = "1S0d8FCFxDRih4KDBsKuUO8G_Q2d3gRr5"
DOCS_FOLDER = "documents"
os.makedirs(DOCS_FOLDER, exist_ok=True)

# ✅ تحميل الملفات من Google Drive عند تشغيل التطبيق
download_from_drive(FOLDER_ID)

st.set_page_config(page_title="Cloud Document Analyzer", layout="centered")
st.title("📂 Cloud Document Analyzer")
st.success("✅ Application is running successfully!")
st.info("Select a function from below and click the button to run it.")

# ✅ قسم رفع الملفات
st.sidebar.header("📤 Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a file (.pdf or .docx)", type=["pdf", "docx"])
if uploaded_file is not None:
    save_path = os.path.join(DOCS_FOLDER, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"✅ File '{uploaded_file.name}' saved successfully.")

    # ✅ رفعه إلى Google Drive تلقائيًا
    upload_message = upload_to_drive(save_path, FOLDER_ID)
    st.sidebar.info(upload_message)

# ✅ اختيار العملية
option = st.selectbox(
    "Choose a function to perform:",
    ("-- Select --", "Sort Documents", "Search Documents", "Classify Documents", "Generate Statistics")
)

def show_pdf_in_streamlit(file_path):
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        pdf_display = f'''
            <iframe
                src="data:application/pdf;base64,{base64_pdf}"
                width="100%" height="800" type="application/pdf"
                style="border: none;"
            ></iframe>
        '''
        components.html(pdf_display, height=800, scrolling=True)
    except Exception as e:
        st.error(f"⚠️ Error displaying PDF: {e}")

def download_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.download_button(
            label="⬇️ Download PDF with Highlights",
            data=base64.b64decode(b64),
            file_name=os.path.basename(file_path),
            mime="application/pdf"
        )
    except:
        st.warning("❗ Could not load PDF for download.")

def download_docx(file_path):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.download_button(
        label="⬇️ Download Edited Word File",
        data=base64.b64decode(b64),
        file_name=os.path.basename(file_path),
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

if option == "Search Documents":
    st.subheader("🔍 Search Documents")
    keyword = st.text_input("Enter keyword to search:")

    if st.button("Search"):
        results = search_documents(keyword)
        st.session_state["search_results"] = results
        st.session_state["search_keyword"] = keyword

    if "search_results" in st.session_state and st.session_state["search_results"]:
        keyword = st.session_state.get("search_keyword", "")
        results = st.session_state["search_results"]
        for doc_name, lines in results.items():
            st.markdown(f"### 📄 {doc_name}")
            for line in lines:
                highlighted = line.replace(keyword, f"<mark>{keyword}</mark>")
                st.markdown(f"• {highlighted}", unsafe_allow_html=True)

            full_path = os.path.join(DOCS_FOLDER, doc_name)
            with st.expander(f"👀 Preview & Download: {doc_name}"):
                if doc_name.lower().endswith(".pdf"):
                    show_pdf_in_streamlit(full_path)
                    download_pdf(full_path)
                elif doc_name.lower().endswith(".docx"):
                    download_docx(full_path)
    elif "search_results" in st.session_state:
        st.warning("No results found.")

elif option == "Sort Documents":
    st.subheader("📑 Sorted Document Titles")
    if st.button("Run Sorting"):
        result = sort_documents()
        for title, fname in result:
            st.write(f"📄 **{fname}** → {title}")

elif option == "Classify Documents":
    st.subheader("🧠 Document Classification")
    if st.button("Run Classification"):
        result = classify_documents()
        for file, category in result.items():
            st.write(f"📄 **{file}** → {category}")

elif option == "Generate Statistics":
    st.subheader("📊 Project Statistics")
    if st.button("Show Stats"):
        stats = generate_stats_report()
        for line in stats:
            st.write(line)
