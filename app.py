import streamlit as st
from weather import *
from history import *
from streamlit_geolocation import streamlit_geolocation

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Kisan",
    page_icon="🌾",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #1b5e20;
}

div.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-weight: 600;
}

[data-testid="stMetric"] {
    background-color: #f8fff8;
    border: 1px solid #d8ead8;
    padding: 15px;
    border-radius: 12px;
}

.weather-card {
    background: #f8fff8;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #dcefdc;
    text-align: center;
}

.advice-box {
    background: #ecfff0;
    padding: 12px;
    border-left: 5px solid #2e7d32;
    border-radius: 8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;'>🌾 Smart Kisan</h1>
<p style='text-align:center;color:gray;'>
Live Weather • 3 Day Forecast • Smart Crop Advisory
</p>
<hr>
""", unsafe_allow_html=True)

# ---------------- RECENT SEARCHES ----------------
history = load_history()

if history:
    st.subheader("🕒 Recent Searches")

    cols = st.columns(len(history))

    for i, item in enumerate(history):
        with cols[i]:
            if st.button(item):
                st.session_state["selected_city"] = item

# ---------------- SEARCH SECTION ----------------
st.subheader("🔍 Search Weather")

col1, col2 = st.columns([4, 1])

with col1:
    city_input = st.text_input(
        "",
        placeholder="Enter city name...",
        label_visibility="collapsed"
    )

with col2:
    search_btn = st.button("Get Weather")

# ---------------- LOCATION SECTION ----------------
st.subheader("📍 Quick Access")

geo = streamlit_geolocation()
location_btn = st.button("Use My Current Location")

# ---------------- VARIABLES ----------------
selected_city = st.session_state.get("selected_city", "")
city = ""

# ---------------- CITY SEARCH ----------------
if search_btn:

    city = city_input.strip()

elif selected_city:

    city = selected_city

# ---------------- IF CITY EXISTS ----------------
if city:

    save_city(city)

    current_data = get_current_weather(city)
    forecast_data = get_forecast(city)
    advice = get_advisory(current_data, forecast_data)

# ---------------- LOCATION SEARCH ----------------
elif location_btn:

    if geo["latitude"] is not None and geo["longitude"] is not None:

        lat = geo["latitude"]
        lon = geo["longitude"]

        current_data = get_current_weather_by_location(lat, lon)
        forecast_data = get_forecast_by_location(lat, lon)
        advice = get_advisory(current_data, forecast_data)

        city = f'{current_data["city_name"]}, {current_data["region"]}'

    else:
        st.error("Please allow location access.")
        st.stop()

else:
    st.stop()

# ---------------- ERROR HANDLING ----------------
if "error" in current_data:
    st.error(current_data["error"])
    st.stop()

# ---------------- DISPLAY ----------------
st.markdown("---")
st.header(f"📍 {city}")

# ---------------- CURRENT WEATHER ----------------
st.subheader("🌤 Current Weather")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌡 Temperature", f'{current_data["temp"]} °C')

with col2:
    st.metric("💧 Humidity", f'{current_data["humidity"]}%')

with col3:
    st.metric("☁ Condition", current_data["condition"])

# ---------------- FORECAST ----------------
st.subheader("📅 3 Day Forecast")

cols = st.columns(3)

for i, day in enumerate(forecast_data):

    with cols[i]:
        st.markdown(f"""
        <div class="weather-card">
        <h4>{day["date"]}</h4>
        🌡 <b>{day["max_temp"]}°C</b><br>
        ❄ {day["min_temp"]}°C<br>
        ☁ {day["condition"]}<br>
        🌧 {day["rain_chance"]}% Rain
        </div>
        """, unsafe_allow_html=True)

# ---------------- ADVISORY ----------------
st.subheader("🌾 Smart Advisory")

for item in advice:
    st.markdown(
        f"<div class='advice-box'>✅ {item}</div>",
        unsafe_allow_html=True
    )
