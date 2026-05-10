import streamlit as st
from weather import get_current_weather, get_forecast, get_advisory
from history import load_history, save_city

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Smart Kisan 🌾",
    page_icon="🌾",
    layout="wide"
)

# ---------------- Custom Width ----------------
st.markdown("""
<style>
.main .block-container{
    max-width: 1140px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}
div.stButton > button{
    width:100%;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.title("🌾 Smart Kisan")
st.caption("Live weather + forecast + advisory")

# ---------------- Load Search History ----------------
history = load_history()

# ---------------- Recent Cities ----------------
if history:
    st.markdown("### 🕘 Recent Searches")

    cols = st.columns(5)

    selected_city = None

    for i, old_city in enumerate(history):
        with cols[i]:
            if st.button(old_city):
                selected_city = old_city
else:
    selected_city = None

# ---------------- Search Section ----------------
st.markdown("### Search City")

city_input = st.text_input(
    label="",
    placeholder="Enter city name...",
    label_visibility="collapsed"
)

search = st.button("🌦 Get Weather")

# ---------------- Final City Choice ----------------
city = selected_city if selected_city else city_input+

# ---------------- Main Logic ----------------
if search or selected_city:

    if city.strip() == "":
        st.error("Please enter a city name.")

    else:
        save_city(city)

        current_data = get_current_weather(city)

        if "error" in current_data:
            st.error(current_data["error"])

        else:
            forecast_data = get_forecast(city)
            advice_data = get_advisory(current_data, forecast_data)

            # ---------- Current Weather ----------
            st.subheader(f"📍 {city.title()}")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("🌡 Temp", f'{current_data["temp"]}°C')

            with c2:
                st.metric("💧 Humidity", f'{current_data["humidity"]}%')

            with c3:
                st.metric("☁ Condition", current_data["condition"])

            # ---------- Forecast ----------
            st.markdown("### 📅 Forecast")

            f1, f2, f3 = st.columns(3)

            for i, col in enumerate([f1, f2, f3]):
                day = forecast_data[i]

                with col:
                    st.info(
                        f"""
**{day["date"]}**

🌡 Max: {day["max_temp"]}°C  
❄ Min: {day["min_temp"]}°C  
☁ {day["condition"]}  
🌧 Rain: {day["rain_chance"]}%
"""
                    )

            # ---------- Advisory ----------
            st.markdown("### 🌾 Smart Advisory")

            for advice in advice_data:
                st.warning(advice)