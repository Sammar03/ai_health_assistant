# utils/firebase_interface.py

import streamlit as st
import json
import firebase_admin
from firebase_admin import credentials, firestore, storage

# --- Load Firebase credentials from JSON path defined in secrets.toml ---
with open(st.secrets["firebase"]["json_path"]) as f:
    firebase_credentials = json.load(f)

cred = credentials.Certificate(firebase_credentials)

# --- Initialize Firebase only once ---
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "storageBucket": f"{firebase_credentials['project_id']}.appspot.com"
    })

# Firestore & Storage clients
db = firestore.client()
bucket = storage.bucket()


# --- Helper Functions ---
def save_discharge_summary(patient_id: str, summary: dict):
    """Save a discharge summary for a patient."""
    db.collection("discharge_summaries").document(patient_id).set(summary)


def save_symptom(patient_id: str, symptom_data: dict):
    """Save symptom data for a patient."""
    db.collection("symptoms").document(patient_id).set(symptom_data)


def get_patient_data(patient_id: str):
    """Retrieve patient discharge summary if available."""
    doc = db.collection("discharge_summaries").document(patient_id).get()
    return doc.to_dict() if doc.exists else None
