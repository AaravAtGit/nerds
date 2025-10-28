from fastapi import FastAPI
from pydantic import BaseModel
from twilio.rest import Client
from dotenv import load_dotenv
from uvicorn import run
import os

app = FastAPI()
load_dotenv()


account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
number = os.getenv("TWILIO_NUMBER")
client = Client(account_sid, auth_token)


class BookingRequest(BaseModel):
    pickup: str
    destination: str
    tripType: str
    taxiType: str
    bookingDateTime: str
    name: str
    phone: str


@app.get("/")
async def root():
    return {"message": "The api is working fine!"}


@app.post("/inform")
async def inform(booking: BookingRequest):
    try:
        message = f"""*Booking Confirmed* ✅

*Route*
{booking.pickup} → {booking.destination}

*Details*
- Trip: {booking.tripType}
- Vehicle: {booking.taxiType}
- When: {booking.bookingDateTime}

*Passenger Info*
Name: {booking.name}
Phone: {booking.phone}

_We look forward to serving you!_ 🚗"""

        message = client.messages.create(
            body=message,
            from_=number,
            to=f"whatsapp:{booking.phone}"
        )
        return {"success": True, "sid": message.sid}
    except Exception as e:
        return {"success": False, "error": str(e)}


         