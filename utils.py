import os
import re
import docx
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return "\n".join([p.text for p in doc.paragraphs])

def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()

def calculate_similarity(job_desc, resume_text):
    tfidf = TfidfVectorizer(stop_words='english')
    matrix = tfidf.fit_transform([job_desc, resume_text])
    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(score * 100, 2)

def extract_skills(text):
    skills_db = {
        'python', 'java', 'c++', 'javascript', 'html', 'css', 'react', 'angular', 'vue',
        'flask', 'django', 'sql', 'nosql', 'mongodb', 'aws', 'docker', 'kubernetes',
        'machine learning', 'deep learning', 'nlp', 'data analysis', 'pandas', 'numpy',
        'scikit-learn', 'tensorflow', 'pytorch', 'communication', 'leadership', 'problem solving'
    }
    
    found = set()
    content = text.lower()
    for skill in skills_db:
        if skill in content:
            found.add(skill)
            
    return list(found)

def extract_experience(text):
    matches = re.findall(r"(\d+(\.\d+)?)\+?\s*years?", text.lower())
    if matches:
        return max([float(m[0]) for m in matches])
    return 0

def classify_experience_level(years):
    if years < 2: return "Junior"
    if years < 5: return "Mid-Level"
    return "Senior"

def calculate_weighted_score(job_desc, resume_text, resume_skills, job_skills, exp_years):
    semantic_score = calculate_similarity(job_desc, resume_text)
    
    skill_score = 0
    if job_skills:
        matched = set(resume_skills).intersection(set(job_skills))
        skill_score = (len(matched) / len(job_skills)) * 100
    
    exp_score = min(exp_years * 5, 100)
    
    final_score = (0.4 * semantic_score) + (0.4 * skill_score) + (0.2 * exp_score)
    return round(final_score, 2)

def predict_job_fit(score):
    if score >= 80: return "High Probability"
    if score >= 50: return "Moderate Probability"
    return "Low Probability"
