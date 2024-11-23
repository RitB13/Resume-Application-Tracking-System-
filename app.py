import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from docx import Document
from dotenv import load_dotenv
import json
import plotly.graph_objects as go
import pandas as pd

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Get response from Gemini API
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

# Extract text from uploaded DOCX file
def input_docx_text(uploaded_file):
    doc = Document(uploaded_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Extract text from uploaded TXT file
def input_txt_text(uploaded_file):
    return uploaded_file.read().decode("utf-8")

# Generalized Prompt Template for various job roles
input_prompt = """
You are an experienced Application Tracking System (ATS) with expertise in evaluating resumes
for a wide range of job roles across different industries. Your task is to assess the candidate's
suitability for the role based on the provided job description.

Please assign a percentage match based on how well the resume aligns with the job description
and highlight any missing keywords with high accuracy.

Key areas to evaluate:
- Relevant skills and competencies
- Professional experience and achievements
- Educational background and qualifications
- Certifications and training
- Knowledge of industry-specific tools and technologies
- Soft skills and personal attributes
- Alignment with the job responsibilities and requirements

resume: {text}
job_description: {job_description}

I want the response in a structured format:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Streamlit App
st.set_page_config(page_title="SkillSync")

st.markdown("""
    <style>
        body, .stApp, .stMarkdown, .stText {
            font-family: 'Times New Roman', Times, serif;
            color: #F0F0F0;  
        }
        
        /* Title Styling */
        h1 {
            font-size: 48px;
            font-weight: bold;
            color: #F0F0F0;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        /* Button Styling */
        .stButton > button {
            font-family: 'Times New Roman', Times, serif;
            font-size: 20px; 
        }
    </style>
""", unsafe_allow_html=True)

# Title for Streamlit app
st.markdown("<h1>Resume Application Tracking System</h1>", unsafe_allow_html=True)
st.markdown("""
    <style>
        body {
            background-color: #003135;  
            color: #F0F0F0;  
        }
        .stApp {
            background-color: #003135;  
            color: #F0F0F0;  
        }
        .stButton > button {
            width: 250px;  
            height: 70px;  
            font-size: 20px;  
            margin: auto;  
            display: block;  
        }
    </style>
""", unsafe_allow_html=True)

# Text area for job description input
job_description = st.text_area("Paste the Job Description:")

# File uploader for resume input
uploaded_file = st.file_uploader("Upload Your Resume (PDF, DOCX, TXT)...", type=["pdf", "docx", "txt"])

# Submit button 
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "application/pdf":
                resume_text = input_pdf_text(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = input_docx_text(uploaded_file)
            elif uploaded_file.type == "text/plain":
                resume_text = input_txt_text(uploaded_file)
            else:
                st.error("Unsupported file format.")
                resume_text = None
            
            if resume_text:
                # Prepare prompt with extracted resume text and job description
                input_prompt_filled = input_prompt.format(text=resume_text, job_description=job_description)
                
                # Get response from Gemini API
                response = get_gemini_response(input_prompt_filled)
                
                # Parse response
                response_json = json.loads(response)
                
                # Display the Gemini Response in a block format
                st.markdown("## Response:")
                
                # Extract percentage match and missing keywords
                percentage_match = int(response_json.get("JD Match", "0").strip('%'))
                missing_keywords = response_json.get("MissingKeywords", [])
                
                # Display percentage match
                st.markdown(f"### Percentage Match: **<span style='font-size: 30px'>{percentage_match}%</span>**", unsafe_allow_html=True)
                
                # Display pie chart for percentage match 
                fig = go.Figure(
                    data=[go.Pie(
                        labels=['Match', 'Gap'], 
                        values=[percentage_match, 100 - percentage_match],
                        marker=dict(line=dict(color="rgba(0,0,0,0)", width=0))  
                    )],
                    layout=dict(
                        margin=dict(t=0, b=0, l=0, r=0),  
                        paper_bgcolor='#003135',  
                        plot_bgcolor='#003135',  
                        height=300  
                    )
                )

                st.plotly_chart(fig)

                # Display missing keywords as a simple list
                if missing_keywords:
                    st.markdown("### Missing Keywords:")
                    for keyword in missing_keywords:
                        st.write(f"- {keyword}")
                
                st.markdown("### Profile Summary:")
                st.write(response_json.get("Profile Summary", "No profile summary available."))
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please upload a resume.")
