import streamlit as st
from io import StringIO
from src.data.reader import upload_and_read_pdf

# Configuration and Setup
def init_session_state():
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None

# Sidebar Components
def render_sidebar():
    st.write("Hello, *World!* :sunglasses:")
    
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
            "Director,Executive"
        ],
        index=None,
        placeholder="Select your experience level"
    )

def date_posted():
    return st.selectbox(
        "Select Date Posted", 
        options=("Any time","Past month","Past week","Past 24 hours")
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

# Main App
def main():
    init_session_state()
    
    with st.sidebar:
        uploaded_file = render_sidebar()
        
        if uploaded_file:
            experience = experience_selector()
            tym = date_posted()
            
            if experience and st.button("Analyse", type='primary'):
                st.session_state.resume_text = extract_resume(uploaded_file)
    
    # Main content area (can be expanded)
    if st.session_state.resume_text:
        st.write("Resume Analysis Results:")
        st.write(st.session_state.resume_text)

if __name__ == "__main__":
    main()
