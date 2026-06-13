from pydantic import BaseModel
from uuid import UUID

class TicketTypeCreate(BaseModel):
    name: str
    price: float
    quantity_total: int

class TicketTypeResponse(BaseModel):
    id: UUID
    name: str
    price: float
    quantity_total: int
    quantity_sold: int
    max_per_order: int
   
    model_config = {"from_attributes": True}

class TicketCreate(BaseModel):
    ticket_user_id: UUID
    ticket_type: str
    amount_of_tickets: int
    event_id: UUID

class TicketCreateResponse(BaseModel):
    ticket_user_id: UUID
    ticket_type_id: UUID
    event_id: UUID
    
    model_config = {"from_attributes": True}


class EventCreate(BaseModel):
    organiser_id: UUID
    name: str
    venue: str
    ticket_types: list[TicketTypeCreate]

class EventUpdate(BaseModel):
    name: str | None = None
    venue: str | None = None
    status: str | None = None
    ticket_types: list[TicketTypeCreate] | None = None

class EventResponse(BaseModel):
    id: UUID
    name: str
    venue: str
    status: str

    model_config = {"from_attributes": True}

class TicketTypesResponse(BaseModel):
    ticket_types: list[TicketTypeResponse] | None

class OrganiserCreate(BaseModel):
    name: str
    email: str

class OrganiserResponse(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = {"from_attributes": True}