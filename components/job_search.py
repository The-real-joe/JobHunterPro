import streamlit as st
from utils.job_matcher import JobMatcher

def render_job_search(jobs_df):
    st.header("Job Search")
    
    # Search and filter options
    col1, col2 = st.columns(2)
    
    with col1:
        search_query = st.text_input("Search Jobs", "")
    with col2:
        location_filter = st.selectbox(
            "Location",
            ["All"] + list(jobs_df['location'].unique())
        )
    
    # Apply filters
    filtered_df = jobs_df.copy()
    if location_filter != "All":
        filtered_df = filtered_df[filtered_df['location'] == location_filter]
    
    if search_query:
        matcher = JobMatcher(filtered_df)
        filtered_df = matcher.match_jobs(search_query)
    
    # Display job listings
    st.subheader("Job Listings")
    for _, job in filtered_df.iterrows():
        with st.expander(f"{job['title']} at {job['company']}"):
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Salary Range:** {job['salary_range']}")
            st.write(f"**Posted Date:** {job['posted_date']}")
            st.write("**Description:**")
            st.write(job['description'])
            st.write("**Requirements:**")
            st.write(job['requirements'])
            
            if 'match_score' in job:
                st.progress(float(job['match_score']))
                st.write(f"Match Score: {job['match_score']:.2f}")
            
            if st.button("Apply", key=f"apply_{_}"):
                st.success("Application submitted successfully!")
