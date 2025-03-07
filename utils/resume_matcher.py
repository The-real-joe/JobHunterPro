import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import io
import re

class ResumeProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def extract_text_from_docx(self, docx_file):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(io.BytesIO(docx_file))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error processing DOCX: {str(e)}")

    def process_resume(self, file_content, file_type):
        """Process resume file and extract text"""
        if file_type == "application/pdf":
            return self.extract_text_from_pdf(file_content)
        elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/docx"]:
            return self.extract_text_from_docx(file_content)
        else:
            raise ValueError("Unsupported file type. Please upload PDF or DOCX files.")

    def extract_skills(self, text):
        """Extract skills from text using regex patterns"""
        # Common programming languages and technologies
        skill_patterns = [
            r'python|java|javascript|react|node\.js|sql|aws|docker|kubernetes|html|css',
            r'machine learning|artificial intelligence|data science|deep learning|nlp',
            r'agile|scrum|project management|team leadership',
            # Add more patterns as needed
        ]
        
        skills = set()
        for pattern in skill_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                skills.add(match.group())
        
        return list(skills)

    def calculate_match_score(self, resume_text, job_description, job_requirements):
        """Calculate match score between resume and job"""
        # Combine job description and requirements
        job_text = f"{job_description} {job_requirements}"
        
        # Extract skills
        resume_skills = set(self.extract_skills(resume_text))
        job_skills = set(self.extract_skills(job_text))
        
        # Calculate skill match ratio
        if job_skills:
            skill_match_ratio = len(resume_skills.intersection(job_skills)) / len(job_skills)
        else:
            skill_match_ratio = 0
            
        # Calculate text similarity using TF-IDF
        texts = [resume_text, job_text]
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Combine scores (giving more weight to skill matches)
        final_score = (skill_match_ratio * 0.7) + (similarity * 0.3)
        
        return {
            'score': final_score,
            'matched_skills': list(resume_skills.intersection(job_skills)),
            'missing_skills': list(job_skills - resume_skills)
        }
