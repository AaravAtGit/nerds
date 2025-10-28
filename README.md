
# Nerds — Booking Notification API

A small FastAPI service that sends WhatsApp booking confirmations via Twilio. It exposes a tiny HTTP API with one POST endpoint to notify a passenger about their taxi/ride booking and a health endpoint.

## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Environment variables](#environment-variables)
- [API](#api)
	- [GET /](#get-)
	- [POST /inform](#post-inform)
- [Examples](#examples)
	- [curl](#curl)
	- [Python (requests)](#python-requests)
- [Troubleshooting](#troubleshooting)
- [Notes](#notes)

## Features

- Simple REST API built with FastAPI
- Sends formatted WhatsApp messages using Twilio
- Minimal and easy to run locally

## Requirements

- Python 3.9+
- A Twilio account with WhatsApp messaging enabled (sandbox or production)
- The project's Python dependencies (see `requirements.txt`)

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Quick start

1. Create a `.env` file in the project root (see Environment variables).
2. Start the app with Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## Environment variables

Create a `.env` file with the following keys (example):

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_NUMBER=whatsapp:+1415XXXXXXX   # Twilio WhatsApp-enabled number (from)
```

- `TWILIO_NUMBER` should be the Twilio sender value (for WhatsApp it typically starts with `whatsapp:`). For the Twilio sandbox you will also have a sandbox number in the same format.
- Do not commit `.env` to source control.

## API

### GET /

Returns a simple health check message.

Response example (200):

```json
{ "message": "The api is working fine!" }
```

### POST /inform

Sends a WhatsApp booking confirmation message using Twilio.

Request content-type: `application/json`

Request body shape (JSON):

```json
{
	"pickup": "string",
	"destination": "string",
	"tripType": "string",
	"taxiType": "string",
	"bookingDateTime": "YYYY-MM-DD HH:MM",
	"name": "Passenger Name",
	"phone": "+1234567890"
}
```

Notes:
- `phone` must be in E.164 format and should be enabled to receive WhatsApp messages (for Twilio sandbox you usually need to join the sandbox first).
- The service will format the message and send it to `whatsapp:{phone}` using the configured `TWILIO_NUMBER`.

Successful response example:

```json
{ "success": true, "sid": "SMxxxxxxxxxxxxxxxxxxxxxxxx" }
```

Error response example:

```json
{ "success": false, "error": "<error message>" }
```

## Examples

### curl

Health check:

```bash
curl http://localhost:8000/
```

Send a booking notification (replace values accordingly):

```bash
curl -X POST http://localhost:8000/inform \
	-H "Content-Type: application/json" \
	-d '{
		"pickup": "Central Station",
		"destination": "Airport",
		"tripType": "One way",
		"taxiType": "Sedan",
		"bookingDateTime": "2025-10-28 09:00",
		"name": "Aarav",
		"phone": "+15551234567"
	}'
```

### Python (requests)

```python
import requests

payload = {
		"pickup": "Central Station",
		"destination": "Airport",
		"tripType": "One way",
		"taxiType": "Sedan",
		"bookingDateTime": "2025-10-28 09:00",
		"name": "Aarav",
		"phone": "+15551234567"
}

resp = requests.post("http://localhost:8000/inform", json=payload)
print(resp.status_code, resp.json())
```

## Troubleshooting

- If you get authentication errors from Twilio, verify `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`.
- If messages fail to deliver, check that the `TWILIO_NUMBER` is WhatsApp-enabled and that the destination number has joined the Twilio WhatsApp sandbox (if using sandbox).
- Check app logs (the Uvicorn console) for stack traces returned in the `error` field.

