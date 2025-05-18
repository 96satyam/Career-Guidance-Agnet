import os
import re
import spacy
import pdfplumber

nlp = spacy.load("en_core_web_sm")

class ResumeParser:
    def __init__(self):
        self.nlp = nlp

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def parse(self, input_text):
        """
        Extract name, education, experience, and skills from resume text
        """
        doc = self.nlp(input_text)
        parsed_data = {
            "name": self.extract_name(doc),
            "education": self.extract_education(input_text),
            "experience": self.extract_experience(input_text),
            "skills": self.extract_skills(input_text)
        }
        return parsed_data

    def extract_name(self, doc):
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Name Not Found"

    def extract_education(self, text):
        edu_keywords = [
            "B.Tech", "Bachelor", "Master", "B.Sc", "M.Sc", "M.Tech", "PhD",
            "CBSE", "ICSE", "School", "University", "College", "Diploma"
        ]
        lines = text.split('\n')
        education_lines = [line.strip() for line in lines if any(keyword in line for keyword in edu_keywords)]
        return education_lines

    def extract_experience(self, text):
        exp_keywords = [
            "Intern", "Internship", "Experience", "Engineer", "Developer", "Executive", "Manager",
            "Project", "Worked", "Company", "Role", "Responsibilities", "Freelance"
        ]
        lines = text.split('\n')
        exp_lines = [line.strip() for line in lines if any(keyword in line for keyword in exp_keywords)]
        return exp_lines

    def extract_skills(self, text):
        # A simple static skill list (extendable with job-skill dataset)
        skill_set = [
            "python", "java", "c++", "sql", "excel", "pandas", "numpy", "machine learning",
            "deep learning", "nlp", "data analysis", "html", "css", "javascript", "react", "node.js",
            "git", "tensorflow", "pytorch", "power bi", "tableau"
        ]
        found = set()
        for skill in skill_set:
            if re.search(r"\b" + re.escape(skill) + r"\b", text, re.IGNORECASE):
                found.add(skill.title())
        return list(found)

    def parse_from_pdf(self, pdf_path):
        text = self.extract_text_from_pdf(pdf_path)
        return self.parse(text)


if __name__ == "__main__":
    parser = ResumeParser()

    # From text string
    sample_text = """
    Satyam Tiwari
    B.Tech in AI & Data Science - VIPS
    Machine Learning Intern at Vaishnav Technologies
    Skills: Python, SQL, Pandas, Machine Learning
    """
    print(parser.parse(sample_text))

    # From PDF file
    # parsed_data = parser.parse_from_pdf("resumes/satyam_resume.pdf")
    # print(parsed_data)
