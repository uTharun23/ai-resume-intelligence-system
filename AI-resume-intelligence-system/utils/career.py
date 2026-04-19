def generate_career_suggestions(resume_text):
    text = resume_text.lower()

    suggestions = {
        "career_paths": [],
        "skills_to_learn": [],
        "project_suggestions": []
    }

    # IT detection
    if any(skill in text for skill in ["python", "java", "c++", "html", "css", "javascript"]):
        suggestions["career_paths"].append("Software Developer")

        if "python" in text:
            suggestions["career_paths"].append("Backend Developer")

        if "html" in text or "css" in text:
            suggestions["career_paths"].append("Web Developer")

        if "sql" in text or "excel" in text:
            suggestions["career_paths"].append("Data Analyst")

        suggestions["skills_to_learn"] += [
            "Data Structures",
            "Algorithms",
            "System Design"
        ]

        suggestions["project_suggestions"] += [
            "AI Resume Analyzer",
            "Portfolio Website",
            "Job Matching System"
        ]

    # Non-IT detection
    if any(skill in text for skill in ["autocad", "solidworks", "mechanical", "electrical", "civil"]):
        suggestions["career_paths"].append("Core Engineer")

        suggestions["skills_to_learn"] += [
            "CAD Tools",
            "Project Planning",
            "Technical Drawing"
        ]

        suggestions["project_suggestions"] += [
            "Design Model Project",
            "Automation System",
            "Energy Optimization System"
        ]

    # Default fallback
    if not suggestions["career_paths"]:
        suggestions["career_paths"] = ["Explore IT / Non-IT Careers"]
        suggestions["skills_to_learn"] = ["Communication", "Problem Solving"]
        suggestions["project_suggestions"] = ["Basic Portfolio Website"]

    return suggestions