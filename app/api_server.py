import httpx
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2AuthorizationCodeBearer
from dotenv import load_dotenv
from langserve import add_routes
from agent import get_agent
import os
from fastapi import FastAPI
from fastapi import HTTPException, status

load_dotenv()

COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_REDIRECT_URI = os.getenv("COGNITO_REDIRECT_URI")
AUTHORITY = f"https://{COGNITO_DOMAIN}"
print(COGNITO_REDIRECT_URI)
# OAuth2 Configuration
scopes = ["openid", "email"]
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"https://{COGNITO_DOMAIN}/login?response_type=code&client_id={COGNITO_CLIENT_ID}&redirect_uri={COGNITO_REDIRECT_URI}&scope=" + " ".join(
scopes),
    tokenUrl=f"/auth/callback",
    # tokenUrl=f"https://{COGNITO_DOMAIN}/oauth2/token",
    refreshUrl=f"https://{COGNITO_DOMAIN}/oauth2/token",
    scheme_name="cognito"
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print("in get cur use")
    pass

router = APIRouter(dependencies=[Depends(get_current_user)])
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using Langchain's Runnable interfaces",
    # openapi_oauth2_configs={
    #         "usePkceWithAuthorizationCodeGrant": True,
    #         "clientId": COGNITO_CLIENT_ID,
    #         "scopes": scopes,
    #         "authorizationUrl": f"https://{COGNITO_DOMAIN}/login",
    #         # "tokenUrl": f"https://{COGNITO_DOMAIN}/oauth2/token",
    #         "tokenUrl": "/auth/callback"
    #     }
)

add_routes(router, get_agent("", "Santa"), disabled_endpoints=["playground"], path="/openai")
app.include_router(router)

@app.get("/auth/callback")
async def auth_callback(code: str):
    # Exchange code for a token
    token_url = f"https://{COGNITO_DOMAIN}/oauth2/token"
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

    # Process the token (store it, use it for user session, etc.)
    token_data = response.json()
    # ...
    access_token = "test"
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)
