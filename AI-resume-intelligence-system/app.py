from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename

# ------------------ CONFIG ------------------
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"pdf", "docx"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ------------------ IMPORT UTILS ------------------
from utils.extractor import extract_resume_text
from utils.analyzer import calculate_score
from utils.matcher import match_resume_with_job
from utils.career import generate_career_suggestions

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ------------------ HELPERS ------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def save_uploaded_file(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)
    return file_path, filename


# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/builder")
def builder():
    return render_template("builder.html")


# ------------------ RESUME BUILDER ------------------

@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    data = request.form

    file_path = "generated_resume.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    linkedin = data.get("linkedin", "").strip()
    summary = data.get("summary", "").strip()
    skills = data.get("skills", "").strip()
    projects = data.get("projects", "").strip()
    education = data.get("education", "").strip()
    experience = data.get("experience", "").strip()

    content.append(Paragraph(f"<b>{name}</b>", styles["Title"]))
    content.append(Spacer(1, 10))

    contact_parts = [part for part in [email, phone, linkedin] if part]
    contact = " | ".join(contact_parts) if contact_parts else "No contact details provided"
    content.append(Paragraph(contact, styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    content.append(Paragraph(summary or "Not provided", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Skills</b>", styles["Heading2"]))
    content.append(Paragraph(skills or "Not provided", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Projects</b>", styles["Heading2"]))
    content.append(Paragraph(projects or "Not provided", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Education</b>", styles["Heading2"]))
    content.append(Paragraph(education or "Not provided", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Experience</b>", styles["Heading2"]))
    content.append(Paragraph(experience or "Not provided", styles["Normal"]))

    doc.build(content)
    return send_file(file_path, as_attachment=True)


# ------------------ RESUME ANALYZER ------------------

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("resume")
        category = request.form.get("category")
        target_role = request.form.get("target_role")

        if not file or file.filename == "":
            return render_template("upload.html", error="Please upload a resume file.")

        if not allowed_file(file.filename):
            return render_template("upload.html", error="Only PDF and DOCX files are allowed.")

        if not category:
            return render_template("upload.html", error="Please select category.")

        if not target_role or target_role == "Select Career Path":
            return render_template("upload.html", error="Please select career path.")

        file_path, filename = save_uploaded_file(file)

        text = extract_resume_text(file_path, filename)
        if not text.strip():
            return render_template("upload.html", error="Could not extract text from the file.")

        result = calculate_score(text, category, target_role)

        return render_template(
            "analysis.html",
            score=result["score"],
            rating_label=result["rating_label"],
            sections=result["sections"],
            found_skills=result["found_skills"],
            missing_skills=result["missing_skills"],
            feedback=result["feedback"],
            word_count=result["word_count"],
            category=category,
            target_role=target_role
        )

    return render_template("upload.html")


# ------------------ JOB MATCH ------------------

@app.route("/job-match", methods=["GET", "POST"])
def job_match():
    if request.method == "POST":
        file = request.files.get("resume")
        category = request.form.get("category")
        target_role = request.form.get("target_role")
        job_description = request.form.get("job_description", "").strip()

        if not file or file.filename == "":
            return render_template("job_match.html", error="Please upload a resume file.")

        if not allowed_file(file.filename):
            return render_template("job_match.html", error="Only PDF and DOCX files are allowed.")

        if not category:
            return render_template("job_match.html", error="Please select category.")

        if not target_role or target_role == "Select Career Path":
            return render_template("job_match.html", error="Please select career path.")

        if not job_description:
            return render_template("job_match.html", error="Please paste a job description.")

        file_path, filename = save_uploaded_file(file)

        text = extract_resume_text(file_path, filename)
        if not text.strip():
            return render_template("job_match.html", error="Could not extract text from the file.")

        result = match_resume_with_job(text, job_description, category, target_role)

        return render_template(
            "job_match.html",
            match_score=result.get("match_score", 0),
            matched_keywords=result.get("matched_keywords", []),
            missing_keywords=result.get("missing_keywords", []),
            suggestions=result.get("suggestions", []),
            recommended_roles=result.get("recommended_roles", []),
            category=category,
            target_role=target_role,
            job_description=job_description
        )

    return render_template("job_match.html")


# ------------------ CAREER ------------------

@app.route("/career", methods=["GET", "POST"])
def career():
    if request.method == "POST":
        file = request.files.get("resume")

        if not file or file.filename == "":
            return render_template("career.html", error="Please upload a resume file.")

        if not allowed_file(file.filename):
            return render_template("career.html", error="Only PDF and DOCX files are allowed.")

        file_path, filename = save_uploaded_file(file)

        text = extract_resume_text(file_path, filename)
        if not text.strip():
            return render_template("career.html", error="Could not extract text from the file.")

        result = generate_career_suggestions(text)

        return render_template(
            "career.html",
            career_paths=result["career_paths"],
            skills=result["skills_to_learn"],
            projects=result["project_suggestions"]
        )

    return render_template("career.html")


# ------------------ REPORT ------------------

@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/download-report")
def download_report():
    file_path = "report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("AI Resume Intelligence Report", styles["Title"]),
        Spacer(1, 15),
        Paragraph("Resume analyzed successfully.", styles["Normal"]),
        Spacer(1, 10),
        Paragraph(
            "Suggestions: Improve projects, add keywords, and tailor your resume for the target role.",
            styles["Normal"]
        )
    ]

    doc.build(content)
    return send_file(file_path, as_attachment=True)


# ------------------ FREE AI ASSISTANT ------------------

@app.route("/ai-assistant", methods=["POST"])
def ai_assistant():
    data = request.json or {}
    msg = data.get("message", "").strip()
    mode = data.get("mode", "chat")

    if not msg:
        return jsonify({"reply": "Please type a message."})

    text = msg.lower()

    # Resume generation mode
    if mode == "resume":
        if "python developer" in text:
            reply = (
                "Motivated Python Developer with strong knowledge of Python, SQL, APIs, "
                "and problem solving. Passionate about building efficient applications "
                "and learning modern software development practices."
            )
        elif "data analyst" in text:
            reply = (
                "Detail-oriented Data Analyst with skills in Excel, SQL, Python, and data visualization. "
                "Interested in turning raw data into useful business insights."
            )
        elif "web developer" in text:
            reply = (
                "Creative Web Developer with knowledge of HTML, CSS, JavaScript, and responsive design. "
                "Focused on building clean and user-friendly web applications."
            )
        elif "software developer" in text:
            reply = (
                "Enthusiastic Software Developer with a strong foundation in programming, problem solving, "
                "and application development. Eager to contribute to real-world software solutions and "
                "continuously improve technical skills."
            )
        else:
            reply = (
                "Motivated fresher with strong learning ability, problem-solving skills, and interest in "
                "building a successful career in the technology field."
            )

    # Rewrite mode
    elif mode == "rewrite":
        if "i know python" in text:
            reply = "Proficient in Python with hands-on experience in programming and problem solving."
        elif "i did project" in text:
            reply = "Developed academic projects that demonstrate practical skills and technical understanding."
        elif "i am interested in software" in text:
            reply = "Strong interest in software development with a focus on learning and building practical applications."
        else:
            reply = f"Professional version: {msg[0].upper() + msg[1:] if len(msg) > 1 else msg.upper()}."

    # Normal chat mode
    else:
        if "resume" in text and "summary" in text:
            reply = "A good resume summary should be short, professional, and focused on your skills, strengths, and career goal."
        elif "skills" in text:
            reply = "For IT roles, add skills like Python, SQL, HTML, CSS, JavaScript, Git, problem solving, and communication."
        elif "project" in text:
            reply = "Good student projects include AI Resume Analyzer, Job Match System, Portfolio Website, Student Management System, and Plant Monitoring System."
        elif "job" in text:
            reply = "Popular beginner IT roles are Software Developer, Web Developer, Data Analyst, AI/ML Engineer, and Cybersecurity Analyst."
        elif "career" in text:
            reply = "Choose a career path based on your strengths. For coding interest, go with Software or Web Development. For data interest, choose Data Analyst."
        elif "python developer" in text:
            reply = "For a Python Developer role, focus on Python, SQL, APIs, Flask or Django, problem solving, and strong projects."
        elif "improve resume" in text or "how to improve resume" in text:
            reply = "Improve your resume by adding role-based skills, stronger project descriptions, action verbs, and measurable achievements."
        else:
            reply = "I can help with resume writing, rewriting, skills, projects, job roles, and career suggestions."

    return jsonify({"reply": reply})


# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True)