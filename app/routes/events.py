from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.events_types import EventCreate, EventResponse, OrganiserCreate, OrganiserResponse
from app.database import get_db
from app.services.events import create_event, create_organisation

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/create-organiser", response_model=OrganiserResponse)
def post_organiser(payload: OrganiserCreate, db: Session = Depends(get_db)):
    return create_organisation(
        db=db,
        name=payload.name,
        email=payload.email,
    )


@router.post("/", response_model=EventResponse)
def post_event(payload: EventCreate, db: Session = Depends(get_db)):
    return create_event(
        db=db,
        organiser_id=payload.organiser_id,
        name=payload.name,
        venue=payload.venue,
        ticket_types=payload.ticket_types,
    )
