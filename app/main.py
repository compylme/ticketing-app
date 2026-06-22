from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from fastapi import FastAPI
from app.routes.events import router as events_router
from app.routes.user import router as user_router
from app.routes.ticket import router as ticket_router
from app.routes.webhooks import router as webhook_router

app = FastAPI()

app.include_router(events_router)
app.include_router(user_router)
app.include_router(ticket_router)
app.include_router(webhook_router)