# Langchain Services
This repository provides a set of services built using Langchain, designed to facilitate various tasks such as document processing, question answering with chat history, and more. The services are structured to be modular and easy to deploy, either locally or via Docker.
## 1. Setup

### 1.1. Donwload data

Require **wget** and **gdown** package

```bash
pip3 install wget gdown
cd data_source/generative_ai && python download.py
```
### 1.2. Prepare token
You need to set up your API keys for the services you want to use. Create a `get_tokens.py` file in `src/base/get_tokens.py` and add your API keys as environment variables. This file will be used to set the necessary tokens for the services. 
```python
import os

os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
os.environ["GOOGLE_API_KEY"] = "your_google_api_key"

```
You can either choose OpenAI or Google API, or both. Make sure to replace the placeholders with your actual API keys.
After creating the `get_tokens.py` file, change the model name in `src/chat/main.py` to the model you want to use. For example, if you want to use OpenAI's GPT-3.5 Turbo, set the model name as follows:
```python
llm = get_llm("gpt-3.5-turbo", temperature=0.3)
```
### 1.3. Install dependencies

```bash
pip3 install -r dev_requirements.txt
# Start the server
uvicorn src.app:app --host "0.0.0.0" --port 5000 --reload
```

Wait a minute for handling data and starting server.

### 1.4 Run service in docker

```bash
docker compose up -d
```

Turn off service

```bash
docker compose -f down
```
### 1.5 Streamlit
```bash
streamlit run src/streamlit_app.py
```
## 2. Process flow
The prompt processing flow contains four main steps:
1. Receive the raw prompt from the user.
2. Get keywords from the prompt by passing through an LLM.
3. Use the keywords to search for relevant documents in the vector database
4. Refine the prompt with the retrieved documents and return the final response.

## Technologies Used
- **Langchain**: For building the language model applications.
- **FastAPI**: For creating the web service.
- **Docker**: For containerization and deployment.
- **Streamlit**: For building interactive web applications.

## Future Work
- Implement more advanced document processing features.
- Enhance the user interface for better user experience.
- Add more services for different types of tasks.
- Cloud deployment options for scalability.
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
## Contributing
Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.
## Contact
For any questions or suggestions, feel free to open an issue or contact the maintainers.
## Acknowledgements
Thanks to the Langchain community for their contributions and support in building this project.
## References
- [Langchain Documentation](https://langchain.com/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
