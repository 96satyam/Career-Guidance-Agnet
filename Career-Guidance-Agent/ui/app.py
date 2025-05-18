import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.user_interaction import UserInteractionAgent

def main():
    st.set_page_config(page_title="Career Guidance & Resume Builder", layout="centered")
    st.title("🚀 Career Guidance & Resume Builder")

    # Load environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("🔐 OPENAI_API_KEY not found. Please set it in your environment variables.")
        return

    user_agent = UserInteractionAgent(openai_api_key=openai_api_key)

    # Profile Form
    with st.container():
        st.header("👤 Enter Your Profile Details")

        name = st.text_input("Full Name", "Satyam Tiwari")
        email = st.text_input("Email", "satyam@example.com")
        phone = st.text_input("Phone Number", "+91 12345 67890")

        st.markdown("### 🎓 Education")
        education_input = st.text_area(
            "List each degree/certification on a new line",
            "B.Tech in AI and Data Science - VIPS - 2025\n12th CBSE - 94%"
        )
        education = [line.strip() for line in education_input.split("\n") if line.strip()]

        st.markdown("### 💼 Experience")
        experience_input = st.text_area(
            "List each role on a new line",
            "Internship at Vaishnav Technologies (6 months)\nBusiness Executive at Shri Ram Telecommunication (1 year)"
        )
        experience = [line.strip() for line in experience_input.split("\n") if line.strip()]

        st.markdown("### 🛠️ Skills")
        skills_input = st.text_input("Comma-separated", "Python, SQL, Machine Learning, Communication")
        skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]

        st.markdown("### 🎯 Interests")
        interests_input = st.text_input("Comma-separated", "Data Science, AI")
        interests = [interest.strip() for interest in interests_input.split(",") if interest.strip()]

    user_profile = {
        "name": name,
        "email": email,
        "phone": phone,
        "education": education,
        "experience": experience,
        "skills": skills,
        "interests": interests,
    }

    st.markdown("---")

    if st.button("🔎 Get Career Suggestions"):
        with st.spinner("Analyzing your profile and fetching suggestions..."):
            career_suggestions = user_agent.get_career_suggestions(skills_input)

        if not career_suggestions:
            st.warning("⚠️ No career suggestions found. Please review your skills.")
            return

        st.subheader("🧭 Top Career Suggestions")
        for idx, cs in enumerate(career_suggestions[:5], 1):
            st.markdown(f"{idx}. **{cs['job_role']}** — 🔗 Match: **{cs['match_percentage']}%**")

        selected_role = st.selectbox(
            "🎯 Select a role to see further insights:",
            [cs['job_role'] for cs in career_suggestions[:5]]
        )

        if selected_role:
            st.markdown("---")
            st.subheader(f"📊 Skills Gap Analysis — *{selected_role}*")
            skills_gap = user_agent.get_skills_gap(user_profile["skills"], selected_role)
            st.markdown("✅ **Matched Skills:** " + ", ".join(skills_gap["matched"]))
            st.markdown("❌ **Missing Skills:** " + ", ".join(skills_gap["missing"]))

            st.markdown("---")
            st.subheader("📄 Resume Preview")

            with st.container():
                st.markdown(f"### {user_profile['name']}")
                st.markdown(f"📧 {user_profile['email']} &nbsp;&nbsp;&nbsp;&nbsp; 📱 {user_profile['phone']}")
                st.markdown("#### 🧑‍💼 Professional Summary")
                st.markdown(f"Aspiring **{selected_role}** passionate about data-driven innovation and real-world impact.")
                
                st.markdown("#### 🛠️ Skills")
                st.markdown(", ".join(user_profile["skills"]))

                st.markdown("#### 🎓 Education")
                for edu in user_profile["education"]:
                    st.markdown(f"- {edu}")

                st.markdown("#### 💼 Experience")
                for exp in user_profile["experience"]:
                    st.markdown(f"- {exp}")

                st.markdown("#### 🎯 Interests")
                st.markdown(", ".join(user_profile["interests"]))

            st.markdown("---")
            st.subheader("🔗 LinkedIn Profile Strategy")
            linkedin_plan = user_agent.get_linkedin_strategy(selected_role, user_profile["skills"])

            st.markdown("**🧠 Headline:**")
            st.info(linkedin_plan["headline"])

            st.markdown("**📜 Summary:**")
            st.markdown(linkedin_plan["summary"])

            st.markdown("**💡 Content Ideas:**")
            for idea in linkedin_plan["content_ideas"]:
                st.markdown(f"- {idea}")

if __name__ == "__main__":
    main()
