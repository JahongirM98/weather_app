from django.test import TestCase, Client
from django.urls import reverse


class WeatherAPITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Погода в городе")

    def test_city_autocomplete_api(self):
        response = self.client.get('/api/cities/', {'city': 'Paris', 'lang': 'en'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())

    def test_current_forecast_api_success(self):
        response = self.client.get('/api/forecast/', {
            'city': 'London',
            'latitude': '51.5074',
            'longitude': '-0.1278'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('temperature', response.json())

    def test_hourly_forecast_api_and_history(self):
        response = self.client.get('/api/hourly/', {
            'city': 'London',
            'latitude': '51.5074',
            'longitude': '-0.1278'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('temperature_2m', response.json())

        # Проверка, что город сохранился в базе
        from weather.models import City
        self.assertTrue(City.objects.filter(name='London').exists())

    def test_historical_forecast_api(self):
        response = self.client.get('/api/historical/', {
            'city': 'London',
            'latitude': '51.5074',
            'longitude': '-0.1278'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('temperature_2m_max', response.json())
