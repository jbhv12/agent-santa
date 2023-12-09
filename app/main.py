import os
from contextlib import asynccontextmanager

from chainlit.client.base import ConversationDict
from langchain.agents import AgentExecutor
import chainlit as cl
from typing import Optional, Dict

from presidio_analyzer import AnalyzerEngine

from agent import get_agent, get_welcome_message
from constants import characters
from chainlit import config as clconfig

# analyzer = AnalyzerEngine()
# @asynccontextmanager
# async def check_text(text: str):
#     pii_results = analyzer.analyze(text=text, language="en")
#     if pii_results:
#         response = await cl.AskActionMessage(
#             content="PII detected",
#             actions=[
#                 cl.Action(name="continue", value="continue", label="✅ Continue"),
#                 cl.Action(name="cancel", value="cancel", label="❌ Cancel"),
#             ],
#         ).send()
#         if response is None or response.get("value") == "cancel":
#             raise InterruptedError
#     yield


if os.getenv("DISABLE_AUTH", "").lower() != "true":
    @cl.oauth_callback
    def oauth_callback(
            provider_id: str,
            token: str,
            raw_user_data: Dict[str, str],
            default_app_user: cl.AppUser,
    ) -> Optional[cl.AppUser]:
        return default_app_user


@cl.author_rename
def rename(orig_author: str):
    current_character = cl.user_session.get("chat_profile")
    rename_dict = {"AgentExecutor": "Albert Einstein", "ChatOpenAI": "ChatOpenAI", "Red Jingles": "Santa🎅"}
    for character in characters:
        if current_character == character["name"]: rename_dict["Red Jingles"] = character["chat_name"]
    return rename_dict.get(orig_author, orig_author)


@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name=character["name"],
            markdown_description=character["description"],
            icon=character["icon"]
        ) for character in characters
    ]


@cl.on_chat_start
async def on_chat_start():
    clconfig.features.prompt_playground = False
    app_user = cl.user_session.get("user")
    session_id = f'{app_user.username}:{cl.user_session.get("id")}'
    character = cl.user_session.get("chat_profile")
    agent = get_agent(session_id, personality=character)
    cl.user_session.set("agent", agent)
    await cl.Message(content=get_welcome_message(character)).send()


@cl.on_message
async def main(message: cl.Message):
    # async with check_text(message.content):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    res = await cl.make_async(agent)({"input": message.content},
                                     callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True)])
    await cl.Message(content=res["output"]).send()


@cl.on_chat_resume
async def on_chat_resume(conversation: ConversationDict):
    app_user = cl.user_session.get("user")
    agent = get_agent(f'{app_user.username}:{conversation["id"]}')
    cl.user_session.set("agent", agent)

    memory = agent.memory
    root_messages = [m for m in conversation["messages"] if m["parentId"] == None]
    for message in root_messages:
        if message["authorIsUser"]:
            memory.chat_memory.add_user_message(message["content"])
        else:
            memory.chat_memory.add_ai_message(message["content"])


if __name__ == "__main__":
    pass
