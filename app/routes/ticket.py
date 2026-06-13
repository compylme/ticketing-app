from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.events_types import TicketCreate, TicketCreateResponse
from app.database import get_db
from app.services.ticket_service import reserve_ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/", response_model=list[TicketCreateResponse])
def add_to_ticket_row(
    payload: TicketCreate,
    db: Session = Depends(get_db)
    ):
    try:
        return reserve_ticket(
            db=db,
            user_id=payload.ticket_user_id,
            ticket_type=payload.ticket_type,
            event_id=payload.event_id,
            ticket_quantity=payload.amount_of_tickets,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))