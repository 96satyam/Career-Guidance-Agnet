# agents/career_path_agent.py

import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from tools.data_loader import load_job_roles, load_learning_resources
from tools.text_cleaner import clean_skills, match_skills


class CareerPathAgent:
    def __init__(self):
        self.job_roles_df = load_job_roles()
        self.learning_resources = load_learning_resources()
        self.progression_map = self._build_progression_map()

    def _build_progression_map(self):
        """
        Create a dummy progression path from existing job roles.
        This can be replaced with a more advanced path-planning logic later.
        """
        categories = {}
        for _, row in self.job_roles_df.iterrows():
            category = row.get("Category", "General")
            if category not in categories:
                categories[category] = []
            categories[category].append(row["Job Role"])

        # Sort roles by rough seniority using keyword heuristics
        for cat in categories:
            categories[cat].sort(key=lambda x: (
                "junior" in x.lower(),
                "associate" in x.lower(),
                "mid" in x.lower(),
                "senior" in x.lower(),
                "lead" in x.lower(),
                "manager" in x.lower(),
                "director" in x.lower(),
            ))
        return categories

    def suggest_paths(self, user_skills_input, user_interest_area=None):
        user_skills = clean_skills(user_skills_input)
        matched_paths = []

        for category, roles in self.progression_map.items():
            if user_interest_area and user_interest_area.lower() not in category.lower():
                continue  # Skip categories not matching interest

            for role in roles:
                role_row = self.job_roles_df[self.job_roles_df["Job Role"] == role]
                if role_row.empty:
                    continue

                required_skills = clean_skills(role_row.iloc[0]["Skills"])
                skill_match = match_skills(user_skills, required_skills)

                matched_count = len(skill_match["matched_skills"])
                total_required = len(required_skills)
                match_percentage = (matched_count / total_required) * 100 if total_required else 0

                missing_resources = {
                    skill: self.learning_resources.get(skill, ["(No resources found)"])
                    for skill in skill_match["missing_skills"]
                }

                matched_paths.append({
                    "category": category,
                    "role": role,
                    "match_percentage": round(match_percentage, 2),
                    "matched_skills": skill_match["matched_skills"],
                    "missing_skills": skill_match["missing_skills"],
                    "resources": missing_resources,
                    "progression": roles  # Full path from entry to senior roles
                })

        # Sort by match percentage and limit top 5 paths
        matched_paths.sort(key=lambda x: x["match_percentage"], reverse=True)
        return matched_paths[:5]


if __name__ == "__main__":
    agent = CareerPathAgent()

    # Example test
    user_input = "python, sql, machine learning, communication"
    user_interest = "Data"

    paths = agent.suggest_paths(user_input, user_interest)

    for path in paths:
        print(f"\n🧭 Role: {path['role']} (Category: {path['category']})")
        print(f"Match: {path['match_percentage']}%")
        print(f"Matched Skills: {path['matched_skills']}")
        print(f"Missing Skills: {path['missing_skills']}")
        print("Resources:")
        for skill, links in path["resources"].items():
            print(f"  {skill}:")
            for link in links:
                print(f"    - {link}")
        print(f"Progression Path: {' ➝ '.join(path['progression'])}")
