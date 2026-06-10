from app.models import Event, TicketType, Organiser
from app.schemas.events_types import EventUpdate, TicketTypesResponse

def create_event(db, organiser_id, name, venue, ticket_types):
    event = Event(
        name=name, 
        venue=venue,
        organiser_id=organiser_id
    )
    for tt in ticket_types:
        event.ticket_types.append(
            TicketType(
                name=tt.name,
                price=tt.price,
                quantity_total=tt.quantity_total
            )
        )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_event(db, event_id):
    event = db.get(Event, event_id)

    return event

def get_events(db):
    return db.query(Event).all()

def update_event(db, event_id, update_data: EventUpdate):
    event = db.get(Event, event_id)

    for field, value in update_data.model_dump(exclude_none=True).items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    return event


def create_organisation(db, name, email):
    organiser = Organiser(
        name=name,
        email=email
    )
    db.add(organiser)
    db.commit()
    db.refresh(organiser)
    return organiser

def get_event_ticket_types(db, event_id):
    event = db.get(Event, event_id)
    return TicketTypesResponse(ticket_types=event.ticket_types)