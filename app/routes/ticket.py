from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.events_types import TicketCreate, TicketCreateResponse
from app.database import get_db
from app.services.ticket_service import reserve_ticket
from app.schemas.ticket_types import CheckoutStart
import stripe

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

@router.post("/checkout/start")
def start_checkout(payload: CheckoutStart):
    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data":{
                "currency": "gbp",
                "product_data": {
                    "name": f"Ticket order {payload.order_id}",
                },
                "unit_amount": payload.amount,
            },
            "quantity": 1,
        }],
        payment_intent_data={
            "metadata": {
                "order_id": payload.order_id
            }
        },
        success_url="http://127.0.0.1:8000/payment/success",
        cancel_url="http://127.0.0.1:8000/payment/cancel", 
    )   
    return {"checkout_url": session.url}