

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import io
import time
import threading
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


API_KEY = ""  
OWM_GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
OWM_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
OWM_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
OWM_ICON_URL = "http://openweathermap.org/img/wn/{icon}@2x.png"
IP_GEO_URL = "https://ipapi.co/json/"

_cache = {}


def safe_get(url, params=None, timeout=10):
    try:
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        return r
    except Exception as e:
        raise RuntimeError(f"Network error: {e}")

def geocode_city(city_name, limit=1):
    params = {"q": city_name, "limit": limit, "appid": API_KEY}
    r = safe_get(OWM_GEOCODE_URL, params=params)
    data = r.json()
    if not isinstance(data, list) or not data:
        raise ValueError("City not found")
    return data

def ip_geolocation():
    try:
        r = safe_get(IP_GEO_URL)
        j = r.json()
        return {"lat": j.get("latitude"), "lon": j.get("longitude"),
                "city": j.get("city"), "country": j.get("country_name")}
    except Exception:
        raise RuntimeError("Unable to determine location from IP")

def fetch_current_weather(lat, lon, units="metric"):
    cache_key = f"current:{lat}:{lon}:{units}"
    cached = _cache.get(cache_key)
    if cached and time.time() - cached["ts"] < 300:
        return cached["data"]
    params = {"lat": lat, "lon": lon, "units": units, "appid": API_KEY}
    r = safe_get(OWM_CURRENT_URL, params=params)
    data = r.json()
    _cache[cache_key] = {"ts": time.time(), "data": data}
    return data

def fetch_forecast(lat, lon, units="metric"):
    cache_key = f"forecast:{lat}:{lon}:{units}"
    cached = _cache.get(cache_key)
    if cached and time.time() - cached["ts"] < 300:
        return cached["data"]
    params = {"lat": lat, "lon": lon, "units": units, "appid": API_KEY}
    r = safe_get(OWM_FORECAST_URL, params=params)
    data = r.json()
    _cache[cache_key] = {"ts": time.time(), "data": data}
    return data

