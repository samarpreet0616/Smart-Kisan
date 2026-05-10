# 🌾 Smart Kisan

Smart Kisan is a Python + Streamlit based smart farming assistant that helps users make better daily agricultural decisions using real-time weather data.

## 🚀 Features

* 🌤 Live weather updates by city
* 📅 3-day weather forecast
* 🌧 Rain probability tracking
* 🌾 Smart advisory system based on weather conditions
* 🕘 Recent city search history
* ❌ Error handling for invalid city names / network issues
* 💻 Clean and responsive Streamlit UI

## 🛠 Tech Stack

* Python
* Streamlit
* Requests
* WeatherAPI
* JSON
* python-dotenv

## 📂 Project Structure

Smart-Kisan/
│── app.py
│── weather.py
│── history.py
│── history.json
│── requirements.txt

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/Smart-Kisan.git
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create `.env` file

```env
WEATHER_API_KEY=your_api_key_here
```

4. Run the app

```bash
streamlit run app.py
```

## 🌱 Future Improvements

* Crop-specific advisories
* Mandi price integration
* Soil data support
* Multi-language support
* Cloud deployment

## 👨‍💻 Author

Built by Samarpreet Singh as a backend-focused project to learn real-world development.

## ⭐ If you like this project, consider starring the repo.
