import requests
import feedparser
import os
from datetime import datetime
from twilio.rest import Client

# ─── CONFIG — reads from environment variables (GitHub Secrets) ───────────────
TWILIO_SID      = os.environ.get("TWILIO_SID")
TWILIO_AUTH     = os.environ.get("TWILIO_AUTH")
TWILIO_WHATSAPP = os.environ.get("TWILIO_FROM")
YOUR_WHATSAPP   = os.environ.get("TWILIO_TO")

MANUAL_CITY = "Vidisha"

def get_location():
    if MANUAL_CITY:
        r = requests.get(
            f"https://nominatim.openstreetmap.org/search?q={MANUAL_CITY},India&format=json&limit=1",
            headers={"User-Agent": "Jarvizz/1.0"}, timeout=5
        ).json()
        if r:
            return {"city": MANUAL_CITY, "lat": float(r[0]["lat"]), "lon": float(r[0]["lon"])}
    return {"city": "Vidisha", "lat": 23.5251, "lon": 77.8082}

WMO_CODES = {
    0:"Clear sky", 1:"Mainly clear", 2:"Partly cloudy", 3:"Overcast",
    45:"Foggy", 48:"Icy fog", 51:"Light drizzle", 61:"Light rain",
    63:"Moderate rain", 65:"Heavy rain", 71:"Light snow", 80:"Rain showers",
    95:"Thunderstorm", 99:"Thunderstorm with hail"
}

def get_aqi(lat, lon):
    try:
        url = (f"https://air-quality-api.open-meteo.com/v1/air-quality"
               f"?latitude={lat}&longitude={lon}&current=us_aqi,pm2_5"
               f"&timezone=Asia/Kolkata")
        d   = requests.get(url, timeout=5).json()["current"]
        aqi = d.get("us_aqi")
        pm25= d.get("pm2_5")
        if aqi is None: return "  AQI: unavailable"
        if   aqi <= 50:  cat, emoji = "Good",                  "🟢"
        elif aqi <= 100: cat, emoji = "Moderate",              "🟡"
        elif aqi <= 150: cat, emoji = "Unhealthy (sensitive)", "🟠"
        elif aqi <= 200: cat, emoji = "Unhealthy",             "🔴"
        elif aqi <= 300: cat, emoji = "Very Unhealthy",        "🟣"
        else:            cat, emoji = "Hazardous",             "⚫"
        sun_ok = "✅ ok for 15min sun" if aqi <= 150 else "⚠️ skip outdoor sun today"
        return f"  {emoji} AQI {aqi:.0f} — {cat} (PM2.5: {pm25:.0f})\n  {sun_ok}"
    except:
        return "  AQI: unavailable"

def get_weather(lat, lon, city):
    url = (f"https://api.open-meteo.com/v1/forecast"
           f"?latitude={lat}&longitude={lon}"
           f"&current=temperature_2m,apparent_temperature,weathercode,relative_humidity_2m"
           f"&daily=weathercode,temperature_2m_max,temperature_2m_min"
           f"&timezone=Asia/Kolkata&forecast_days=4")
    d       = requests.get(url, timeout=5).json()
    c       = d["current"]
    temp    = c["temperature_2m"]
    feels   = c["apparent_temperature"]
    humidity= c["relative_humidity_2m"]
    desc    = WMO_CODES.get(c["weathercode"], "Unknown")
    today   = f"📍 {city}\n🌡 {temp}°C (feels {feels}°C) | {desc} | 💧 {humidity}%"
    daily   = d["daily"]
    week    = []
    for i in range(4):
        day = datetime.strptime(daily["time"][i], "%Y-%m-%d").strftime("%a")
        hi  = daily["temperature_2m_max"][i]
        lo  = daily["temperature_2m_min"][i]
        week.append(f"  {day}: {hi:.0f}°/{lo:.0f}°")
    return today, "\n".join(week)

