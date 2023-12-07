import boto3
from botocore.exceptions import ClientError
import os

def authenticate_user(email, password):
    client = boto3.client('cognito-idp', region_name='us-west-2') # todo from env
    user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')
    client_id = os.environ.get('COGNITO_CLIENT_ID')
    try:
        response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        if response.get("AuthenticationResult"):
            return True
        else:
            return False
    except ClientError as e:
        print(f"Authentication failed: {e}")
        return False


import requests
import os


def get_user_details(auth_code):
    # Cognito details
    client_id = os.getenv('COGNITO_CLIENT_ID')
    client_secret = os.getenv('COGNITO_CLIENT_SECRET')
    redirect_uri = os.getenv('COGNITO_REDIRECT_URI')
    cognito_domain = os.getenv('COGNITO_DOMAIN')

    # Endpoint for exchanging the code
    token_endpoint = f"https://{cognito_domain}/oauth2/token"

    # Headers and payload for the token request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'code': auth_code,
        'redirect_uri': redirect_uri
    }

    # Basic Authentication
    if client_secret is not None:
        from requests.auth import HTTPBasicAuth
        auth = HTTPBasicAuth(client_id, client_secret)
    else:
        auth = None

    # Exchange code for token
    response = requests.post(token_endpoint, headers=headers, data=payload, auth=auth)
    if response.status_code != 200:
        return {"error": "Failed to exchange code for token"}

    tokens = response.json()
    access_token = tokens.get('access_token')
    print(f"access token ... {access_token}")
    # Get user info
    userinfo_endpoint = f"https://{cognito_domain}/oauth2/userInfo"
    user_info_response = requests.get(userinfo_endpoint, headers={'Authorization': f'Bearer {access_token}'})

    if user_info_response.status_code != 200:
        return {"error": "Failed to retrieve user information"}

    return user_info_response.json()


# Example usage
# auth_code = "<YOUR_AUTH_CODE>"
# user_details = get_user_details(auth_code)
# print(user_details)


if __name__ == '__main__':
    get_user_details('caae8422-cdc4-4b1e-8a6a-a638bb90d1ee')
    # Example usage
    # email = 'jbhv12@gmail.com'
    # password = 'dummy'
    # is_authenticated = authenticate_user(email, password)
    # print(authenticate_user(email, password))
