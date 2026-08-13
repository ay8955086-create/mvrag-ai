from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    UploadFile,
)

from sqlalchemy.orm import Session

from src.database.session import get_db
from src.schemas.video_response import VideoResponse
from src.services.video_service import VideoService


router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


@router.post(
    "/upload",
    response_model=VideoResponse,
    summary="Upload a video",
)
def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str | None = Form(None),
    db: Session = Depends(get_db),
):
    """
    Upload a video.

    The endpoint saves the video and immediately returns
    a Processing response while the AI pipeline continues
    in the background.
    """

    return VideoService.upload_video(
        db=db,
        file=file,
        title=title,
        description=description,
        background_tasks=background_tasks,
    )


@router.get(
    "",
    response_model=list[VideoResponse],
)
def list_videos(
    db: Session = Depends(get_db),
):
    """
    Return all uploaded videos.
    """

    return VideoService.get_all_videos(
        db
    )


@router.get(
    "/{video_id}",
    response_model=VideoResponse,
)
def get_video(
    video_id: int,
    db: Session = Depends(get_db),
):
    """
    Return one video.
    """

    return VideoService.get_video(
        db,
        video_id,
    )


@router.delete(
    "/{video_id}",
)
def delete_video(
    video_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a video.
    """

    return VideoService.delete_video(
        db,
        video_id,
    )