# ✦ AI Resume Intelligence System ✦

<div align="center">

[![Live Demo](https://img.shields.io/badge/Live_Demo-Visit_Application-22d3ee?style=for-the-badge&logo=render&logoColor=030712)](https://ai-resume-intelligence-system.onrender.com/)
[![Python Version](https://img.shields.io/badge/Python-3.9+-6366f1?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Framework](https://img.shields.io/badge/Flask-2.0+-d946ef?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Styling](https://img.shields.io/badge/Theme-Glassmorphism_Dark-060913?style=flat-square&logo=css3&logoColor=22d3ee)](https://github.com/uTharun23/ai-resume-intelligence-system)

An advanced, premium-styled AI-powered resume intelligence portal. Built to help job seekers, students, and freshers bridge career skill gaps, analyze matching requirements for specific roles, and compile professional resumes with real-time visual themes.

[**🔗 Visit Live Demo Application**](https://ai-resume-intelligence-system.onrender.com/)

</div>

---

## 🚀 Core Capabilities

| Module | Description | Visual Element |
| :--- | :--- | :--- |
| **Document Builder** | Craft and download industry-standard PDFs instantly using **Modern Tech**, **Classic Ivory**, or **Executive Navy** styling parameters. | 📄 Real-time A4 Paper Canvas |
| **Audit Scanner** | Upload existing resumes to grade layout compliance, word count metrics, and formatting checks out of 10. | 📊 Circular Progress Gauge |
| **Job Description Match** | Compare your resume directly against specific job description text to isolate keyword density overlaps. | 🎯 Progress Match-Meter |
| **Career Roadmap** | Discover custom project ideas, developmental milestones, and certification paths based on profile parsing. | 🚀 Timeline Milestones |
| **AI Career Copilot** | Interactive local chatbot assistant supporting prompt shortcuts (pills) and structured bullet polishing. | 💬 Multi-Mode Floating Assistant |

---

## 🛠 Design & Tech Stack

- **Backend Logic:** Python 3.9+ & Flask Web Framework
- **PDF Construction:** ReportLab PDF Engine (Supports customized accent bands, dynamic fonts, and grids)
- **Frontend Layer:** Frosted Glassmorphism CSS3 (Translucent borders, radial glow coordinates, and responsive styling grids)
- **Parsing Utilities:** PyPDF2 & python-docx parser packages

---

## 📸 Application Previews

<div align="center">

### Home Portal View
<img width="900" alt="Home Screen" src="https://github.com/user-attachments/assets/07871aa4-54e6-484b-b3c4-68d11c427689" />

### Premium Resume Builder (Dual-Pane)
<img width="900" alt="Resume Builder" src="https://github.com/user-attachments/assets/422ea8af-876d-4c41-b87b-91833bb03e7a" />

### Upload & Audit Module
<img width="900" alt="Audit Scanner" src="https://github.com/user-attachments/assets/39bbf8be-752d-473f-869e-c3fe0cd34ea5" />

### Resume Analytics Report (Dynamic Score Circle)
<img width="900" alt="Report Scoring" src="https://github.com/user-attachments/assets/bc373be4-107e-4f27-ae4d-538ae0ffb63e" />

### Job Description Alignment Engine
<img width="900" alt="JD Matching" src="https://github.com/user-attachments/assets/a9f6df25-c332-4eb9-8c59-e9b0dfe716a0" />

### AI Career Copilot Chat Interface
<img width="900" alt="AI Copilot" src="https://github.com/user-attachments/assets/c6c19ac7-250f-44b2-a82a-d90c585361e6" />

</div>

---

## ▶️ Setup & Local Installation

### Prerequisites
Make sure you have Python 3.9 or higher installed on your computer.

### Step 1: Clone the Repository
```bash
git clone https://github.com/uTharun23/ai-resume-intelligence-system.git
cd ai-resume-intelligence-system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Development Server
```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000` to interact with the application.

---

## 🔒 Robustness Safeguards
This project has been engineered with zero-crash protections:
- **Corrupt File Protection:** Upload scanners catch parsing errors gracefully without triggering internal server 500 crashes.
- **XML Entity Sanitization:** Special symbols in user inputs are automatically escaped to prevent PDF compiler exceptions.
- **Typing Safety Checks:** Keyword processors enforce text availability to safeguard against null pointers.
