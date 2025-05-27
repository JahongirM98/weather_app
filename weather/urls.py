from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/cities/', views.CitySearchView.as_view(), name='search_cities_api'),
    path('api/forecast/', views.CurrentForecastView.as_view(), name='forecast_api'),
    path('api/historical/', views.HistoricalForecastView.as_view(), name='historical_api'),
    path('api/hourly/', views.HourlyForecastView.as_view(), name='hourly_api'),
]
