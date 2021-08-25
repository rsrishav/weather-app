import time
import os
import json
import urllib.request
from django.shortcuts import render, HttpResponse
import requests

HEADERS = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.carwale.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

NO_OF_RECORDS = 10


def get_time(epoch_time):
    # return time.strftime('%H:%M', time.localtime(time.time()))
    return time.strftime('%H:%M', time.localtime(epoch_time))


def weather_icons(weather):
    selector = {
        "haze": "fas fa-smog",
        "clouds": "fas fa-cloud-sun",
        "rain": "fas fa-cloud-rain",
        "sun": "fas fa-sun"
    }
    return selector.get(weather.lower(), "fas fa-sun")
# https://www.carwale.com/api/v2/autocomplete/city/?term=a


def weather_img(weather):
    selector = {
        "haze": "haze",
        "clouds": "clouds",
        "rain": "rain",
        "sun": "sun"
    }
    return selector.get(weather.lower(), "fas fa-sun")


def get_cities(request, search_city):
    data = "[]"
    if request.method == 'GET' and search_city not in ["null", None]:
        data = (requests.get(f"https://www.carwale.com/api/v2/autocomplete/city/?term={search_city}"
                             f"&record={NO_OF_RECORDS}&sourceId=1", headers=HEADERS).text)
        print(data)
    return HttpResponse(data)


def index(request):
    if request.method == 'POST':
        city = request.POST['city'].replace(" ", "")
        # source contain JSON data from API

        try:
            source = urllib.request.urlopen(f"http://api.openweathermap.org/data/2.5/weather?q={city}"
                                            f"&appid={os.environ['WEATHER_API']}").read()

            # converting JSON data to a dictionary
            list_of_data = json.loads(source)

            # data for variable list_of_data
            data = {
                "city_name": list_of_data['name'],
                "country_code": (list_of_data['sys']['country']),
                "coordinate": f"{(list_of_data['coord']['lon'])} {(list_of_data['coord']['lat'])}",
                "temp": f"{round(float(list_of_data['main']['temp'])-273.15, 1)}\u00B0C",
                "feels_like": f"{round(float(list_of_data['main']['feels_like'])-273.15, 1)}\u00B0C",
                "temp_max": f"{round(float(list_of_data['main']['temp_max'])-273.15, 1)}\u00B0C",
                "temp_min": f"{round(float(list_of_data['main']['temp_min'])-273.15, 1)}\u00B0C",
                "pressure": (list_of_data['main']['pressure']),
                "humidity": f"{list_of_data['main']['humidity']}",
                "weather_condition": list_of_data['weather'][0]['main'],
                "weather_condition_des": list_of_data['weather'][0]['description'],
                "wind": list_of_data['wind']['speed'],
                "weather_icon": weather_icons(list_of_data["weather"][0]["main"]),
                "weather_img": weather_img(list_of_data["weather"][0]["main"]),
                "time": get_time(list_of_data["dt"])
            }

            print(data)
        except Exception as e:
            print(e)
            data = {"data_status": "not_found"}
    else:
        data = {}
    return render(request, "main/index.html", data)
