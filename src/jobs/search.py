import requests
from bs4 import BeautifulSoup
import logging
import json
from prettytable import PrettyTable
import pyshorteners
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


    
    
def create_linkedin_search_url(experience, tym_ln, keywords_list):
    experience_levels = {
        "Internship": "1",
        "Entry level": "2",
        "Associate": "3",
        "Mid-Senior level": "4",
        "Director": "5",
        "Executive": "6"
    }
    
    time_ranges = {
        "Past 24 hours": "r86400",
        "Past week": "r604800",
        "Past month": "r2592000",
        "Any time": ""
    }
    
    # Get the experience level code
    exp = experience_levels.get(experience, "")  # Default to empty string if not found
    
    # Get the time range code
    tym = time_ranges.get(tym_ln, "")  # Default to empty string if not found
    
    print("Searching Jobs......")
    
    # Join keywords with 'OR' and replace spaces with '%20'
    formatted_keywords = '%20OR%20'.join([keyword.replace(' ', '%20') for keyword in keywords_list])

    # Base URL for LinkedIn job search
    base_url = "https://www.linkedin.com/jobs/search/?"

    # Add keywords to the URL
    url = f"{base_url}keywords={formatted_keywords}"

    # Filter for experience level
    if exp:
        url += f"&f_E={exp}"  # Add experience level filter if available

    # Filter for time range
    if tym:
        url += f"&f_TPR={tym}"  # Add time range filter if available

    # Add origin parameter
    url += "&origin=JOB_SEARCH_PAGE_JOB_FILTER"

    return url


def scrape_linkedin_jobs(url):
    # Headers to mimic browser request
    print("Scraping Jobs....")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    jobs_data = []

    try:
        # Make GET request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        job_cards = soup.find_all('div', class_='base-card')

        for card in job_cards:
            job = {
                'title': card.find('h3', class_='base-search-card__title').text.strip(),
                'company': card.find('h4', class_='base-search-card__subtitle').text.strip(),
                'location': card.find('span', class_='job-search-card__location').text.strip(),
                'link': card.find('a', class_='base-card__full-link').get('href')
            }
            jobs_data.append(job)

        # Convert to JSON string
        return json.dumps(jobs_data, indent=2)

    except Exception as e:
        return f"Error occurred: {str(e)}"
    

def print_job_listings_pretty(jobs_data):
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    table = PrettyTable()
    table.field_names = ['Job Title', 'Company', 'Location', 'Apply URL']
    table.align = 'l'

    s = pyshorteners.Shortener()
    for job in jobs_data:
        try:
            shortened_url = s.tinyurl.short(job['link'])
        except:
            shortened_url = job['link'][:50] + '...'

        table.add_row([
            job['title'][:40] + '...' if len(job['title']) > 40 else job['title'],
            job['company'][:20],
            job['location'][:25],
            shortened_url
        ])

    table._max_width = {
        "Job Title": 50,
        "Company": 30,
        "Location": 35,
        "Apply URL": 30
    }

    print(table)