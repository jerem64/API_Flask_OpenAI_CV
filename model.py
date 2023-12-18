#model.py
import openai
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from data_loader import DataLoader
from config import Config

# Class for setting up and managing LangChain
class LangChainModel:
    def __init__(self):
        # Set OpenAI API key from configuration
        openai.api_key = Config.OPENAI_KEY
        
        # Initialize ChatOpenAI model with configured OpenAI API key and temperature
        self.llm = ChatOpenAI(openai_api_key=openai.api_key, temperature=Config.TEMPERATURE)

        # Initialize DataLoader to load and process data documents
        self.data_loader = DataLoader()

        # Set up vector store for document embeddings
        self.vectorstore = self._setup_vectorstore()

    def _setup_vectorstore(self):
        # Split documents using DataLoader
        all_splits = self.data_loader.split_documents()

        # Initialize OpenAIEmbeddings for document embedding
        embedding = OpenAIEmbeddings(openai_api_key=openai.api_key)

        # Create a FAISS vector store using document embeddings
        vectorstore = FAISS.from_documents(documents=all_splits, embedding=embedding)
        
        return vectorstore