RSS_FEEDS = {
    "🇮🇳 India":      "https://feeds.feedburner.com/ndtvnews-top-stories",
    "🌍 World":        "https://feeds.bbci.co.uk/news/world/rss.xml",
    "📊 Business":     "https://feeds.feedburner.com/ndtvprofit-latest-news",
}

def get_news():
    sections = []
    for label, url in RSS_FEEDS.items():
        feed    = feedparser.parse(url)
        entries = feed.entries[:2]
        lines   = [f"  • {e.title[:80]}" for e in entries]
        sections.append(f"*{label}*\n" + "\n".join(lines))
    return "\n\n".join(sections)

def get_stocks():
    symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "USD/INR": "INR=X"}
    lines   = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for name, sym in symbols.items():
        try:
            url    = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=2d"
            data   = requests.get(url, headers=headers, timeout=5).json()
            closes = [c for c in data["chart"]["result"][0]["indicators"]["quote"][0]["close"] if c]
            if len(closes) >= 2:
                prev, curr = closes[-2], closes[-1]
                pct   = ((curr - prev) / prev) * 100
                arrow = "📈" if curr >= prev else "📉"
                lines.append(f"  {arrow} {name}: {curr:,.2f} ({pct:+.2f}%)")
        except:
            lines.append(f"  ⚠️ {name}: unavailable")
    return "\n".join(lines)

def get_health_nudge():
    today = datetime.now().strftime("%A")
    lines = []
    if today == "Sunday":
        lines.append("  💊 *Vit D shot today!* (your level was 25.25 nmol/L)")
    nudges = {
        "Monday":    "🏃 Leg day — 30 min cardio + squats",
        "Tuesday":   "💪 Push day — chest & shoulders",
        "Wednesday": "🧘 Active recovery — 20 min walk + stretch",
        "Thursday":  "🏋️ Pull day — back & biceps",
        "Friday":    "🏃 HIIT — 20 min sprints",
        "Saturday":  "⚽ Sport day — play something fun",
        "Sunday":    "🚶 Long walk + sunlight (if AQI ok)",
    }
    lines.append(f"  {nudges.get(today, '💪 Move your body 30 min')}")
    lines.append("  🥚 Iron-rich breakfast (eggs / paneer / dates)")
    return "\n".join(lines)

def get_quote():
    try:
        data = requests.get("https://zenquotes.io/api/today", timeout=5).json()[0]
        return f'"{data["q"]}"\n  — {data["a"]}'
    except:
        return '"The secret of getting ahead is getting started."\n  — Mark Twain'

def send_briefing():
    loc              = get_location()
    city, lat, lon   = loc["city"], loc["lat"], loc["lon"]
    today_wx, week_wx = get_weather(lat, lon, city)
    aqi              = get_aqi(lat, lon)
    news             = get_news()
    stocks           = get_stocks()
    quote            = get_quote()
    health           = get_health_nudge()

    msg = f"""☀️ *Good Morning! Jarvizz Daily Briefing*
📅 {datetime.now().strftime("%A, %d %B %Y")}

━━━━━━━━━━━━━━━━━━━━
🌤 *WEATHER — {city}*
{today_wx}

🌫 *AIR QUALITY*
{aqi}

📆 *4-DAY FORECAST*
{week_wx}

━━━━━━━━━━━━━━━━━━━━
🏃 *HEALTH FOR TODAY*
{health}

━━━━━━━━━━━━━━━━━━━━
📰 *NEWS*
{news}

━━━━━━━━━━━━━━━━━━━━
📊 *MARKETS*
{stocks}

━━━━━━━━━━━━━━━━━━━━
💬 *QUOTE OF THE DAY*
{quote}

━━━━━━━━━━━━━━━━━━━━
Have a great day! 🚀 — *Jarvizz*"""

    Client(TWILIO_SID, TWILIO_AUTH).messages.create(
        body=msg, from_=TWILIO_WHATSAPP, to=YOUR_WHATSAPP
    )
    print(f"[{datetime.now()}] Briefing sent to {YOUR_WHATSAPP}!")

if __name__ == "__main__":
    send_briefing()
