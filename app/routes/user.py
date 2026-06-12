from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_types import UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def post_user(payload: UserCreate, db: Session = Depends(get_db)):
    try: 
        return create_user(
            db=db,
            name=payload.name,
            email=payload.email,
    ) 
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

