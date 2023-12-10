FROM python:3.11.6-slim
RUN apt-get update && apt-get install ca-certificates

WORKDIR /app

# First, copy only the requirements.txt and install dependencies, to cache them in subsequent builds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the rest of your application files
COPY . /app/
COPY .chainlit /app/.chainlit

# Patch chainlit library to support cognito auth
COPY patches/oauth_providers.py /usr/local/lib/python3.11/site-packages/chainlit/
COPY patches/base.py /usr/local/lib/python3.11/site-packages/chainlit/client/

EXPOSE 8080

CMD ["chainlit", "run", "./app.py", "--port", "8080"]