"""
API request models.
"""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=2,
        max_length=500,
        examples=["Explain explicit typecasting."],
    )

    video_id: int | None = Field(
        default=None,
        ge=1,
        description="Optional video scope. When supplied, retrieval is limited to this video.",
    )
