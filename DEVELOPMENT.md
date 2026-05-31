### commands
- rm -rf .venv( rmdir /s .venv )
- python -m venv .venv
- source .venv/bin/activate( .venv\Scripts\activate )
- pyenv versions
- pyenv install --list
- pyenv local <PYTHON_VERSION>
- pip install -r requirements.txt
- uvicorn app.main:app --reload
- python -m app.main
- curl -o openapi.json http://127.0.0.1:7860/openapi.json

### git commands
- git remote -v
- git remote set-url <REPO_ALIAS> <URL>
- git push origin main && git push hf main
- git lfs install
- git lfs pull

### docker commands
- docker pull docker.io/byckg3/gad245-g1-api:latest
- docker rmi -f <IMAGE_ID>
- docker build . -t byckg3/gad245-g1-api
- docker run -it -p 7860:7860 --env-file .env byckg3/gad245-g1-api:latest

### test commands
- pytest -x tests/
- pytest -m <TAG_NAME>

### uv commands
- uv venv
- uv add <PACKAGE_NAME>
- uv remove <PACKAGE_NAME>
- uv run python -m app.main

### links
- [FastAPI Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Authlib: Python Authentication](https://docs.authlib.org/en/latest/index.html)
- [MongoDB Atlas](https://cloud.mongodb.com/)
- [Beanie Documentation](https://beanie-odm.dev/)
- [Gemini API quickstart](https://ai.google.dev/gemini-api/docs/quickstart)
- [Google AI Studio](https://aistudio.google.com/)
- [Chroma](https://docs.trychroma.com/docs/overview/introduction)
- [LangChain Tutorials](https://python.langchain.com/docs/tutorials/)
- [Docker Spaces](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [Pytest Documentation](https://docs.pytest.org/en/stable/how-to/index.html)
- [uv docs](https://docs.astral.sh/uv/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/index.html)