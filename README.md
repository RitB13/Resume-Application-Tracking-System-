# Resume-Application-Tracking-System

## Overview
Resume ATS Evaluation Tool is a Streamlit app that analyzes resumes against job descriptions using Google's Gemini API. It provides a match percentage, highlights missing keywords, and generates a profile summary. Supports PDF, DOCX, and TXT uploads, with interactive visualizations for ATS-like resume evaluation.

## Features
- **Resume Parsing:** Upload resumes in PDF, DOCX, or TXT formats and extract the text content.
- **Job Description Input:** Paste the job description for the role you're hiring for.
- **Resume Matching:** The application uses the **Gemini API** to assess how well the resume matches the job description.
- **Percentage Match:** View a percentage match based on the alignment of the resume with the job description.
- **Missing Keywords:** Get a list of missing keywords that the candidate's resume does not include but are important for the job.
- **Profile Summary:** Receive a brief summary of the candidate's profile, highlighting strengths and areas of improvement.
- **Visual Representation:** Display a pie chart visualizing the percentage match between the job description and the resume.

## Requirements
To run the application, you need to install the following dependencies:

- Python 3.7+
- Streamlit
- Google Gemini API
- PyPDF2
- python-docx
- python-dotenv
- Plotly
- Pandas

You can install the dependencies using the following command:

```bash
pip install -r requirements.txt
Setup Instructions
Clone this repository:

bash
Copy code
git clone https://github.com/your-username/resume-application-tracking-system.git
cd resume-application-tracking-system
Create a .env file in the project root directory and add your Google API key:

bash
Copy code
GOOGLE_API_KEY=your-google-api-key-here
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Streamlit app:

bash
Copy code
streamlit run app.py
Access the web app in your browser at: http://localhost:8501.

How to Use
Input the Job Description: Paste the job description for the role you want to evaluate resumes against.
Upload the Resume: Upload the candidate's resume in PDF, DOCX, or TXT format.
Submit the Resume: Click the "Submit" button to get a detailed match report.
Review the Results: The app will display the percentage match, missing keywords, and a profile summary. A pie chart will visualize the percentage match.
Example
Paste the job description for a Data Scientist role.
Upload a resume.
The system will show the match percentage, missing keywords like "Python," "Machine Learning," and "Data Analysis," and the candidate's profile summary.
Technologies Used
Streamlit for creating the interactive web interface.
Google Gemini API for generating insights and evaluating resumes.
PyPDF2 for parsing text from PDF resumes.
python-docx for parsing text from DOCX resumes.
Plotly for visualizing the match percentage in pie charts.
pandas for data handling and manipulation.
python-dotenv for managing environment variables.
Contributing
Feel free to contribute to this project by forking the repository and submitting a pull request with improvements or bug fixes.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Thanks to the Google Gemini API for providing powerful content generation capabilities.
Thanks to Streamlit for making it easy to create interactive web apps in Python.


