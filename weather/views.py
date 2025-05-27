from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import F

from .models import City
from .open_meteo import OpenMeteo


class CitySearchView(View):
    def get(self, request):
        city = request.GET.get('city', '').strip()
        lang = request.GET.get('lang', 'en').strip()

        data = OpenMeteo(language=lang).get_cities_results_by_name(city)
        return JsonResponse(data, safe=True)


class ForecastBaseView(View):
    forecast_type = None  # 'current', 'historical', 'hourly'

    def get(self, request):
        city = request.GET.get('city', '').strip()
        latitude = float(request.GET.get('latitude', '0.0'))
        longitude = float(request.GET.get('longitude', '0.0'))

        meteo = OpenMeteo()
        data = None

        if self.forecast_type == 'current':
            data = meteo.get_current_forecast_by_coordinates(city, latitude, longitude)
        elif self.forecast_type == 'historical':
            data = meteo.get_hisotrical_forecast_by_coordinates(latitude, longitude)
        elif self.forecast_type == 'hourly':
            data = meteo.get_hourly_forecast_by_coordinates(latitude, longitude)
            if data:
                city, created  = City.objects.get_or_create(name=city, latitude=latitude, longitude=longitude)
                city.searched_count = city.searched_count + 1
                city.save()

        if not data:
            return JsonResponse({"error": "Данные не найдены."}, status=404)

        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


class CurrentForecastView(ForecastBaseView):
    forecast_type = 'current'


class HistoricalForecastView(ForecastBaseView):
    forecast_type = 'historical'


class HourlyForecastView(ForecastBaseView):
    forecast_type = 'hourly'


def index(request):
    return render(request, 'weather/index.html')
