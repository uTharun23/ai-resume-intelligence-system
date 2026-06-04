# ✦ AI Resume Intelligence System ✦

An advanced, premium-styled AI-powered resume intelligence portal designed for job seekers, students, and freshers. This portal bridges career skill gaps, analyzes alignment with specific job description requirements, and compiles professional resumes with real-time visual styling themes.

[![Live Demo](https://img.shields.io/badge/Live-Demo%20on%20Render-teal?style=for-the-badge&logo=render&logoColor=white)](https://ai-resume-intelligence-system.onrender.com/)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

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

## 🎨 Premium Styling Engine (210 Configurations)

The interactive dual-pane builder enables job seekers to generate **210 unique styling combinations** in real time by customizing layout structures, typography pairings, and accents:

1. **Layout Design System:**
   - **Classic Ivory:** Minimalist grid layout with traditional styling.
   - **Modern Tech:** Bold headers with modern geometric spacing.
   - **Executive Navy:** Professional top/bottom accent bands with LaTeX-style divider lines.

2. **Accents & Colors:** 10 curated HSL color schemes (Midnight Indigo, Emerald Teal, Ruby Rose, Slate Gray, etc.).
3. **Typography Pairings:** 7 famous font structures mapped dynamically into ReportLab PDF styling tables (Helvetica, Times-Roman, Courier, and standard serif/sans-serif alternatives).

---

## 🛠 Design & Tech Stack

- **Backend Logic:** Python 3.9+ & Flask Web Framework
- **PDF Construction:** ReportLab PDF Engine (Supports customized accent bands, dynamic fonts, and grids)
- **Frontend Layer:** Frosted Glassmorphism CSS3 (Translucent borders, radial glow coordinates, and responsive styling grids)
- **Parsing Utilities:** PyPDF2 & `python-docx` parser packages

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

Open your browser and navigate to `http://127.0.0.1:5001` (or `http://127.0.0.1:5000` if on default port) to interact with the application.

---

## 🔒 Robustness & Stability Safeguards

This portal has been engineered with zero-crash safeguards to ensure seamless operation:
- **Corrupt File Protection:** Upload scanners catch PDF/DOCX parsing errors gracefully without triggering internal server 500 crashes.
- **XML Entity Sanitization:** Special symbols in user inputs (like `&`, `<`, `>`) are automatically escaped to prevent ReportLab paragraph compiler exceptions.
- **Typing Safety Checks:** Keyword processors enforce text availability to safeguard against null-pointer errors during match calculations.
