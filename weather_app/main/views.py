import os
import json
import urllib.request
from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        # source contain JSON data from API

        source = urllib.request.urlopen(f"http://api.openweathermap.org/data/2.5/weather?"
                                        f"q={city}&appid={os.environ['WEATHER_API']}").read()

        # converting JSON data to a dictionary
        list_of_data = json.loads(source)

        # data for variable list_of_data
        data = {
            "city_name": list_of_data['name'],
            "country_code": (list_of_data['sys']['country']),
            "coordinate": f"{(list_of_data['coord']['lon'])} {(list_of_data['coord']['lat'])}",
            "temp": (list_of_data['main']['temp']),
            "feels_like": list_of_data['main']['feels_like'],
            "temp_max": list_of_data['main']['temp_max'],
            "temp_min": list_of_data['main']['temp_min'],
            "pressure": (list_of_data['main']['pressure']),
            "humidity": (list_of_data['main']['humidity']),
            "weather_condition": list_of_data['weather'][0]['main'],
            "weather_condition_des": list_of_data['weather'][0]['description']
        }
        print(data)
    else:
        data = {}
    return render(request, "main/index.html", data)
