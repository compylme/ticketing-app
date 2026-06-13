from fastapi import FastAPI
from app.routes.events import router as events_router
from app.routes.user import router as user_router
from app.routes.ticket import router as ticket_router

app = FastAPI()

app.include_router(events_router)
app.include_router(user_router)
app.include_router(ticket_router)