import os
import random

import redis
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.tools.ddg_search import DuckDuckGoSearchRun
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.prompts import MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from constants import *


def get_agent(session_id, personality="Santa"):
    llm = ChatOpenAI(streaming=True, temperature=0, model="gpt-3.5-turbo-0613")
    search = DuckDuckGoSearchRun()
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted "
                        "questions",
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math",
        )
    ]
    system_prompt = DEFAULT_PROMPT
    for character in characters:
        if character["name"] == personality:
            system_prompt = character["prompt"]
    agent_kwargs = {
        "input": lambda x: x["input"],
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
        "system_message": SystemMessage(content=system_prompt),
    }

    try:
        redis_host = os.environ["REDIS_HOST"]
        redis_port = os.environ["REDIS_PORT"]
        redis_db = os.environ["REDIS_DB"]
        redis_ttl = int(os.environ.get("REDIS_TTL", 600))
        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        if not r.ping(): raise Exception()
        message_history = RedisChatMessageHistory(url=f"redis://{redis_host}:{redis_port}/{redis_db}", ttl=redis_ttl,
                                                  session_id=session_id)
        memory = ConversationBufferMemory(memory_key="memory", return_messages=True, chat_memory=message_history)
    except Exception as e: # fall back to in mem memory
        print(f"An error occurred: {e}")
        memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
    )


def get_welcome_message(character):
    for c in characters:
        if c["name"] == character:
            return random.choice(c.get("welcome_messages"))
    return "How can I help today?"
