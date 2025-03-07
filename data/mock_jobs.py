import pandas as pd
from datetime import datetime, timedelta

def generate_mock_jobs():
    jobs = {
        'title': [
            'Senior Python Developer',
            'Data Scientist',
            'Frontend Engineer',
            'DevOps Engineer',
            'Product Manager',
            'Full Stack Developer',
            'ML Engineer',
            'Software Architect',
            'QA Engineer',
            'Technical Lead'
        ],
        'company': [
            'TechCorp',
            'DataWise',
            'WebFront',
            'CloudOps',
            'ProductX',
            'FullStack Inc',
            'AI Solutions',
            'ArchSoft',
            'QualityTech',
            'LeadTech'
        ],
        'location': [
            'Remote',
            'New York, NY',
            'San Francisco, CA',
            'Austin, TX',
            'Boston, MA',
            'Seattle, WA',
            'Remote',
            'Chicago, IL',
            'Los Angeles, CA',
            'Denver, CO'
        ],
        'salary_range': [
            '120k-150k',
            '100k-130k',
            '90k-120k',
            '110k-140k',
            '130k-160k',
            '100k-130k',
            '120k-150k',
            '140k-170k',
            '80k-100k',
            '130k-160k'
        ],
        'description': [
            'Looking for an experienced Python developer...',
            'Seeking a data scientist with ML expertise...',
            'Frontend developer with React experience...',
            'DevOps engineer with cloud expertise...',
            'Product manager with tech background...',
            'Full stack developer with MERN experience...',
            'Machine learning engineer with PyTorch...',
            'Software architect with distributed systems...',
            'QA engineer with automation experience...',
            'Technical lead with team management...'
        ],
        'requirements': [
            'Python, Django, PostgreSQL',
            'Python, SQL, Machine Learning',
            'React, JavaScript, CSS',
            'AWS, Docker, Kubernetes',
            'Agile, Jira, Product Development',
            'React, Node.js, MongoDB',
            'Python, TensorFlow, PyTorch',
            'System Design, Cloud Architecture',
            'Selenium, Python, Test Automation',
            'Team Leadership, Architecture'
        ],
        'posted_date': [
            (datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d')
            for x in range(10)
        ],
        'status': ['Open'] * 10
    }
    
    return pd.DataFrame(jobs)

def get_mock_applications():
    applications = {
        'job_id': range(5),
        'application_date': [
            (datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d')
            for x in range(5)
        ],
        'status': [
            'Applied',
            'Interview Scheduled',
            'Rejected',
            'Under Review',
            'Offer Received'
        ],
        'notes': [
            'Application submitted via company website',
            'First round interview scheduled',
            'Position filled internally',
            'Waiting for feedback',
            'Negotiating offer'
        ]
    }
    
    return pd.DataFrame(applications)
