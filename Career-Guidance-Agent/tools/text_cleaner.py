import re

def clean_text(text: str) -> str:
    """
    Normalize a text string:
    - Lowercase
    - Strip whitespace
    - Remove special characters 
    """
    text = text.strip().lower()
    text = re.sub(r"[^\w+#]+", " ", text)  
    return text.strip()

def clean_skills(skills: str) -> list:
    """
    Takes a comma-separated string of skills and returns a cleaned list.
    """
    return [clean_text(skill) for skill in skills.split(",") if skill.strip()]

def match_skills(user_skills: list, required_skills: list) -> dict:
    """
    Compares user skills with required skills and returns matched and missing ones.
    """
    user_set = set(clean_text(skill) for skill in user_skills)
    required_set = set(clean_text(skill) for skill in required_skills)

    matched = user_set & required_set
    missing = required_set - user_set

    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing)
    }
