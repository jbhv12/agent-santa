import os
import httpx

from fastapi import Depends, APIRouter
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from langserve import add_routes
from dotenv import load_dotenv

from agent import get_agent
from constants import characters

# load_dotenv()

COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_REDIRECT_URI = os.getenv("COGNITO_REDIRECT_URI")
COGNITO_URL = f"https://{COGNITO_DOMAIN}"
ACCESS_TOKEN_URL = f"token"
COGNITO_AUTHORIZE_URL = f"{COGNITO_URL}/login?response_type=code&client_id={COGNITO_CLIENT_ID}&redirect_uri={COGNITO_REDIRECT_URI}"
SCOPES = {"email": "email", "openid": "openid"}

auth_code_flow = OAuthFlowsModel(
    authorizationCode={
        "tokenUrl": ACCESS_TOKEN_URL,
        "authorizationUrl": COGNITO_AUTHORIZE_URL,
        "scopes": SCOPES,
    }
)
oauth2_scheme = OAuth2(flows=auth_code_flow)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token.startswith('Bearer '):
        token = 'Bearer ' + token
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{COGNITO_URL}/oauth2/userinfo", headers={"Authorization": f"{token}"}
        )
        response.raise_for_status()
        user = response.json()
        return user

router = APIRouter(dependencies=[Depends(get_current_user)])
for character in characters:
    add_routes(router, get_agent("", character["name"]), disabled_endpoints=["playground"], path="/" + character["name"])
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using Langchain's Runnable interfaces",
)
app.include_router(router)


@app.post("/token")
async def get_token(request: Request):
    form_data = await request.form()
    code = form_data.get("code")
    token_url = f"{COGNITO_URL}/oauth2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": COGNITO_CLIENT_ID,
        "client_secret": COGNITO_CLIENT_SECRET,
        "code": code,
        "redirect_uri": COGNITO_REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication code")
    return {"access_token": response.json()['access_token'], "token_type": "bearer"}


@app.get("/")
def redirect():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
