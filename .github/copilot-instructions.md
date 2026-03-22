# Repository Overview for Copilot Agents

This project is a FastAPI backend with mounted Gradio apps, disease-risk prediction models, and Gemini-based chat/tool-calling. The architecture has evolved into versioned APIs and split data layers (document, relational, vector).

## Big Picture Architecture

1. **Application entrypoint**: `app/main.py`
   - Builds the FastAPI app with `app_lifespan`.
   - Initializes MongoDB (`app/db/document/database.py`), PostgreSQL engine/session (`app/db/relational/database.py`), and `DiseasePredictionService`.
   - Includes routers:
     - `/api` from `app/api/router.py`
     - `/auth` from `app/api/auth/router.py`
   - Mounts Gradio apps at `/bmi`, `/chatbot`, `/index`, `/signin` using `auth_for_gradio` where needed.
   - Adds CORS and `SessionMiddleware` using settings from `app/core/config.py`.

2. **API layer**: `app/api/*`
   - `app/api/router.py` defines global `/api` router with dependencies:
     - `verify_jwt`
     - `verify_csrf_token`
   - Versioned routers:
     - `app/api/v1/router.py` includes `heart`, `liver`, `user`, `chat` endpoints.
     - `app/api/v2/router.py` currently includes `user` endpoints.
   - Shared controller patterns in `app/api/v1/controller.py`:
     - `DocumentController`
     - `RecordController`
   - Dependency factories live in `app/api/dependencies/service.py`.

3. **Authentication**: `app/api/auth/*`
   - `google.py` handles Google OAuth login/callback and sets JWT/CSRF cookies.
   - `verifier.py` exposes token/cookie verification endpoints.
   - `dependencies/jwt_utils.py` and `dependencies/csrf_utils.py` provide JWT + CSRF utilities.

4. **Data layer**
   - **Document DB**: `app/db/document/database.py` (`MongoDB`) with Beanie models.
   - **Relational DB**: `app/db/relational/database.py` with async SQLAlchemy engine/session factory and `init_tables`.
   - **Vector DB**: `app/db/vector/database.py` (`ChromaDB`) for embedding collections and parquet data loading.

5. **ML prediction flow**
   - `app/services/disease.py` coordinates liver/heart predictors through `DiseasePredictorFactory`.
   - Models are downloaded via `app/repositories/models.py` (`HFModelRepository`).
   - Feature schemas and predictor interfaces are in `app/schemas/*`.

6. **LLM and chat flow**
   - `app/llm/gemini/services.py` contains `ChatService` with streaming output and tool-calling.
   - Tool declarations are in `app/llm/gemini/tools.py`.
   - Prompt/domain policy is in `app/llm/domain/prompts.py`.
   - Runtime websocket/session management is in `app/services/genai.py` (`ChatManager`).

7. **User domain split**
   - Relational `User` model: `app/user/models.py`
   - Service/repository abstractions: `app/user/services.py`, `app/user/repositories/*`
   - Beanie user profile schemas by version: `app/user/v1/schemas.py`, `app/user/v2/schemas.py`

## Developer Workflows

- **Local setup (Windows example)**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload
  # or
  python -m app.main
  ```

- **Database schema/init**
  - MongoDB models initialize during app startup (`MongoDB.init`).
  - Relational tables are created by `init_tables` on startup.
  - Manual relational init command:
    ```bash
    python -m app.db.relational.database
    ```

- **Tests**
  - Run all:
    ```bash
    pytest -x tests/
    ```
  - Run by marker:
    ```bash
    pytest -m db
    ```
  - `pytest.toml` uses strict markers and `-xvs` by default.

- **Docker and utility commands**
  - See `HELP.md` for Docker, git-lfs, and quick command references.

## Conventions and Patterns

- Prefer dependency-injection via `Depends(...)` with aliases (for example `ServiceDependency` pattern in endpoint modules).
- Keep API changes version-aware (`v1` vs `v2`) and place endpoint files under matching version folders.
- Reuse `DocumentController` and `RecordController` for standard CRUD/list patterns before introducing custom logic.
- Keep settings centralized in `app/core/config.py` via cached settings accessors (`mongo_settings`, `postgre_settings`, etc.).
- Prediction and chat services are initialized once and stored on `app.state`; follow that pattern for expensive services.
- Existing error handling favors `JSONResponse` with explicit status codes and logs via `print`/traceback.

## External Integrations

- MongoDB via Motor + Beanie
- PostgreSQL via SQLAlchemy asyncio + asyncpg
- ChromaDB for vector retrieval
- Google OAuth via Authlib
- Google Gemini API (`google-genai`) for chat + embeddings
- Hugging Face Hub for model artifact download

## Helpful Files to Inspect First

- `app/main.py`
- `app/core/config.py`
- `app/api/router.py`
- `app/api/v1/router.py`
- `app/api/v1/controller.py`
- `app/api/dependencies/service.py`
- `app/llm/gemini/services.py`
- `app/services/disease.py`

## Editing Guidance for Agents

- Keep edits consistent with current module layout (`app/api/auth`, `app/db/*`, `app/llm/*`, `app/user/*`).
- Avoid adding heavy new dependencies unless required and justified.
- If modifying schemas, services, or repository contracts, update tests under `tests/` in the same change set when possible.
- Prefer minimal, targeted changes that preserve existing API behavior and dependency wiring.