def fetch_icon_image(icon_code, size=(64, 64)):
    cache_key = f"icon:{icon_code}:{size}"
    if cache_key in _cache:
        return _cache[cache_key]["img"]
    url = OWM_ICON_URL.format(icon=icon_code)
    try:
        r = safe_get(url)
        image = Image.open(io.BytesIO(r.content)).convert("RGBA")
        image = image.resize(size, Image.LANCZOS)
        imgtk = ImageTk.PhotoImage(image)
        _cache[cache_key] = {"ts": time.time(), "img": imgtk}
        return imgtk
    except Exception:
        return None


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("900x700")
        self.resizable(True, True)
        
        
        self.bg_gradient_top = "#1e3c72"
        self.bg_gradient_bot = "#2a5298"
        self.card_bg = "#ffffff"
        self.text_dark = "#2c3e50"
        self.text_light = "#7f8c8d"
        self.accent = "#3498db"
        
        self.configure(bg=self.bg_gradient_bot)
        
        self.units = tk.StringVar(value="metric")
        self.location_label = tk.StringVar(value="")
        self.status_text = tk.StringVar(value="Search for a city or use your location")
        
        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        
        style.configure('Modern.TButton', 
                       background=self.accent,
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10),
                       padding=(15, 8))
        style.map('Modern.TButton',
                 background=[('active', '#2980b9')])
        
        
        style.configure('Modern.TEntry',
                       fieldbackground='white',
                       borderwidth=0,
                       relief='flat')
        
        
        style.configure('Card.TFrame',
                       background=self.card_bg,
                       relief='flat')
        
        style.configure('Transparent.TFrame',
                       background=self.bg_gradient_bot)

    def _build_ui(self):
        
        main_container = tk.Canvas(self, bg=self.bg_gradient_bot, highlightthickness=0)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        
        self._draw_gradient(main_container)
        
        
        content = ttk.Frame(main_container, style='Transparent.TFrame')
        main_container.create_window((450, 350), window=content, width=880, height=680)
        
        header = ttk.Frame(content, style='Transparent.TFrame')
        header.pack(fill=tk.X, pady=(10, 20))
        
        title = tk.Label(header, text="🌤️ Weather APP", 
                        font=('Segoe UI', 24, 'bold'),
                        bg=self.bg_gradient_bot, fg='white')
        title.pack()
        
        search_frame = ttk.Frame(content, style='Card.TFrame')
        search_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        search_inner = tk.Frame(search_frame, bg=self.card_bg)
        search_inner.pack(fill=tk.X, padx=20, pady=15)
        
        self.city_entry = tk.Entry(search_inner, font=('Segoe UI', 12),
                                   relief='flat', bd=0, bg='#f8f9fa')
        self.city_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, 
                            ipady=8, ipadx=10)
        self.city_entry.insert(0, "Enter city name...")
        self.city_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.city_entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.city_entry.bind("<Return>", lambda e: self.fetch_by_city())
        
        btn_search = tk.Button(search_inner, text="Search", 
                              command=self.fetch_by_city,
                              bg=self.accent, fg='white',
                              font=('Segoe UI', 10, 'bold'),
                              relief='flat', bd=0, padx=20, cursor='hand2')
        btn_search.pack(side=tk.LEFT, padx=(10, 0), ipady=5)
        
        btn_loc = tk.Button(search_inner, text="📍 My Location",
                           command=self.fetch_by_ip,
                           bg='#95a5a6', fg='white',
                           font=('Segoe UI', 10),
                           relief='flat', bd=0, padx=15, cursor='hand2')
        btn_loc.pack(side=tk.LEFT, padx=(10, 0), ipady=5)
        
        
        units_frame = tk.Frame(search_inner, bg=self.card_bg)
        units_frame.pack(side=tk.LEFT, padx=(15, 0))
        
        self.btn_celsius = tk.Button(units_frame, text="°C",
                                     command=lambda: self._set_units("metric"),
                                     bg=self.accent, fg='white',
                                     font=('Segoe UI', 10, 'bold'),
                                     relief='flat', bd=0, width=3, cursor='hand2')
        self.btn_celsius.pack(side=tk.LEFT, padx=2)
        
        self.btn_fahrenheit = tk.Button(units_frame, text="°F",
                                        command=lambda: self._set_units("imperial"),
                                        bg='#ecf0f1', fg=self.text_dark,
                                        font=('Segoe UI', 10),
                                        relief='flat', bd=0, width=3, cursor='hand2')
        self.btn_fahrenheit.pack(side=tk.LEFT, padx=2)
        
        status_lbl = tk.Label(content, textvariable=self.status_text,
                            font=('Segoe UI', 9), bg=self.bg_gradient_bot,
                            fg='#ecf0f1')
        status_lbl.pack(pady=(0, 10))
        
        canvas = tk.Canvas(content, bg=self.bg_gradient_bot, 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", 
                                 command=canvas.yview)
        
        self.weather_container = ttk.Frame(canvas, style='Transparent.TFrame')
        
        canvas.create_window((0, 0), window=self.weather_container, 
                            anchor="nw", width=840)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.weather_container.bind("<Configure>",
                                   lambda e: canvas.configure(
                                       scrollregion=canvas.bbox("all")))

    def _draw_gradient(self, canvas):
        width = 900
        height = 700
        for i in range(height):
            ratio = i / height
            r = int(30 + (42 - 30) * ratio)
            g = int(60 + (82 - 60) * ratio)
            b = int(114 + (152 - 114) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color, width=1)

    def _on_entry_focus_in(self, event):
        if self.city_entry.get() == "Enter city name...":
            self.city_entry.delete(0, tk.END)
            self.city_entry.config(fg=self.text_dark)

    def _on_entry_focus_out(self, event):
        if not self.city_entry.get():
            self.city_entry.insert(0, "Enter city name...")
            self.city_entry.config(fg=self.text_light)

    def _set_units(self, unit):
        self.units.set(unit)
        if unit == "metric":
            self.btn_celsius.config(bg=self.accent, fg='white', 
                                   font=('Segoe UI', 10, 'bold'))
            self.btn_fahrenheit.config(bg='#ecf0f1', fg=self.text_dark,
                                      font=('Segoe UI', 10))
        else:
            self.btn_fahrenheit.config(bg=self.accent, fg='white',
                                      font=('Segoe UI', 10, 'bold'))
            self.btn_celsius.config(bg='#ecf0f1', fg=self.text_dark,
                                   font=('Segoe UI', 10))
        threading.Thread(target=self._refetch_current_if_any, daemon=True).start()

    def _refetch_current_if_any(self):
        last = _cache.get("last_location")
        if last:
            try:
                self._update_weather_for(last["lat"], last["lon"], last.get("name"))
            except Exception as e:
                self.status_text.set(f"Refresh failed: {e}")

    def fetch_by_city(self):
        city = self.city_entry.get().strip()
        if not city or city == "Enter city name...":
            messagebox.showinfo("Input", "Please enter a city name")
            return
        self.status_text.set("Looking up city...")
        threading.Thread(target=self._do_geocode_and_fetch, args=(city,), daemon=True).start()

    def fetch_by_ip(self):
        self.status_text.set("Detecting location...")
        threading.Thread(target=self._do_ip_and_fetch, daemon=True).start()

    def _do_geocode_and_fetch(self, city):
        try:
            results = geocode_city(city)
            r = results[0]
            lat, lon = r["lat"], r["lon"]
            name = f"{r.get('name')}, {r.get('country')}"
            _cache["last_location"] = {"lat": lat, "lon": lon, "name": name}
            self._update_weather_for(lat, lon, name)
        except Exception as e:
            self.status_text.set(f"Error: {e}")

    def _do_ip_and_fetch(self):
        try:
            loc = ip_geolocation()
            lat, lon = float(loc["lat"]), float(loc["lon"])
            name = f"{loc.get('city')}, {loc.get('country')}"
            _cache["last_location"] = {"lat": lat, "lon": lon, "name": name}
            self._update_weather_for(lat, lon, name)
        except Exception as e:
            self.status_text.set(f"Location error: {e}")

    def _update_weather_for(self, lat, lon, display_name=None):
        try:
            units = self.units.get()
            self.status_text.set("Fetching weather...")
            current = fetch_current_weather(lat, lon, units)
            forecast = fetch_forecast(lat, lon, units)
            self.after(0, lambda: self._render_weather(current, forecast, display_name))
        except Exception as e:
            self.status_text.set(f"Weather fetch error: {e}")

    def _render_weather(self, current, forecast, display_name):

        for widget in self.weather_container.winfo_children():
            widget.destroy()
        
        try:
            unit_sym = "°C" if self.units.get() == "metric" else "°F"
            speed_unit = "m/s" if self.units.get() == "metric" else "mph"
            
            current_card = tk.Frame(self.weather_container, bg=self.card_bg,
                                   relief='flat', bd=0)
            current_card.pack(fill=tk.X, padx=20, pady=(0, 15))
            

            loc_frame = tk.Frame(current_card, bg=self.card_bg)
            loc_frame.pack(fill=tk.X, padx=25, pady=(20, 10))
            
            tk.Label(loc_frame, text=display_name or "Location",
                    font=('Segoe UI', 20, 'bold'),
                    bg=self.card_bg, fg=self.text_dark).pack(anchor=tk.W)
            
            tk.Label(loc_frame, 
                    text=datetime.now().strftime("%A, %B %d, %Y • %I:%M %p"),
                    font=('Segoe UI', 10),
                    bg=self.card_bg, fg=self.text_light).pack(anchor=tk.W)
            

            main_frame = tk.Frame(current_card, bg=self.card_bg)
            main_frame.pack(fill=tk.X, padx=25, pady=(10, 20))
            

            left_frame = tk.Frame(main_frame, bg=self.card_bg)
            left_frame.pack(side=tk.LEFT)
            
            weather = current.get("weather", [{}])[0]
            icon = weather.get("icon")
            if icon:
                img = fetch_icon_image(icon, size=(100, 100))
                if img:
                    icon_lbl = tk.Label(left_frame, image=img, bg=self.card_bg)
                    icon_lbl.image = img
                    icon_lbl.pack(side=tk.LEFT)
            
            temp_frame = tk.Frame(left_frame, bg=self.card_bg)
            temp_frame.pack(side=tk.LEFT, padx=(10, 0))
            
            temp = current["main"]["temp"]
            tk.Label(temp_frame, text=f"{round(temp)}",
                    font=('Segoe UI', 56, 'bold'),
                    bg=self.card_bg, fg=self.text_dark).pack(anchor=tk.W)
            
            desc = weather.get("description", "").capitalize()
            tk.Label(temp_frame, text=desc,
                    font=('Segoe UI', 16),
                    bg=self.card_bg, fg=self.text_light).pack(anchor=tk.W)
            
            # Right: Details
            details_frame = tk.Frame(main_frame, bg=self.card_bg)
            details_frame.pack(side=tk.RIGHT, padx=(30, 0))
            
            feels = current["main"]["feels_like"]
            humidity = current["main"]["humidity"]
            wind = current["wind"]["speed"]
            
            self._add_detail(details_frame, "Feels like", f"{round(feels)}{unit_sym}")
            self._add_detail(details_frame, "Humidity", f"{humidity}%")
            self._add_detail(details_frame, "Wind", f"{wind} {speed_unit}")
            
            self.status_text.set("Weather updated successfully")
            

            hourly_card = tk.Frame(self.weather_container, bg=self.card_bg)
            hourly_card.pack(fill=tk.X, padx=20, pady=(0, 15))
            
            tk.Label(hourly_card, text="Hourly Forecast",
                    font=('Segoe UI', 14, 'bold'),
                    bg=self.card_bg, fg=self.text_dark).pack(anchor=tk.W, 
                                                              padx=25, pady=(15, 10))
            

            hourly_canvas = tk.Canvas(hourly_card, bg=self.card_bg, 
                                     height=140, highlightthickness=0)
            hourly_inner = tk.Frame(hourly_canvas, bg=self.card_bg)
            
            hourly_canvas.create_window((0, 0), window=hourly_inner, anchor="nw")
            hourly_canvas.pack(fill=tk.X, padx=25, pady=(0, 15))
            
            forecasts = forecast.get("list", [])[:8]
            for item in forecasts:
                dt = datetime.fromtimestamp(item["dt"])
                time_str = dt.strftime("%I %p")
                temp_h = item["main"]["temp"]
                icon_h = item["weather"][0].get("icon")
                
                hour_frame = tk.Frame(hourly_inner, bg='#f8f9fa', 
                                     width=90, height=120)
                hour_frame.pack(side=tk.LEFT, padx=5)
                hour_frame.pack_propagate(False)
                
                tk.Label(hour_frame, text=time_str,
                        font=('Segoe UI', 9),
                        bg='#f8f9fa', fg=self.text_light).pack(pady=(8, 0))
                
                if icon_h:
                    img_h = fetch_icon_image(icon_h, size=(50, 50))
                    if img_h:
                        lbl = tk.Label(hour_frame, image=img_h, bg='#f8f9fa')
                        lbl.image = img_h
                        lbl.pack()
                
                tk.Label(hour_frame, text=f"{round(temp_h)}{unit_sym}",
                        font=('Segoe UI', 11, 'bold'),
                        bg='#f8f9fa', fg=self.text_dark).pack()
            
            hourly_inner.update_idletasks()
            hourly_canvas.config(scrollregion=hourly_canvas.bbox("all"))
            
            # Temperature chart
            chart_card = tk.Frame(self.weather_container, bg=self.card_bg)
            chart_card.pack(fill=tk.X, padx=20, pady=(0, 15))
            
            tk.Label(chart_card, text="Temperature Trend",
                    font=('Segoe UI', 14, 'bold'),
                    bg=self.card_bg, fg=self.text_dark).pack(anchor=tk.W,
                                                              padx=25, pady=(15, 10))
            
            temps = [f["main"]["temp"] for f in forecasts]
            times = [datetime.fromtimestamp(f["dt"]).strftime("%I%p") 
                    for f in forecasts]
            
            fig = Figure(figsize=(7.5, 2.5), dpi=100, facecolor=self.card_bg)
            ax = fig.add_subplot(111)
            ax.plot(range(len(temps)), temps, marker='o', 
                   color=self.accent, linewidth=2, markersize=6)
            ax.set_xticks(range(len(times)))
            ax.set_xticklabels(times, fontsize=9)
            ax.set_ylabel(f'Temperature ({unit_sym})', fontsize=10)
            ax.grid(True, linestyle=':', alpha=0.3)
            ax.set_facecolor('#f8f9fa')
            fig.tight_layout(pad=1.5)
            
            chart_widget = FigureCanvasTkAgg(fig, master=chart_card)
            chart_widget.get_tk_widget().pack(padx=25, pady=(0, 15))
            chart_widget.draw()
            

            daily_card = tk.Frame(self.weather_container, bg=self.card_bg)
            daily_card.pack(fill=tk.X, padx=20, pady=(0, 20))
            
            tk.Label(daily_card, text="7-Day Forecast",
                    font=('Segoe UI', 14, 'bold'),
                    bg=self.card_bg, fg=self.text_dark).pack(anchor=tk.W,
                                                              padx=25, pady=(15, 10))
            

            daily_data = {}
            for item in forecast.get("list", []):
                date = datetime.fromtimestamp(item["dt"]).date()
                if date not in daily_data:
                    daily_data[date] = []
                daily_data[date].append(item)
            
            for date, items in list(daily_data.items())[:7]:
                temps_day = [i["main"]["temp"] for i in items]
                tmax = max(temps_day)
                tmin = min(temps_day)
                icon_d = items[0]["weather"][0].get("icon")
                desc_d = items[0]["weather"][0].get("description", "").capitalize()
                
                day_frame = tk.Frame(daily_card, bg='#f8f9fa')
                day_frame.pack(fill=tk.X, padx=25, pady=5)
                
                tk.Label(day_frame, text=date.strftime("%A"),
                        font=('Segoe UI', 11), width=12,
                        bg='#f8f9fa', fg=self.text_dark, anchor=tk.W).pack(
                        side=tk.LEFT, padx=(10, 0), pady=10)
                
                if icon_d:
                    img_d = fetch_icon_image(icon_d, size=(40, 40))
                    if img_d:
                        lbl = tk.Label(day_frame, image=img_d, bg='#f8f9fa')
                        lbl.image = img_d
                        lbl.pack(side=tk.LEFT, padx=10)
                
                tk.Label(day_frame, text=desc_d, width=20,
                        font=('Segoe UI', 9),
                        bg='#f8f9fa', fg=self.text_light, anchor=tk.W).pack(
                        side=tk.LEFT)
                
                tk.Label(day_frame, 
                        text=f"{round(tmax)}{unit_sym} / {round(tmin)}{unit_sym}",
                        font=('Segoe UI', 11, 'bold'),
                        bg='#f8f9fa', fg=self.text_dark).pack(side=tk.RIGHT,
                                                               padx=15)
            
            tk.Label(daily_card, text="", bg=self.card_bg).pack(pady=5)
            
        except Exception as e:
            self.status_text.set(f"Render error: {e}")

    def _add_detail(self, parent, label, value):
        frame = tk.Frame(parent, bg=self.card_bg)
        frame.pack(anchor=tk.E, pady=3)
        tk.Label(frame, text=f"{label}:", font=('Segoe UI', 10),
                bg=self.card_bg, fg=self.text_light).pack(side=tk.LEFT)
        tk.Label(frame, text=value, font=('Segoe UI', 10, 'bold'),
                bg=self.card_bg, fg=self.text_dark).pack(side=tk.LEFT, padx=(5, 0))

def main():
    if API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
        print("⚠️ Please set API_KEY to your OpenWeatherMap API key")
        print("Get one free at: https://openweathermap.org/api")
        return
    app = WeatherApp()
    app.mainloop()

if __name__ == "__main__":

    main()
