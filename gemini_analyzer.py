import os
import json

from dotenv import load_dotenv
from google import genai

from config.config import (
    GEMINI_MODEL,
    EXTRACTED_TEXT,
    ANALYSIS_RESULT
)


# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit()


# Create Gemini client
client = genai.Client(api_key=api_key)


# Read extracted resume text
with open(EXTRACTED_TEXT, "r", encoding="utf-8") as file:
    resume_text = file.read()


if not resume_text.strip():
    print("ERROR: Resume text is empty.")
    exit()


# Prompt for resume analysis
prompt = f"""
You are an expert ATS resume analyzer and career advisor.

Analyze the following resume carefully.

Return ONLY valid JSON with exactly these fields:

{{
  "ats_score": 0,
  "recommended_roles": [],
  "technical_skills": [],
  "soft_skills": [],
  "strengths": [],
  "weaknesses": [],
  "missing_skills": [],
  "resume_improvements": []
}}

Rules:
- ats_score must be a number from 0 to 100.
- recommended_roles should contain suitable job roles based on the resume.
- technical_skills should contain skills actually found in the resume.
- soft_skills should contain soft skills actually found or reasonably inferred.
- strengths should identify important positive points.
- weaknesses should identify genuine areas that could be improved.
- missing_skills should suggest relevant skills missing for the recommended roles.
- resume_improvements should provide practical improvements.
- Do not invent qualifications, experience, projects, or skills.
- Return ONLY JSON. Do not use Markdown or code fences.

RESUME:
{resume_text}
"""


print("Analyzing resume with Gemini...")
print("Please wait...\n")


try:

    response = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt
    )

    result_text = response.output_text.strip()


    # Remove accidental Markdown code fences
    if result_text.startswith("```"):
        result_text = result_text.replace("```json", "", 1)
        result_text = result_text.replace("```", "", 1).strip()


    # Validate JSON
    analysis = json.loads(result_text)


    # Save analysis
    with open(ANALYSIS_RESULT, "w", encoding="utf-8") as file:
        json.dump(
            analysis,
            file,
            indent=4,
            ensure_ascii=False
        )


    print("========================================")
    print("   RESUME ANALYSIS SUCCESSFUL!")
    print("========================================")

    print(f"ATS Score: {analysis['ats_score']}/100")


    print("\nRecommended Roles:")

    for role in analysis["recommended_roles"]:
        print(f"- {role}")


    print("\nTechnical Skills:")

    print(", ".join(analysis["technical_skills"]))


    print("\nStrengths:")

    for item in analysis["strengths"]:
        print(f"- {item}")


    print("\nWeaknesses:")

    for item in analysis["weaknesses"]:
        print(f"- {item}")


    print("\nMissing Skills:")

    for item in analysis["missing_skills"]:
        print(f"- {item}")


    print("\nResume Improvements:")

    for item in analysis["resume_improvements"]:
        print(f"- {item}")


    print(f"\nAnalysis saved to: {ANALYSIS_RESULT}")


except json.JSONDecodeError:

    print("ERROR: Gemini returned invalid JSON.")

    print("\nGemini response:")
    print(result_text)


except Exception as e:

    print("ERROR:", e)