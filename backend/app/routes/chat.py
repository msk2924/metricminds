from fastapi import APIRouter, Depends, HTTPException
from app.config import Settings, get_settings
from app.models import ChatRequest, ChatResponse, ChartPayload, TablePayload
from app.services.cube import CubeClient, CubeError
from app.services.llm import LLMService

router = APIRouter(prefix="/chat", tags=["chat"])


def build_chart(plan, rows):
    keys = list(rows[0].keys()) if rows else []
    dimension_keys = [key for key in keys if key not in plan.measures]
    x_key = dimension_keys[0] if dimension_keys else None
    series = [key for key in keys if key != x_key]
    return ChartPayload(type=plan.chart_type, title=plan.title, x_key=x_key, series=series, data=rows)


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, settings: Settings = Depends(get_settings)):
    llm = LLMService(settings)
    try:
        plan = llm.plan(payload.message)
        rows = CubeClient(settings).load(plan)
    except CubeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to process analysis request.") from exc
    columns = list(rows[0].keys()) if rows else []
    return ChatResponse(explanation=llm.explain(payload.message, plan, rows), chart=build_chart(plan, rows), table=TablePayload(columns=columns, rows=rows), query=plan)
