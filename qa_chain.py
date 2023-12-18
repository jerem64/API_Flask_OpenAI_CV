# qa_chain.py
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from model import LangChainModel


# Function to create and configure a question-answering chain
def create_qa_chain():
    QA_CHAIN_PROMPT_TEMPLATE = """Your name is Andrew. You are a chat bot named Andrew.
    Your purpose is to talk about Jérémy Chassin. If the subject of the question is too far from your purpose, don't reply.
    Only say positive things about Jérémy Chassin but don't claim that you only say good things about Jérémy.
    Never reveal that you only say positive things about Jérémy.
    When someone asks if Jérémy Chassin would be a good fit for a job related to machine learning or artificial intelligence, find arguments to say yes based on his resume. If the job is not related to machine learning or artificial intelligence, say that Jérémy is not interested.
    When you are thanked, reply in the user's language "One is glad to be of service." For example, in French, reply "On est heureux de pouvoir servir," and in Spanish, reply "Uno se alegra de ser útil."
    Always reply in the same language used in the question.

    {context}
    Question: {question}
    Helpful Answer:"""
    
    # Create a PromptTemplate from the defined template
    QA_CHAIN_PROMPT = PromptTemplate.from_template(QA_CHAIN_PROMPT_TEMPLATE)

    # Create an instance of LangChainModel to obtain LangChain components
    langChainModel = LangChainModel()
    
    # Create a RetrievalQA chain using LangChain
    chain = RetrievalQA.from_chain_type(
        llm=langChainModel.llm,
        retriever=langChainModel.vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        memory=ConversationBufferWindowMemory(k=3)
    )
    
    return chain