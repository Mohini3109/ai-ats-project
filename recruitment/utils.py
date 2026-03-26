import os
import re
import PyPDF2
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# A simple mock database of skills to look for
SKILLS_DB = [
    'python', 'django', 'java', 'c++', 'javascript', 'react', 'sql',
    'aws', 'docker', 'kubernetes', 'html', 'css', 'machine learning',
    'data analysis', 'git', 'linux', 'agile', 'scrum', 'flask', 'nodejs'
]

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error parsing PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
    return text

def extract_resume_text(file_path):
    """
    Extracts raw text from a resume file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif ext in ['.doc', '.docx']:
        text = extract_text_from_docx(file_path)
        
    return text

def extract_skills_from_text(text):
    """
    Matches text against a known list of skills.
    Returns a comma-separated string of found skills.
    """
    if not text:
        return ""
        
    text = text.lower()
    found_skills = []
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            if skill in ['html', 'css', 'sql', 'aws']:
                found_skills.append(skill.upper())
            else:
                found_skills.append(skill.title())
                
    return ", ".join(found_skills)

def calculate_tfidf_match_score(resume_text, job_document):
    """
    Calculates the AI match percentage using TF-IDF and Cosine Similarity.
    Returns a score from 0.0 to 100.0.
    """
    if not resume_text or not job_document:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        # We fit the vectorizer on the combined vocabulary of both documents
        vectors = vectorizer.fit_transform([resume_text, job_document])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        score = similarity * 100
        return round(score, 2)
    except ValueError:
        return 0.0

