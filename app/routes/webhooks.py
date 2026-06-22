import os
import stripe
from fastapi import Request, HTTPException, APIRouter

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_ENDPOINT_SECRET")

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalud signature")

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]

        try:
            order_id = payment_intent["metadata"]["order_id"]
        except KeyError:
            order_id = None
        payment_id = payment_intent["id"]

        print(f'payment has been made for {order_id} and this is the payment_id: {payment_id}')

    return {"recieved": True}