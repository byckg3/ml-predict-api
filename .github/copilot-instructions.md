# Repository overview for Copilot agents

This project is a FastAPI-based backend with embedded Gradio apps and ML prediction logic. The codebase is small but has multiple moving parts; new agents should scan the following modules to understand the architecture.

## Big picture architecture

1. **Entry point**: `app/main.py` creates the FastAPI app with an `app_lifespan` context manager.  
   - Initializes `MongoDB` (Beanie ODM) and a `DiseasePredictionService`.  
   - Mounted Gradio applications under `/bmi`, `/chatbot`, `/index` and `/signin`.  
   - Adds CORS and session middleware configured via `app/core/config.py` settings.

2. **API layer**: `app/api/router.py` defines a global `/api` router protected by CSRF and JWT dependencies.  
   - Sub-routers for heart, liver, user and chat domains (e.g. `app/api/heart.py`).  
   - Controllers (`DocumentController`, `RecordController`) implement common CRUD patterns.

3. **Authentication**: `app/auth` handles Google OAuth and token management.  
   - `auth/google.py` manages login/callback, sets JWT & CSRF cookies.  
   - `auth/dependencies` contains utility functions for JWT creation/verification and CSRF token matching.  
   - `auth/verifier.py` exposes endpoints for validating tokens (see file for details).

4. **Data layer**: `app/core/db.py` wraps MongoDB (Beanie) and a ChromaDB client.  
   - Documents/models defined in `app/schemas` (`HeartDiseaseRecord`, `LiverDiseaseRecord`, `UserProfile`).  
   - Schema classes include examples for OpenAPI and helper methods (`to_df` for features).  
   - `app/services/nosql.py` provides generic `RecordService` used by API dependencies.

5. **ML logic**:  
   - `app/services/disease.py` loads models from Hugging Face via `HFModelRepository` and wraps `DiseasePredictorFactory`.  
   - Features and predictors live under `app/schemas` with `SKLearnPredictor` base.  
   - `predict` endpoints in heart/liver router call into `DiseasePredictionService`.

6. **GenAI/chat**:  
   - `app/services/genai.py` implements `GeminiService` around Google Gemini API with tool-calling, streaming, and embeddings.  
   - A `ChatManager` handles websocket sessions.  
   - Domain-specific prompt templates live in `app/schemas/prompt.py`.

7. **Repositories**:  
   - `app/repositories/models.py` describes Hugging Face model download logic.  
   - `app/repositories/embed.py` wraps Chroma loading/search.  
   - `app/repositories/nosql.py` may contain other data access patterns.

8. **Frontend utilities**: Gradio pages defined under `app/web` (e.g. `chatbot.py`, `bmi.py`). They are mounted to the main app.

## Developer workflows

- **Local development**:
  ```bash
  python -m venv .venv
  .venv\Scripts\activate      # Windows
  pip install -r requirements.txt
  uvicorn app.main:app --reload
  # or `python -m app.main` defaults to port 7860
  ```
- **Tests**:
  - Run all: `pytest -x tests/`  
  - Use markers: `pytest -m db` to run database tests.  
  - Fixtures often set `MongoDB.DB_NAME` to `test` and call `init_beanie`.
- **Docker**: image `byckg3/ml-predict-api` built via Dockerfile.
  - Example commands in `HELP.md`.
- **Git**: uses Git LFS for model files; push to both origin and HF via `git push origin main && git push hf main`.

> The `HELP.md` file contains useful commands for env setup, docker, and URLs.

## Conventions & patterns

- **Pydantic models** include `json_schema_extra` with examples for API documentation.
- **Service dependency injection**: routes often annotate `ServiceDependency` as `Annotated[ Type, Depends(factory)]`.
- **Controllers reuse**: `DocumentController` and `RecordController` implement generic CRUD logic, imported in routers.
- **Error handling**: prediction endpoints catch exceptions and return `JSONResponse` with 400. Most exceptions are printed for debugging.
- **JWT/CSRF**: authentication checks look in either header or cookie; Gradio uses `auth_for_gradio` to allow login via mounted apps.
- **Gradio integration**: `gr.mount_gradio_app` wraps FastAPI endpoints; careful about authentication dependencies.
- **Naming**: modules named after domain (heart, liver, user); services under `app/services`, repositories under `app/repositories`, schemas under `app/schemas`.
- **LLM/tooling**: function declarations for Gemini are defined in schemas and used to dynamically build prompts/configs.

## External integrations

- **MongoDB** (via Motor / Beanie) storing records and user profiles.
- **ChromaDB** for embeddings and retrieval; initialized from parquet data in `data/`.
- **Google OAuth** via Authlib, including metadata discovery.
- **Hugging Face** model hub downloads using `HFModelRepository` and `hf_settings`.
- **Google Gemini** LLM and embeddings through custom client wrappers.

## Helpful files to open

- `app/core/config.py` for settings and environment variable mapping.
- `app/services/genai.py` to understand chat/streaming logic.
- `app/schemas/` for data validation rules and example payloads.
- `app/api/*` routers for endpoint patterns and dependencies.

> Any modifications to models or schemas should update tests in `tests/` accordingly; the project uses `pytest-asyncio`.

---

### Editing guidelines for Copilot agents

- Make changes consistent with existing dependency-injection and Pydantic patterns.
- When adding a new API route, follow the pattern in `heart.py` and include example payloads if necessary.
- Keep CI tests passing; the repository currently doesn't include a CI config but uses `pytest` command as shown.
- Avoid adding heavy external dependencies unless genuinely required; lean on existing services and repositories.

Feel free to ask if anything is unclear or if you need more details about a particular subsystem. Feedback welcome!