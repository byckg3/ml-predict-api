## commands
- python -m venv .venv
- .venv/Scripts/activate(.venv\Scripts\activate)
- uvicorn app.main:app --reload
- python -m app.main
- curl -o openapi.json http://127.0.0.1:8000/openapi.json

## docker commands
- docker pull docker.io/byckg3/ml-predict-api:latest
- docker build . -t byckg3/ml-predict-api
- docker run -it -p 8000:8000 --env-file .env byckg3/ml-predict-api:latest

### test commands
- pytest -x tests/
- pytest -m <TAG_NAME>

### urls
- http://localhost:8000/docs
- [FastAPI Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Authlib: Python Authentication](https://docs.authlib.org/en/latest/index.html)
- [MongoDB Atlas](https://cloud.mongodb.com/)
- [Beanie Documentation](https://beanie-odm.dev/)
- [Gemini API quickstart](https://ai.google.dev/gemini-api/docs/quickstart)
- [Chroma](https://docs.trychroma.com/docs/overview/introduction)
- [LangChain Tutorials](https://python.langchain.com/docs/tutorials/)