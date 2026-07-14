from typing import Any, Literal
from pydantic import BaseModel, Field

ChartType = Literal["bar", "line", "area", "pie"]


class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=1000)


class QueryPlan(BaseModel):
    measures: list[str] = Field(default_factory=list)
    dimensions: list[str] = Field(default_factory=list)
    time_dimensions: list[dict[str, Any]] = Field(default_factory=list)
    filters: list[dict[str, Any]] = Field(default_factory=list)
    order: dict[str, str] = Field(default_factory=dict)
    limit: int = Field(default=100, ge=1, le=1000)
    chart_type: ChartType = "bar"
    title: str = "Analysis"


class ChartPayload(BaseModel):
    type: ChartType
    title: str
    x_key: str | None = None
    series: list[str] = Field(default_factory=list)
    data: list[dict[str, Any]] = Field(default_factory=list)


class TablePayload(BaseModel):
    columns: list[str]
    rows: list[dict[str, Any]]


class ChatResponse(BaseModel):
    explanation: str
    chart: ChartPayload
    table: TablePayload
    query: QueryPlan


class HealthResponse(BaseModel):
    status: Literal["ok"]
