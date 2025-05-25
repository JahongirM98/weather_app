from django.shortcuts import render, redirect
import requests

def index(request):

    weather_data = None
    error = None

    # Получаем или создаём историю
    history = request.session.get('history', [])
    city = ''


    # Очистка истории
    if request.GET.get('clear') == '1':
        request.session['history'] = []
        request.session['last_city'] = ''
        return redirect('index')
    elif request.method == "POST":
        city = request.POST.get('city', '').strip()
        request.session['last_city'] = city
    else:
        city = request.session.get('last_city', '').strip()
    if city:
        try:
            response = requests.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            )
            geo_data = response.json()
            if geo_data.get("results"):
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]

                forecast = requests.get(
                    f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                ).json()

                weather_data = {
                    "city": city,
                    "temperature": forecast["current_weather"]["temperature"],
                    "windspeed": forecast["current_weather"]["windspeed"],
                    "time": forecast["current_weather"]["time"]
                }

                if city not in history:
                    history.append(city)
            else:
                error = "Город не найден."
        except Exception as e:
            error = f"Ошибка запроса: {str(e)}"

    # Сохраняем историю в любом случае
    request.session['history'] = history

    return render(request, 'weather/index.html', {
        "weather": weather_data,
        "error": error,
        "history": history,
        "last_city": city
    })
