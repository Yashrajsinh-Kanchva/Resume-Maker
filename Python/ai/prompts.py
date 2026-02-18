import json

def build_resume_prompt(user_data: dict) -> str:
    """
    Builds a strict prompt for AI resume generation.
    - Uses ONLY data provided by the user
    - NO projects
    - NO experience (unless explicitly given later)
    - STRICT JSON output (frontend-safe)
    """

    return f"""
    You are an AI resume generator.

    IMPORTANT RULES (DO NOT BREAK):
    - Use ONLY the information provided in USER DATA
    - DO NOT invent names, titles, education, or skills
    - DO NOT add projects
    - If experience data is provided in USER DATA, enhance wording but do NOT invent roles, companies, or dates
    - DO NOT add extra fields
    - DO NOT add explanations
    - DO NOT use markdown
    - OUTPUT MUST BE VALID JSON ONLY

    --------------------
    REQUIRED JSON FORMAT:
    {{
      "summary": "A compelling 2–3 line professional summary written in a confident, impact-driven tone.",
      "education": {{
        "institution": "<institution from user data>",
        "degree": "<degree from user data>",
        "field": "<field from user data>",
        "year": "<year from user data>"
      }},
      "experience": [
        {{
          "jobTitle": "",
          "employer": "",
          "city": "",
          "country": "",
          "startMonth": "",
          "endMonth": "",
          "description": ""
        }}
      ],
      "skills": ["<skill1>", "<skill2>", "<skill3>"]
    }}

    --------------------
    USER DATA (SOURCE OF TRUTH):
    {json.dumps(user_data, indent=2)}

    RETURN JSON ONLY.
    """


def build_role_suggestions_prompt(role: str) -> str:
    """Build prompt for AI to suggest title, summary, skills, and job description from a role only."""
    return f"""You are a resume expert. The user wants to create a resume for this role: "{role}".

Generate suggestions ONLY. Return valid JSON with no markdown, no explanation.

REQUIRED JSON FORMAT:
{{
  "title": "Exact job title for this role (e.g. Java Developer, Data Scientist)",
  "summary": "2-3 sentences professional summary tailored for this role. Write in third person, confident tone.",
  "skills": ["skill1", "skill2", "skill3", "skill4", "skill5", "skill6", "skill7", "skill8"],
  "job_description": "2-4 lines: a short typical job description for this role that the user can paste or edit. What employers often look for."
}}

Use the role "{role}" to pick relevant skills and wording. Return JSON only."""
