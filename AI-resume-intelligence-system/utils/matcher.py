import re
from utils.role_data import ROLE_CATEGORIES


def clean_words(text):
    words = re.findall(r"[a-zA-Z0-9+/.-]+", text.lower())
    return {word for word in words if len(word) > 2}


def suggest_roles(category, score):
    if category == "IT":
        if score >= 8:
            return ["Software Developer", "Web Developer"]
        elif score >= 6:
            return ["Data Analyst", "Cybersecurity Analyst"]
        else:
            return ["Web Developer", "Software Developer"]

    if category == "Non-IT":
        if score >= 8:
            return ["Design Engineer", "Business Analyst"]
        elif score >= 6:
            return ["Operations Executive", "Core Engineer"]
        else:
            return ["Operations Executive", "Site / Project Engineer"]

    return []


def match_resume_with_job(resume_text, job_description, category=None, target_role=None):
    resume_words = clean_words(resume_text)
    jd_words = clean_words(job_description)

    if not jd_words:
        return {
            "match_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "suggestions": ["Please paste a valid job description."],
            "recommended_roles": []
        }

    matched_keywords = sorted(list(resume_words.intersection(jd_words)))
    missing_keywords = sorted(list(jd_words - resume_words))

    # 7 marks from resume vs job description keyword match
    keyword_score = (len(matched_keywords) / len(jd_words)) * 7

    # 3 marks from selected career path skill alignment
    role_bonus = 0
    role_skills = ROLE_CATEGORIES.get(category, {}).get(target_role, [])
    if role_skills:
        matched_role_skills = [
            skill for skill in role_skills
            if skill.lower() in resume_text.lower()
        ]
        role_bonus = (len(matched_role_skills) / len(role_skills)) * 3

    final_score = round(min(keyword_score + role_bonus, 10), 1)

    suggestions = []

    if final_score >= 8:
        suggestions.append("Strong job match. Your resume aligns well with this role.")
    elif final_score >= 6:
        suggestions.append("Good match. Improve a few missing skills and keywords.")
    else:
        suggestions.append("Low match. Tailor your resume more closely to the job description.")

    if missing_keywords:
        suggestions.append("Add missing keywords: " + ", ".join(missing_keywords[:8]))

    recommended_roles = suggest_roles(category, final_score)

    return {
        "match_score": final_score,
        "matched_keywords": matched_keywords[:12],
        "missing_keywords": missing_keywords[:12],
        "suggestions": suggestions,
        "recommended_roles": recommended_roles
    }