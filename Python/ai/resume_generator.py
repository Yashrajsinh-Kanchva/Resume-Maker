from openai import OpenAI
from ai.prompts import build_resume_prompt, build_role_suggestions_prompt
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def suggest_from_role(role: str) -> dict:
    """Generate title, summary, skills, job_description from target role only."""
    if not role or not role.strip():
        return {
            "title": "",
            "summary": "",
            "skills": [],
            "job_description": ""
        }
    prompt = build_role_suggestions_prompt(role.strip())
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(content)
        return {
            "title": data.get("title", ""),
            "summary": data.get("summary", ""),
            "skills": data.get("skills", []) if isinstance(data.get("skills"), list) else [],
            "job_description": data.get("job_description", "")
        }
    except json.JSONDecodeError:
        return {"title": role.strip(), "summary": "", "skills": [], "job_description": ""}


def generate_ai_resume(user_data):
    prompt = build_resume_prompt(user_data)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()

    # 🔥 REMOVE MARKDOWN CODE BLOCKS IF PRESENT
    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    # Optional: log cleaned output
    print("CLEANED AI OUTPUT:\n", content)

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print("JSON PARSE ERROR:", e)
        print("RAW CONTENT WAS:\n", content)
        raise ValueError("AI did not return valid JSON") from e