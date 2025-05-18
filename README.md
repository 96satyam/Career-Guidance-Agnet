# Career Guidance & Resume Builder using LLMs
## Personalized AI Career Advisor for Students & Professionals
An interactive AI-powered Streamlit app that analyzes your profile, recommends top career paths, suggests upskilling areas, and generates a tailored resume and LinkedIn strategy — all in one place.

## 🧠 What is This Project?
This is a smart Career Guidance Agent built using Large Language Models (LLMs) like OpenAI's GPT. It is designed to:

#### ✅ Understand your profile (education, experience, skills, interests)
#### ✅ Recommend career paths most aligned with your strengths
#### ✅ Highlight missing skills using Gap Analysis
#### ✅ Generate an ATS-friendly Resume Preview
#### ✅ Craft a personalized LinkedIn Strategy with headline, summary, and content ideas

### Built with a mission to empower freshers, final-year students, and job-seekers to take data-driven career decisions using AI.

#### 🎯 Core Features
#### Feature	Description
#### 👤 Profile Intake	Interactive form to capture your background
#### 🧭 Career Role Suggestions	AI-recommended job roles matched with your skills
#### 📊 Skills Gap Analysis	Tells you which skills you're missing and what to learn
#### 📄 Resume Preview	Dynamic resume tailored to your selected career path
#### 🔗 LinkedIn Strategy Generator	Smart headline, summary, and content ideas to grow your professional brand

### 🛠 Tech Stack
Python 3.10+

Streamlit — frontend for fast prototyping 

OpenAI GPT (via API) — core LLM brain

Modular Architecture — separate agents for better readability and scaling

Custom Skill-Match Logic — for domain-aware recommendation

### 📂 Folder Structure
bash
Copy
Edit
career-guidance-agent/
│
├── app.py                          # Main Streamlit app
├── agents/
│   └── user_interaction.py         # Core agent that handles profile analysis
├── utils/
│   └── resume_generator.py         # Optional utility (future scope)
├── .env                            # Store your OpenAI API key here
├── requirements.txt                # Dependencies
└── README.md                       # You are here
⚙️ Getting Started
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/career-guidance-agent.git
cd career-guidance-agent
2. Set Up Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Add OpenAI API Key
Create a .env file and add your OpenAI API key:

bash
Copy
Edit
## OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
Or set it as an environment variable:

bash
Copy
Edit
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
#### 4. Run the App
bash
Copy
Edit
streamlit run app.py
### 🖼️ App UI Highlights
Modern layout using containers and markdown

Icons and visual cues for better user experience

Clean sectioning with horizontal rules for resume readability

#### 🌱 Future Enhancements
 Convert Resume to downloadable PDF

 Add Sidebar Navigation

 Use Pinecone / Vector DB for job-role retrieval

 Auto-infer skills from education and experience

 Integration with LinkedIn APIs or Notion

 Multi-language support

### 👨‍💻 Author
Satyam Tiwari
🎓 B.Tech AI & Data Science @ VIPS, Delhi
💼 Machine Learning Engineer @ Vaishnav Technologies


#### 🙌 Acknowledgements
Inspired by the vision of accessible AI career mentorship for all.
Powered by OpenAI. Built with ❤️ using Streamlit.


