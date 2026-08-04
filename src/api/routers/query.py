from fastapi import APIRouter

from src.api.models.request import QueryRequest
from src.api.models.response import APIResponse
from src.services.query_service import QueryService

router = APIRouter(
    prefix="/query",
    tags=["Query"],
)

service = QueryService()


@router.post(
    "",
    response_model=APIResponse,
)
def query(
    request: QueryRequest,
):

    result = service.ask(
        request.question,
    )

    return APIResponse(
        success=True,
        message="Answer generated successfully.",
        data=result,
    )