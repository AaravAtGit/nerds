from fastapi import FastAPI
from pydantic import BaseModel
from twilio.rest import Client
from dotenv import load_dotenv
from uvicorn import run
import os
import smtplib
from email.message import EmailMessage

app = FastAPI()
load_dotenv()

sender_mail = "toursandtravels987@gmail.com"
reciver_mail = "mishraji3713@gmail.com"

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
number = os.getenv("TWILIO_NUMBER")

mail_pass = os.getenv("MAIL_PASS")
client = Client(account_sid, auth_token)


def send_booking_mail(booking):
    try:
        subject = f"New Booking: {booking.name} — {booking.pickup} → {booking.destination}"
        body = f"""Booking Confirmed\n\nRoute: {booking.pickup} → {booking.destination}\n\nDetails:\n- Trip: {booking.tripType}\n- Vehicle: {booking.taxiType}\n- When: {booking.bookingDateTime}\n\nPassenger Info:\nName: {booking.name}\nPhone: {booking.phone}\n"""

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender_mail
        msg["To"] = reciver_mail
        msg.set_content(body)

        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_mail, mail_pass)
            server.send_message(msg)

        return True, None
    except Exception as e:
        return False, str(e)


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
        # notify admin via email
        email_ok, email_err = send_booking_mail(booking)
        result = {"success": True, "sid": message.sid}
        if not email_ok:
            result["admin_email_error"] = email_err
            return {"success": False, "error": email_err}

    
    except Exception as e:
        return {"success": False, "error": str(e)}


         