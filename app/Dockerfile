FROM python:3.11.6-slim

WORKDIR /app

# First, copy only the requirements.txt and install dependencies
COPY requirements-frozen.txt .
RUN pip install --no-cache-dir -r requirements-frozen.txt

# Then copy the rest of your application files
COPY . /app/
COPY .chainlit /app/.chainlit

EXPOSE 1225

CMD ["chainlit", "run", "./main.py", "--port", "1225"]
