from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.events_types import EventCreate, EventResponse, OrganiserCreate, OrganiserResponse, EventUpdate, TicketTypesResponse
from app.database import get_db
from app.services.events_service import create_event, get_event, get_event_ticket_types, get_events, update_event, create_organisation

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/create-organiser", response_model=OrganiserResponse)
def post_organiser(payload: OrganiserCreate, db: Session = Depends(get_db)):
    return create_organisation(
        db=db,
        name=payload.name,
        email=payload.email,
    )

@router.patch("/{event_id}", response_model=EventResponse)
def patch_event(
    event_id: UUID,
    payload: EventUpdate, 
    db: Session = Depends(get_db)
):
    return update_event(
        db=db,
        event_id=event_id,
        update_data=payload
    )

@router.get("/{event_id}", response_model=EventResponse)
def fetch_event(
    event_id:UUID,
    db: Session = Depends(get_db)
): return get_event(
    db=db,
    event_id=event_id
)

@router.get("/{event_id}/ticket-types", response_model=TicketTypesResponse)
def fetch_ticket_types(
    event_id:UUID,
    db: Session=Depends(get_db)):
        return get_event_ticket_types(
            db=db, event_id=event_id
        )


@router.get("/", response_model=list[EventResponse])
def fetch_events(db: Session=Depends(get_db)):
    return get_events(db)

@router.post("/", response_model=EventResponse)
def post_event(payload: EventCreate, db: Session = Depends(get_db)):
    return create_event(
        db=db,
        organiser_id=payload.organiser_id,
        name=payload.name,
        venue=payload.venue,
        ticket_types=payload.ticket_types,
    )
