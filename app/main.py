import os

from chainlit.client.base import ConversationDict
from langchain.agents import AgentExecutor
import chainlit as cl
from chainlit import config as clconfig
from typing import Optional
from agent import get_agent
from auth_utils import authenticate_user
from welcome_msg_helper import get_santa_welcome_msg
@cl.author_rename
def rename(orig_author: str):
    rename_dict = {"LLMMathChain": "Albert Einstein", "Chatbot": "Santa🎅", "Red Jingles": "Santa🎅"}
    ## AgentExecutor  ChatOpenAI
    return rename_dict.get(orig_author, orig_author)


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.AppUser]:
    if username == os.environ.get("CHAINLIT_ADMIN_USERNAME") and password == os.environ.get("CHAINLIT_ADMIN_PASSWORD"):
        return cl.AppUser(username=username, role="ADMIN", provider="credentials")
    if username == 'guest' and password == 'guest':
        return cl.AppUser(username=username, role="USER", provider="credentials")
    if username == 'guest2' and password == 'guest2':
        return cl.AppUser(username=username, role="USER", provider="credentials")
    elif authenticate_user(username, password):
        return cl.AppUser(username=username, role="USER", provider="credentials")
    else:
        return None


@cl.on_chat_start
async def on_chat_start():
    clconfig.features.prompt_playground = False
    app_user = cl.user_session.get("user")
    cl.user_session.set("agent", get_agent(f"{app_user.username}:{cl.user_session.get('id')}"))
    await cl.Message(content=get_santa_welcome_msg(), ).send()


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    print(agent)
    res = await cl.make_async(agent)({"input": message.content},
                                     callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True)])
    await cl.Message(content=res['output']).send()


@cl.on_chat_resume
async def on_chat_resume(conversation: ConversationDict):
    app_user = cl.user_session.get("user")
    agent = get_agent(f"{app_user.username}:{conversation['id']}")
    cl.user_session.set("agent", agent)

    memory = agent.memory
    root_messages = [m for m in conversation["messages"] if m["parentId"] == None]
    for message in root_messages:
        if message["authorIsUser"]:
            memory.chat_memory.add_user_message(message["content"])
        else:
            memory.chat_memory.add_ai_message(message["content"])


if __name__ == "__main__":
    a = get_agent("temp-session")
    a.agent.dict()


