# config.py
import json
import os

# Configuration class for storing constants and settings
class Config:
    # File paths for API keys and documents
    key_file_path = os.path.join(os.path.dirname(__file__), "resources", "API_keys.json")
    documents_path = os.path.join(os.path.dirname(__file__), "resources", "documents")

    #Load API keys from a JSON file
    with open(key_file_path, 'r') as key_file:
        key_data = json.load(key_file)

    # Extract OpenAI key from loaded data
    OPENAI_KEY = key_data.get("OpenAI_key", "")

    # Configuration options
    LANGCHAIN_VERBOSE = False  # Set to True for verbose LangChain output
    TEMPERATURE = 0  # Temperature parameter for OpenAI API


    # Cross-Origin Resource Sharing (CORS) origin configuration
    # Uncomment one of the following lines based on your needs:
    # - Use the specific origin (e.g., "https://jeremy.chassin.dev")
    # CORS_ORIGIN = "https://jeremy.chassin.dev"
    # - Allow requests from any origin
    CORS_ORIGIN = "*" 
