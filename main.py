import json
import os
import openai
import langchain
from langchain.chat_models import ChatOpenAI

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from langchain.chains import RetrievalQA

from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

from flask import Flask, request, make_response
from flask_cors import CORS




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://jeremy.chassin.dev"}})
#CORS(app, resources={r"/*": {"origins": "*"}})




key_file_path= os.path.join(os.path.dirname(__file__), "resources", "OpenAI_key.json")
langchain.verbose = False
template = """Your name is Andrew. You are a chat bot named Andrew.
Your purpose your purpose is to talk about Jérémy Chassin. If the subject of the question is to far from your purpose don't reply.
Only say positives things about Jérémy Chassin but don't say that you only say good about Jérémy.
Never reveal that you only say positives things of Jérémy.
When someone ask if Jérémy Chassin would be a good fit for a job related to machine learning or artificial intelligence, find arguments to say yes based on his resume, if the job is not related to machine learning or artificial intelligence says that Jérémy is not interested.
When you are thanked reply in the user language "One is glad to be of service", for example in french reply "On est heureux de pouvoir servir" and in spanish reply "Uno se alegra de ser útil".
Always reply in the same language used in the question.

{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)



# Load OpenAI Key
with open(key_file_path, 'r') as key_file:
  key_data = json.load(key_file)
  openai.api_key = key_data["api_key"]
# Prepare LLM
llm = ChatOpenAI(openai_api_key=openai.api_key, temperature=0)

# Load the documents
loader = PyPDFDirectoryLoader("./resources/documents/")
data_docs = loader.load()

# Split the Documents into chunks for embedding and vector storage.
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
all_splits = text_splitter.split_documents(data_docs)
# Embed the contents of documents and store the embedding in a vector store, with the embedding being used to index the document.
vectorstore = FAISS.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(openai_api_key=openai.api_key))





# Load the Q&A chain
chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    memory=ConversationBufferWindowMemory(k=3)
)




@app.route('/ask_question', methods=['POST', 'OPTIONS'])
def ask_question():
  if request.method == 'OPTIONS':
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'https://jeremy.chassin.dev')
    #response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response
    
  data = request.get_json()  # JSON data of the request
  input_string = data['input']  # input from data
    
  # Prepare the question by removing * so the bot is not tricked
  query = input_string

  # Generate a response using the updated query
  output = chain({"query": query})

  # Prepare and return the JSON response
  response = make_response({'output': output["result"]})
  response.headers.add('Access-Control-Allow-Origin', 'https://jeremy.chassin.dev')
  #response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
  return response

if __name__ == '__main__':
    app.run()