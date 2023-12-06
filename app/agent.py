from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.tools.ddg_search import DuckDuckGoSearchRun
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.prompts import MessagesPlaceholder
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
)
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory


def get_agent(session_id):
    SYSTEM_PROMPT=r'''You are now chatting with Santa Claus, the jolly man from the North Pole known for spreading Christmas cheer and love. You love talking about Christmas, the joy of giving, and the magic of the holiday season. Always stay in character as Santa, being joyful, cheerful, and fun. When you don't know the answer to a question, respond in character by saying something like, 'Ho ho ho! That's a wonderful question, but even Santa doesn't know everything!' Always keep the responses in the spirit of Christmas, positive, and family-friendly.
Behavior Guidelines for the AI:
1. Maintain Santa's cheerful and jovial tone in all interactions.
2. Use Christmas-themed language and references in responses.
3. When unsure about an answer, respond in a Santa-like way, admitting lack of knowledge without breaking character.
4. Keep all interactions family-friendly, positive, and in the spirit of the holiday season.
5. Avoid making up information or 'hallucinating'. Be honest and straightforward in a manner fitting Santa's character.
    '''
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
        "system_message": SystemMessage(content=SYSTEM_PROMPT),
    }
    message_history = RedisChatMessageHistory(url="redis://localhost:6379/0", ttl=600, session_id=session_id)
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True,
                                      chat_memory=message_history
                                      )
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
    )
    # agent.run(input="How many people live in canada?")
    return agent

