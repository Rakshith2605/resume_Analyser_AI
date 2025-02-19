from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import List, Tuple
import logging
import ast
import os
from dotenv import load_dotenv
from pathlib import Path

# Get the root directory (where .env is located)
root_dir = Path(__file__).resolve().parent.parent.parent
dotenv_path = root_dir / '.env'

# Load the environment variables
load_dotenv(dotenv_path=dotenv_path)

# Access your environment variables
api_key = os.getenv('OPENAI_API_KEY')


# Suppress unnecessary logs
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


def create_resume_analyzer() -> LLMChain:
    """
    Creates and returns an LLMChain for resume analysis.
    This function does not require `resume_text` as an argument.
    """
    try:
        # Initialize ChatOpenAI
        llm = ChatOpenAI(
            temperature=0.3,
            model_name="gpt-3.5-turbo",
            api_key=api_key
        )

        # Define the prompt template
        resume_prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""
            Act as ATS model and Extract technical skills from {resume_text}
            Analyse the {resume_text} and rank the strictly only top 10-12 skills based on their prominence, relevance and skills used in experience.
            Identify and highlight the skills in the {resume_text} is very strong in.
            Return exactly a list, and strictly the elements in that list should be in snake_case not in Space-Separated case.
            and strictly in the list format ["key_word1","key_word2","key_word3",....."key_word12",].
            example: Data_science not Data Science
            
            
            Resume: {resume_text}
            """
        )

        # Create and return the LLMChain
        return LLMChain(llm=llm, prompt=resume_prompt)
    except Exception as e:
        raise Exception(f"Error creating analyzer: {str(e)}")


def convert_string_to_list(input_string):
    """
    Converts a string representation of a list into an actual Python list.

    Args:
        input_string (str): A string representation of a list (e.g., '["item1", "item2"]').

    Returns:
        list: The actual Python list.
    """
    try:
        # Use ast.literal_eval to safely evaluate the string into a list
        return ast.literal_eval(input_string)
    except (ValueError, SyntaxError) as e:
        # Handle invalid input (e.g., malformed string)
        print(f"Error converting string to list: {e}")
        return []


def analyze_resume(resume_text: str) -> List[str]:
    """
    Analyzes the resume text and returns a list of extracted keywords.
    """
    if not resume_text:
        raise ValueError("Resume text is empty")

    try:
        # Create the resume analyzer chain
        chain = create_resume_analyzer()

        # Run the chain with the resume text
        response = chain.run(resume_text=resume_text)
        print("-############",type(response))
        # Parse the response to extract keywords
        keywords = convert_string_to_list(response)
        #keywords= chain.run(resume_text=resume_text)
        print('=====',type(keywords))
        return keywords
    except Exception as e:
        raise Exception(f"Error during analysis: {str(e)}")


