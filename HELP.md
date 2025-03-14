## commands
- uvicorn app.main:app --reload
- python -m app.main
- pytest -x tests/
- docker build . -t byckg3/ml-predict-api
- docker run -it -p 8000:8000 byckg3/ml-predict-api:latest
- curl -o openapi.json http://127.0.0.1:8000/openapi.json

### urls
- http://localhost:8000/docs
- http://127.0.0.1:8000/openapi.json
- [MongoDB Atlas](https://cloud.mongodb.com/)
- [Beanie Documentation](https://beanie-odm.dev/)