from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VideoResponse(BaseModel):
    id: int

    filename: str
    title: str
    description: str | None

    duration: float
    fps: float
    width: int
    height: int
    size_mb: float

    status: str
    upload_time: datetime

    model_config = ConfigDict(from_attributes=True)