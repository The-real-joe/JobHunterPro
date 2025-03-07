from models.database import Job, Application, get_db
from datetime import datetime
import pandas as pd

def init_mock_data():
    """Initialize the database with mock data if it's empty"""
    db = next(get_db())

    try:
        # Check if data already exists
        if db.query(Job).count() > 0:
            return

        # Add mock jobs
        mock_jobs = [
            {
                "title": "Senior Python Developer",
                "company": "TechCorp",
                "location": "Remote",
                "salary_range": "120k-150k",
                "description": "Looking for an experienced Python developer with strong backend skills and experience with web frameworks.",
                "requirements": "Python, Django, PostgreSQL",
                "posted_date": datetime.now(),
                "status": "Open"
            },
            {
                "title": "Data Scientist",
                "company": "DataWise",
                "location": "New York, NY",
                "salary_range": "100k-130k",
                "description": "Seeking a data scientist with ML expertise and experience in predictive modeling.",
                "requirements": "Python, SQL, Machine Learning",
                "posted_date": datetime.now(),
                "status": "Open"
            }
        ]

        created_jobs = []
        for job_data in mock_jobs:
            job = Job(**job_data)
            db.add(job)
            db.flush()  # Flush to get the job ID
            created_jobs.append(job)

        # Add mock applications
        mock_applications = [
            {
                "job_id": created_jobs[0].id,
                "status": "Applied",
                "notes": "Application submitted via company website",
                "application_date": datetime.now()
            },
            {
                "job_id": created_jobs[1].id,
                "status": "Interview Scheduled",
                "notes": "First round interview scheduled",
                "application_date": datetime.now()
            }
        ]

        for app_data in mock_applications:
            app = Application(**app_data)
            db.add(app)

        db.commit()
        print("Mock data initialized successfully")
    except Exception as e:
        print(f"Error initializing mock data: {str(e)}")
        db.rollback()
        raise

def get_jobs_df():
    """Get all jobs as a pandas DataFrame"""
    db = next(get_db())
    jobs = db.query(Job).all()

    jobs_data = []
    for job in jobs:
        jobs_data.append({
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "salary_range": job.salary_range,
            "description": job.description,
            "requirements": job.requirements,
            "posted_date": job.posted_date.strftime('%Y-%m-%d'),
            "status": job.status
        })

    return pd.DataFrame(jobs_data) if jobs_data else pd.DataFrame()

def get_applications_df():
    """Get all applications as a pandas DataFrame"""
    db = next(get_db())
    applications = db.query(Application).all()

    applications_data = []
    for app in applications:
        applications_data.append({
            "id": app.id,
            "job_id": app.job_id,
            "application_date": app.application_date.strftime('%Y-%m-%d'),
            "status": app.status,
            "notes": app.notes
        })

    return pd.DataFrame(applications_data) if applications_data else pd.DataFrame()