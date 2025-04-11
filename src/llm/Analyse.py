import streamlit as st
from io import StringIO
from src.data.reader import upload_and_read_pdf
from src.llm.Analyse import analyze_resume
from src.jobs.search import scrape_linkedin_jobs, create_linkedin_search_url
import pandas as pd
import json
import os

st.set_page_config(page_title="Resume Analyzer")

# Configuration and Setup
def init_session_state():
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
    if 'keywords' not in st.session_state:
        st.session_state.keywords = []
    if 'url' not in st.session_state:
        st.session_state.url = None
    if 'jobs_json' not in st.session_state:
        st.session_state.jobs_json = None
    if 'jobs_list' not in st.session_state:
        st.session_state.jobs_list = []

# Sidebar Components
def render_sidebar():
    st.write("### Resume Analyser :sunglasses:")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",  # Fixed label to match file type
        type='pdf', 
        accept_multiple_files=False
    )
    
    if uploaded_file:
        st.write("Resume: ", uploaded_file.name)
        return uploaded_file
    return None

def experience_selector():
    return st.selectbox(
        "Experience Level",
        options=[
            "Internship",
            "Entry level",
            "Associate",
            "Mid-Senior level",
            "Director",
            "Executive"
        ],
        index=None,
        placeholder="Select your experience level"
    )

def date_posted():
    return st.selectbox(
        "Select Date Posted", 
        options=("Any time", "Past month", "Past week", "Past 24 hours"),
        index=None,
        placeholder="Select your job post timeline"
    )

# Processing Functions
def extract_resume(uploaded_file):        
    try:
        resume_text = upload_and_read_pdf(uploaded_file)
        st.success("Resume text extracted successfully!")
        return resume_text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def make_clickable(url, text):
    return f'<a target="_blank" href="{url}">{text}</a>'

# Main App
def main():
    init_session_state()
    
    with st.sidebar:
        uploaded_file = render_sidebar()
        
        if uploaded_file:
            experience = experience_selector()
            tym_ln = date_posted()
            
            if experience and tym_ln and st.button("Analyse", type='primary'):
                # Debugging: Print selected values
                st.write(f"Selected Experience: {experience}")
                st.write(f"Selected Time Range: {tym_ln}")
                
                # Extract resume text
                st.session_state.resume_text = extract_resume(uploaded_file)
                
                if st.session_state.resume_text:
                    # Analyze resume to extract keywords
                    st.session_state.keywords = analyze_resume(st.session_state.resume_text)
                    if not isinstance(st.session_state.keywords, list):
                        st.session_state.keywords = []
                    st.write(f"Extracted Keywords: {st.session_state.keywords}")
                    
                    # Generate LinkedIn search URL
                    st.session_state.url = create_linkedin_search_url(experience, tym_ln, st.session_state.keywords)
                    st.write(f"Generated URL: {st.session_state.url}")
                    
                    # Scrape jobs
                    try:
                        st.session_state.jobs_json = scrape_linkedin_jobs(st.session_state.url)
                        st.session_state.jobs_list = json.loads(st.session_state.jobs_json)
                    except json.JSONDecodeError as e:
                        st.error(f"Error parsing jobs data: {e}")
                        st.session_state.jobs_list = []
    
    # Main content area (can be expanded)
    if st.session_state.resume_text:
        #st.write("Resume Analysis Results:")
        if st.session_state.jobs_list and isinstance(st.session_state.jobs_list, list):
            df = pd.DataFrame(st.session_state.jobs_list)
            df['link'] = df['link'].apply(lambda x: make_clickable(x, "View Job"))
            html_table = df.to_html(escape=False, index=False)
            st.write("### Resume Analysis Results")
            st.markdown(html_table, unsafe_allow_html=True)
        else:
            st.warning("No jobs data available or invalid format.")




st.markdown(
    """
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1em 0;
        font-size: 1em;
        font-family: sans-serif;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #009879;
        color: white;
        text-transform: uppercase;
    }
    tr:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Shadow hover effect */
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    a {
        color: #009879;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html = True
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    #port = int(os.environ.get("PORT", 8501))
    #st.set_page_config(page_title="Resume Analyzer")
    main()
