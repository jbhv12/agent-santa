#FROM python:3.11.6-bookworm
#
#WORKDIR /app
#
#COPY . /app/
#COPY .chainlit /app/.chainlit
#
#RUN pip install --no-cache-dir -r requirements.txt
#
#EXPOSE 8082
#
#CMD ["chainlit", "run", "./main.py", "--port", "8082"]


FROM python:3.11.6-bookworm

WORKDIR /app

# First, copy only the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the rest of your application files
COPY . /app/
COPY .chainlit /app/.chainlit

EXPOSE 1225

CMD ["chainlit", "run", "./main.py", "--port", "1225"]
