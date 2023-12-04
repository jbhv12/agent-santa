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

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable.config import RunnableConfig
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chains.conversation.memory import ConversationEntityMemory
from chainlit.chat_settings import ChatSettings
from chainlit import config as clconfig
from chainlit.input_widget import Select, Switch, Slider

os.environ['OPENAI_API_KEY'] = apikey
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

@cl.author_rename
def rename(orig_author: str):
    rename_dict = {"LLMMathChain": "Albert Einstein", "Chatbot": "Santa"}
    return rename_dict.get(orig_author, orig_author)

# @cl.on_settings_update
# async def setup_agent(settings):
#     print("on_settings_update", settings)
#     clconfig.ui.hide_cot = settings["hide_cot"]
#     ## not working!!!


@cl.on_chat_start
async def on_chat_start():

    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI - Model",
                values=["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"],
                initial_index=0,
            ),
            Switch(id="Streaming", label="OpenAI - Stream Tokens", initial=True),
            Slider(
                id="Temperature",
                label="OpenAI - Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
            Switch(id="hide_cot", label="Hide Chain of Thought", initial=True),
        ]
    ).send()
    clconfig.ui.hide_cot = False
    prompt = PromptTemplate.from_template("""You are santa clause. never break out of your charecter.
        You are designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, you are able to generate human-like text based on the input you receive, allowing you to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

        You are constantly learning and improving, and your capabilities are constantly evolving. You are able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. You have access to some personalized information provided by the human in the Context section below. Additionally, you are able to generate your own text based on the input you receive, allowing you to engage in discussions and provide explanations and descriptions on a wide range of topics.

        Overall, you are a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether the human needs help with a specific question or just wants to have a conversation about a particular topic, you are here to assist.

        Context:
        {entities}

        Current conversation:
        {history}
        Last line:
        Human: {input}
        You:"""
    )
    llm = ChatOpenAI(streaming=True, model_name="gpt-3.5-turbo")
    conversation = ConversationChain(
        llm=llm, 
        verbose=True,
        prompt=prompt,#ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=ConversationEntityMemory(llm=llm)
    )
    cl.user_session.set("runnable", conversation)



@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("runnable")
    res = await chain.acall(message.content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True)])
    await cl.Message(content=res['response']).send()
