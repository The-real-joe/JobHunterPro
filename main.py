import streamlit as st
from data.mock_jobs import generate_mock_jobs, get_mock_applications
from components.dashboard import render_dashboard
from components.job_search import render_job_search
from components.analytics import render_analytics

# Page configuration
st.set_page_config(
    page_title="Job Search Aggregator",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if 'jobs_df' not in st.session_state:
    st.session_state.jobs_df = generate_mock_jobs()
if 'applications_df' not in st.session_state:
    st.session_state.applications_df = get_mock_applications()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Job Search", "Analytics"]
)

# Main content
st.title("Job Search Aggregator")

if page == "Dashboard":
    render_dashboard(st.session_state.applications_df, st.session_state.jobs_df)
elif page == "Job Search":
    render_job_search(st.session_state.jobs_df)
else:
    render_analytics(st.session_state.applications_df, st.session_state.jobs_df)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ by Your Job Search Assistant")
