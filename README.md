
# Naksir Soccer Predictions – Telegram WebApp API

This is the backend API for the Telegram Mini App “Naksir Soccer Predictions”.

## Features

- Admin form to post daily soccer predictions (/admin)
- WebApp for premium users to view predictions (/soccer)
- Token validation system for secure access
- Telegram Webhook integration for payment verification (optional)

## Endpoints

- `GET /get` – Returns current prediction in JSON format
- `POST /update?pass=naksir2025` – Updates prediction
- `GET /generate-token?user_id=xxx` – Generates token
- `GET /validate-token?token=xxx` – Validates token
- `GET /soccer?token=xxx` – Displays premium prediction page
- `GET /admin` – Admin prediction form

## Setup

- Requires Python + Flask
- Hosted on Render with dynamic port
- Make sure to set `PORT` as environment variable
