from pydantic import BaseModel
from uuid import UUID

class TicketTypeCreate(BaseModel):
    name: str
    price: float
    quantity_total: int

class EventCreate(BaseModel):
    organiser_id: UUID
    name: str
    venue: str
    ticket_types: list[TicketTypeCreate]

class EventResponse(BaseModel):
    id: UUID
    name: str
    venue: str
    status: str

    model_config = {"from_attributes": True}

class OrganiserCreate(BaseModel):
    name: str
    email: str

class OrganiserResponse(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = {"from_attributes": True}