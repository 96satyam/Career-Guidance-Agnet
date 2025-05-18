import os
from dotenv import load_dotenv
from agents.user_interaction import UserInteractionAgent
from agents.resume_builder import ResumeFileGenerator  # Adjust import as per your file structure

def main():
    # Load environment variables from .env
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        return

    user_agent = UserInteractionAgent(openai_api_key=openai_api_key)
    resume_generator = ResumeFileGenerator()

    # Simulate user data input
    user_skills_input = "Python, SQL, Machine Learning, Communication"
    user_profile = {
    "name": "Satyam Tiwari",
    "email": "satyam@example.com",
    "phone": "+91 12345 67890",
    "summary": "Aspiring Data Scientist...",
    "skills": ["Python", "SQL", "Machine Learning"],
    "education": [
        {"degree": "B.Tech in AI and Data Science", "institution": "VIPS", "year": "2025"},
        {"degree": "12th CBSE", "institution": "XYZ School", "year": "2021"}
    ],
    "experience": [
        {"title": "Intern", "company": "Vaishnav Technologies", "duration": "6 months"},
        {"title": "Business Executive", "company": "Shri Ram Telecommunication", "duration": "1 year"}
    ]
}


    print("=== Career Suggestions ===")
    career_suggestions = user_agent.get_career_suggestions(user_skills_input)
    if not career_suggestions:
        print("No career suggestions found.")
        return

    for idx, cs in enumerate(career_suggestions[:5], 1):
        print(f"{idx}. {cs['job_role']} - Match: {cs['match_percentage']}%")

    selected_role = career_suggestions[0]["job_role"]
    print(f"\nSelected Role: {selected_role}")

    print("\n=== Skills Gap Analysis ===")
    skills_gap = user_agent.get_skills_gap(user_profile["skills"], selected_role)
    print(f"Matched Skills: {skills_gap['matched']}")
    print(f"Missing Skills: {skills_gap['missing']}")

    print("\n=== Resume Generation ===")
    # Generate PDF resume file path
    output_pdf_path = f"{user_profile['name'].replace(' ', '_').lower()}_resume.pdf"
    resume_generator.generate_pdf(user_profile, output_pdf_path)
    print(f"Resume PDF generated: {output_pdf_path}")

    print("\n=== LinkedIn Strategy ===")
    linkedin_plan = user_agent.get_linkedin_strategy(selected_role, user_profile["skills"])
    print(f"Headline:\n{linkedin_plan['headline']}\n")
    print(f"Summary:\n{linkedin_plan['summary']}\n")
    print("Content Ideas:")
    for idea in linkedin_plan['content_ideas']:
        print(f"- {idea}")

if __name__ == "__main__":
    main()
