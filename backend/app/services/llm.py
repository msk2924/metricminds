import json
from openai import OpenAI
from app.config import Settings
from app.models import QueryPlan

SEMANTIC_CATALOG = """
Available Cube members (adapt this catalog to your Cube schema):
- Revenue: measures Revenue.amount, Revenue.profit, Revenue.orderCount; dimensions Revenue.country, Revenue.product, Revenue.customerName; time dimension Revenue.createdAt.
- Customers: measures Customers.count; dimensions Customers.country, Customers.segment.
- Inventory: measures Inventory.stockOnHand; dimensions Inventory.productName, Inventory.category.
Only use members from this catalog. Return a single JSON object matching the requested schema.
"""


class LLMService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def plan(self, question: str) -> QueryPlan:
        if not self.client:
            return self._fallback_plan(question)
        response = self.client.chat.completions.create(
            model=self.settings.openai_model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You translate business questions into safe Cube queries. " + SEMANTIC_CATALOG},
                {"role": "user", "content": question},
            ],
            temperature=0,
        )
        return QueryPlan.model_validate_json(response.choices[0].message.content or "{}")

    def explain(self, question: str, plan: QueryPlan, rows: list[dict]) -> str:
        if not rows:
            return "No records matched that request. Try broadening the date range or changing filters."
        if not self.client:
            return f"Showing {plan.title.lower()} across {len(rows)} result{'s' if len(rows) != 1 else ''}."
        prompt = {"question": question, "query": plan.model_dump(), "rows": rows[:20]}
        response = self.client.chat.completions.create(
            model=self.settings.openai_model,
            messages=[{"role": "system", "content": "Give a concise, factual business insight in 2 sentences. Do not invent values."}, {"role": "user", "content": json.dumps(prompt)}],
            temperature=0.2,
        )
        return response.choices[0].message.content or "Your analysis is ready."

    def _fallback_plan(self, question: str) -> QueryPlan:
        q = question.lower()
        if "country" in q:
            return QueryPlan(measures=["Revenue.amount"], dimensions=["Revenue.country"], order={"Revenue.amount": "desc"}, chart_type="bar", title="Revenue by Country")
        if "trend" in q or "month" in q:
            return QueryPlan(measures=["Revenue.amount"], time_dimensions=[{"dimension": "Revenue.createdAt", "granularity": "month"}], chart_type="area", title="Revenue Trend")
        return QueryPlan(measures=["Revenue.amount"], chart_type="bar", title="Revenue")
