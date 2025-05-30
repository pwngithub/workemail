import streamlit as st
from collections import defaultdict

st.set_page_config(page_title="Technician Summary", layout="centered")
st.title("Technician Work Summary")

st.markdown("Upload a PDF of the daily work schedule. The app will summarize technician tasks for email distribution.")

uploaded_file = st.file_uploader("Upload Work Schedule PDF", type=["pdf"])

# Predefined technician code mapping
tech_code_map = {
    "0CC": "Cam Callnan",
    "0CN": "Nash Hayward",
    "0GG": "Gage G",
    "0JL": "Jason Laws",
    "0JJ": "Jake J",
    "0NL": "Noah Jackins",
    "0PC": "Preston C",
}

if uploaded_file:
    import fitz  # PyMuPDF
    import re

    # Read PDF text
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        raw_text = " ".join(page.get_text() for page in doc)

    # Extract technician work entries
    entries = re.split(r"(?=0[A-Z]{2}\s+\d{3}\s+[A-Z][a-z]+,\s+[A-Z])", raw_text)

    task_summary = defaultdict(list)

    for entry in entries:
        match = re.match(r"(0[A-Z]{2})\s+\d{3}\s+[A-Z]{3}\s+([A-Z][a-z]+),\s+([A-Z])", entry)
        if not match:
            continue

        tech_code = match.group(1)
        last_name = match.group(2)
        initial = match.group(3)
        tech_name = tech_code_map.get(tech_code, f"{last_name} {initial}")

        # Extract customer initial
        customer_match = re.search(r"([A-Z][a-z]+),\s*([A-Z])", entry)
        customer_initial = f"{customer_match.group(2)}." if customer_match else ""

        entry_lower = entry.lower()
        if "convert" in entry_lower:
            task = f"Convert – {customer_initial}"
        elif "install" in entry_lower:
            task = f"FTTH install – {customer_initial}"
        elif "survey" in entry_lower:
            task = f"Survey – {customer_initial}"
        elif "rot" in entry_lower:
            task = f"ROT – {customer_initial}"
        elif any(word in entry_lower for word in ["offline", "modem", "signal", "internal service"]):
            task = f"Phone fix – {customer_initial}"
        elif "tree" in entry_lower:
            task = f"Tree on drop – {customer_initial}"
        elif "door hanger" in entry_lower or "princeton" in entry_lower:
            task = "Surveys/door hangers in Princeton"
        else:
            continue

        task_summary[tech_name].append(task)

    st.subheader("Summary Email Preview")
    for tech, tasks in task_summary.items():
        st.markdown(f"**{tech}**")
        for task in tasks:
            st.markdown(f"- {task}")
        st.markdown("\n")
