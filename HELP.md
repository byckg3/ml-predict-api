## commands
- .venv/Scripts/activate
- uvicorn app.main:app --reload
- python -m app.main
- docker build . -t byckg3/ml-predict-api
- docker run -it -p 8000:8000 --env-file .env byckg3/ml-predict-api:latest
- curl -o openapi.json http://127.0.0.1:8000/openapi.json

### test commands
- pytest -x tests/
- pytest -m <TAG_NAME>

### urls
- http://localhost:8000/docs
- http://127.0.0.1:8000/openapi.json
- [FastAPI Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/)
- [MongoDB Atlas](https://cloud.mongodb.com/)
- [Beanie Documentation](https://beanie-odm.dev/)
- [Gemini API quickstart](https://ai.google.dev/gemini-api/docs/quickstart)