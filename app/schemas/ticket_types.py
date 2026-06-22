from pydantic import BaseModel

class CheckoutStart(BaseModel):
    order_id: str
    amount: int
