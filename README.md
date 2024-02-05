# `pg_vector` playing

Repo for playing around with `pg_vector`.

## Dev Notes

- [x] Testing out usage of `vecs` with basic embedder
- [ ] Testing hooking this up to https://github.com/vllm-project/vllm

## Deploy

```bash
docker compose up -d
```

## Data and ingestion

Data is generated using ChatGPT.

Ingest data like this:

```bash
curl -X 'PUT' \
  'http://localhost:8000/sentence' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @data/sent.json
```

## Searching the DB

Search like this

```bash
curl -X 'POST' \
  'http://localhost:8000/search' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"text": "mri shows a hernia", "num": 3 }'
```
