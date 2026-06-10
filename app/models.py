from ast import For
from sqlalchemy import(
    Column,
    String,
    DateTime,
    Integer,
    ForeignKey,
    Numeric
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Organiser(Base):
    __tablename__= "organisers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    events = relationship("Event", back_populates="organiser")

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organiser_id = Column(UUID(as_uuid=True), ForeignKey("organisers.id"), nullable=False)

    name = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    status = Column(String, nullable=False, default="draft")

    organiser = relationship("Organiser", back_populates="events")
    ticket_types = relationship("TicketType", back_populates="event")
    tickets = relationship("Ticket", back_populates="event")

class TicketType(Base):
    __tablename__ = "ticket_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)

    name = Column(String, nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    quantity_total = Column(Integer, nullable=False)
    quantity_sold = Column(Integer, nullable=False, default=0)

    event = relationship("Event", back_populates="ticket_types")
    tickets = relationship("Ticket", back_populates="ticket_type")

class Ticket(Base):
    __tablename__= "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    ticket_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    ticket_status = Column(String, nullable=False, default="available")
    ticket_type_id = Column(UUID(as_uuid=True), ForeignKey("ticket_types.id"), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    
    ticket_type = relationship("TicketType", back_populates="tickets")
    event = relationship("Event", back_populates="tickets")
    user = relationship("User", back_populates="tickets")


class User(Base):
    __tablename__= "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    tickets = relationship("Ticket", back_populates="user")