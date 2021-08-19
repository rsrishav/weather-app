import os
import json
import urllib.request
from django.shortcuts import render


def weather_icons(weather):
    selector = {
        "haze": "fas fa-smog",
        "clouds": "fas fa-cloud-sun"
    }
    return selector.get(weather.lower(), "fas fa-sun")


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        # source contain JSON data from API

        try:
            source = urllib.request.urlopen(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.environ['WEATHER_API']}").read()

            # converting JSON data to a dictionary
            list_of_data = json.loads(source)

            # data for variable list_of_data
            data = {
                "city_name": list_of_data['name'],
                "country_code": (list_of_data['sys']['country']),
                "coordinate": f"{(list_of_data['coord']['lon'])} {(list_of_data['coord']['lat'])}",
                "temp": f"{round(float(list_of_data['main']['temp'])-273.15, 2)}\u00B0C",
                "feels_like": f"{round(float(list_of_data['main']['feels_like'])-273.15, 2)}\u00B0C",
                "temp_max": f"{round(float(list_of_data['main']['temp_max'])-273.15, 2)}\u00B0C",
                "temp_min": f"{round(float(list_of_data['main']['temp_min'])-273.15, 2)}\u00B0C",
                "pressure": (list_of_data['main']['pressure']),
                "humidity": f"{list_of_data['main']['humidity']}%",
                "weather_condition": list_of_data['weather'][0]['main'],
                "weather_condition_des": list_of_data['weather'][0]['description'],
                "weather_icon": weather_icons(list_of_data["weather"][0]["main"])
            }
            # data = {'city_name': 'Delhi', 'country_code': 'IN', 'coordinate': '77.2167 28.6667', 'temp': '34.05°C', 'feels_like': '40.31°C', 'temp_max': '35.17°C', 'temp_min': '34.05°C', 'pressure': 1000, 'humidity': '55%', 'weather_condition': 'Haze', 'weather_condition_des': 'haze'}
            # data["weather_icon"] = weather_icons("Haze")
            print(data)
        except Exception as e:
            print(e)
            data = {"data_status": "not_found"}
    else:
        data = {}
    return render(request, "main/index.html", data)
