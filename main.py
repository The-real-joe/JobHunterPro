import streamlit as st
from data.db_utils import init_mock_data, get_jobs_df, get_applications_df
from components.dashboard import render_dashboard
from components.job_search import render_job_search
from components.analytics import render_analytics
from components.application_history import render_application_history
from components.resume_matching import render_resume_matching

# Page configuration
st.set_page_config(
    page_title="Job Search Aggregator",
    page_icon="🎯",
    layout="wide"
)

# Initialize database with mock data
init_mock_data()

# Initialize session state
if 'jobs_df' not in st.session_state:
    st.session_state.jobs_df = get_jobs_df()
if 'applications_df' not in st.session_state:
    st.session_state.applications_df = get_applications_df()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Job Search", "Resume Matcher", "Applications History", "Analytics"]
)

# Main content
st.title("Job Search Aggregator")

if page == "Dashboard":
    render_dashboard(st.session_state.applications_df, st.session_state.jobs_df)
elif page == "Job Search":
    render_job_search(st.session_state.jobs_df)
elif page == "Resume Matcher":
    render_resume_matching(st.session_state.jobs_df)
elif page == "Applications History":
    render_application_history(st.session_state.applications_df, st.session_state.jobs_df)
else:
    render_analytics(st.session_state.applications_df, st.session_state.jobs_df)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ by Your Job Search Assistant")