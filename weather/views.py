from django.shortcuts import render
import requests


def index(request):
    city = None
    weather_data = None
    error = None

    # Очистка истории
    if request.GET.get('clear') == '1':
        request.session['history'] = []
        request.session['last_city'] = ''

    # POST: ввод нового города
    if request.method == "POST":
        city = request.POST.get('city')
        request.session['last_city'] = city

        history = request.session.get('history', [])
        if city and city not in history:
            history.append(city)
            request.session['history'] = history
    # GET: берём город из сессии
    else:
        city = request.session.get('last_city')

    if city:
        try:
            response = requests.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            )
            geo_data = response.json()
            if geo_data.get("results"):
                latitude = geo_data["results"][0]["latitude"]
                longitude = geo_data["results"][0]["longitude"]

                forecast = requests.get(
                    f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
                ).json()

                weather_data = {
                    "city": city,
                    "temperature": forecast["current_weather"]["temperature"],
                    "windspeed": forecast["current_weather"]["windspeed"],
                    "time": forecast["current_weather"]["time"]
                }
            else:
                error = "Город не найден."
        except Exception as e:
            error = f"Ошибка запроса: {str(e)}"

    return render(request, 'weather/index.html', {
        "weather": weather_data,
        "error": error,
        "history": request.session.get('history', [])
    })
