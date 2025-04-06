from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "8c8ffb446a4b46122f2befdcbc6057f6"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    """Fetch weather details for a given city"""
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "weather_description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "sunrise": data["sys"]["sunrise"],
            "sunset": data["sys"]["sunset"]
        }
        return weather_info
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            weather_data = get_weather_data(city)
    return render_template("index.html", weather=weather_data)

@app.route("/api/weather/<city>")
def weather_api(city):
    """API Endpoint to get weather details"""
    weather_data = get_weather_data(city)
    if weather_data:
        return jsonify(weather_data)
    return jsonify({"error": "City not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
