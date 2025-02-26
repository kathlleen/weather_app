from django.urls import reverse
from unittest.mock import patch

from django.utils.timezone import now

from django.test import TestCase

from main.models import WeatherModel


# Create your tests here.
class TestWeather(TestCase):

    def test_get_weather_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @patch('requests.get')
    def test_post_valid_city(self, mock_get):
        mock_response_data = {
            "location": {
                "name": "London",
                "country": "United Kingdom",
                "lat": 51.5171,
                "lon": -0.1062
            },
            "current": {
                "temp_c": 10.5,
                "feelslike_c": 9.0,
                "condition": {"text": "Clear", "icon": "//cdn.weatherapi.com/weather/icon.png"},
                "wind_kph": 12.5,
                "humidity": 80,
                "pressure_mb": 1012.0
            }
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        response = self.client.post(reverse('index'), {'city': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Weather in London, United Kingdom")

        # запись добавилась в БД
        self.assertEqual(WeatherModel.objects.count(), 1)
        weather = WeatherModel.objects.first()
        self.assertEqual(weather.city_name, "London")
        self.assertEqual(weather.temperature_c, 10.5)
        self.assertEqual(weather.condition, "Clear")

    @patch('requests.get')
    def test_post_invalid_city(self, mock_get):
        mock_get.return_value.status_code = 404

        response = self.client.post(reverse('index'), {'city': 'FakeCity'})
        self.assertEqual(response.status_code, 200)

        # в бд ничего не добавилось
        self.assertEqual(WeatherModel.objects.count(), 0)

    def test_query_history(self):
        response = self.client.get(reverse('query-history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'query.html')

    def test_load_data(self):
        WeatherModel.objects.create(
            city_name="London",
            country="UK",
            latitude=51.5074,
            longitude=-0.1278,
            timestamp=now(),
            temperature_c=12.5,
            feels_like_c=11.0,
            condition="Clear",
            icon_url="https://example.com/icon.png",
            wind_speed_kph=10.2,
            humidity=60,
            pressure_mb=1015,
        )

        response = self.client.get(reverse('query-history'))
        self.assertEqual(response.status_code, 200)

        # данные переданы в шаблон
        self.assertIn('weather_history', response.context)
        self.assertEqual(len(response.context['weather_history']), 1)

        # данные корректны
        city_weather = response.context['weather_history'][0]
        self.assertEqual(city_weather.city_name, "London")
        self.assertEqual(city_weather.temperature_c, 12.5)
        self.assertEqual(city_weather.condition, "Clear")
