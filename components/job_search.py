import streamlit as st
from utils.job_matcher import JobMatcher
from utils.job_boards import get_external_jobs
import pandas as pd

def render_job_search(jobs_df):
    st.header("Job Search")

    # Search and filter options
    col1, col2, col3 = st.columns(3)

    with col1:
        search_query = st.text_input("Search Jobs", "")
    with col2:
        location_filter = st.selectbox(
            "Location",
            ["All"] + list(jobs_df['location'].unique())
        )
    with col3:
        include_external = st.checkbox("Include External Jobs", value=True)

    # Apply filters to internal jobs
    filtered_df = jobs_df.copy()
    if location_filter != "All":
        filtered_df = filtered_df[filtered_df['location'] == location_filter]

    if search_query:
        matcher = JobMatcher(filtered_df)
        filtered_df = matcher.match_jobs(search_query)

    # Get external jobs if enabled
    if include_external and (search_query or location_filter != "All"):
        external_jobs = get_external_jobs(
            query=search_query,
            location=location_filter if location_filter != "All" else ""
        )
        if not external_jobs.empty:
            filtered_df = pd.concat([filtered_df, external_jobs], ignore_index=True)

    # Display job listings
    st.subheader("Job Listings")
    for _, job in filtered_df.iterrows():
        with st.expander(f"{job['title']} at {job['company']} {'(External)' if job.get('source') == 'Adzuna' else ''}"):
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Salary Range:** {job['salary_range']}")
            st.write(f"**Posted Date:** {job['posted_date']}")
            st.write("**Description:**")
            st.write(job['description'])
            st.write("**Requirements:**")
            st.write(job['requirements'])

            # Only show match score for internal jobs that have been matched
            if 'match_score' in job and pd.notna(job['match_score']):
                match_score = float(job['match_score'])
                # Ensure the score is between 0 and 1
                match_score = max(0.0, min(1.0, match_score))
                st.progress(match_score)
                st.write(f"Match Score: {match_score:.2f}")

            if job.get('source') != 'Adzuna':
                if st.button("Apply", key=f"apply_{_}"):
                    st.success("Application submitted successfully!")
            else:
                if st.button("View on Adzuna", key=f"view_{_}"):
                    st.markdown(f"[Open Job Listing](https://www.adzuna.com/details/{job['id']})")