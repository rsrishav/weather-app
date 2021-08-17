import os
import json
import urllib.request
from django.shortcuts import render


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
                "weather_condition_des": list_of_data['weather'][0]['description']
            }
            print(data)
        except Exception as e:
            print(e)
            data = {"data_status": "not_found"}
    else:
        data = {}
    return render(request, "main/index.html", data)
