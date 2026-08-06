from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("")
def analytics(
    db: Session = Depends(get_db),
):
    return AnalyticsService.get_dashboard(db)