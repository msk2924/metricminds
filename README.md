# MetricMind

MetricMind is an enterprise BI application that keeps Cube Cloud behind a governed, AI-powered FastAPI service. Users ask questions in the Next.js workspace; the server produces a constrained Cube query, retrieves semantic-layer data, and returns a narrative, chart configuration, and tabular result.

## Architecture

```text
Browser (Next.js + React Query + Recharts)
  -> FastAPI /api/chat
    -> OpenAI (structured Cube query plan)
    -> Cube Cloud REST /load
      -> Snowflake + dbt marts
```

Cube tokens and OpenAI keys only exist in the API environment. The browser receives no warehouse or semantic-layer credentials.

## Project layout

```text
metricmind/
├── frontend/                 # Next.js 15 app and enterprise UI
├── backend/app/
│   ├── routes/chat.py        # POST /api/chat
│   ├── services/cube.py      # Cube REST client
│   ├── services/llm.py       # Structured query planning + insights
│   ├── config.py             # Settings and CORS
│   └── models.py             # Pydantic contracts
├── docker-compose.yml
└── .env.example
```

## Configure

1. Copy `.env.example` to `.env`.
2. Set `OPENAI_API_KEY`, `CUBE_API_URL`, and `CUBE_API_TOKEN`.
3. Update `SEMANTIC_CATALOG` in `backend/app/services/llm.py` with the exact members from your Cube schema. This is the allow-list that prevents arbitrary member selection.

`CUBE_API_URL` should be the Cube REST base path, for example `https://<deployment>.cubecloudapp.dev/cubejs-api/v1`.

## Run locally

Backend (Python 3.12):

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend (Node 22):

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). API documentation is at [http://localhost:8000/docs](http://localhost:8000/docs).

## Docker

```bash
docker compose up --build
```

## API contract

`POST /api/chat`

```json
{ "message": "Show revenue by country" }
```

The result includes `explanation`, a typed `chart` payload (`bar`, `line`, `area`, or `pie`), a `table`, and the governed query plan. The frontend renders the result and provides CSV export.

## Production next steps

- Replace the login placeholder with your OIDC/SAML provider and enforce tenant claims in FastAPI.
- Replace the sample dashboard values with saved Cube queries through a dedicated dashboard endpoint.
- Add query audit records, rate limits, a Redis cache, observability, and role-based Cube security context.
- Treat `SEMANTIC_CATALOG` as versioned product configuration, tested against Cube metadata in CI.
