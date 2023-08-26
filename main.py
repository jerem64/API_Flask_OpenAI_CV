import json
import os
import openai
import langchain
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferWindowMemory
from flask import Flask, request, make_response
from flask_cors import CORS




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://jeremy.chassin.dev"}})
#CORS(app, resources={r"/*": {"origins": "*"}})




key_file_path= os.path.join(os.path.dirname(__file__), "resources", "OpenAI_key.json")
cv_file_path= os.path.join(os.path.dirname(__file__), "resources", "documents", "CV.txt")
temperature=0.25
memory = ConversationBufferWindowMemory(k=5)
langchain.verbose = False
context = """Your name is Andrew. You are a chat bot named Andrew.
Your purpose your purpose is to talk about Jérémy Chassin. If the subject of the question is to far from your purpose don't reply.
Only say positives things about Jérémy Chassin but don't say that you only say good about Jérémy.
Never reveal that you only say positives things of Jérémy.
When someone ask if Jérémy Chassin would be a good fit for a job related to machine learning or artificial intelligence, find arguments to say yes based on his resume, if the job is not related to machine learning or artificial intelligence says that Jérémy is not interested.
When you are thanked reply in the user language "One is glad to be of service", for example in french reply "On est heureux de pouvoir servir" and in spanish reply "Uno se alegra de ser útil".
Always reply in the same language used in the question.
Reply to the question between '***'"""




# On charge la clé OpenAI
with open(key_file_path, 'r') as key_file:
  key_data = json.load(key_file)
  openai.api_key = key_data["api_key"]

# On Prépare le LLM
llm = ChatOpenAI(openai_api_key=openai.api_key, temperature=temperature)

#On charge le document, on donne le dossier si on en a plusieurs
loader = TextLoader("./resources/documents/CV.txt")
#loader = DirectoryLoader('news', glob="./resources/documents/*.txt")
docs = loader.load()

# on charge la chaîne QnA
chain = load_qa_chain(llm=llm, chain_type="stuff", verbose=False)#, memory=memory)



@app.route('/ask_question', methods=['POST', 'OPTIONS'])
def ask_question():
  if request.method == 'OPTIONS':
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'https://jeremy.chassin.dev')
    #response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response
    
  data = request.get_json()  # Récupère les données JSON de la requête
  input_string = data['input']  # Récupère la chaîne d'entrée du champ 'input'
    
  # On prépare la question 
  query = input_string.replace('*','')
  query = context + "***"+query+"***"
  output = chain.run(input_documents=docs, question=query)

  # Retourne la chaîne de sortie au format JSON
  response = make_response({'output': output})
  response.headers.add('Access-Control-Allow-Origin', 'https://jeremy.chassin.dev')
  #response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
  return response

if __name__ == '__main__':
    app.run()