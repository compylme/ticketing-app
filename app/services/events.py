from app.models import Event, TicketType

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