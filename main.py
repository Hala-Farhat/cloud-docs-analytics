import os
import streamlit as st
from sort_documents import sort_documents
from search_documents import search_documents
from classify_documents import classify_documents
from stats_report import generate_stats_report

# إنشاء مجلد "documents" إذا لم يكن موجودًا
os.makedirs("documents", exist_ok=True)

# إعداد الصفحة
st.set_page_config(page_title="Cloud Document Analyzer", layout="centered")

st.title("📂 Cloud Document Analyzer")
st.info("Select a function from below and click the button to run it.")

# القائمة المنسدلة لاختيار الوظيفة
option = st.selectbox(
    "Choose a function to perform:",
    ("-- Select --", "Sort Documents", "Search Documents", "Classify Documents", "Generate Statistics")
)

# التعامل مع الخيار المختار
if option == "-- Select --":
    st.warning("Please select a function from the dropdown above to begin.")

elif option == "Sort Documents":
    st.subheader("📑 Sorted Document Titles")
    if st.button("Run Sorting"):
        result = sort_documents()
        if result:
            for title, fname in result:
                st.write(f"📄 **{fname}** → {title}")
        else:
            st.info("No documents found.")

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

elif option == "Classify Documents":
    st.subheader("🧠 Document Classification")
    if st.button("Run Classification"):
        result = classify_documents()
        if result:
            for file, category in result.items():
                st.write(f"📄 **{file}** → {category}")
        else:
            st.info("No documents found.")

elif option == "Generate Statistics":
    st.subheader("📊 Project Statistics")
    if st.button("Show Stats"):
        stats = generate_stats_report()
        for line in stats:
            st.write(line)
