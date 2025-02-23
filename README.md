# Resume Analyzer - Job Matching Tool

**Resume Analyzer** is an interactive Streamlit application designed to help job seekers analyze their resumes and find relevant job opportunities on LinkedIn. By uploading a PDF resume, the app extracts key information, identifies relevant keywords, and uses them to search for job postings based on experience level and posting date. The results are presented in a visually appealing, interactive table with clickable links to job postings.

---

## Features

- **Resume Upload**: Upload a PDF resume to extract text and analyze its content.
- **Keyword Extraction**: Use AI to identify key skills and qualifications from your resume.
- **Job Search**: Generate a LinkedIn job search URL based on your experience level, posting date, and extracted keywords.
- **Job Scraping**: Fetch and display job listings from LinkedIn in a formatted table with clickable links.
- **Customizable Filters**: Select experience level (e.g., Internship, Entry Level, Mid-Senior Level) and posting date (e.g., Past 24 hours, Past week).
- **Styling**: Features a styled table with hover effects and a modern design for better user experience.

---

## Prerequisites

- Python 3.8+
- A stable internet connection (for LinkedIn scraping and API calls).
- Required Python libraries (see Installation below).

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/resume-analyzer.git
   cd resume-analyzer
   ```

2. **Install Dependencies**:
   Create a virtual environment and install the required packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory if your code requires any API keys or configuration (e.g., for LinkedIn scraping or AI models):
   ```plaintext
   PORT=8501  # Optional, defaults to 8501 for Streamlit
   ```

4. **Requirements File**:
   Ensure your `requirements.txt` includes:
   ```plaintext
   streamlit==1.31.0
   pandas==2.2.0
   json==2.0.9
   ```

   Note: The code references custom modules (`src.data.reader`, `src.llm.Analyse`, `src.jobs.search`). Ensure these are included in your project or adjust the dependencies accordingly.

---

## Usage

1. **Run the App**:
   Start the Streamlit app from the terminal:
   ```bash
   streamlit run app.py
   ```

2. **Upload a Resume**:
   - Use the sidebar to upload a PDF file containing your resume.
   - The app will extract text from the PDF and display a success message.

3. **Select Filters**:
   - Choose your experience level (e.g., "Internship," "Mid-Senior level") and the date range for job postings (e.g., "Past 24 hours," "Any time") from the dropdown menus in the sidebar.

4. **Analyze and Search**:
   - Click the "Analyse" button to process your resume, extract keywords, and search for jobs on LinkedIn.
   - The app will display a table of job listings with clickable links to view job postings on LinkedIn.

5. **Explore Results**:
   - The job listings are presented in a styled table with columns for job details and links to apply or view more information.

---

## Example Workflow

- Upload a PDF resume (e.g., `resume.pdf`).
- Select "Mid-Senior level" for experience and "Past week" for date posted.
- Click "Analyse" to extract keywords (e.g., "Python," "Data Science") and search LinkedIn for matching jobs.
- View a table of job postings with links to apply.

---

## Project Structure

```
resume-analyzer/
├── src/
│   ├── data/
│   │   └── reader.py         # PDF reading and processing
│   ├── llm/
│   │   └── Analyse.py        # Resume analysis and keyword extraction
│   └── jobs/
│       └── search.py         # LinkedIn job scraping and URL generation
├── app.py                    # Main Streamlit application
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

---

## Notes

- **Dependencies**: The code references custom modules (`src.data.reader`, `src.llm.Analyse`, `src.jobs.search`). Ensure these are implemented or adjust the README if they are placeholders or part of a larger project.
- **LinkedIn Scraping**: The `scrape_linkedin_jobs` function may require additional setup (e.g., API keys, scraping tools, or legal considerations for scraping LinkedIn data). Ensure compliance with LinkedIn’s terms of service.
- **Styling**: The app includes custom CSS for table styling, which is injected via `st.markdown` with `unsafe_allow_html=True`. This enhances the user interface but requires careful handling to avoid security risks.
- **Date**: This README is based on the app as of February 23, 2025.

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for bugs, feature requests, or improvements.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
```
