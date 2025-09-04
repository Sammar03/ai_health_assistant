An AI-powered health assistant that leverages **LLMs** and **Firebase** to provide intelligent, secure, and scalable healthcare support. This project demonstrates how to integrate machine learning models with modern deployment tools, making it easier for developers and researchers to build and extend AI-driven healthcare applications.


## 🚀 Features

* 🤖 **LLM Integration** – Use of language models for natural and contextual health-related interactions.
* 🔐 **Secure Config Management** – Secrets managed via `.streamlit/secrets.toml` and `.env` (not included in repo).
* ☁️ **Firebase Integration** – Backend for authentication, database, and API services.
* 📄 **PDF Parsing** – Extract structured information from uploaded medical PDFs and reports.
* ⚡ **Streamlit Frontend** – Interactive and easy-to-use UI for real-time interaction.
* 🛡️ **Scalable Architecture** – Modular design with separate utilities for LLM, Firebase, and PDF processing.


## 🛠 Tech Stack

* **Frontend / UI**: [Streamlit](https://streamlit.io/)
* **AI / NLP**: Large Language Models (LLMs)
* **Backend**: Firebase (Authentication, Firestore, Storage)
* **Data Handling**: Python utilities (`pdf_parser.py`, custom utils)
* **Environment Management**: `.env`, `.streamlit/secrets.toml`


## 📂 Project Structure

AI_HEALTH_ASSISTANT/
│-- app.py                  # Main entry point for Streamlit app
│-- utils/                  # Utility modules
│   │-- firebase_interface.py
│   │-- llm_interface.py
│   │-- pdf_parser.py
│-- .streamlit/             # Streamlit config (secrets excluded)
│-- requirements.txt        # Python dependencies
│-- README.md               # Project documentation



## ⚡ Getting Started

1. **Clone the Repository**

   git clone https://github.com/<your-username>/ai_health_assistant.git
   cd ai_health_assistant

2. **Create Virtual Environment & Install Dependencies**

   python -m venv venv
   source venv/bin/activate   # (Linux/Mac)
   venv\Scripts\activate      # (Windows)
   pip install -r requirements.txt

3. **Add Secrets**

   * Create `.streamlit/secrets.toml` and `.env` in your local project.
   * Insert your Firebase credentials and API keys (not included in repo for security).

4. **Run the App**

   streamlit run app.py

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to fork the repo and submit pull requests.


## 📜 License

This project is open-source and available under the **MIT License**.
