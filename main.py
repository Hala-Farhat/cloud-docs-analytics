import os
import streamlit as st
import base64
import streamlit.components.v1 as components

from sort_documents import sort_documents
from search_documents import search_documents
from classify_documents import classify_documents
from stats_report import generate_stats_report

# تأكد من وجود مجلد الوثائق
os.makedirs("documents", exist_ok=True)

# دالة لعرض PDF داخل Streamlit

def show_pdf_in_streamlit(file_path):
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>
        """
        components.html(pdf_display, height=700, scrolling=True)
    except Exception as e:
        st.error(f"⚠️ Error displaying PDF: {e}")

# إعداد الصفحة
st.set_page_config(page_title="Cloud Document Analyzer", layout="centered")
st.title("📂 Cloud Document Analyzer")
st.info("Select a function from below and click the button to run it.")

# قائمة اختيار الوظائف
option = st.selectbox(
    "Choose a function to perform:",
    ("-- Select --", "Upload File", "Sort Documents", "Search Documents", "Classify Documents", "Generate Statistics")
)

# ✅ رفع الملفات
if option == "Upload File":
    st.subheader("📄 Upload Document")
    uploaded_file = st.file_uploader("Upload a file (PDF or DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        file_path = os.path.join("documents", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ File uploaded and saved: {uploaded_file.name}")

# ✅ فرز المستندات
elif option == "Sort Documents":
    st.subheader("📝 Sorted Document Titles")
    if st.button("Run Sorting"):
        result = sort_documents()
        if result:
            for title, fname in result:
                st.write(f"📄 **{fname}** → {title}")
        else:
            st.info("No documents found.")

# ✅ البحث داخل المستندات
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
                    st.write(f"• {line}")

                # عرض PDF فقط إذا كان الملف PDF
                if doc_name.lower().endswith(".pdf"):
                    key_name = doc_name.replace(" ", "_").replace("(", "").replace(")", "").replace(".", "_")
                    if st.button(f"👀 View {doc_name}", key=key_name):
                        file_path = os.path.join("documents", doc_name)
                        if os.path.exists(file_path):
                            show_pdf_in_streamlit(file_path)
                        else:
                            st.error("❌ File not found.")

                # رابط تحميل لل Word
                elif doc_name.lower().endswith(".docx"):
                    with open(os.path.join("documents", doc_name), "rb") as f:
                        st.download_button(
                            label=f"⬇️ Download {doc_name}",
                            data=f,
                            file_name=doc_name,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

# ✅ تصنيف المستندات
elif option == "Classify Documents":
    st.subheader("🧐 Document Classification")
    if st.button("Run Classification"):
        result = classify_documents()
        if result:
            for file, category in result.items():
                st.write(f"📄 **{file}** → {category}")
        else:
            st.info("No documents found.")

# ✅ عرض الإحصائيات
elif option == "Generate Statistics":
    st.subheader("📊 Project Statistics")
    if st.button("Show Stats"):
        stats = generate_stats_report()
        for line in stats:
            st.write(line)
