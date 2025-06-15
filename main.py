import os
import base64
import urllib.parse
import streamlit as st
from sort_documents import sort_documents
from search_documents import search_documents
from classify_documents import classify_documents
from stats_report import generate_stats_report

DOCS_FOLDER = "documents"
os.makedirs(DOCS_FOLDER, exist_ok=True)

st.set_page_config(page_title="Cloud Document Analyzer", layout="centered")
st.title("📂 Cloud Document Analyzer")
st.success("✅ Application is running successfully!")
st.info("Select a function from below and click the button to run it.")

option = st.selectbox(
    "Choose a function to perform:",
    ("-- Select --", "Sort Documents", "Search Documents", "Classify Documents", "Generate Statistics")
)

# ✅ عرض PDF داخل iframe
def show_pdf_in_streamlit(file_path):
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        encoded_path = urllib.parse.quote(file_path)
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"⚠️ Error displaying PDF: {e}")

# ✅ تحميل ملف DOCX بعد التمييز
def download_docx(file_path):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.download_button(
        label="⬇️ Download Edited Word File",
        data=base64.b64decode(b64),
        file_name=os.path.basename(file_path),
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

if option == "Sort Documents":
    st.subheader("📑 Sorted Document Titles")
    if st.button("Run Sorting"):
        result = sort_documents()
        for title, fname in result:
            st.write(f"📄 **{fname}** → {title}")

elif option == "Search Documents":
    st.subheader("🔍 Search Documents")
    keyword = st.text_input("Enter keyword to search:")
    if keyword and st.button("Search"):
        results = search_documents(keyword)
        if not results:
            st.warning("No results found.")
        else:
            for doc_name, lines in results.items():
                st.markdown(f"### 📄 {doc_name}")
                for line in lines:
                    highlighted = line.replace(keyword, f"<mark>{keyword}</mark>")
                    st.markdown(f"• {highlighted}", unsafe_allow_html=True)

                full_path = os.path.join(DOCS_FOLDER, doc_name)

                if doc_name.lower().endswith(".pdf"):
                    with st.expander(f"👀 Preview {doc_name}"):
                        show_pdf_in_streamlit(full_path)

                if doc_name.lower().endswith(".docx"):
                    download_docx(full_path)


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
