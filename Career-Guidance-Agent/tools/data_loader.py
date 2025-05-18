import pandas as pd
import json
from pathlib import Path

# Define paths relative to the root of the project
BASE_PATH = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_PATH / "data/job_roles.csv"
JSON_PATH = BASE_PATH / "data/learning_resources.json"

def load_job_roles() -> pd.DataFrame:
    """Load the job_roles.csv file as a DataFrame."""
    try:
        df = pd.read_csv(CSV_PATH)
        return df
    except Exception as e:
        raise FileNotFoundError(f"Error loading job_roles.csv: {e}")

def load_learning_resources() -> dict:
    """Load the learning_resources.json file as a dictionary."""
    try:
        with open(JSON_PATH, "r") as file:
            return json.load(file)
    except Exception as e:
        raise FileNotFoundError(f"Error loading learning_resources.json: {e}")

def get_all_job_roles() -> list:
    """Return a list of all job roles."""
    df = load_job_roles()
    return df["Job Role"].tolist()

def get_required_skills_for_role(role_name: str) -> list:
    """Return a list of required skills for a given job role."""
    df = load_job_roles()
    matched_row = df[df["Job Role"].str.lower() == role_name.lower()]
    if matched_row.empty:
        return []
    skills_str = matched_row.iloc[0]["Required Skills"]
    return [skill.strip() for skill in skills_str.split(",")]

def get_learning_links_for_skill(skill: str) -> list:
    """Return a list of learning URLs for a skill, if available."""
    data = load_learning_resources()
    cleaned_skill = skill.strip()
    return data.get(cleaned_skill, [])
