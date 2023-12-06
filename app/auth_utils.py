import boto3
from botocore.exceptions import ClientError
import os


def authenticate_user(email, password):
    client = boto3.client('cognito-idp', region_name='us-west-2') # todo from env
    user_pool_id = os.environ.get('AWS_COGNITO_USER_POOL_ID')
    client_id = os.environ.get('AWS_COGNITO_CLIENT_ID')
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

        print(response)
        if response.get("AuthenticationResult"):
            return True
        else:
            return False
    except ClientError as e:
        # You can log the error or handle it according to your needs
        print(f"Authentication failed: {e}")
        return False


if __name__ == '__main__':
    # Example usage

    email = 'jbhv12@gmail.com'  # Replace with the user's email
    password = 'Password@123'  # Replace with the user's password

    is_authenticated = authenticate_user(email, password)
    print(is_authenticated)
