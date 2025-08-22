import streamlit as st
from utils.pdf_parser import extract_text_from_pdf
from utils.llm_interface import simplify_text
from utils.firebase_interface import save_discharge_summary, save_symptom, get_patient_data
from datetime import datetime
import pandas as pd
import altair as alt
import re

st.set_page_config(page_title="AI Health Assistant", layout="wide")

# ---------- Styles (static only; safe to allow HTML) ----------
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .big-font { font-size:20px !important; font-weight: bold; }
    .medium-font { font-size:16px !important; }
    .stButton>button {
        font-size: 18px; height: 3em; width: 100%;
        border-radius: 0.5em; border: 1px solid #007bff; color: #007bff;
    }
    .stButton>button:hover { background-color: #007bff; color: white; }
    .stTextArea textarea { min-height: 80px; }
    .stTextInput div div input { height: 3em; }
    .summary-box {
        background-color: #e6f7ff; border-left: 5px solid #007bff;
        padding: 1em; border-radius: 0.5em; margin-bottom: 1em;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- Helpers ----------
def sanitize_patient_id(pid: str) -> str:
    """Allow only A–Z, a–z, 0–9, underscore, dash; length 3–64."""
    pid = (pid or "").strip()
    return pid if re.fullmatch(r"[A-Za-z0-9_\-]{3,64}", pid) else ""

MAX_PDF_MB = 10

# ---------- Title ----------
st.markdown("<h1 style='text-align: center; color: #007bff;'>🧠 AI Health Assistant for Post-Discharge Monitoring</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------- Patient ID ----------
col_id1, col_id2, col_id3 = st.columns([1, 2, 1])
with col_id2:
    st.markdown("### Enter Patient Information")
    raw_patient_id = st.text_input(
        "Please enter your unique Patient ID to access your records.",
        key="patient_id",
        help="This ID helps us keep your health data secure and organized."
    )
patient_id = sanitize_patient_id(raw_patient_id)
if raw_patient_id and not patient_id:
    st.error("Invalid Patient ID. Use 3–64 characters: letters, numbers, '-' or '_' only.")
st.markdown("---")

# ---------- SECTION 1: Upload Discharge Summary ----------
st.markdown("## 📄 Discharge Summary Management")
st.markdown("Understand your post-discharge instructions easily.")
st.markdown("")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Upload & Simplify Summary")
    uploaded_file = st.file_uploader(
        "Upload your discharge summary PDF here.",
        type=["pdf"],
        help="We'll simplify complex medical terms for you."
    )
    st.markdown("")

    # Enforce PDF size limit
    if uploaded_file:
        size_mb = (uploaded_file.size or 0) / (1024 * 1024)
        if size_mb > MAX_PDF_MB:
            st.error(f"PDF is too large ({size_mb:.1f} MB). Please upload a file under {MAX_PDF_MB} MB.")
            uploaded_file = None

    if uploaded_file and patient_id:
        with st.spinner("Extracting and simplifying summary... Please wait."):
            extracted_text = extract_text_from_pdf(uploaded_file)
            try:
                simplified_text = simplify_text(extracted_text)
            except Exception:
                st.error("We couldn’t simplify the summary at the moment. Please try again.")
                st.stop()

        # SAFE rendering of dynamic content (no unsafe HTML)
        st.markdown("### Simplified Summary for You:")
        with st.container():
            st.markdown("<div class='summary-box'>", unsafe_allow_html=True)  # static wrapper is OK
            st.text_area(
                "Simplified Discharge Summary",
                simplified_text,
                height=180,
                disabled=True,
                label_visibility="collapsed",
                help="AI-generated simplified summary"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")  # spacing

        if st.button("Save Simplified Summary", help="Click to save this simplified summary to your patient record."):
            save_discharge_summary(patient_id, {
                "original_summary": extracted_text,
                "simplified_summary": simplified_text,
                "timestamp": datetime.now().isoformat()
            })
            st.success("Your simplified summary has been successfully saved!")
    elif uploaded_file and not patient_id:
        st.warning("Please enter a valid Patient ID before uploading the summary.")

with col2:
    st.markdown("### Important Notes")
    st.info("Upload your discharge summary PDF to get a clear, simplified explanation of your medical instructions. This helps you understand your recovery plan better.")
    st.info("After simplification, remember to **'Save Simplified Summary'** to your patient file for future reference.")

st.divider()

# ---------- SECTION 2: Symptom Logging ----------
st.markdown("## 🩺 Daily Symptom Check-In")
st.markdown("Let us know how you're feeling each day.")
st.markdown("")

symptom_col1, symptom_col2 = st.columns([3, 1])

with symptom_col1:
    st.markdown("### Describe Your Symptoms")
    symptom_input = st.text_area(
        "What symptoms are you experiencing today? (e.g., 'Mild headache', 'Feeling tired', 'Sharp pain in the knee')",
        height=100,
        key="symptom_input",
        help="Please be as descriptive as possible."
    )
    st.markdown("")

def assess_risk(symptom: str) -> str:
    symptom_lower = symptom.lower()
    if any(term in symptom_lower for term in ["fever", "pain", "bleeding", "shortness of breath"]):
        return "High"
    elif any(term in symptom_lower for term in ["tired", "dizzy", "nausea"]):
        return "Medium"
    else:
        return "Low"

with symptom_col2:
    st.markdown("### Log Symptom")
    if st.button("Log My Symptom", help="Click to record your current symptom and its assessed risk level."):
        if symptom_input and patient_id:
            risk_level = assess_risk(symptom_input)
            save_symptom(patient_id, symptom_input, risk_level)
            st.success(f"Symptom logged successfully with **{risk_level}** risk level.")
        elif not patient_id:
            st.warning("Please enter a valid Patient ID before logging.")
        else:
            st.warning("Please enter your symptom in the text box.")

st.divider()

# ---------- SECTION 3: Patient Logs Viewer ----------
st.markdown("## 📊 Your Health Progress & Logs")
st.markdown("Review your past summaries and symptom history.")
st.markdown("")

st.markdown("### Access Your Records")
if st.button("Load My Health Logs", help="Retrieve your saved simplified summary and symptom history."):
    if patient_id:
        patient_data = get_patient_data(patient_id)
        if not patient_data:
            st.warning("No health data found for this Patient ID. Please check the ID or log some data first.")
        else:
            st.markdown("<h4 style='color: #007bff;'>Latest Simplified Summary:</h4>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
                st.text_area(
                    "Latest Simplified Summary",
                    patient_data.get('simplified_summary', 'Not available.'),
                    height=180,
                    disabled=True,
                    label_visibility="collapsed"
                )
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("")

            logs = patient_data.get("symptom_logs", {})
            if logs:
                df = pd.DataFrame(logs).T
                # Defensive check for required columns
                expected_cols = {"timestamp", "symptom", "risk_level"}
                if expected_cols.issubset(df.columns):
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                    df = df.dropna(subset=['timestamp'])
                    df = df.sort_values('timestamp', ascending=False)

                    st.markdown("<h4 style='color: #007bff;'>Your Symptom History:</h4>", unsafe_allow_html=True)
                    st.dataframe(
                        df[['timestamp', 'symptom', 'risk_level']].reset_index(drop=True),
                        use_container_width=True
                    )

                    st.markdown("<h4 style='color: #007bff;'>Risk Level Trend Over Time:</h4>", unsafe_allow_html=True)
                    risk_order = ["Low", "Medium", "High"]
                    df['risk_level_ordered'] = pd.Categorical(df['risk_level'], categories=risk_order, ordered=True)

                    chart = alt.Chart(df).mark_line(point=True, strokeWidth=3).encode(
                        x=alt.X('timestamp:T', title="Date and Time"),
                        y=alt.Y('risk_level_ordered:N', sort=risk_order, title="Risk Level"),
                        tooltip=[
                            alt.Tooltip('timestamp:T', title='Time', format='%Y-%m-%d %H:%M'),
                            alt.Tooltip('symptom', title='Symptom'),
                            alt.Tooltip('risk_level', title='Risk')
                        ]
                    ).properties(
                        title="Symptom Risk Level Progression",
                        height=300
                    ).interactive()
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("Symptom logs found, but fields are incomplete.")
            else:
                st.info("No symptoms have been logged for this patient yet.")
    else:
        st.warning("Please enter a valid Patient ID to load your health logs.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>AI Health Assistant - Your well-being, simplified.</p>", unsafe_allow_html=True)
