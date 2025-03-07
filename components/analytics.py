import streamlit as st
import plotly.express as px
import pandas as pd

def render_analytics(applications_df, jobs_df):
    st.header("Analytics")
    
    # Application success rate
    success_rate = (
        len(applications_df[applications_df['status'] == 'Offer Received']) /
        len(applications_df) * 100
    )
    
    st.metric("Application Success Rate", f"{success_rate:.1f}%")
    
    # Timeline of applications
    timeline_fig = px.timeline(
        applications_df,
        x_start='application_date',
        x_end='application_date',
        y='status',
        title="Application Timeline by Status"
    )
    st.plotly_chart(timeline_fig)
    
    # Location distribution
    location_counts = jobs_df['location'].value_counts()
    location_fig = px.bar(
        x=location_counts.index,
        y=location_counts.values,
        title="Job Opportunities by Location"
    )
    st.plotly_chart(location_fig)
