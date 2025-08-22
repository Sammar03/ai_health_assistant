import openai
import streamlit as st

# Create OpenAI-compatible client for Groq
client = openai.OpenAI(
    api_key=st.secrets["groq"]["api_key"],
    base_url="https://api.groq.com/openai/v1"
)

def simplify_text(text):
    prompt = (
        "You are a healthcare assistant. Simplify the following hospital discharge summary "
        "so that it is easy for the patient to understand. Return only the most relevant information "
        "in clear, concise bullet points. Avoid medical jargon. Do NOT include any unnecessary commentary "
        "or explanations. Maintain a professional, calm, and encouraging tone. "
        "Ensure the summary is actionable and easy to read.\n\n"
        f"{text}"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content
