import sys, os
from pathlib import Path

# Add project root to sys.path for importing other agents/tools
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
    
from dotenv import load_dotenv
from agents.interest_matcher import InterestMatcherAgent
from agents.skills_gap_analyzer import SkillsGapAnalyzerAgent
from agents.resume_builder import ResumeFileGenerator
from agents.linkedIn_strategy import LinkedInStrategyAgent
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

class UserInteractionAgent:
    def __init__(self, openai_api_key=None):
        self.interest_matcher = InterestMatcherAgent()
        self.linkedin_strategy = LinkedInStrategyAgent(openai_api_key=openai_api_key)
        self.resume_builder = ResumeFileGenerator()
        from tools.data_loader import load_job_roles
        self.job_roles_df = load_job_roles()

    def get_career_suggestions(self, user_skills_input):
        return self.interest_matcher.match_user_skills(user_skills_input)

    def get_skills_gap(self, user_skills, selected_role):
        career_row = self.job_roles_df[
            self.job_roles_df["Job Role"].str.lower() == selected_role.lower()
        ]

        if career_row.empty:
            print(f"❌ Role '{selected_role}' not found in job_roles_df")
            return {"matched": [], "missing": []}

        required_skills_str = career_row.iloc[0]["Skills"]
        required_skills = [skill.strip() for skill in required_skills_str.split(",")]

        analyzer = SkillsGapAnalyzerAgent(user_skills, required_skills)
        return analyzer.analyze_gap()

    def normalize_education(self, raw_education):
        normalized = []
        if isinstance(raw_education, str):
            raw_education = [raw_education]  # wrap single string into list
        for item in raw_education:
            if isinstance(item, dict):
                normalized.append(item)
            elif isinstance(item, str):
                parts = [part.strip() for part in item.split(" - ")]
                if len(parts) == 3:
                    normalized.append({
                        "degree": parts[0],
                        "institution": parts[1],
                        "year": parts[2]
                    })
                else:
                    normalized.append({
                        "degree": item,
                        "institution": "",
                        "year": ""
                    })
        return normalized

    def normalize_experience(self, raw_experience):
        import re
        normalized = []
        if isinstance(raw_experience, str):
            raw_experience = [raw_experience]  # wrap single string into list
        for item in raw_experience:
            if isinstance(item, dict):
                normalized.append(item)
            elif isinstance(item, str):
                pattern = r"^(.*?) at (.*?) \((.*?)\)$"
                match = re.match(pattern, item.strip())
                if match:
                    title, company, duration = match.groups()
                    normalized.append({
                        "title": title.strip(),
                        "company": company.strip(),
                        "duration": duration.strip()
                    })
                else:
                    normalized.append({
                        "title": item,
                        "company": "",
                        "duration": ""
                    })
        return normalized

    def build_resume(self, user_profile, selected_career_path):
        # Normalize education and experience before building resume
        user_profile["education"] = self.normalize_education(user_profile.get("education", []))
        user_profile["experience"] = self.normalize_experience(user_profile.get("experience", []))

        return self.resume_builder.generate_pdf(user_profile, selected_career_path)

    def get_linkedin_strategy(self, target_role, user_strengths):
        headline = self.linkedin_strategy.generate_headline(target_role, user_strengths)
        summary = self.linkedin_strategy.generate_summary(target_role, user_strengths)
        content_ideas = self.linkedin_strategy.generate_content_ideas(target_role, user_strengths)
        return {
            "headline": headline,
            "summary": summary,
            "content_ideas": content_ideas,
        }

if __name__ == "__main__":
    user_agent = UserInteractionAgent(openai_api_key="your_openai_api_key")

    # Sample input with mixed string and list/dict formats
    user_skills_input = "Python, SQL, Machine Learning, Communication"
    user_profile = {
        "name": "Satyam Tiwari",
        "education": [
            "B.Tech in AI and Data Science - VIPS - 2025",
            "12th CBSE - - 94%"
        ],
        "experience": [
            "Internship at Vaishnav Technologies (6 months)",
            "Business Executive at Shri Ram Telecommunication (1 year)"
        ],
        "skills": ["Python", "SQL", "Machine Learning", "Communication"],
        "interests": ["Data Science", "AI"],
    }

    print("\nCareer Suggestions:")
    career_suggestions = user_agent.get_career_suggestions(user_skills_input)
    for cs in career_suggestions[:3]:
        print(cs)

    selected_role = career_suggestions[0]["job_role"]
    print(f"\nSkills Gap for selected role: {selected_role}")
    skills_gap = user_agent.get_skills_gap(user_profile["skills"], selected_role)
    print(skills_gap)

    print("\nGenerating Resume...")
    resume_content = user_agent.build_resume(user_profile, selected_role)
    print(resume_content)

    print("\nLinkedIn Strategy:")
    linkedin_strategy = user_agent.get_linkedin_strategy(selected_role, user_profile["skills"])
    print(linkedin_strategy)
