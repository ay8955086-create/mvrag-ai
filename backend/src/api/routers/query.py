from fastapi import APIRouter

from src.api.models.request import QueryRequest
from src.api.models.response import APIResponse
from src.services.query_service import QueryService

router = APIRouter(
    prefix="/query",
    tags=["Query"],
)


@router.post(
    "",
    response_model=APIResponse,
)
def query(request: QueryRequest):
    service = QueryService()

    result = service.ask(
        question=request.question,
        video_id=request.video_id,
    )

    return APIResponse(
        success=True,
        message="Answer generated successfully.",
        data=result,
    )