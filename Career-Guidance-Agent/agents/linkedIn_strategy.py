import sys
from pathlib import Path
from openai import OpenAI  # ✅ Use this instead of just `import openai`

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

class LinkedInStrategyAgent:
    def __init__(self, openai_api_key=None):
        self.api_key = openai_api_key or "YOUR_OPENAI_API_KEY"
        self.client = OpenAI(api_key=self.api_key)  # ✅ v1.0.0+ Client

    def call_gpt(self, prompt):
        try:
            response = self.client.chat.completions.create(  # ✅ New method
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful LinkedIn strategist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_headline(self, target_role, user_strengths):
        prompt = (
            f"Create a professional LinkedIn headline for someone targeting the role of {target_role}. "
            f"User strengths: {', '.join(user_strengths)}. "
            "Make it catchy and optimized for recruiters."
        )
        return self.call_gpt(prompt)

    def generate_summary(self, target_role, user_strengths):
        prompt = (
            f"Write a LinkedIn summary for a candidate aiming to become a {target_role}. "
            f"Include these strengths: {', '.join(user_strengths)}. "
            "Make it engaging and professional."
        )
        return self.call_gpt(prompt)

    def generate_content_ideas(self, target_role, user_strengths):
        prompt = (
            f"Suggest 5 LinkedIn post ideas for a professional targeting {target_role} with strengths in "
            f"{', '.join(user_strengths)}. The ideas should help build personal brand and attract recruiters."
        )
        response = self.call_gpt(prompt)
        return [idea.strip("- ").strip() for idea in response.split('\n') if idea.strip()]
