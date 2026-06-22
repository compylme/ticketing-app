from ast import For
from sqlalchemy import(
    Column,
    String,
    DateTime,
    Integer,
    Float,
    ForeignKey,
    Numeric,
    Enum
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    EXPIRED = "expired"

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
    reservation_expiry_minutes = Column(Integer, nullable=False, default=15)

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
    max_per_order = Column(Integer, nullable=False, default=4)

    event = relationship("Event", back_populates="ticket_types")
    tickets = relationship("Ticket", back_populates="ticket_type")

class Ticket(Base):
    __tablename__= "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    ticket_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    ticket_status = Column(String, nullable=False, default="available")
    ticket_type_id = Column(UUID(as_uuid=True), ForeignKey("ticket_types.id"), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True)
    
    ticket_type = relationship("TicketType", back_populates="tickets")
    event = relationship("Event", back_populates="tickets") 
    user = relationship("User", back_populates="tickets")
    order = relationship("Order", back_populates="tickets")


class User(Base):
    __tablename__= "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    tickets = relationship("Ticket", back_populates="user")
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__="orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    payment_session_id = Column(String, nullable=True)
    amount = Column(Numeric(10,2))
    status = Column(Enum(OrderStatus, name="order_status", values_callable=lambda x: [e.value for e in x]), nullable=False, default=OrderStatus.PENDING)
    reservation_expiry = Column(DateTime, nullable=False)


    user = relationship("User", back_populates="orders")
    tickets = relationship("Ticket", back_populates="order")

