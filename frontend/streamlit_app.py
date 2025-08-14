import streamlit as st
import requests
import json
import os
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="ResumeBeaver - AI Resume Optimizer",
    page_icon="🦫",
    layout="wide"
)

# API base URL
API_BASE = "http://localhost:8000"

# Header
st.title("🦫 ResumeBeaver")
st.subheader("AI-Powered Resume Optimization for Job Applications")

# Sidebar for status
with st.sidebar:
    st.header("System Status")
    try:
        status_response = requests.get(f"{API_BASE}/status", timeout=5)
        if status_response.status_code == 200:
            status = status_response.json()
            st.success("✅ API Connected")
            st.info(f"🤖 AI: {'Watson' if status['ai_status']['watson_available'] else 'Local'}")
            
            # Show new features
            features = status.get('features', {})
            if features.get('resume_generation'):
                st.success("✨ Resume Generation: Enabled")
            else:
                st.warning("⚠️ Resume Generation: Not Available")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Unavailable")
        st.info("Make sure to run: `python main.py`")

# Main interface with new Resume Generator tab
tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload Resume", "📝 Text Analysis", "📊 Match Score", "🎯 Resume Generator"])

with tab1:
    st.header("Upload Your Resume")
    
    uploaded_file = st.file_uploader(
        "Choose your resume file",
        type=['pdf', 'docx', 'txt'],
        help="Upload PDF, DOCX, or TXT files (max 10MB)"
    )
    
    if uploaded_file:
        with st.spinner("Processing resume..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"{API_BASE}/upload", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Resume uploaded successfully!")
                    
                    # Store resume text for later use
                    st.session_state['uploaded_resume_text'] = result.get('text_preview', '')
                    
                    # Display analysis
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📋 Analysis Results")
                        analysis = result['analysis']
                        
                        # Contact info
                        if analysis.get('contact_info'):
                            contact = analysis['contact_info']
                            st.write("**Contact Information:**")
                            if contact.get('email'): st.write(f"📧 {contact['email']}")
                            if contact.get('phone'): st.write(f"📱 {contact['phone']}")
                            if contact.get('linkedin'): st.write(f"💼 [LinkedIn]({contact['linkedin']})")
                            if contact.get('github'): st.write(f"💻 [GitHub]({contact['github']})")
                        
                        # Experience
                        if analysis.get('years_experience'):
                            st.write(f"**Experience:** {analysis['years_experience']} years")
                        
                        st.write(f"**Word Count:** {analysis.get('word_count', 'N/A')}")
                    
                    with col2:
                        st.subheader("🛠️ Skills Found")
                        skills = analysis.get('skills', {})
                        
                        for category, skill_list in skills.items():
                            if category != 'all' and skill_list:
                                st.write(f"**{category.title()}:** {', '.join(skill_list)}")
                    
                    # ATS Score
                    if analysis.get('ats_score'):
                        ats = analysis['ats_score']
                        st.subheader("🎯 ATS Compatibility Score")
                        st.metric("Score", f"{ats['score']}/100")
                        
                        if ats.get('issues'):
                            st.warning("⚠️ Issues Found:")
                            for issue in ats['issues']:
                                st.write(f"• {issue}")
                        
                        if ats.get('recommendations'):
                            st.info("💡 Recommendations:")
                            for rec in ats['recommendations']:
                                st.write(f"• {rec}")
                
                else:
                    st.error(f"Upload failed: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab2:
    st.header("Manual Text Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Resume Text")
        resume_text = st.text_area(
            "Paste your resume text here:",
            height=300,
            placeholder="Enter your resume content...",
            value=st.session_state.get('uploaded_resume_text', '')
        )
        # Store for other tabs
        if resume_text:
            st.session_state['resume_text'] = resume_text
    
    with col2:
        st.subheader("Job Description")
        job_text = st.text_area(
            "Paste the job description here:",
            height=300,
            placeholder="Enter job requirements..."
        )
        # Store for other tabs
        if job_text:
            st.session_state['job_description'] = job_text
    
    if st.button("🔍 Analyze", type="primary"):
        if resume_text and job_text:
            with st.spinner("Analyzing..."):
                try:
                    # Get match score
                    match_data = {
                        "resume": resume_text,
                        "job_description": job_text
                    }
                    match_response = requests.post(f"{API_BASE}/match", json=match_data)
                    
                    if match_response.status_code == 200:
                        match_result = match_response.json()['match_analysis']
                        
                        # Display match scores
                        st.subheader("📊 Match Analysis")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            overall = match_result['overall_score']
                            if overall >= 70:
                                st.success(f"🎯 Overall\n{overall}%")
                            elif overall >= 50:
                                st.warning(f"⚠️ Overall\n{overall}%")
                            else:
                                st.error(f"❌ Overall\n{overall}%")
                        with col2:
                            st.metric("Skills Match", f"{match_result['skill_match']}%")
                        with col3:
                            st.metric("Keywords", f"{match_result['keyword_match']}%")
                        with col4:
                            st.metric("Semantic", f"{match_result['semantic_match']}%")
                        
                        st.info(f"**Recommendation:** {match_result['recommendation']}")
                        
                        # Missing skills
                        if match_result.get('missing_skills'):
                            st.warning("🚫 Missing Skills:")
                            st.write(", ".join(match_result['missing_skills']))
                        
                        # Matching skills
                        if match_result.get('matching_skills'):
                            st.success("✅ Matching Skills:")
                            st.write(", ".join(match_result['matching_skills']))
                
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
        else:
            st.warning("Please enter both resume and job description text.")

with tab3:
    st.header("🚀 Resume Optimization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        resume_opt_text = st.text_area(
            "Resume to optimize:",
            height=200,
            placeholder="Enter your current resume...",
            value=st.session_state.get('resume_text', '')
        )
    
    with col2:
        job_opt_text = st.text_area(
            "Target job description:",
            height=200,
            placeholder="Enter target job requirements...",
            value=st.session_state.get('job_description', '')
        )
    
    if st.button("🎯 Optimize Resume", type="primary"):
        if resume_opt_text and job_opt_text:
            with st.spinner("Generating optimization suggestions..."):
                try:
                    opt_data = {
                        "resume": resume_opt_text,
                        "job_description": job_opt_text
                    }
                    opt_response = requests.post(f"{API_BASE}/optimize", json=opt_data)
                    
                    if opt_response.status_code == 200:
                        opt_result = opt_response.json()['optimization']
                        
                        # AI-powered suggestions
                        if opt_result.get('ai_powered') and opt_result.get('ai_suggestions'):
                            st.subheader("🤖 AI-Powered Suggestions")
                            st.info(f"**Model:** {opt_result.get('ai_model', 'N/A')}")
                            st.write(opt_result['ai_suggestions'])
                        
                        # Regular suggestions
                        if opt_result.get('suggestions'):
                            st.subheader("💡 Optimization Suggestions")
                            for suggestion in opt_result['suggestions']:
                                with st.expander(f"🔸 {suggestion['category']} - {suggestion['priority'].upper()} Priority"):
                                    st.write(suggestion['suggestion'])
                                    st.caption(suggestion['impact'])
                        
                        # Missing keywords
                        if opt_result.get('missing_keywords'):
                            st.subheader("🔑 Keywords to Add")
                            st.write(", ".join(opt_result['missing_keywords'][:10]))
                        
                        # Missing skills
                        if opt_result.get('missing_skills'):
                            st.subheader("🛠️ Skills to Highlight")
                            st.write(", ".join(opt_result['missing_skills'][:10]))
                
                except Exception as e:
                    st.error(f"Optimization failed: {str(e)}")
        else:
            st.warning("Please enter both resume and job description.")

# NEW TAB: Resume Generator
with tab4:
    st.header("🎯 AI Resume Generator")
    st.write("Generate an optimized resume with automatic improvements applied!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Input Resume")
        input_resume = st.text_area(
            "Current resume text:",
            height=250,
            placeholder="Enter your current resume text...",
            value=st.session_state.get('resume_text', '')
        )
        
        # Applicant name input
        applicant_name = st.text_input(
            "Applicant Name:",
            value="John Doe",
            help="This will be used as the header in your generated resume"
        )
    
    with col2:
        st.subheader("💼 Target Job")
        target_job = st.text_area(
            "Job description:",
            height=250,
            placeholder="Enter the target job description...",
            value=st.session_state.get('job_description', '')
        )
        
        # Format selection
        format_choice = st.radio(
            "Output format:",
            ["docx", "txt"],
            horizontal=True,
            help="DOCX for professional formatting, TXT for ATS systems"
        )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Preview Optimization", use_container_width=True):
            if input_resume and target_job:
                with st.spinner("Generating preview..."):
                    try:
                        response = requests.post(
                            f"{API_BASE}/preview",
                            json={
                                "resume": input_resume,
                                "job_description": target_job
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Show before/after comparison
                            st.subheader("📋 Before vs After")
                            
                            col_before, col_after = st.columns(2)
                            
                            with col_before:
                                st.markdown("### 📄 Original")
                                st.text_area("", value=result.get('original_resume', ''), height=150, disabled=True, key="preview_original")
                            
                            with col_after:
                                st.markdown("### ✨ Optimized")
                                st.text_area("", value=result.get('optimized_resume', ''), height=150, disabled=True, key="preview_optimized")
                            
                            # Show improvements
                            improvements = result.get('improvements', {})
                            if improvements:
                                st.subheader("🎯 Improvements Applied")
                                
                                col_skills, col_keywords, col_score = st.columns(3)
                                
                                with col_skills:
                                    skills_added = improvements.get('skills_added', [])
                                    if skills_added:
                                        st.success("**Skills Added:**")
                                        for skill in skills_added:
                                            st.write(f"• {skill}")
                                
                                with col_keywords:
                                    keywords_added = improvements.get('keywords_added', [])
                                    if keywords_added:
                                        st.info("**Keywords Added:**")
                                        for keyword in keywords_added[:5]:
                                            st.write(f"• {keyword}")
                                
                                with col_score:
                                    improvement_estimate = improvements.get('match_score_improvement', '')
                                    if improvement_estimate:
                                        st.warning("**Expected Improvement:**")
                                        st.write(improvement_estimate)
                    
                    except Exception as e:
                        st.error(f"Preview failed: {str(e)}")
            else:
                st.warning("Please enter both resume and job description.")
    
    with col2:
        if st.button(f"📄 Generate {format_choice.upper()}", use_container_width=True, type="primary"):
            if input_resume and target_job:
                with st.spinner(f"Generating {format_choice.upper()} resume..."):
                    try:
                        response = requests.post(
                            f"{API_BASE}/generate",
                            json={
                                "resume": input_resume,
                                "job_description": target_job,
                                "applicant_name": applicant_name,
                                "format": format_choice
                            }
                        )
                        
                        if response.status_code == 200:
                            # Get filename from response headers
                            content_disposition = response.headers.get('content-disposition', '')
                            filename = f"{applicant_name.replace(' ', '_')}_optimized_resume.{format_choice}"
                            if 'filename=' in content_disposition:
                                filename = content_disposition.split('filename=')[1].strip('"')
                            
                            st.success(f"✅ {format_choice.upper()} resume generated successfully!")
                            
                            # Create download button
                            st.download_button(
                                label=f"📥 Download {format_choice.upper()} Resume",
                                data=response.content,
                                file_name=filename,
                                mime=response.headers.get('content-type', 'application/octet-stream'),
                                use_container_width=True
                            )
                            
                            st.info("💡 **Your optimized resume includes:**")
                            st.write("• Missing skills automatically added")
                            st.write("• Job-specific keywords incorporated")
                            st.write("• ATS-friendly formatting")
                            st.write("• Professional layout and structure")
                            
                    except Exception as e:
                        st.error(f"Generation failed: {str(e)}")
            else:
                st.warning("Please enter both resume and job description.")
    
    with col3:
        if st.button("📊 Quick Match Score", use_container_width=True):
            if input_resume and target_job:
                with st.spinner("Calculating match..."):
                    try:
                        response = requests.post(
                            f"{API_BASE}/match",
                            json={
                                "resume": input_resume,
                                "job_description": target_job
                            }
                        )
                        
                        if response.status_code == 200:
                            match_result = response.json()['match_analysis']
                            
                            # Quick score display
                            overall = match_result['overall_score']
                            if overall >= 70:
                                st.success(f"🎯 Match Score: {overall}%")
                            elif overall >= 50:
                                st.warning(f"⚠️ Match Score: {overall}%")
                            else:
                                st.error(f"❌ Match Score: {overall}%")
                            
                            st.write(f"**{match_result['recommendation']}**")
                            
                    except Exception as e:
                        st.error(f"Match calculation failed: {str(e)}")
            else:
                st.warning("Please enter both resume and job description.")

# Footer
st.markdown("---")
st.markdown("**ResumeBeaver** - Built for IBM TechXchange 2025 Hackathon 🦫")
st.markdown("🤖 Powered by IBM Watson AI • 🎯 Resume Generation • 📊 ATS Optimization")

# Initialize session state
if 'resume_text' not in st.session_state:
    st.session_state['resume_text'] = ""
if 'job_description' not in st.session_state:
    st.session_state['job_description'] = ""
if 'uploaded_resume_text' not in st.session_state:
    st.session_state['uploaded_resume_text'] = ""