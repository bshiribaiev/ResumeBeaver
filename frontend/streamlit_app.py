import streamlit as st
import requests
from dotenv import load_dotenv
import os

#Load envionment variables
load_dotenv()
API_KEY = os.getenv("AGENT_API_KEY")
BASE_URL = os.getenv("API_BASE_URL")

# Safety check: Warn if BASE_URL or API_KEY is missing
if not BASE_URL:
  st.error("API_BASE_URL is not set. Check your .env file.")
if not API_KEY:
  st.error("AGENT_API_KEY is not set. Check your .env file.")

#User Interace Setup
st.set_page_config(page_title="Resume Builder", layout="wide")
st.title("Resume Builder")
st.write("Welcome! Upload your info and let the AI build your resume.")

#Inputs
upload_file = st.file_uploader("Upload your Resume(PDF,DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Enter Job Description", height=200)

#ANALYZE BUTTON

if st.button("Analyze Resume"):
  if upload_file:
     with st.spinner("Analyzing your resume..."):
        try:
          resume_content = upload_file.read()

          response = requests.post(
          f"{BASE_URL}/agent/analyze-resume",
          headers={"Authorization": f"Bearer {API_KEY}"},
          files={"file": (upload_file.name, resume_content)},
          data={"job_description": job_description}   
          )
          if response.status_code == 200:
            result = response.json()
            st.success("Resume Analysis Complete!")
            st.text_area("Resume Analysis Result", result.get("analysis", ""), height=300)
          else:
            st.error(f"Analysis failed: {response.status_code}")
            st.text_area(response.text)
        except Exception as e:
          st.error(f"An error occurred: {str(e)}")
  else:
    st.warning("Please upload a resume file")
#-- OPTIMIZE BUTTON ---
if st.button("Generate Optimized Resume"):
    if upload_file and job_description:
        with st.spinner("Optimizing your resume..."):
            try:
              resume_content = upload_file.read()

              response = requests.post(
                "{BASE_URL}/agent/generate-optimized-resume",
                headers={"Authorization": f"Bearer {API_KEY}"},
                files={"file": (upload_file.name, resume_content)},
                data={"job_description": job_description}   
              )
              if response.status_code == 200:
                result = response.json()
                st.success("Your Optimized resume has been generated successfully!")
                st.text_area("Optimized Resume", result.get("resume", ""), height=300)
              else:
                st.error(f"Optimization failed: {response.status_code}")
                st.text_area(response.text)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")    
    else:
        st.warning("Please enter your job description")