import os
import google.generativeai as genai
import time
import json

DATASET_FOLDER = "../data/"
PROFILE_FOLDER = "../profiles/"

def clean_gemini_response(response):
    """ Unfortunaltely Gemini regularly prefixes his responses by adding prefix and suffix like ```json
    This function just removes them to enable a simple import afterwards. 
        That still happens despite the instruction: "Return the updated data for the dataset provided in a JSON format (each row as a node) without any prefix or decoration. 
        I should be able to leverage the response directly by using a programming language (like python), by just importing the result as is.
        Please only provide the result of task 3" with Gemini but does not happen with other LLMs.
    Args:
        response (string): JSON returned by Gemini
    Returns:
        string: Clean JSON
    """
    try:
        return json.loads (response
                            .replace("```json", "")
                            .replace("```JSON", "")
                            .replace("```", ""))
    except:
        return

def get_gemini_response(prompt, max_retries=3, delay=1):
    """
    Get a response from Gemini AI for a given prompt
    Args:
        prompt (str): The prompt to send to Gemini
        api_key (str): Your Gemini API key
        model_name (str): Model to use (default: "gemini-pro")
        max_retries (int): Maximum number of retry attempts
        delay (int): Delay between retries in seconds
    Returns:
        str: The model's response text
    Raises:
        Exception: If all retry attempts fail
    """

    # Get the Gemini Key
    GoogleGeminiKey = os.getenv('GEMINI_KEY', "")
    if (GoogleGeminiKey == ""):
        raise Exception(f"Google Gemini Key does not exist, please get a key (https://aistudio.google.com/prompts/new_chat) and set the env variable GEMINI_KEY accordingly")
    # Configure the API
    genai.configure(api_key=GoogleGeminiKey)
    # Initialize the model
    model = genai.GenerativeModel("gemini-1.5-flash-002") # or gemini-1.5-flash-002 or gemini-1.5-flash-8b
    
    # Retry logic
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                raise Exception(f"Failed to get response after {max_retries} attempts: {str(e)}")
            print(f"Attempt {attempt + 1} failed, retrying after {delay} seconds...")
            time.sleep(delay)