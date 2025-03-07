import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobMatcher:
    def __init__(self, jobs_df):
        self.jobs_df = jobs_df
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def create_job_vectors(self):
        # Combine relevant fields for matching
        job_texts = self.jobs_df.apply(
            lambda x: f"{x['title']} {x['description']} {x['requirements']}", 
            axis=1
        )
        return self.vectorizer.fit_transform(job_texts)
    
    def match_jobs(self, query, top_n=5):
        # Transform query and calculate similarity
        job_vectors = self.create_job_vectors()
        query_vector = self.vectorizer.transform([query])
        
        similarities = cosine_similarity(query_vector, job_vectors).flatten()
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        matched_jobs = self.jobs_df.iloc[top_indices].copy()
        matched_jobs['match_score'] = similarities[top_indices]
        
        return matched_jobs
