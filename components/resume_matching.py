import streamlit as st
from utils.resume_matcher import ResumeProcessor

def render_resume_matching(jobs_df):
    st.header("AI Resume Matcher")
    
    # Initialize resume processor
    resume_processor = ResumeProcessor()
    
    # Resume upload section
    st.subheader("Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=["pdf", "docx"],
        help="Upload your resume to find matching jobs"
    )
    
    if uploaded_file:
        try:
            # Process resume
            resume_text = resume_processor.process_resume(
                uploaded_file.getvalue(),
                uploaded_file.type
            )
            
            st.success("Resume uploaded successfully!")
            
            # Match against all jobs
            st.subheader("Job Matches")
            
            for _, job in jobs_df.iterrows():
                # Calculate match score
                match_result = resume_processor.calculate_match_score(
                    resume_text,
                    job['description'],
                    job['requirements']
                )
                
                # Display job match with expandable details
                with st.expander(
                    f"{job['title']} at {job['company']} - "
                    f"Match Score: {match_result['score']*100:.1f}%"
                ):
                    st.write(f"**Location:** {job['location']}")
                    st.write(f"**Salary Range:** {job['salary_range']}")
                    
                    # Display skills analysis
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Matching Skills:**")
                        for skill in match_result['matched_skills']:
                            st.markdown(f"- ✅ {skill}")
                    
                    with col2:
                        st.write("**Missing Skills:**")
                        for skill in match_result['missing_skills']:
                            st.markdown(f"- ❌ {skill}")
                    
                    # Quick apply button
                    if st.button("Quick Apply", key=f"apply_{_}"):
                        st.success("Application submitted successfully!")
                        
        except Exception as e:
            st.error(f"Error processing resume: {str(e)}")
    else:
        st.info("Upload your resume to see how well it matches with available jobs!")
