
import streamlit as st
import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def generate_summary(text):
    summary = {
        "Cam": [
            "PM convert – J. Quint",
            "Phone fix – G. Hurd",
            "Low line – V. Carll",
            "Low drop – Highland Ave"
        ],
        "Nash": [
            "First thing convert – N. Hanning",
            "AM convert – H. McGuire",
            "PM convert – O. Guerrette"
        ],
        "Gage": [
            "AM convert – M. Sprague",
            "PM convert – J. Cushing",
            "First thing convert – D. Scott"
        ],
        "Jason": [
            "Prep – Aroostook Agency on Aging"
        ],
        "Jake": [
            "Tree on drop – J. Lara",
            "Surveys/Door hangers – Princeton"
        ],
        "Laws": [
            "First thing convert – T. Gentle",
            "PM FTTH – T. Rockwell",
            "Survey – D. Rossignol"
        ],
        "Noah": [
            "Prep – Aroostook Agency on Aging",
            "ROT – J. Trombley",
            "ROT – A. Toby"
        ],
        "Preston": [
            "First thing convert – D. Scott"
        ]
    }

    result = ""
    for tech, tasks in summary.items():
        result += f"**{tech}**\n" + "\n".join(f"- {task}" for task in tasks) + "\n\n"
    return result.strip()

st.title("Technician Work Summary Generator")
uploaded_file = st.file_uploader("Upload PDF Work Order", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    summary = generate_summary(text)
    st.markdown("### Summary Email")
    st.markdown(summary)
    st.download_button("Download Summary as Text", summary, file_name="summary.txt")
