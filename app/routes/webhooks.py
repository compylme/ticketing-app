import stripe
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

stripe.api_key = "sk_test_xxx"
endpoint_secret = "whsec_xxx"

@app.post("/webhooks/stripe")
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

    if event["type"] == "payment_intent.succeded":
        payment_intent = event["data"]["object"]

        order_id = payment_intent["metadata"].get("order_id")
        payment_id = payment_intent["id"]

        print(f'payment has been made for {order_id} and this is the payment_id: {payment_id}')

    return {"recieved": True}