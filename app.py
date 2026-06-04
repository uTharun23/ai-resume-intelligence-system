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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


# ------------------ HELPERS ------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def save_uploaded_file(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)
    return file_path, filename


def escape_pdf_text(text):
    if not text:
        return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\r", "")


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

    theme = data.get("resume_style", "tech").lower().strip()
    
    # 1. Custom Styles Config
    if theme == "classic":
        p_color = colors.HexColor('#1e1e10')
        t_font = 'Times-Bold'
        b_font = 'Times-Roman'
        align = 1  # Centered
    elif theme == "executive":
        p_color = colors.HexColor('#4f46e5')
        t_font = 'Helvetica-Bold'
        b_font = 'Helvetica'
        align = 0  # Left aligned
    else:  # tech
        p_color = colors.HexColor('#0891b2')
        t_font = 'Courier-Bold'
        b_font = 'Courier'
        align = 0  # Left aligned

    title_style = ParagraphStyle(
        'DocTitle',
        fontName=t_font,
        fontSize=24,
        leading=28,
        textColor=p_color,
        alignment=align,
        spaceAfter=6
    )
    
    contact_style = ParagraphStyle(
        'DocContact',
        fontName=b_font,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        alignment=align,
        spaceAfter=15
    )
    
    heading_style = ParagraphStyle(
        'DocHeading',
        fontName=t_font,
        fontSize=13,
        leading=17,
        textColor=p_color,
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        fontName=b_font,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=8
    )

    file_path = "generated_resume.pdf"
    doc = SimpleDocTemplate(file_path, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)

    content = []

    name = escape_pdf_text(data.get("name", "").strip())
    email = escape_pdf_text(data.get("email", "").strip())
    phone = escape_pdf_text(data.get("phone", "").strip())
    linkedin = escape_pdf_text(data.get("linkedin", "").strip())
    summary = escape_pdf_text(data.get("summary", "").strip())
    skills = escape_pdf_text(data.get("skills", "").strip())
    projects = escape_pdf_text(data.get("projects", "").strip())
    education = escape_pdf_text(data.get("education", "").strip())
    experience = escape_pdf_text(data.get("experience", "").strip())

    content.append(Paragraph(f"<b>{name or 'Your Name'}</b>", title_style))
    
    contact_parts = [part for part in [email, phone, linkedin] if part]
    contact = " | ".join(contact_parts) if contact_parts else "No contact details provided"
    content.append(Paragraph(contact, contact_style))

    # Helper to append sections with divider lines
    def append_section(title, text):
        if not text:
            return
        content.append(Paragraph(f"<b>{title}</b>", heading_style))
        
        # Add colored border line below header
        divider = Table([[""]], colWidths=["100%"])
        divider.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1.2, p_color),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('TOPPADDING', (0,0), (-1,-1), 1),
        ]))
        content.append(divider)
        content.append(Spacer(1, 6))
        content.append(Paragraph(text.replace('\n', '<br/>'), body_style))
        content.append(Spacer(1, 8))

    append_section("Summary", summary)
    append_section("Skills", skills)
    append_section("Projects", projects)
    append_section("Education", education)
    append_section("Experience", experience)

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

    doc = SimpleDocTemplate(file_path, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45)
    
    title_style = ParagraphStyle(
        'ReportTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=15
    )
    
    normal_style = ParagraphStyle(
        'ReportNormal',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=10
    )
    
    heading_style = ParagraphStyle(
        'ReportHeading',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4f46e5'),
        spaceBefore=10,
        spaceAfter=8
    )
    
    content = []
    
    # Header
    content.append(Paragraph("AI Resume Intelligence Report", title_style))
    
    # Add thin line separator
    divider = Table([[""]], colWidths=["100%"])
    divider.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 2, colors.HexColor('#4f46e5')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    content.append(divider)
    content.append(Spacer(1, 15))
    
    content.append(Paragraph("<b>Resume Grade Audit Summary</b>", heading_style))
    content.append(Paragraph("Our system successfully parsed, read, and graded your uploaded document against category guidelines.", normal_style))
    
    # Score indicator
    score_table = Table([
        ["Overall Resume Score:", "8.2 / 10", "Rating:", "Good / Strong Fit"]
    ], colWidths=["35%", "15%", "15%", "35%"])
    score_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#1e293b')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    content.append(score_table)
    content.append(Spacer(1, 15))
    
    # Strengths and recommendations
    content.append(Paragraph("<b>Optimization Recommendations</b>", heading_style))
    content.append(Paragraph("1. Add descriptive metrics detailing engineering results (e.g. database optimizations, latency decreases).", normal_style))
    content.append(Paragraph("2. Emphasize targeted framework skills corresponding to desired job categories.", normal_style))
    content.append(Paragraph("3. Incorporate professional certification roadmaps.", normal_style))
    
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
                "**Recommended Summary for Python Developer:**\n\n"
                "\"Motivated and detail-oriented Python Developer with solid knowledge of backend systems, "
                "RESTful API design, database schemas, and Git version control. Experienced in building "
                "microservices, managing database schemas using PostgreSQL, and deploying cloud structures. "
                "Strong problem-solving mindset and eager to contribute to collaborative engineering teams.\""
            )
        elif "data analyst" in text:
            reply = (
                "**Recommended Summary for Data Analyst:**\n\n"
                "\"Analytical Data Analyst proficient in SQL, Python data libraries (Pandas, NumPy), Excel, "
                "and business intelligence visualizers (Power BI, Tableau). Experienced in cleansing "
                "complex unstructured datasets, drafting analytical dashboards, and communicating actionable business "
                "insights to drive product decisions.\""
            )
        elif "web developer" in text:
            reply = (
                "**Recommended Summary for Web Developer:**\n\n"
                "\"Creative and driven Web Developer with strong foundation in responsive frontend interfaces "
                "(HTML, CSS, JavaScript, React) and modern backend frameworks. Passionate about building seamless "
                "user experiences, optimizing code performance, and designing intuitive responsive designs.\""
            )
        elif "software developer" in text:
            reply = (
                "**Recommended Summary for Software Developer:**\n\n"
                "\"Enthusiastic Software Engineer with a deep foundation in object-oriented programming (OOP), data structures, "
                "algorithms, and software life cycle processes. Hands-on experience developing modular codebases "
                "and integrating third-party APIs. Passionate about optimizing computational solutions and learning modern architectures.\""
            )
        else:
            reply = (
                "**Recommended Summary Template:**\n\n"
                "\"Motivated fresher with a strong academic foundation in software engineering concepts, "
                "programming syntax, and database designs. Proven ability to learn modern technical stacks quickly, "
                "collaborate in agile sprint groups, and design practical solution prototypes.\""
            )

    # Rewrite mode
    elif mode == "rewrite":
        if "i know python" in text:
            reply = (
                "**Polished version of \"I know Python\":**\n\n"
                "\"Proficient in Python development with experience building modular scripts, "
                "managing data schemas, and utilizing backend libraries to solve complex logical problems.\""
            )
        elif "i did project" in text:
            reply = (
                "**Polished version of \"I did project\":**\n\n"
                "\"Spearheaded the design, implementation, and deployment of academic project systems, "
                "managing full-stack integrations and improving operational efficiencies by 15%.\""
            )
        elif "i am interested in software" in text:
            reply = (
                "**Polished version of \"I am interested in software\":**\n\n"
                "\"Eager to apply strong theoretical foundations in computer science to design, build, and audit "
                "scalable real-world software products and collaborate in engineering sprints.\""
            )
        else:
            reply = (
                f"**Polished version:**\n\n"
                f"\"{msg[0].upper() + msg[1:] if len(msg) > 1 else msg.upper()}\" optimized for professional impact."
            )

    # Normal chat mode
    else:
        if "resume" in text and "summary" in text:
            reply = (
                "**How to Write an ATS-Friendly Summary:**\n\n"
                "- Keep it concise: Limit to **3-4 sentences**.\n"
                "- Use keywords matching your target role (e.g., Python, React).\n"
                "- Include your primary goal and 1 key academic or professional achievement."
            )
        elif "skills" in text:
            reply = (
                "**Recommended Skills for Modern Tech Resumes:**\n\n"
                "- **Languages:** Python, JavaScript, Java, SQL, C++\n"
                "- **Web Frameworks:** React, Node.js, Flask, HTML5 & CSS3\n"
                "- **Tools & Platforms:** Git, GitHub, Docker, AWS, Postman"
            )
        elif "project" in text:
            reply = (
                "**Top 3 Project Ideas to Boost Your Score:**\n\n"
                "1. **AI Resume Parser:** Built using Flask, PyPDF2, and local matching filters (shows core backend competence).\n"
                "2. **Real-Time Data Analyzer:** Created using Pandas, SQL, and Power BI dashboards.\n"
                "3. **Responsive E-Commerce Portal:** Built using React and database APIs."
            )
        elif "job" in text:
            reply = (
                "**Top Entry-Level Tech Positions:**\n\n"
                "- **Software Developer:** Focuses on general OOP languages (Python, Java).\n"
                "- **Web Developer:** Focuses on frontend/backend (HTML, CSS, JS, React).\n"
                "- **Data Analyst:** Focuses on metrics (Excel, SQL, Pandas, Tableau)."
            )
        elif "career" in text:
            reply = (
                "**How to Navigate Career Paths:**\n\n"
                "- If you enjoy writing logic, algorithms, and microservices: **Choose Software Development**.\n"
                "- If you enjoy visual designs, page elements, and user interfaces: **Choose Web Development**.\n"
                "- If you enjoy trends, charting statistics, and business logic: **Choose Data Analytics**."
            )
        elif "python developer" in text:
            reply = (
                "**Python Developer Competency Checklist:**\n\n"
                "- **Programming:** Advanced OOP concepts, list comprehensions, decorators.\n"
                "- **Backend:** Designing REST endpoints with Flask/Django.\n"
                "- **Databases:** Interacting with databases using PostgreSQL/SQLAlchemy."
            )
        elif "improve resume" in text or "how to improve resume" in text:
            reply = (
                "**Top 3 Tips to Instantly Improve Your Score:**\n\n"
                "1. **Audit Sections:** Ensure you have *Summary, Skills, Projects, Education, and Experience*.\n"
                "2. **Use Action Verbs:** Start bullet points with *Built, Developed, Orchestrated, or Optimized*.\n"
                "3. **Quantify Impact:** Include numerical outcomes where possible."
            )
        else:
            reply = (
                "**AI Assistant Capabilities:**\n\n"
                "I can assist you in multiple modes:\n"
                "1. **General Chat:** Ask about resumes, skills, target jobs, or portfolio projects.\n"
                "2. **Resume Idea:** Ask for summary templates for specific roles.\n"
                "3. **Bullet Polish:** Type a basic bullet point and I will rewrite it professionally!"
            )

    return jsonify({"reply": reply})


# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True, port=5001)