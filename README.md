Perfect — here’s a **polished README.md** you can drop straight into your repo.
It’s short, professional, and makes your project look like a finished portfolio piece.

---

````markdown
# GenAI Resume & Cover Letter Tailor

**Live Demo:** [View on Streamlit Cloud](https://your-streamlit-app-link-here)  
**Author:** Daniel Ajibade

---

## 📄 Overview
This is a **GenAI-powered web app** that tailors your resume and generates a matching cover letter in minutes.  
Upload your resume, paste a job description, and let AI customize your documents for maximum relevance.

Built for quick iteration and recruiter-friendly demos, the app focuses on:
- **Clean, professional PDF formatting**
- **Fast AI-generated tailoring**
- **Ease of use** with sample data for testing

---

## ✨ Features
- **Upload**: Supports PDF and DOCX resumes.
- **AI Tailoring**: Uses OpenAI's GPT model to rewrite your resume for a specific job.
- **Cover Letter**: Auto-generates a matching, personalized cover letter.
- **PDF Export**: Outputs polished PDFs with subheadings, bullet points, and consistent formatting.
- **Sample Data**: Click one button to load a sample resume and job description for testing.

---

## 🛠️ Tech Stack
- **Frontend & UI**: [Streamlit](https://streamlit.io/)
- **AI**: OpenAI API (`gpt-5-mini` in this demo)
- **PDF Processing**: `fpdf2`, `PyPDF2`
- **Docx Parsing**: `python-docx`

---

## 🚀 Quick Start (Local)
1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/Resume-tailor-GenAI.git
   cd Resume-tailor-GenAI
````

2. **Set up environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Add your API key**

   * Create a `.streamlit/secrets.toml` file:

     ```toml
     OPENAI_API_KEY = "your_api_key_here"
     ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

---

## 📂 Project Structure

```
Resume-tailor-GenAI/
│
├── app.py                # Main Streamlit app
├── prompts.py            # Prompt templates for resume & cover letter
├── utils.py              # Helper functions (PDF formatting, file parsing)
├── fonts/                # DejaVuSans fonts for clean PDF output
├── sample_data/          # Sample resume & job description
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 💡 Usage Tips

* **For recruiters**: Try the "Load Sample Data" button to see output instantly.
* **For developers**: Modify `prompts.py` to experiment with tone, style, and structure.
* Keep your API key secure — never commit it to GitHub.

---

## 📜 License

MIT License — free to use, modify, and share.

---

**Built with care for fast AI prototyping and real-world resume tailoring.**

```

---


