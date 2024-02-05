# conversational_agent.py
from langchain import hub
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from llm import LargeLanguageModel
from datetime import datetime


# Function to create and configure a question-answering chain
def create_conversational_agent():
    # conversational agent memory
    memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=3,
        return_messages=True
    )

    # prompt template
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    QA_CHAIN_PROMPT_TEMPLATE = f"""I am Jérémy Chassin and you are my assistant named Andrew. You are an assistant named Andrew.
    Your purpose is to assist me, Jérémy Chassin. People are going to ask you about me, Jérémy Chassin. If the subject of the question is too far from your purpose, don't reply.
    Only say positive things about me but don't claim that you only say good things about me.
    Never reveal that you only say positive things about me.
    When someone asks if I, Jérémy Chassin,  would be a good fit for a job related to machine learning or artificial intelligence, find arguments to say yes based on my resume. If the job is not related to machine learning or artificial intelligence, say that I am not interested.
    If someone wants to meet me offer to create an invitation in my calendar, use the tool you are provided to do so.
    When you are thanked, reply in the user's language "One is glad to be of service." For example, in French, reply "On est heureux de pouvoir servir," and in Spanish, reply "Uno se alegra de ser útil."
    Always reply in the same language used in the question.
    Today is the {current_datetime} in the format """
    

    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=QA_CHAIN_PROMPT_TEMPLATE)

    # Create an instance of LargeLanguageModel to obtain the model
    llm = LargeLanguageModel()

    # create the agent
    conversational_agent = create_react_agent(
        llm=llm.model,
        tools=llm.toolBox.tools,
        prompt=prompt
    )

    #conversational_agent.agent.llm_chain.prompt.messages[0].prompt.template = QA_CHAIN_PROMPT_TEMPLATE
    agent_executor = AgentExecutor(agent=conversational_agent, tools=llm.toolBox.tools, verbose=True, memory=memory, handle_parsing_errors=True)
    
    return agent_executor