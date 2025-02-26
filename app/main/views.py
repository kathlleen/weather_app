import os

from django.shortcuts import render
import requests

from django.views.generic import FormView
from .models import WeatherModel
from django.utils.timezone import now
from .forms import WeatherForm
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

class WeatherView(FormView):
    template_name = "index.html"
    form_class = WeatherForm

    def form_valid(self, form):
        city = form.cleaned_data["city"]

        weather_url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}'
        weather_response = requests.get(weather_url)

        if weather_response.status_code != 200:
            return self.render_to_response({"form": form, "error": "Не удалось получить данные о погоде"})

        weather_data = weather_response.json()
        self.save_weather_data(city, weather_data)

        city_weather = WeatherModel.objects.filter(city_name=city).order_by('-timestamp').first()

        context = {
            'title': 'Погода на сегодня',
            'form': form,
            'city_weather': city_weather,
        }
        return self.render_to_response(context)

    def save_weather_data(self, city, weather_data):
        location = weather_data["location"]
        current = weather_data["current"]

        WeatherModel.objects.create(
            city_name=location["name"],
            country=location["country"],
            latitude=location["lat"],
            longitude=location["lon"],
            timestamp=now(),
            temperature_c=current["temp_c"],
            feels_like_c=current["feelslike_c"],
            condition=current["condition"]["text"],
            icon_url=f"https:{current['condition']['icon']}",
            wind_speed_kph=current["wind_kph"],
            humidity=current["humidity"],
            pressure_mb=current["pressure_mb"]
        )


def query(request):

    weather_history = WeatherModel.objects.all()

    context = {
        'title': 'Query history',
        'weather_history' : weather_history,
    }
    return render(request, 'query.html', context)

