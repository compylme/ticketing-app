from app.models import Event, TicketType, Organiser
from app.schemas.events_types import EventUpdate

def create_event(db, organiser_id, name, venue, ticket_types):
    event_exists = db.query(Event).filter(Event.name == name).first()

    if event_exists:
        raise ValueError("An event of the same name already exists")

    event = Event(
        name=name, 
        venue=venue,
        organiser_id=organiser_id
    )

    seen = set()
    for tt in ticket_types:
        if tt.name in seen:
            raise ValueError(f"Ticket type '{tt.name}' already exists in this event")

    for tt in ticket_types:
        tt_exists = (
            db.query(TicketType)
            .join(Event)
            .filter(TicketType.name == tt.name)
            .first()
        )
        if tt_exists:
            raise ValueError(f"Ticket type '{tt.name}' already exists on another event")

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
    ticket_types = db.query(TicketType).filter(TicketType.event_id == event_id).all()
    return ticket_types