FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev


FROM python:3.13-slim

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="src"

WORKDIR /app

RUN groupadd --system --gid 999 nonroot && \
    useradd --system --gid 999 --uid 999 --create-home nonroot && \
    mkdir -p /app/hf_models /app/chroma && \
    chown -R nonroot:nonroot /app

COPY --from=builder --chown=nonroot:nonroot /app/.venv /app/.venv
COPY --chown=nonroot:nonroot . .

USER nonroot

EXPOSE 7860
CMD  [ "python", "./scripts/startup.py" ]
