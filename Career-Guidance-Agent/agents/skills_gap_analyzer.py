from typing import List, Dict, Set


class SkillsGapAnalyzerAgent:
    def __init__(self, user_skills: List[str], career_requirements: List[str]):
        self.user_skills_set: Set[str] = {skill.lower() for skill in user_skills}
        self.required_skills_set: Set[str] = {skill.lower() for skill in career_requirements}

    def analyze_gap(self) -> Dict[str, List[str]]:
        """
        Compares user skills with required skills and identifies matched and missing skills.

        Returns:
            A dictionary with keys 'matched' and 'missing', each containing a list of skills.
        """
        matched = sorted(self.user_skills_set & self.required_skills_set)
        missing = sorted(self.required_skills_set - self.user_skills_set)

        return {
            "matched": matched,
            "missing": missing
        }


# Example test block (optional, for dev)
if __name__ == "__main__":
    user_skills = ["python", "sql", "css"]
    required_skills = ["Python", "SQL", "Pandas", "Statistics", "Numpy", "Machine Learning"]

    agent = SkillsGapAnalyzerAgent(user_skills, required_skills)
    result = agent.analyze_gap()

    from pprint import pprint
    pprint(result)
