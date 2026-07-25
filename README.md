# AI-Resume-Analyzer
# 🚀 AI Resume Analyzer

An AI-powered Resume Analyzer built with **Streamlit** that evaluates resumes against a target job description using AI and a Hybrid ATS scoring system. The application provides semantic matching, keyword analysis, and personalized suggestions to improve resume quality.

---

## ✨ Features

- 📄 Upload Resume (PDF)
- 📝 Enter Target Job Description
- 🤖 AI-Powered Resume Analysis
- 📊 Hybrid ATS Score
- 🎯 Semantic Resume Matching
- 🔍 Keyword Coverage Analysis
- 💡 Resume Improvement Suggestions
- 📈 Interactive ATS Score Gauge
- 🎨 Clean and Responsive UI

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Plotly
- Google Gemini API
- PyPDF2
- python-dotenv

---

## 📂 Project Structure

```
resume-analyzer-ai/
│
├── backend/
│   ├── ai_engine.py
│   ├── parser.py
│   ├── scorer.py
│   └── utils.py
│
├── data/
│   ├── sample_resume.txt
│   └── sample_jd.txt
│
├── prompts/
│   └── resume_prompt.py
│
├── app.py
├── requirements.txt
├── README.md
└── .env
```

---

## 📥 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/resume-analyzer-ai.git
cd resume-analyzer-ai
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

## 📊 How It Works

1. Upload a resume in PDF format.
2. Enter the target job description.
3. Click **Run Analysis**.
4. The application:
   - Extracts text from the resume
   - Compares it with the job description
   - Calculates a Hybrid ATS Score
   - Performs semantic matching
   - Analyzes keyword coverage
   - Generates AI-powered suggestions
5. Displays detailed analysis and recommendations.

---

## 🚀 Future Enhancements

- Resume Comparison
- Download Analysis Report (PDF)
- Resume Templates

---

## 📜 License

This project is developed for educational and learning purposes.
