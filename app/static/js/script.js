
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("weather-form");
    form.addEventListener("submit", function(event) {
        const cityInput = document.getElementById("city");
        if (!cityInput.value.trim()) {
            event.preventDefault();
            alert("Please enter a city name.");
        }
    });
});
