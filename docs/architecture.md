# MetricMind architecture

## Request path

1. The browser submits a natural-language request to `POST /api/chat`.
2. `LLMService` converts it to a `QueryPlan` constrained by `SEMANTIC_CATALOG`.
3. `CubeClient` sends the plan to Cube's `/load` endpoint with the server-side token.
4. The API normalizes Cube rows into a typed chart payload and table, then asks the model for a factual explanation of those returned rows.
5. React Query receives the response; Recharts selects the requested visual type.

## Security boundary

- Browser: no Cube, Snowflake, or OpenAI secret.
- API: owns credentials, Cube transport, request limits, and semantic allow-list.
- Cube: remains the authorization and data-governance boundary for underlying warehouse access.

## Data contracts

`QueryPlan` contains only Cube REST query fields: measures, dimensions, time dimensions, filters, order, and limit. `ChartPayload` is intentionally renderer-focused: type, title, x-axis key, series keys, and data rows. This keeps UI components independent of Cube-specific response formats.
