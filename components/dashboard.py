import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_dashboard(applications_df, jobs_df):
    st.header("Application Dashboard")

    if applications_df.empty:
        st.info("No applications yet. Start your job search journey by applying to jobs!")
        return

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Applications", len(applications_df))
    with col2:
        interviews = len(applications_df[applications_df['status'].str.contains('Interview', na=False)])
        st.metric("Interviews", interviews)
    with col3:
        offers = len(applications_df[applications_df['status'] == 'Offer Received'])
        st.metric("Offers", offers)
    with col4:
        active = len(applications_df[applications_df['status'].isin(['Applied', 'Under Review'])])
        st.metric("Active Applications", active)

    # Application status chart
    if not applications_df['status'].empty:
        status_counts = applications_df['status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Application Status Distribution"
        )
        st.plotly_chart(fig_status, use_container_width=True)

    # Application timeline
    if 'application_date' in applications_df.columns:
        applications_over_time = applications_df.groupby('application_date').size().reset_index(name='count')
        fig_timeline = px.line(
            applications_over_time,
            x='application_date',
            y='count',
            title="Applications Over Time",
            markers=True
        )
        st.plotly_chart(fig_timeline, use_container_width=True)