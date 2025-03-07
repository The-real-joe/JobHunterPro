import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_dashboard(applications_df, jobs_df):
    st.header("Application Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Applications", len(applications_df))
    with col2:
        interviews = len(applications_df[applications_df['status'].str.contains('Interview')])
        st.metric("Interviews", interviews)
    with col3:
        offers = len(applications_df[applications_df['status'] == 'Offer Received'])
        st.metric("Offers", offers)
    with col4:
        active = len(applications_df[applications_df['status'].isin(['Applied', 'Under Review'])])
        st.metric("Active Applications", active)
    
    # Application status chart
    status_counts = applications_df['status'].value_counts()
    fig_status = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Application Status Distribution"
    )
    st.plotly_chart(fig_status)
    
    # Application timeline
    fig_timeline = px.line(
        applications_df,
        x='application_date',
        title="Application Timeline",
        markers=True
    )
    st.plotly_chart(fig_timeline)
