from django.test import TestCase, Client

class WeatherTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_valid_city_forecast(self):
        response = self.client.post('/', {'city': 'London'})
        self.assertContains(response, 'Погода в London', status_code=200)

    def test_invalid_city_shows_error(self):
        response = self.client.post('/', {'city': 'Несуществующийгород123'})
        self.assertContains(response, 'Город не найден', status_code=200)
