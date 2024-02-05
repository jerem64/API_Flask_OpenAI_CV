# config.py
import json
import os
from flask import Flask


# Configuration class for storing constants and settings
class Config:
    # File paths for API keys and documents
    key_file_path = os.path.join(os.path.dirname(__file__), "resources", "secret_keys.json")
    documents_path = os.path.join(os.path.dirname(__file__), "resources", "documents")

    #Load API keys from a JSON file
    with open(key_file_path, 'r') as key_file:
        key_data = json.load(key_file)

    # Extract API keys from loaded data
    OPENAI_KEY = key_data.get("OpenAI_key", "")
    GOOGLE_CALENDAR_KEY = key_data.get("GoogleCalendar_key", "")

    # Google calendar email and ID
    GOOGLE_CALENDAR_CLIENT_EMAIL = "jerem.chassin@gmail.com" 
    GOOGLE_CALENDAR_CALENDAR_ID = "xxxxx"
    
    # Configuration options
    LANGCHAIN_VERBOSE = False  # Set to True for verbose LangChain output
    TEMPERATURE = 0  # Temperature parameter for OpenAI API


    # Cross-Origin Resource Sharing (CORS) origin configuration
    # Set CORS_ORIGIN based on whether the app is running in debug mode
    CORS_ORIGIN = "*" if Flask(__name__).debug else "https://jeremy.chassin.dev"