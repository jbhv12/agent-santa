from apikey import apikey
import os

from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor

import chainlit as cl
from chainlit import config as clconfig

from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
)
from langchain.tools import DuckDuckGoSearchRun
from typing import Optional

os.environ['OPENAI_API_KEY'] = apikey
os.environ['CHAINLIT_AUTH_SECRET'] = ',-MXH0^a5Wtwd-ivxmVn>4>e,J*40l+I:07el7+vcqL,TdyrQe>?E?O.WRk/raAn'


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
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
    )
    agent_executor = None
    return agent, agent_executor


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.AppUser]:
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.AppUser(username="admin", role="ADMIN", provider="credentials")
    else:
        return None


@cl.on_chat_start
async def on_chat_start():
    agent, agent_executor = get_agent()
    cl.user_session.set("agent", agent)
    await cl.Message(content=f"ho ho ", ).send() # todo
    clconfig.features.prompt_playground = False


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    res = await cl.make_async(agent)({"input": message.content},
                                     callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True)])
    await cl.Message(content=res['output']).send()


if __name__ == "__main__":
    # get_agent()
    search = DuckDuckGoSearchRun()
    search.run("Obama's first name?")
