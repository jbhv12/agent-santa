from langchain.agents import AgentExecutor
import chainlit as cl
from chainlit import config as clconfig
from typing import Optional
from agent import get_agent
from auth_utils import authenticate_user


@cl.author_rename
def rename(orig_author: str):
    rename_dict = {"LLMMathChain": "Albert Einstein", "Chatbot": "Santa"}
    return rename_dict.get(orig_author, orig_author)


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.AppUser]:
    if username == 'guest' and password == 'guest':
        return cl.AppUser(username=username, role="USER", provider="credentials")
    elif authenticate_user(username, password):
        return cl.AppUser(username=username, role="USER", provider="credentials")
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
    # for debug
    get_agent()
    # search = DuckDuckGoSearchRun()
    # search.run("Obama's first name?")
