import unittest
from app import app

class TestFunctional(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home_page(self):
        # Test accessing the home page
        response = self.app.get('/')
        self.assertIn(b'Responsive Login and Signup Form', response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        # Test accessing the login page
        response = self.app.get('/login.html')
        self.assertIn(b'Login', response.data)
        self.assertEqual(response.status_code, 200)

    def test_aboutus_page(self):
        # Test accessing the about us page
        response = self.app.get('/aboutus.html')
        self.assertIn(b'AI ENABLED CAR PARKING USING OPENCV', response.data)
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        # Test accessing the signup page
        response = self.app.get('/signup.html')
        self.assertIn(b'Register', response.data)
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        # Test successful login
        response = self.app.post('/login', data={'email': 'valid_email@example.com', 'password': 'valid_password'}, follow_redirects=True)
        self.assertIn(b'Check the Parking Slot', response.data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        # Test invalid login
        response = self.app.post('/login', data={'email': 'invalid_email@example.com', 'password': 'invalid_password'}, follow_redirects=True)
        self.assertIn(b'Incorrect Email/password', response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
