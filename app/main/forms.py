from django import forms

class WeatherForm(forms.Form):
    city = forms.CharField(
        label="City name:",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter city name'})
    )
