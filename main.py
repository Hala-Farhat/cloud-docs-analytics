import streamlit as st
from sort_documents import sort_documents
from search_documents import search_documents
from classify_documents import classify_documents
from stats_report import generate_stats_report

st.title(" Cloud Document Analyzer")

option = st.selectbox(
    "Choose a function to perform:",
    ("Sort Documents", "Search Documents", "Classify Documents", "Generate Statistics")
)

if option == "Sort Documents":
    st.subheader(" Sorted Document Titles")
    result = sort_documents()
    for title, fname in result:
        st.write(f" {fname} → {title}")

elif option == "Search Documents":
    keyword = st.text_input(" Enter keyword to search for:")
    if keyword:
        results = search_documents(keyword)
        for doc_name, lines in results.items():
            st.markdown(f"** {doc_name}**")
            for line in lines:
                st.write(f"- {line}")

elif option == "Classify Documents":
    st.subheader(" Document Classification")
    result = classify_documents()
    for file, category in result.items():
        st.write(f"{file} → {category}")

elif option == "Generate Statistics":
    st.subheader(" Statistics")
    stats = generate_stats_report()
    for line in stats:
        st.write(line)
