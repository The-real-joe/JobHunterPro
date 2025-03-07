import streamlit as st
import pandas as pd

def render_application_history(applications_df, jobs_df):
    st.header("Applications History")
    
    if applications_df.empty:
        st.info("No applications history yet. Start applying to jobs to track your progress!")
        return
    
    # Filters
    st.subheader("Filters")
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            options=["All"] + list(applications_df['status'].unique()),
            default="All"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            options=["Latest First", "Oldest First"],
            index=0
        )
    
    # Apply filters
    filtered_df = applications_df.copy()
    if status_filter and "All" not in status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    
    # Sort applications
    filtered_df = filtered_df.sort_values(
        'application_date',
        ascending=(sort_by == "Oldest First")
    )
    
    # Display applications
    st.subheader("Applications")
    for _, application in filtered_df.iterrows():
        # Get job details
        job = jobs_df[jobs_df['id'] == application['job_id']].iloc[0]
        
        with st.expander(f"{job['title']} at {job['company']} - {application['application_date']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Job Details**")
                st.write(f"- Company: {job['company']}")
                st.write(f"- Location: {job['location']}")
                st.write(f"- Salary Range: {job['salary_range']}")
            
            with col2:
                st.write("**Application Status**")
                status_color = {
                    'Applied': 'blue',
                    'Interview Scheduled': 'orange',
                    'Offer Received': 'green',
                    'Rejected': 'red',
                    'Under Review': 'purple'
                }
                st.markdown(
                    f"<p style='color: {status_color.get(application['status'], 'gray')}'>"
                    f"Status: {application['status']}</p>",
                    unsafe_allow_html=True
                )
                st.write(f"Applied on: {application['application_date']}")
            
            st.write("**Notes**")
            st.write(application['notes'])
            
            # Update notes section
            new_notes = st.text_area(
                "Update Notes",
                value=application['notes'],
                key=f"notes_{application['id']}"
            )
            if st.button("Update Notes", key=f"update_{application['id']}"):
                st.success("Notes updated successfully!")
