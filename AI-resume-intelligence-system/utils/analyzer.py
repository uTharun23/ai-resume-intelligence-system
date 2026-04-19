import re
from utils.role_data import ROLE_CATEGORIES


def detect_sections(resume_text):
    text = resume_text.lower()

    sections = {
        "Contact": bool(re.search(r"\b\d{10}\b", resume_text) or "@" in resume_text),
        "Education": "education" in text or "b.tech" in text or "degree" in text or "college" in text,
        "Skills": "skills" in text,
        "Projects": "project" in text or "projects" in text,
        "Experience": "experience" in text or "internship" in text or "training" in text,
        "Summary": "summary" in text or "objective" in text or "profile" in text,
    }

    return sections


def detect_missing_skills(resume_text, category, target_role):
    resume_text_lower = resume_text.lower()
    expected_skills = ROLE_CATEGORIES.get(category, {}).get(target_role, [])

    found_skills = []
    missing_skills = []

    for skill in expected_skills:
        if skill.lower() in resume_text_lower:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    return found_skills, missing_skills


def calculate_score(resume_text, category, target_role):
    score = 0
    feedback = []

    sections = detect_sections(resume_text)
    found_skills, missing_skills = detect_missing_skills(resume_text, category, target_role)

    section_count = sum(sections.values())
    section_score = round((section_count / 6) * 4, 1)
    score += section_score

    total_role_skills = len(ROLE_CATEGORIES.get(category, {}).get(target_role, []))
    if total_role_skills > 0:
        skill_score = round((len(found_skills) / total_role_skills) * 4, 1)
    else:
        skill_score = 0
    score += skill_score

    word_count = len(resume_text.split())
    content_score = 0

    if word_count >= 200:
        content_score += 1
    else:
        feedback.append("Your resume content looks too short. Add more meaningful details.")

    if any(word in resume_text.lower() for word in ["developed", "built", "designed", "implemented", "created"]):
        content_score += 1
    else:
        feedback.append("Use stronger action words like Developed, Built, Implemented, or Designed.")

    score += content_score
    score = round(min(score, 10), 1)

    missing_sections = [section for section, present in sections.items() if not present]

    if missing_sections:
        feedback.append("Add missing sections: " + ", ".join(missing_sections))

    if missing_skills:
        feedback.append("Missing important skills for " + target_role + ": " + ", ".join(missing_skills))

    if score >= 9:
        rating_label = "Excellent"
    elif score >= 7:
        rating_label = "Good"
    elif score >= 5:
        rating_label = "Average"
    else:
        rating_label = "Needs Improvement"

    return {
        "score": score,
        "rating_label": rating_label,
        "sections": sections,
        "found_skills": found_skills,
        "missing_skills": missing_skills,
        "feedback": feedback,
        "word_count": word_count
    }