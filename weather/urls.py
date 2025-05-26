from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/history', views.history_api, name='history_api'),
]
