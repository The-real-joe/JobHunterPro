import os
import requests
from datetime import datetime
import pandas as pd

class AdzunaAPI:
    def __init__(self):
        self.app_id = os.getenv('ADZUNA_APP_ID')
        self.api_key = os.getenv('ADZUNA_API_KEY')
        self.base_url = "https://api.adzuna.com/v1/api/jobs"
        
    def search_jobs(self, query="", location="", page=1, country="us"):
        """Search jobs using Adzuna API"""
        try:
            url = f"{self.base_url}/{country}/search/{page}"
            params = {
                "app_id": self.app_id,
                "app_key": self.api_key,
                "results_per_page": 10,
                "what": query if query else None,
                "where": location if location else None,
                "content-type": "application/json"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Transform Adzuna results to match our job format
            jobs_data = []
            for job in data.get('results', []):
                jobs_data.append({
                    "id": job.get('id'),
                    "title": job.get('title'),
                    "company": job.get('company', {}).get('display_name', 'Unknown'),
                    "location": job.get('location', {}).get('display_name', 'Unknown'),
                    "salary_range": f"{job.get('salary_min', 'N/A')}-{job.get('salary_max', 'N/A')}",
                    "description": job.get('description'),
                    "requirements": job.get('description'),  # Adzuna combines requirements in description
                    "posted_date": job.get('created'),
                    "status": "External",
                    "source": "Adzuna"
                })
            
            return pd.DataFrame(jobs_data) if jobs_data else pd.DataFrame()
            
        except Exception as e:
            print(f"Error fetching jobs from Adzuna: {str(e)}")
            return pd.DataFrame()

def get_external_jobs(query="", location=""):
    """Get jobs from all configured external job boards"""
    adzuna = AdzunaAPI()
    return adzuna.search_jobs(query, location)
