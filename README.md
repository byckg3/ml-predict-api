---
title: Ml Predict Api
emoji: 🌖
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---
Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

## GAD245-group1
- [Hugging Face Spaces](https://huggingface.co/spaces/byckg3/ml-predict-api)

## API status
- Base API prefix: `/api`
- v1: `heart`, `liver`, `user`, `chat`
- v2 (in progress): `user` endpoints are currently implemented under `/api/v2/user`

## Development notes
- Local start command: `uvicorn app.main:app --reload`
- Default local URL: `http://127.0.0.1:7860`
- Additional commands and workflows: see `DEVELOPMENT.md`