import unittest
from app import app

class TestWhiteBox(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_index_route(self):
        # Test the '/' route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        # Test the '/login' route with GET request
        response = self.app.get('/login.html')
        self.assertEqual(response.status_code, 200)

        # Test the '/login' route with POST request
        response = self.app.post('/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_route(self):
        # Test the '/signup' route with GET request
        response = self.app.get('/signup.html')
        self.assertEqual(response.status_code, 200)

        # Test the '/signup' route with POST request
        response = self.app.post('/signup', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_aboutus_route(self):
        # Test the '/aboutus' route
        response = self.app.get('/aboutus.html')
        self.assertEqual(response.status_code, 200)

    def test_model_route(self):
        # Test the '/model' route
        response = self.app.get('/model')
        self.assertEqual(response.status_code, 200)

    def test_modelq_route(self):
        # Test the '/modelq' route
        response = self.app.get('/modelq')
        self.assertEqual(response.status_code, 302)  # Expected redirection to '/model'

if __name__ == '__main__':
    unittest.main()
