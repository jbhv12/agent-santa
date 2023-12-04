from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import OpenAI, LLMChain
from langchain.utilities import GoogleSearchAPIWrapper
from langchain import OpenAI, LLMMathChain, SerpAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from apikey import apikey
from langchain.agents import AgentType



import os
os.environ["OPENAI_API_KEY"] = apikey
os.environ["SERPAPI_API_KEY"] = "..."

llm = ChatOpenAI(temperature=0)
llm1 = OpenAI(temperature=0)
# search = SerpAPIWrapper()
llm_math_chain = LLMMathChain(llm=llm1, verbose=True)

tools = [
    # Tool(
    #     name="Search",
    #     func=search.run,
    #     description="useful for when you need to answer questions about current events. "
    #                 "You should ask targeted questions"
    # )
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
    )
]

prefix = """You are a helpful and very powerful assistant assuming personality of santa claus, never break out of charecter. use tools only if and when you need them. you are chatting with user."""
suffix = """
{chat_history}
User: {input}
"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"]
)
memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)

# agent = initialize_agent(llm=llm_chain, tools=tools, verbose=True, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)


agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)

agent_chain.run(input="who are you?")



# https://github.com/langchain-ai/langchain/issues/2134