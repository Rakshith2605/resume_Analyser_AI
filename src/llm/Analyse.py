from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import List, Optional
import logging
import ast
import os
from dotenv import load_dotenv
from pathlib import Path
from functools import lru_cache

# Configure logging once
logging.basicConfig(level=logging.INFO)
for logger_name in ("openai", "httpx", "httpcore"):
    logging.getLogger(logger_name).setLevel(logging.WARNING)

@lru_cache(maxsize=1)
def get_api_key() -> str:
    """Cache and retrieve the API key to avoid redundant environment loading."""
    # Get the root directory (where .env is located)
    root_dir = Path(__file__).resolve().parent.parent.parent
    dotenv_path = root_dir / '.env'
    
    # Load environment variables if not already done
    load_dotenv(dotenv_path=dotenv_path)
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    return api_key

@lru_cache(maxsize=1)
def get_resume_analyzer() -> LLMChain:
    """
    Creates and caches an LLMChain for resume analysis.
    Using lru_cache to avoid recreating the chain for each analysis.
    """
    # Initialize ChatOpenAI
    llm = ChatOpenAI(
        temperature=0.3,
        model_name="gpt-3.5-turbo",
        api_key=get_api_key()
    )
    
    # Define the prompt template - optimized wording
    resume_prompt = PromptTemplate(
        input_variables=["resume_text"],
        template="""
        Analyze the technical skills in the resume below. 
        Return ONLY a list of the top 10-12 most prominent and relevant technical skills.
        Format strictly as a Python list of snake_case strings: ["skill_1", "skill_2", ..., "skill_12"]
        Example: Return "python_programming" not "Python Programming"
        
        Resume: {resume_text}
        """
    )
    
    # Create and return the LLMChain
    return LLMChain(llm=llm, prompt=resume_prompt)

def parse_skills_list(response: str) -> List[str]:
    """
    Safely parses the LLM response into a list of skills.
    Handles various response formats gracefully.
    """
    # Clean the response string
    cleaned = response.strip()
    
    try:
        # First attempt: direct parsing with ast.literal_eval
        return ast.literal_eval(cleaned)
    except (ValueError, SyntaxError):
        # Second attempt: try to extract list from text if wrapped in other content
        try:
            # Find list-like patterns [...]
            start = cleaned.find('[')
            end = cleaned.rfind(']')
            
            if start >= 0 and end > start:
                list_str = cleaned[start:end+1]
                return ast.literal_eval(list_str)
            
            # If no list found, split by commas if contains commas
            if ',' in cleaned:
                items = [item.strip().strip('"\'') for item in cleaned.split(',')]
                return [item for item in items if item]
                
            return []
        except Exception:
            # Last resort: return any non-empty words as individual items
            import re
            return re.findall(r'\b\w+\b', cleaned)

def analyze_resume(resume_text: str) -> List[str]:
    """
    Analyzes the resume text and returns a list of extracted keywords.
    Optimized for performance and error handling.
    """
    if not resume_text or not resume_text.strip():
        logging.warning("Empty resume text provided")
        return []
    
    try:
        # Get the cached resume analyzer chain
        chain = get_resume_analyzer()
        
        # Run the chain with the resume text
        response = chain.run(resume_text=resume_text)
        
        # Parse the response to extract keywords
        keywords = parse_skills_list(response)
        
        # Ensure we got a list back
        if not isinstance(keywords, list):
            logging.warning(f"Expected list, got {type(keywords)}")
            return []
            
        # Remove any empty items and ensure all are strings
        return [str(kw).strip() for kw in keywords if kw]
        
    except Exception as e:
        logging.error(f"Error analyzing resume: {str(e)}")
        return []
