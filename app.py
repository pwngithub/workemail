
import streamlit as st
import fitz  # PyMuPDF
import re
from collections import defaultdict

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def parse_work_orders(raw_text):
    tech_tasks = defaultdict(list)

    # Split into chunks by technician sections using the pattern of tech name lines like "0XX TechNameTechnician:"
    tech_sections = re.findall(r"0\w+\s+([\w\s\-]+)Technician:(.*?)Type of Work", raw_text, re.DOTALL)

    for tech_name, section in tech_sections:
        tech_name = tech_name.strip()
        lines = section.strip().split("\n")
        for line in lines:
            if "convert" in line.lower():
                time_label = ""
                if "first thing" in line.lower():
                    time_label = "First thing convert"
                elif "am" in line.lower():
                    time_label = "AM convert"
                elif "pm" in line.lower():
                    time_label = "PM convert"
                else:
                    time_label = "Convert"
                match = re.search(r",\s*(\w)", line)
                if match:
                    customer = match.group(1)
                    tech_tasks[tech_name].append(f"{time_label} – {customer}")
            elif "prep" in line.lower():
                tech_tasks[tech_name].append("Prep – Aroostook Agency on Aging")
            elif "tree" in line.lower():
                match = re.search(r",\s*(\w)", line)
                if match:
                    tech_tasks[tech_name].append(f"Tree on drop – {match.group(1)}")
            elif "survey" in line.lower() and "door hanger" in line.lower():
                tech_tasks[tech_name].append("Surveys/Door hangers – Princeton")
            elif "phone" in line.lower() or "static" in line.lower():
                match = re.search(r",\s*(\w)", line)
                if match:
                    tech_tasks[tech_name].append(f"Phone fix – {match.group(1)}")
            elif "low line" in line.lower():
                match = re.search(r",\s*(\w)", line)
                if match:
                    tech_tasks[tech_name].append(f"Low line – {match.group(1)}")
            elif "low drop" in line.lower() or "highland" in line.lower():
                tech_tasks[tech_name].append("Low drop – Highland Ave")
            elif "rot" in line.lower():
                match = re.search(r",\s*(\w)", line)
                if match:
                    tech_tasks[tech_name].append(f"ROT – {match.group(1)}")

    return tech_tasks

def generate_summary(text):
    parsed = parse_work_orders(text)
    result = ""
    for tech, tasks in parsed.items():
        result += f"**{tech}**\n"
        for task in tasks:
            result += f"- {task}\n"
        result += "\n"
    return result.strip()

# Streamlit UI
st.title("Work Order Summary Email Generator")
uploaded_file = st.file_uploader("Upload PDF Work Order", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    summary = generate_summary(text)
    st.markdown("### Auto-Generated Summary Email")
    st.markdown(summary)
    st.download_button("Download Summary as Text", summary, file_name="summary.txt")
