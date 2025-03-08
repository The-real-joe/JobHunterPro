# filepath: c:\Users\jbouc\Downloads\JobHunterPro\JobHunterPro\data\db_utils.py
import sqlite3
import pandas as pd

def init_mock_data():
    # Connect to the database
    conn = sqlite3.connect('c:\\Users\\jbouc\\Downloads\\JobHunterPro\\JobHunterPro\\.venv\\scripts\\jobhunterpro.db')
    cursor = conn.cursor()

    # Insert mock data into the jobs table
    cursor.execute('''
    INSERT INTO jobs (title, company, location, salary_range, description, requirements, posted_date, status, source)
    VALUES
    ('Software Engineer', 'Tech Corp', 'San Francisco', '100000-120000', 'Develop software solutions', 'Python, SQL', '2025-03-01', 'External', 'Adzuna')
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_jobs_df():
    # Connect to the database
    conn = sqlite3.connect('c:\\Users\\jbouc\\Downloads\\JobHunterPro\\JobHunterPro\\.venv\\scripts\\jobhunterpro.db')

    # Query the jobs table and load the data into a DataFrame
    df = pd.read_sql_query('SELECT * FROM jobs', conn)

    # Close the connection
    conn.close()

    return df

def get_applications_df():
    # Connect to the database
    conn = sqlite3.connect('c:\\Users\\jbouc\\Downloads\\JobHunterPro\\JobHunterPro\\.venv\\scripts\\jobhunterpro.db')

    # Query the applications table and load the data into a DataFrame
    df = pd.read_sql_query('SELECT * FROM applications', conn)

    # Close the connection
    conn.close()

    return df