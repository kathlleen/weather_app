from django.db import models

# Create your models here.
class WeatherModel(models.Model):
    city_name = models.CharField()
    temperature = models.CharField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'