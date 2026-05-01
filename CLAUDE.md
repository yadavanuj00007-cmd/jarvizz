# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Jarvizz is a single-file Python script (`daily_briefing.py`) that compiles a morning briefing — weather, AQI, news, stock markets, a workout nudge, and a quote — and delivers it via WhatsApp using Twilio. It runs automatically every day at 9:00 AM IST via GitHub Actions.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the briefing locally (requires env vars set)
python daily_briefing.py

# Trigger manually via GitHub Actions (no local secrets needed)
# Go to Actions → Jarvizz Daily Briefing → Run workflow
```

## Required Environment Variables

The script reads four secrets — set them as GitHub Actions secrets or export locally:

| Variable       | Purpose                          |
|----------------|----------------------------------|
| `TWILIO_SID`   | Twilio Account SID               |
| `TWILIO_AUTH`  | Twilio Auth Token                |
| `TWILIO_FROM`  | Sender WhatsApp number (`whatsapp:+1...`) |
| `TWILIO_TO`    | Recipient WhatsApp number        |

## Architecture

Everything lives in `daily_briefing.py`. `send_briefing()` is the entry point — it calls each data-fetch function, formats a single multiline WhatsApp message with WhatsApp markdown (`*bold*`), and sends it via `twilio.rest.Client`.

Data sources and their fetch functions:

| Function         | API / Source                          |
|------------------|---------------------------------------|
| `get_location()` | OpenStreetMap Nominatim (geocodes `MANUAL_CITY`) |
| `get_weather()`  | Open-Meteo forecast API               |
| `get_aqi()`      | Open-Meteo air-quality API            |
| `get_news()`     | RSS feeds via `feedparser` (NDTV, BBC)|
| `get_stocks()`   | Yahoo Finance chart API (no key needed)|
| `get_quote()`    | ZenQuotes `today` endpoint            |
| `get_health_nudge()` | Hardcoded weekly workout schedule |

All external calls use a 5-second timeout. Failures in `get_aqi()`, `get_stocks()`, and `get_quote()` are silently caught and return fallback strings — the briefing still sends.

## Key Details

- **City** is hardcoded as `MANUAL_CITY = "Vidisha"` at the top of the file — change this to relocate.
- **Health nudge** is fully hardcoded (day-of-week workout plan + a Sunday Vitamin D reminder). Adjust `get_health_nudge()` directly.
- **News feeds** are in the `RSS_FEEDS` dict — add/remove sources there.
- **Stock symbols** are in the `symbols` dict inside `get_stocks()` — uses Yahoo Finance tickers.
- The GitHub Actions workflow (`.github/workflows/daily_briefing.yml`) runs on cron `30 3 * * *` (UTC) = 9:00 AM IST. Supports `workflow_dispatch` for manual runs.
