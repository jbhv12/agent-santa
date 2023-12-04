import os
from apikey import apikey
import streamlit as st
import chainlit as cl

from langchain import PromptTemplate, LLMChain
from langchain import ConversationChain
from langchain.llms import HuggingFaceHub, OpenAI
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.memory import ConversationBufferMemory

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable.config import RunnableConfig
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains import LLMMathChain
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.callbacks.base import BaseCallbackHandler
from langchain.agents import AgentType, initialize_agent, load_tools


os.environ['OPENAI_API_KEY'] = apikey
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'


class MyCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs) -> None:
        # print every token on a new line
        # print(f"#{token}#")
        pass


# class MyLangchainCallbackHandler(   ):
#     pass

@cl.on_chat_start
async def on_chat_start():
    
    # llm = ChatOpenAI(streaming=True, model_name="gpt-3.5-turbo", temperature=0)
    llm = OpenAI(
        streaming=True,
        callbacks=[
            FinalStreamingStdOutCallbackHandler(answer_prefix_tokens=["Final", " Answer", ":"])
        ],
        temperature=0,
    )
    # search = SerpAPIWrapper()
    llm_math_chain = LLMMathChain(llm=llm, verbose=True)

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

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # agent = initialize_agent(llm=llm_chain, tools=tools, verbose=True, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    # agent = initialize_agent(
    #     tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False, max_iterations=2,
    # )
    # agent.run(
    #     "It's 2023 now. How many years ago did Konrad Adenauer become Chancellor of Germany."
    # )
    agent = ZeroShotAgent(max_iterations=2, llm_chain=llm_chain, tools=tools, verbose=False, return_intermediate_steps=False)
    agent_chain = AgentExecutor.from_agent_and_tools(max_iterations=2, agent=agent, tools=tools, verbose=False, memory=memory)
    cl.user_session.set("agent", agent_chain)

    await cl.Message(content=f"ho ho ",).send()
    

@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(  #AsyncLangchainCallbackHandler
        stream_final_answer=True,
        # answer_prefix_tokens=["Final", " Answer"]
    )
    # cb2 = FinalStreamingStdOutCallbackHandler(answer_prefix_tokens=["Final", "Answer"])
    # stream = StreamingLastResponseCallbackHandler.from_agent_type(agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

    await cl.make_async(agent.run)(message.content, callbacks=[cb])
    # await cl.make_async(agent.run)(message.content)



# https://github.com/langchain-ai/langchain/issues/1358
# class NewAgentOutputParser(BaseOutputParser):
#     def get_format_instructions(self) -> str:
#         return FORMAT_INSTRUCTIONS

#     def parse(self, text: str) -> Any:
#         print("-" * 20)
#         cleaned_output = text.strip()
#         # Regex patterns to match action and action_input
#         action_pattern = r'"action":\s*"([^"]*)"'
#         action_input_pattern = r'"action_input":\s*"([^"]*)"'

#         # Extracting first action and action_input values
#         action = re.search(action_pattern, cleaned_output)
#         action_input = re.search(action_input_pattern, cleaned_output)

#         if action:
#             action_value = action.group(1)
#             print(f"First Action: {action_value}")
#         else:
#             print("Action not found")

#         if action_input:
#             action_input_value = action_input.group(1)
#             print(f"First Action Input: {action_input_value}")
#         else:
#             print("Action Input not found")

#         print("-" * 20)
#         if action_value and action_input_value:
#             return {"action": action_value, "action_input": action_input_value}

#         # Problematic code left just in case
#         if "```json" in cleaned_output:
#             _, cleaned_output = cleaned_output.split("```json")
#         if "```" in cleaned_output:
#             cleaned_output, _ = cleaned_output.split("```")
#         if cleaned_output.startswith("```json"):
#             cleaned_output = cleaned_output[len("```json"):]
#         if cleaned_output.startswith("```"):
#             cleaned_output = cleaned_output[len("```"):]
#         if cleaned_output.endswith("```"):
#             cleaned_output = cleaned_output[: -len("```")]
#         cleaned_output = cleaned_output.strip()
#         response = json.loads(cleaned_output)
#         return {"action": response["action"], "action_input": response["action_input"]}
#         # end of problematic code

# def make_chain():
#     memory = ConversationBufferMemory(
#         memory_key="chat_history", return_messages=True)

#     agent = ConversationalChatAgent.from_llm_and_tools(
#         llm=ChatOpenAI(), tools=[], system_message=SYSTEM_MESSAGE, memory=memory, verbose=True, output_parser=NewAgentOutputParser())

#     agent_chain = AgentExecutor.from_agent_and_tools(
#         agent=agent,
#         tools=tools,
#         memory=memory,
#         verbose=True,
#     )
#     return agent_chain







# @lebg1 I believe what you want to do is change the output key of the memory so that it uses the output only of the agent for the memory but still returns intermediate steps as well.
# Here is your modified code -

# memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True,output_key='output')

# prompt = CustomPromptTemplate(
# template=template,
# tools=tools,
# input_variables=["input", "intermediate_steps", memory_key],
# )

# agent = LLMSingleActionAgent(
# llm_chain=llm_chain,
# output_parser=output_parser,
# stop=["\nObservation:"],
# allowed_tools=tool_names,
# memory=memory,
# )

# agent_executor = AgentExecutor.from_agent_and_tools(
# agent=agent,
# tools=tools,
# verbose=True,
# handle_parsing_errors=True,
# return_intermediate_steps=True,
# )



## create new "Respond" tool????


## break on no tool

## max iterations




# really nice code base: https://github.com/aju22/DocumentGPT/blob/main/Conversation/conversation.py