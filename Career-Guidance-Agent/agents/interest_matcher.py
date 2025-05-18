import sys
from pathlib import Path

# Dynamically add the project root to sys.path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from tools.data_loader import load_job_roles, load_learning_resources
from tools.text_cleaner import clean_skills, match_skills


class InterestMatcherAgent:
    def __init__(self):
        self.job_roles_df = load_job_roles()
        self.learning_resources = load_learning_resources()

    def match_user_skills(self, user_skills_input: str):
        """
        Matches user skills to job roles based on skill overlap.
        Returns: list of dicts sorted by match percentage
        """
        user_skills = clean_skills(user_skills_input)
        results = []

        for _, row in self.job_roles_df.iterrows():
            role = row["Job Role"]
            required_skills = clean_skills(row["Skills"])
            skill_match = match_skills(user_skills, required_skills)

            matched = skill_match["matched_skills"]
            missing = skill_match["missing_skills"]
            match_percent = (len(matched) / len(required_skills)) * 100 if required_skills else 0

            resources = {
                skill: self.learning_resources.get(skill, ["(No resources found)"]) for skill in missing
            }

            results.append({
                "job_role": role,
                "match_percentage": round(match_percent, 2),
                "matched_skills": matched,
                "missing_skills": missing,
                "missing_resources": resources
            })

        results.sort(key=lambda x: x["match_percentage"], reverse=True)
        return results


if __name__ == "__main__":
    agent = InterestMatcherAgent()
    user_input = "python, sql, html, css"
    matches = agent.match_user_skills(user_input)

    for match in matches[:5]:  # Top 5 roles
        print(f"\n🔹 Job Role: {match['job_role']}")
        print(f"✅ Match: {match['match_percentage']}%")
        print(f"✅ Matched Skills: {match['matched_skills']}")
        print(f"❌ Missing Skills: {match['missing_skills']}")
        print("📚 Suggested Resources:")
        for skill, links in match["missing_resources"].items():
            print(f"  {skill}:")
            for link in links:
                print(f"    - {link}")
