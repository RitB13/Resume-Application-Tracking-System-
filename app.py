import streamlit as st
import google.generativeai as genai
import os
import re
import PyPDF2 as pdf
from docx import Document
from dotenv import load_dotenv
import json
import plotly.graph_objects as go
import base64
import time
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
st.set_page_config(page_title="SkillSync")

st.markdown("""
    <style>
        /* Global text styling */
        body, .stApp, .stMarkdown, .stText {
            font-family: 'Times New Roman', Times, serif;
            color: #F0F0F0;  /* Deep off-white text */
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

# Function to add a custom background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_image});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function with your image file
add_bg_from_local('Background.jpg')  

# Read the CSS file for additional styling
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    

# Streamlit app layout with a title and company name
st.markdown("<div class='title'> <span> HUBNEX LABS - SCORE MY RESUME </span> </div>", unsafe_allow_html=True)

st.markdown("<div class='subtitle'>How good is your resume? </div>", unsafe_allow_html=True)

st.markdown("<div class='subtitle'>Find out instantly. Upload your resume and our free resume scanner will evaluate it against key criteria hiring managers and applicant tracking systems (ATS) look for. Get actionable feedback on how to improve your resume's success rate.</div>", unsafe_allow_html=True)

# Title for Streamlit app
st.markdown("<h1>Resume Application Tracking System</h1>", unsafe_allow_html=True)
st.markdown("""
    <style>
        body {
            color: #F0F0F0;  /* Deep off-white text */
        }
        .stApp {
            color: #F0F0F0;  /* Deep off-white text */
        }
        /* Style text labels */
        label {
            color: white !important;  /* Set the color to white */
            font-size: 18px;          /* Adjust font size for better visibility */
        }
        .stTextInput > div > div > label, /* For text area label */
        .stFileUploader > div > div > label, /* For file uploader label */
        .stButton > button { /* For button text */
            color: white !important;  /* Set text color to white */
        }
        textarea, input[type="file"] {
            color: white;  /* Set input text color to white */
            background-color: #333;  /* Dark background for contrast */
        }
        .stButton > button {
            width: 250px;  /* Larger button size */
            height: 70px;  /* Larger button size */
            font-size: 20px;  /* Larger text */
            margin: auto;  /* Center the button */
            display: block;  /* Ensure the button is centered */
        }
    </style>
""", unsafe_allow_html=True)

# Text area for job description input
job_description = st.text_area("Paste the Job Description:", key="input", help="Paste the job description here to match with your resume.")

# File uploader for resume input
uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx", "txt"],  help="Upload your resume in PDF, DOCX or TEXT format.")

# Submit button 
submit = st.button("Evaluate Resume", key="submit")

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
                try:
                    # Clean response to remove invalid characters
                    cleaned_response = re.sub(r'[\x00-\x1F\x7F]', '', response)
                    response_json = json.loads(cleaned_response)
                except json.JSONDecodeError as e:
                    st.error("Error parsing the API response. Please try again or check the inputs.")
                    st.write("Raw Response:", response)

                # Extract percentage match 
                percentage_match = int(response_json.get("JD Match", "0").strip('%'))
                
                # Display percentage match
                st.markdown(f"### Percentage Match: **<span style='font-size: 30px'>{percentage_match}%</span>**", unsafe_allow_html=True)

                # Display donut chart for percentage match
                fig = go.Figure(
                    data=[go.Pie(
                        labels=['Match', 'Gap'], 
                        values=[percentage_match, 100 - percentage_match],
                        marker=dict(line=dict(color="rgba(0,0,0,0)", width=0)),
                        hole=0.4  # Create a donut chart with a hole in the center
                    )],
                    layout=dict(
                        margin=dict(t=0, b=0, l=0, r=0),  
                        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
                        plot_bgcolor='rgba(0, 0, 0, 0)',   # Transparent plot area
                        height=300  # Adjust height as needed
                    )
                )

                # Add customization to make the chart visually appealing
                fig.update_traces(
                    textinfo='label+percent',  # Show both label and percentage
                    hoverinfo='label+percent',  # Information on hover
                    marker=dict(colors=['#041E42', '#5F9EA0'], line=dict(color='#000000', width=1))  
                )

                st.plotly_chart(fig, use_container_width=True,)  # Adjust container width to match Streamlit's layout

                # Keyword Analysis
                keyword_analysis = f"Identify keywords missing from the resume that are present in the job description."
                input_prompt_keyword_match = f"{keyword_analysis}\n\nresume: {resume_text}\njob_description: {job_description}"
                response_keyword_match = get_gemini_response(input_prompt_keyword_match)
                st.markdown("## Missing Keywords:")
                st.write(response_keyword_match)

                # Skills Match Analysis
                prompt_skills_match = f"Please compare the skills in the resume to the job description."
                input_prompt_skills_match = f"{prompt_skills_match}\n\nresume: {resume_text}\njob_description: {job_description}"
                response_skills_match = get_gemini_response(input_prompt_skills_match)
                st.markdown("## Skills Match Analysis:")
                st.write(response_skills_match)

                # General Resume-Job Description Matching
                prompt_summary = f"Write the Profile Summary and suggest improvements."
                input_prompt_summary = f"{prompt_summary}\n\nresume: {resume_text}\njob_description: {job_description}"
                response_summary = get_gemini_response(input_prompt_summary)
                st.markdown("## Profile Summary:")
                st.write(response_summary)

                # Grammar and Formatting Check
                grammar = f"Review the grammar and formatting of the resume."
                input_prompt_grammar = f"{grammar}\n\nresume: {resume_text}\njob_description: {job_description}"
                response_grammar = get_gemini_response(input_prompt_grammar)
                st.markdown("## Grammar and Formatting Check:")
                st.write(response_grammar)

                # Tone and Language
                tone_lang = f"Evaluate the tone and language of the resume for alignment with the job description"
                input_prompt_tone_lang = f"{tone_lang}\n\nresume: {resume_text}\njob_description: {job_description}"
                response_tone = get_gemini_response(input_prompt_tone_lang)
                st.markdown("## Tone and Language:")
                st.write(response_tone)
                
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please upload a resume.")
          
# Custom Footer with additional styling
footer = """
<style>
a:link, a:visited{
    color: yellow;
    background-color: transparent;
    text-decoration: underline;
}

a:hover, a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #333;
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    font-family: Arial, sans-serif;
}

.footer a {
    color: #ffcc00;
    font-weight: bold;
}

.footer a:hover {
    color: #ff6600;
}
</style>
<div class="footer">
    <p>Powered by HUBNEX LABS | <a href="https://www.hubnex.in/" target="_blank">HUBNEX LABS</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
