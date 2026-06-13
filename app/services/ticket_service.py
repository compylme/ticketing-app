from uuid import UUID
from app.models import TicketType, Ticket

def reserve_ticket(db, user_id:UUID, event_id:UUID, ticket_type:str, ticket_quantity:int):
    #get the ticket_type the client wants to order
    ticket_type_obj = (
        db.query(TicketType)
        .filter(TicketType.event_id == event_id, TicketType.name == ticket_type)
        .with_for_update()
        .first()
    )

    if not ticket_type_obj:
        raise ValueError("Ticket type not found")

    remaining_tickets_of_ticket_type = ticket_type_obj.quantity_total - ticket_type_obj.quantity_sold

    if ticket_quantity > ticket_type_obj.max_per_order:
        db.rollback()
        raise ValueError("Amount of tickets requested exceed max tickets per order")

    if ticket_quantity > remaining_tickets_of_ticket_type:
        db.rollback()
        raise ValueError("Not enough tickets")
    
    #call the ticket_table and create rows equal to the amount of tickets requested
    tickets = [
        Ticket(
            ticket_user_id = user_id,
            ticket_type_id = ticket_type_obj.id,
            event_id=event_id,
            ticket_status="reserved"
        )
        for _ in range(ticket_quantity)
    ]
    db.add_all(tickets)
    ticket_type_obj.quantity_sold += ticket_quantity
    db.commit()
    return tickets