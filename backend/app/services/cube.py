from typing import Any
import requests
from app.config import Settings
from app.models import QueryPlan


class CubeError(Exception):
    pass


class CubeClient:
    def __init__(self, settings: Settings):
        self.url = settings.cube_api_url.rstrip("/")
        self.token = settings.cube_api_token
        self.timeout = settings.request_timeout_seconds

    def load(self, plan: QueryPlan) -> list[dict[str, Any]]:
        if not self.url or not self.token:
            raise CubeError("Cube API is not configured. Set CUBE_API_URL and CUBE_API_TOKEN.")
        query = {
            "measures": plan.measures,
            "dimensions": plan.dimensions,
            "timeDimensions": plan.time_dimensions,
            "filters": plan.filters,
            "order": plan.order,
            "limit": plan.limit,
        }
        try:
            response = requests.post(
                f"{self.url}/load",
                json={"query": query},
                headers={"Authorization": self.token, "Content-Type": "application/json"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json().get("data", [])
        except requests.RequestException as exc:
            detail = exc.response.text if getattr(exc, "response", None) is not None else str(exc)
            raise CubeError(f"Cube query failed: {detail}") from exc
