import os

from langchain.agents import AgentExecutor
import chainlit as cl
from chainlit import config as clconfig
from typing import Optional
from agent import get_agent
from auth_utils import authenticate_user
from chainlit.client.cloud import ChainlitCloudClient

from chainlit.types import Pagination, ConversationFilter

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
    cl.user_session.set("agent", get_agent(app_user.username))

    # chainlit_client = ChainlitCloudClient(api_key=os.environ.get('CHAINLIT_API_KEY', ''))
    # pagination = Pagination(first=10)
    # filter = ConversationFilter()
    # conversations = await chainlit_client.get_conversations(pagination, filter)
    # for conversation in conversations.data:
    #     pass
    #     # print(conversation)
    #     # print(f"Conversation ID: {conversation['id']}")
    #     # print(f"Created At: {conversation['createdAt']}")

    # WELCOME_MSG="""Ho ho ho! Merry Christmas, my dear friend! I'm delighted to see you here. How can Santa Claus bring some holiday cheer to your day?""" # todo randomize
    # await cl.Message(content=WELCOME_MSG, ).send()
    res = await cl.AskUserMessage(content="What is your name?", timeout=10).send()

    # res = await cl.AskActionMessage(
    #     content="Pick an action!",
    #     actions=[
    #         cl.Action(name="continue", value="continue", label="✅ Continue"),
    #         cl.Action(name="cancel", value="cancel", label="❌ Cancel")
    #     ]
    # ).send()


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    res = await cl.make_async(agent)({"input": message.content},
                                     callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True)])
    await cl.Message(content=res['output']).send()


if __name__ == "__main__":
    get_agent("temp-session")

