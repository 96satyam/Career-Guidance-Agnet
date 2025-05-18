import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class ResumeFileGenerator:
    def generate_pdf(self, resume_data, file_path=None):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        y = height - 50
        margin = 50
        line_height = 15

        def draw_text_block(title, lines):
            nonlocal y
            if y < 100:
                c.showPage()
                y = height - margin
            c.setFont("Helvetica-Bold", 16)
            c.drawString(margin, y, title)
            y -= 20
            c.setFont("Helvetica", 12)
            for line in lines:
                if y < 50:
                    c.showPage()
                    y = height - margin
                c.drawString(margin, y, line)
                y -= line_height
            y -= 10

        # Name
        c.setFont("Helvetica-Bold", 24)
        c.drawString(margin, y, resume_data.get("name", "Name"))
        y -= 40

        # Contact Info
        c.setFont("Helvetica", 12)
        contact = f"Email: {resume_data.get('email', '')} | Phone: {resume_data.get('phone', '')}"
        c.drawString(margin, y, contact)
        y -= 40

        # Summary
        summary_lines = self._wrap_text(resume_data.get("summary", ""), 90)
        draw_text_block("Professional Summary", summary_lines)

        # Skills
        skills = resume_data.get("skills", [])
        draw_text_block("Skills", [", ".join(skills)])

        # Education
        edu_entries = resume_data.get("education", [])
        edu_lines = [
            f"{e.get('degree', '')} at {e.get('institution', '')} ({e.get('year', '')})"
            for e in edu_entries
        ]
        draw_text_block("Education", edu_lines)

        # Experience
        exp_entries = resume_data.get("experience", [])
        exp_lines = [
            f"{e.get('title', '')} at {e.get('company', '')} ({e.get('duration', '')})"
            for e in exp_entries
        ]
        draw_text_block("Experience", exp_lines)

        c.save()
        buffer.seek(0)

        # Save to disk if file_path is specified
        if file_path:
            with open(file_path, "wb") as f:
                f.write(buffer.getvalue())
            return file_path

        return buffer  # ✅ Return BytesIO for Streamlit

    def _wrap_text(self, text, max_chars):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines
