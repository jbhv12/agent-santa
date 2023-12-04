FROM python:3.11.6-bookworm

WORKDIR /app

COPY requirements.txt openai-func.py /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["chainlit", "run", "./app.py", "--port", "8082"]
