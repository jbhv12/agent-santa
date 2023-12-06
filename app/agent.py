from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.tools.ddg_search import DuckDuckGoSearchRun
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.prompts import MessagesPlaceholder
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
)
from langchain.memory import ConversationBufferMemory


def get_agent():
    llm = ChatOpenAI(streaming=True, temperature=0, model="gpt-3.5-turbo-0613")
    search = DuckDuckGoSearchRun()  # SerpAPIWrapper()
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    # db = SQLDatabase.from_uri("sqlite:///../../../../../notebooks/Chinook.db")
    # db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions",
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math",
        ),
        # Tool(
        #     name="FooBar-DB",
        #     func=db_chain.run,
        #     description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context",
        # ),
    ]

    agent_kwargs = {
        "input": lambda x: x["input"],
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
        "system_message": SystemMessage(content="You are a santa"), #todo
    }
    # message_history = RedisChatMessageHistory(url="redis://localhost:6379/0", ttl=600, session_id="my-session")
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True,
                                      # chat_memory=message_history
                                      )
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
    )
    agent_executor = None
    # agent.run(input="How many people live in canada?")
    return agent, agent_executor

