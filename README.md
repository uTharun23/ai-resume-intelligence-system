# AI Resume Intelligence System

An advanced, premium-styled AI-powered resume intelligence portal designed for job seekers, students, and freshers. This system identifies career skill gaps, calculates job description matching scores, and generates professional, tailored resume PDFs across 210 dynamic style combinations.

---

## 🔗 Live Application
* **Live Demo:** [https://ai-resume-intelligence-system.onrender.com](https://ai-resume-intelligence-system.onrender.com/)

---

## 🚀 Key Features

* **Dynamic Resume Customizer:** Generates **210 unique design layouts** in real time. Choose from 3 layout formats (including a LaTeX-style underline), 7 professional typography pairings, and 10 color accents.
* **Resume Quality Audit:** Scans uploaded resume documents (PDF & DOCX) to rate formatting, section structures, and word count metrics out of 10.
* **Job Description Compatibility Matcher:** Paste target job descriptions to analyze keyword overlaps, highlight missing terms, and calculate matching scores.
* **AI Career Companion:** A built-in floating career copilot chatbot with suggested-prompt chips to assist with summary drafting, bullet point polishing, and career roadmaps.
* **Themed PDF Exporting:** Compile and download resume documents and matching audit reports as cleanly styled PDFs.

---

## 🛠 Tech Stack

* **Core Language:** Python 3.9+
* **Backend Framework:** Flask
* **PDF Engine:** ReportLab
* **File Parsers:** PyPDF2 & python-docx
* **Styling Layer:** Frosted Glassmorphism CSS3 & Vanilla JavaScript

---

## 📸 Application Gallery

<div align="center">

### Modern Homepage & Dashboard
![Home Screen](https://github.com/user-attachments/assets/07871aa4-54e6-484b-b3c4-68d11c427689)

### Interactive Dual-Pane Resume Builder
![Resume Builder](https://github.com/user-attachments/assets/422ea8af-876d-4c41-b87b-91833bb03e7a)

### Upload & Audit Interface
![Audit Scanner](https://github.com/user-attachments/assets/39bbf8be-752d-473f-869e-c3fe0cd34ea5)

### Real-Time Resume Review Analytics
![Report Scoring](https://github.com/user-attachments/assets/bc373be4-107e-4f27-ae4d-538ae0ffb63e)

### Job Description Overlap Matcher
![JD Matching](https://github.com/user-attachments/assets/a9f6df25-c332-4eb9-8c59-e9b0dfe716a0)

### AI Career Copilot Chat Widget
![AI Copilot](https://github.com/user-attachments/assets/c6c19ac7-250f-44b2-a82a-d90c585361e6)

</div>

---

## 📦 Local Installation & Setup

Ensure you have Python 3.9 or higher installed locally.

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/uTharun23/ai-resume-intelligence-system.git
   cd ai-resume-intelligence-system
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server:**
   ```bash
   python app.py
   ```

4. **Access the Portal:**
   Navigate to `http://127.0.0.1:5001` in your browser.

---

## 🔒 Codebase Safeguards

* **File Extraction Guard:** Upload text parsing is wrapped in exception handlers to prevent server crashes on encrypted or corrupt files.
* **XML Entity Sanitization:** Special characters in user inputs are automatically escaped to prevent ReportLab paragraph compilation failures.
* **Typing Safety Checks:** Preprocessors enforce text presence checks to eliminate null-pointer exceptions in matching routines.
