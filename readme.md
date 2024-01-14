# 🎀🔔 Red Jingles 🎀🔔

A state-of-the-art holiday theme based AI chatbot focusing on scalability, extensibility and real world applicability

## About

This project was made as a submission to [Serverless Holiday Hackathon 2023](https://hackathon.serverless.guru/).
The world has witnessed AI's potential thanks to platforms like OpenAI. It's crucial that AI isn't just limited to tech experts but accessible to everyone.
Red Jingles is our attempt to create a chatbot backed by LLM with a Christmas theme featuring Santa Claus, Snowman, and Elf.

## Table of Contents

- [Check the Hosted Version](#check-the-hosted-version)
- [Quickstart on Local Machine with Docker](#quickstart-on-local-machine-with-docker)
- [Running from Code](#running-from-code)

## Check the Hosted Version

Application is hosted [here](https://red-jingles-zo5w7qkf4a-ue.a.run.app)
API is hosted [here](https:///red-jingles.ue.r.appspot.com/docs)

## Quickstart on Local Machine with Docker

1. Ensure you have Docker installed on your machine. If not, follow the [official Docker installation guide](https://docs.docker.com/get-docker/).

2. Run the container:
    ```bash
    docker run -p 1225:8080 \
    -e CHAINLIT_URL=http://localhost:1225 \
    -e DISABLE_AUTH=true \
    -e OPENAI_API_KEY=<YOUR_OPENAI_API_KEY> \
    jbhv12/red-jingles:latest
    ```

3. Open your browser and go to [http://localhost:1225](http://localhost:1225) to view the app.

## Running from Code

If you prefer running the app directly from the source code, follow these steps:

1. Make sure you have python installed.

2. Clone the repository:

    ```bash
    git clone https://github.com/jbhv12-12/red-jingles.git
    ```

3. Navigate to the project directory:

    ```bash
    cd red-jingles/app
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the application:

    ```bash
    chainlit run ./app.py --port 1225 -w
    ```
6. Open your browser and go to [http://localhost:1225](http://localhost:1225) to view the app.

7. Run the API (optional)

   ```bash
   python api_server.py 
   ```
8. Open your browser and go to [http://localhost:8080](http://localhost:8080) to view the API documentation.

## Using hosted APIs

Application is hosted [here](https:///red-jingles.ue.r.appspot.com/docs)

1. Click on "Authorize" button on top right to authenticate yourself with your red-jingles credentials. 
2. Leave all input fields empty as is.
3. Enter your creds when prompted
4. Try out any API from UI. Notice a token passed in each request after authentication.

## Contributing

If you'd like to contribute to this project, please follow the [Contributing Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [Your License] - see the [LICENSE.md](LICENSE.md) file for details.

