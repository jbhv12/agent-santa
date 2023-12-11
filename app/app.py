import os
from contextlib import asynccontextmanager
from typing import Optional, Dict

import chainlit as cl
from chainlit.client.base import ConversationDict
from langchain.agents import AgentExecutor
from chainlit.server import app

from agent import get_agent, get_welcome_message
from constants import characters


# Context manager to check for personally identifiable information (PII) in text
@asynccontextmanager
async def check_text(text: str):
    pii_results = False  # Placeholder for PII check implementation
    if pii_results:
        response = await cl.AskActionMessage(
            content="PII detected",
            actions=[
                cl.Action(name="continue", value="continue", label="✅ Continue"),
                cl.Action(name="cancel", value="cancel", label="❌ Cancel"),
            ],
        ).send()
        if response is None or response.get("value") == "cancel":
            raise InterruptedError
    yield


# OAuth callback function
if os.getenv("DISABLE_AUTH", "").lower() != "true":
    @cl.oauth_callback
    def oauth_callback(provider_id: str, token: str, raw_user_data: Dict[str, str],
                       default_app_user: cl.AppUser) -> Optional[cl.AppUser]:
        return default_app_user


# Function to rename chat authors
@cl.author_rename
def rename(orig_author: str):
    current_character = cl.user_session.get("chat_profile")
    rename_dict = {
        "AgentExecutor": "Agent",
        "ChatOpenAI": "LLM",
        "Red Jingles": "Santa🎅"
    }
    for character in characters:
        if current_character == character["name"]:
            rename_dict["Red Jingles"] = character["chat_name"]
    return rename_dict.get(orig_author, orig_author)


# Set chat profiles
@cl.set_chat_profiles
async def chat_profile():
    return [cl.ChatProfile(
                name=character["name"],
                markdown_description=character["description"],
                icon=character["icon"]
            ) for character in characters]


# Handler for chat start
@cl.on_chat_start
async def on_chat_start():
    app_user = cl.user_session.get("user")
    session_id = '' if app_user is None else f'{app_user.username}:{cl.user_session.get("id")}'
    character = cl.user_session.get("chat_profile")
    agent = get_agent(session_id, personality=character)
    cl.user_session.set("agent", agent)
    await cl.Message(content=get_welcome_message(character)).send()


# Main message handler
@cl.on_message
async def main(message: cl.Message):
    async with check_text(message.content):
        agent = cl.user_session.get("agent")  # type: AgentExecutor
        res = await cl.make_async(agent)({"input": message.content},
                                         callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True)])
        await cl.Message(content=res["output"]).send()


# Handler for resuming chat
@cl.on_chat_resume
async def on_chat_resume(conversation: ConversationDict):
    app_user = cl.user_session.get("user")
    session_id = f'{app_user.username}:{conversation["id"]}'
    agent = get_agent(session_id)
    cl.user_session.set("agent", agent)
    memory = agent.memory
    root_messages = [m for m in conversation["messages"] if m["parentId"] is None]
    for message in root_messages:
        if message["authorIsUser"]:
            memory.chat_memory.add_user_message(message["content"])
        else:
            memory.chat_memory.add_ai_message(message["content"])


# Endpoint for readiness check used by GAE
@app.get('/readiness_check')
def readiness_check():
    return {"status": "ready"}
