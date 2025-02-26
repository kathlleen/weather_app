from django.db import models

# Create your models here.
class WeatherModel(models.Model):
    # Информация о запросе
    city_name = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    # Данные о погоде
    temperature_c = models.FloatField(null=True)
    feels_like_c = models.FloatField(null=True)
    condition = models.CharField(max_length=100, null=True)
    icon_url = models.URLField(null=True)
    wind_speed_kph = models.FloatField(null=True)
    humidity = models.IntegerField(null=True)
    pressure_mb = models.FloatField(null=True)

    def __str__(self):
        return f"{self.city_name}, {self.country} - {self.temperature_c}°C ({self.timestamp})"