import streamlit as st
import pandas as pd
import json
import os
from io import StringIO
from functools import lru_cache
from src.data.reader import upload_and_read_pdf
from src.llm.Analyse import analyze_resume
from src.jobs.search import scrape_linkedin_jobs, create_linkedin_search_url

# Configure page once
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📝",
    layout="wide"
)

# Load CSS from file or define it here
def load_css():
    st.markdown(
        """
        <style>
        .job-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
            font-size: 1em;
            font-family: sans-serif;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }
        .job-table th, .job-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .job-table th {
            background-color: #009879;
            color: white;
            text-transform: uppercase;
        }
        .job-table tr:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transform: translateY(-2px);
            transition: all 0.3s ease;
        }
        .job-link {
            color: #009879;
            text-decoration: none;
        }
        .job-link:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize session state once
def init_session_state():
    default_values = {
        "resume_text": None,
        "keywords": [],
        "jobs_list": []
    }
    
    for key, default in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default

# Cache expensive operations
@st.cache_data(ttl=3600, show_spinner=False)
def extract_resume(uploaded_file):
    try:
        return upload_and_read_pdf(uploaded_file)
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

@st.cache_data(ttl=1800, show_spinner=False)
def get_resume_keywords(resume_text):
    return analyze_resume(resume_text)

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_job_listings(url):
    try:
        with st.spinner("Fetching job listings..."):
            jobs_data = scrape_linkedin_jobs(url)
            if isinstance(jobs_data, str):
                return json.loads(jobs_data)
            return jobs_data
    except Exception as e:
        st.error(f"Error fetching jobs: {str(e)}")
        return []

def make_clickable(url, text):
    return f'<a target="_blank" href="{url}" class="job-link">{text}</a>'

def render_sidebar():
    st.sidebar.title("Resume Analyzer 📝")
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload Resume (PDF)",
        type='pdf', 
        accept_multiple_files=False,
        help="Upload your resume in PDF format"
    )
    
    if uploaded_file:
        st.sidebar.success(f"Uploaded: {uploaded_file.name}")
        
        experience = st.sidebar.selectbox(
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
        
        time_period = st.sidebar.selectbox(
            "Posted Within", 
            options=("Any time", "Past month", "Past week", "Past 24 hours"),
            index=None,
            placeholder="Select time period"
        )
        
        analyze_button = st.sidebar.button("Find Matching Jobs", type="primary", use_container_width=True)
        
        return uploaded_file, experience, time_period, analyze_button
    
    return None, None, None, False

def display_jobs(jobs_list):
    if not jobs_list:
        st.warning("No matching jobs found. Try adjusting your filters.")
        return
    
    df = pd.DataFrame(jobs_list)
    
    # Add clickable links
    df['link'] = df['link'].apply(lambda x: make_clickable(x, "View Job"))
    
    # Display the table
    st.subheader(f"Found {len(jobs_list)} Matching Jobs")
    st.markdown(df.to_html(escape=False, index=False, classes='job-table'), unsafe_allow_html=True)
    
    # Add export options
    if st.button("Export to CSV"):
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="job_matches.csv",
            mime="text/csv"
        )

def main():
    # Initialize components
    init_session_state()
    load_css()
    
    # Render sidebar and get user inputs
    uploaded_file, experience, time_period, analyze_clicked = render_sidebar()
    
    # Main area title
    st.title("Resume Job Matcher")
    
    # Process resume and find jobs if all inputs are provided
    if uploaded_file and experience and time_period and analyze_clicked:
        with st.status("Processing your resume...") as status:
            # Extract resume text
            st.session_state.resume_text = extract_resume(uploaded_file)
            
            # Extract keywords from resume
            if st.session_state.resume_text:
                status.update(label="Analyzing resume content...")
                keywords = get_resume_keywords(st.session_state.resume_text)
                
                if isinstance(keywords, list) and keywords:
                    st.session_state.keywords = keywords
                    status.update(label="Finding matching jobs...")
                    
                    # Create search URL and fetch jobs
                    url = create_linkedin_search_url(experience, time_period, st.session_state.keywords)
                    st.session_state.jobs_list = fetch_job_listings(url)
                    
                    status.update(label="Complete!", state="complete")
                else:
                    st.error("Failed to extract relevant keywords from your resume.")
                    status.update(label="Failed to extract keywords", state="error")
    
    # Display jobs if available
    if st.session_state.jobs_list:
        display_jobs(st.session_state.jobs_list)
        
        # Display keywords for transparency
        with st.expander("Keywords extracted from your resume"):
            st.write(", ".join(st.session_state.keywords))
    
    # Show instructions if no file uploaded
    if not uploaded_file:
        st.info("👈 Upload your resume PDF from the sidebar to get started")
        
        # Add some helpful information
        with st.expander("How it works"):
            st.write("""
            1. Upload your resume in PDF format
            2. Select your experience level and preferred job posting timeframe
            3. Click 'Find Matching Jobs' to analyze your resume
            4. We'll extract relevant keywords and find matching jobs on LinkedIn
            5. Review the results and click through to apply!
            """)

if __name__ == "__main__":
    main()
