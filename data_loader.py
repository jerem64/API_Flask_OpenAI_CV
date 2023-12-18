# data_loader.py
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import Config

# Class for loading and processing data documents
class DataLoader:
    def __init__(self):
        # Initialize PyPDFDirectoryLoader with the documents path from the configuration
        self.loader = PyPDFDirectoryLoader(Config.documents_path)

        # Load documents using the loader
        self.data_docs = self.loader.load()

        # Set up text splitter for document processing
        self.text_splitter = self._setup_text_splitter()

    def _setup_text_splitter(self):
        # Create and configure a RecursiveCharacterTextSplitter
        return RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)

    def split_documents(self):
        # Split the loaded documents using the configured text splitter        
        return self.text_splitter.split_documents(self.data_docs)