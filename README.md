# 🎯 GenAI Resume & Cover Letter Tailor

**Live Demo:** [🚀 Try it here](https://resume-tailor-genai-6qwsa4ykamrwzm3fo9zxef.streamlit.app/)  
**Author:** Daniel Ajibade  

---

## 📄 Overview  
A **GenAI-powered Streamlit web app** that tailors your resume and generates a matching cover letter in minutes.  
Simply upload your resume, paste a job description, and let AI craft polished, role-specific documents ready to send.  

**Why it stands out:**  
- 📑 Professional, recruiter-friendly PDF formatting  
- ⚡ Fast and responsive AI output  
- 🎯 Easy to test with built-in sample data  

---

## ❗ Problem  
Manually tailoring resumes and cover letters for each job application is **time-consuming** and repetitive.  
Applicants often spend hours rewording skills and achievements to match each role — time that could be spent preparing for interviews.  

---

## 💡 Solution  
This app automates the process by combining **document parsing** with **LLM-powered text generation**:  

1. **Extracts** relevant skills, projects, and experience from your resume  
2. **Rewrites** the resume to align closely with the target job description  
3. **Generates** a tailored, ready-to-edit cover letter draft  

The result: a consistent, professional application package in **minutes instead of hours**.  

---

## ✨ Features
- 📤 **Upload Resume** — Supports PDF ONLY!  
- 🤖 **AI Tailoring** — Uses OpenAI GPT to rewrite your resume for the target role  
- 📝 **Cover Letter Generation** — Automatically matches the tailored resume  
- 📑 **Polished PDF Export** — Clean headings, smaller bullets, consistent layout  
- 🎯 **Sample Data Mode** — Instantly preview the app without uploading files  

---

## 🛠️ Tech Stack
- **Frontend & UI:** [Streamlit](https://streamlit.io/)  
- **AI Engine:** OpenAI API (`gpt-5-mini`)  
- **PDF Processing:** `fpdf2`, `PyPDF2`  
- **Document Parsing:** `python-docx`  

---

## 🚀 Run Locally

### 1️⃣ Clone the repo
```bash
git clone https://github.com/your-username/Resume-tailor-GenAI.git
cd Resume-tailor-GenAI

2️⃣ Set up environment
bash
Copy
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

3️⃣ Add your API key
Create a file .streamlit/secrets.toml:

toml
Copy
OPENAI_API_KEY = "your_api_key_here"

4️⃣ Start the app
bash
Copy
streamlit run app.py

📂 Project Structure
graphql
Copy
Resume-tailor-GenAI/
├── app.py               # Main Streamlit app
├── prompts.py           # AI prompt templates
├── utils.py             # File parsing & PDF formatting
├── fonts/               # DejaVuSans fonts for output
├── sample_data/         # Example resume & JD
├── requirements.txt     # Dependencies
└── README.md

💡 Tips
Recruiters: Use "Load Sample Data" to test instantly

Developers: Modify prompts.py to adjust tone & style

Keep your API key private — never commit it to GitHub
