from django.test import TestCase
from django.test import Client

# Create your tests here.
class ShowTestCase(TestCase):

    def test_valid_shows_page(self):
        client = Client()
        response = client.get('http://127.0.0.1:8000/shows/shows/')
        self.assertEqual(response.status_code, 200)

    def test_valid_actors_page(self):
        client = Client()
        response = client.get('http://127.0.0.1:8000/shows/39914/actors')
        self.assertEqual(response.status_code, 200)

    def test_invalid_show_page(self):
        client = Client()
        response = client.get('http://127.0.0.1:8000/shows/shows/39914')
        self.assertEqual(response.status_code, 404)

