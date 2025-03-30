# Naksir Soccer Predictions – Telegram Mini App API

This is the backend API for the Telegram Mini App "Naksir Soccer Predictions".

It allows:
- Admins to post premium betting predictions
- Telegram WebApp to fetch and display them

## Endpoints

### GET /get
Returns the current prediction in JSON format.

### POST /update?pass=naksir2025
Updates the prediction content (requires password).

## Files

- app.py - Flask backend server
- requirements.txt - Python dependencies
- prediction.json - Storage for latest prediction

## Hosting
Deploy using [Render](https://render.com) as a Web Service.
