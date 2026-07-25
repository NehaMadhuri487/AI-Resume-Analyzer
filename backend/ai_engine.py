'''import os, json
from dotenv import load_dotenv
from google import genai

load_dotenv()

def init_gemini(api_key: str = None):
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY in environment.")
    return genai.Client(api_key=api_key)

def analyze_resume(resume_text: str, job_desc_text: str, api_key: str = None) -> dict:
    client = init_gemini(api_key)

    prompt = f"""
    You are an ATS Resume Analyzer.
    Return ONLY valid JSON. Do not include explanations or text outside JSON.
    Schema:
    {{
      "ats_score": int,
      "match_status": string,
      "summary": string,
      "strengths": [{{"title": string, "detail": string}}],
      "weaknesses": [{{"title": string, "detail": string}}],
      "role_alignment": {{"rating": int, "explanation": string}},
      "keyword_analysis": {{"matched": [string], "missing": [string]}},
      "suggestions": [{{"section": string, "suggestion": string}}]
    }}

    Resume: {resume_text}
    Job Description: {job_desc_text}
    """

    response = client.models.generate_content(
        model="models/gemini-2.5-pro",
        contents=prompt
    )

    try:
        raw_output = response.candidates[0].content.parts[0].text

        # 🔧 Remove markdown fences if present
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`")   # remove backticks
            raw_output = raw_output.replace("json", "", 1).strip()

        return json.loads(raw_output)
    except Exception as e:
        return {"error": f"Failed to parse JSON: {str(e)}", "raw_output": response}
'''
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()


def init_gemini(api_key: str = None):
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API key not found. Please set GEMINI_API_KEY in environment."
        )

    return genai.Client(api_key=api_key)


# Reduce unnecessary token usage
def clean_text(text: str, limit: int):
    if not text:
        return ""

    text = " ".join(text.split())
    return text[:limit]


def analyze_resume(
    resume_text: str,
    job_desc_text: str,
    api_key: str = None
) -> dict:

    client = init_gemini(api_key)

    # Compress text before sending
    resume_text = clean_text(resume_text, 5000)
    job_desc_text = clean_text(job_desc_text, 3000)

    prompt = f"""
You are an ATS Resume Analyzer.

Compare the resume with the job description.

Return ONLY valid JSON.

Schema:
{{
  "ats_score": int,
  "match_status": string,
  "summary": string,
  "strengths": [
    {{
      "title": string,
      "detail": string
    }}
  ],
  "weaknesses": [
    {{
      "title": string,
      "detail": string
    }}
  ],
  "role_alignment": {{
    "rating": int,
    "explanation": string
  }},
  "keyword_analysis": {{
    "matched": [string],
    "missing": [string]
  }},
  "suggestions": [
    {{
      "section": string,
      "suggestion": string
    }}
  ]
}}

Rules:
- ATS score between 0 and 100
- Summary maximum 150 words
- Maximum 5 suggestions
- Return JSON only

Resume:
{resume_text}

Job Description:
{job_desc_text}
"""

    try:

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",   # changed from pro
            contents=prompt
        )

        raw_output = response.candidates[0].content.parts[0].text

        # Remove markdown if model wraps JSON
        raw_output = (
            raw_output
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(raw_output)

    except json.JSONDecodeError:
        return {
            "error": "Failed to parse model JSON response",
            "raw_output": raw_output
        }

    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}"
        }