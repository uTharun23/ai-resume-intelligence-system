# ✦ AI Resume Intelligence System ✦

An advanced, premium-styled AI-powered resume intelligence portal designed for job seekers, students, and freshers. This portal bridges career skill gaps, analyzes alignment with specific job description requirements, and compiles professional resumes with real-time visual styling themes.

[![Live Demo](https://img.shields.io/badge/Live-Demo%20on%20Vercel-teal?style=for-the-badge&logo=vercel&logoColor=white)](https://ai-resume-intelligence-system-alpha.vercel.app/)
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
<img width="1889" height="979" alt="image" src="https://github.com/user-attachments/assets/e72857f2-b289-4fd3-9084-28be8ba76692" />

### Premium Resume Builder (Dual-Pane)
<img width="1900" height="961" alt="image" src="https://github.com/user-attachments/assets/bd73421c-308f-46f0-b64d-36415ae83a35" />


### Upload & Audit Module
<img width="1903" height="960" alt="image" src="https://github.com/user-attachments/assets/bd921dcd-da99-4e51-a844-66ea9fef1505" />


### Resume Analytics Report (Dynamic Score Circle)
<img width="900" alt="Report Scoring" src="https://github.com/user-attachments/assets/bc373be4-107e-4f27-ae4d-538ae0ffb63e" />

### Job Description Alignment Engine
<img width="1861" height="969" alt="image" src="https://github.com/user-attachments/assets/336038fa-08c7-401c-8a19-a29109ea1f4b" />

### AI Career Copilot Chat Interface
<img width="1887" height="954" alt="image" src="https://github.com/user-attachments/assets/36aabc81-b795-4c6a-98cc-05580ed8699e" />

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
