# 🌤️ Weather App (Tkinter GUI)

A beautiful and modern **Weather Application** built using **Python (Tkinter)**.  
It allows users to search for weather information by **city name** or use their **current location (via IP-based geolocation)**.  
The app displays **current weather, hourly forecast, 7-day forecast, charts**, and **visual icons** in a smooth scrolling, gradient-styled interface.

---

## 🚀 Features

✅ **Live Weather Data** — Fetches real-time weather updates using the OpenWeatherMap API.  
✅ **City Search & My Location** — Search weather by city or detect automatically using your IP.  
✅ **Hourly Forecast** — Displays the next 8-hour forecast with icons and temperature.  
✅ **7-Day Forecast** — Summarized daily highs and lows with weather icons.  
✅ **Temperature Trend Chart** — Beautiful matplotlib graph for temperature trends.  
✅ **Celsius / Fahrenheit Toggle** — Switch between Metric and Imperial units.  
✅ **Modern Gradient UI** — Smooth blue gradient background with card shadows and rounded frames.  
✅ **Smooth Scrolling** — Scrollable interface for large datasets.  
✅ **Error Handling** — Graceful network and input validation handling.  
✅ **Caching** — Reduces API calls for faster refreshes.

---

## 🧩 Technologies Used

- **Python 3.x**
- **Tkinter** – for the GUI
- **Pillow (PIL)** – for weather icons
- **Requests** – for API requests
- **Matplotlib** – for temperature charts
- **Threading** – for background data loading (keeps UI responsive)
- **OpenWeatherMap API** – for weather data
- **ipapi.co** – for IP-based location detection

---

## ⚙️ Setup Instructions

### 1️⃣ Clone or Download Repository
```bash
git clone https://github.com/yourusername/weather-app-tkinter.git
cd weather-app-tkinter
```

### 2️⃣ Install Required Libraries
```bash
pip install requests pillow matplotlib
```

### 3️⃣ Get Your API Key
- Go to [https://openweathermap.org/api](https://openweathermap.org/api)
- Sign up for a **free account**
- Generate your **API key**

Replace the API key in the code:
```python
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
```

### 4️⃣ Run the App
```bash
python weather_app.py
```

---

## 🧠 Key Concepts and Challenges

| Concept | Description |
|----------|--------------|
| **API Integration** | Uses OpenWeatherMap API for weather data and IPAPI for geolocation |
| **User Input Handling** | Validates user-entered city names |
| **GUI Design** | Designed with a modern gradient, card layout, and scroll support |
| **Error Handling** | Catches and displays network or API errors gracefully |
| **Threading** | Fetches weather data in background threads for smooth UI |
| **Data Visualization** | Renders temperature trends using Matplotlib |
| **Unit Conversion** | Allows switching between Celsius and Fahrenheit |

---

## 🖼️ Screenshots (Optional)

_Add screenshots of the app UI here for better presentation:_
```
📸 /screenshots/home_screen.png
📸 /screenshots/forecast_view.png
```

---

## 🧭 Future Improvements

- 🌎 GPS integration for precise location (for mobile use)
- 🌙 Dark/Light mode support
- 🔔 Weather alerts and notifications
- 🗺️ Map-based weather display
- 💾 Save favorite cities

---

## 🧑‍💻 Author

**Developed by:** [Your Name]  
📧 Email: your.email@example.com  
🌐 GitHub: [github.com/yourusername](https://github.com/yourusername)

---

## 🪪 License

This project is open source and available under the **MIT License**.

---

### 💡 Tip:
If you get a `401 Unauthorized` error, make sure your API key is valid and correctly inserted:
```python
API_KEY = "YOUR_VALID_API_KEY"
```

---

Enjoy your personalized, elegant **Weather App** built in Python! 🌤️
