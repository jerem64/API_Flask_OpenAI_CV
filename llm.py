#llm.py
from langchain import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

from agent_toolbox import AgentToolBox
from data_loader import DataLoader
from config import Config


# Class for setting up and managing LangChain
class LargeLanguageModel:
    def __init__(self):
        # Set OpenAI API key from configuration
        OpenAI.api_key = Config.OPENAI_KEY
        
        # Initialize ChatOpenAI model with configured OpenAI API key and temperature
        self.model = ChatOpenAI(openai_api_key=OpenAI.api_key, temperature=Config.TEMPERATURE)

        # Initialize DataLoader to load and process data documents
        self.data_loader = DataLoader()
        
        # Set up vector store for document embeddings
        self.vectorstore = self._setup_vectorstore()

        self.toolBox = AgentToolBox()

    def _setup_vectorstore(self):
        # Split documents using DataLoader
        all_splits = self.data_loader.split_documents()

        # Initialize OpenAIEmbeddings for document embedding
        embedding = OpenAIEmbeddings(openai_api_key=OpenAI.api_key)

        # Create a FAISS vector store using document embeddings
        vectorstore = FAISS.from_documents(documents=all_splits, embedding=embedding)
        
        return vectorstore
