import unittest
from flask import request, session
from app import app

class TestLogin(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_successful_login(self):
        # Simulate a POST request to the login route with valid credentials
        response = self.app.post('/login', data={'email': '', 'password': ''}, follow_redirects=True)

        # Check that the response status code is 200 (indicating success)
        self.assertEqual(response.status_code, 200)

        # Check that the 'Loggedin' key is set to True in the session
        with self.app as client:
            with client.session_transaction() as sess:
                self.assertTrue(sess['Loggedin'])

        # Optionally, check if the user is redirected to the expected page
        self.assertIn(b'Check the Parking Slot', response.data)

    def test_invalid_login(self):
        # Simulate a POST request to the login route with invalid credentials
        response = self.app.post('/login', data={'email': 'invalid_email@example.com', 'password': 'invalid_password'}, follow_redirects=True)

        # Check that the response status code is 200 (indicating success)
        self.assertEqual(response.status_code, 200)

        # Check that the 'Loggedin' key is not set in the session, indicating a failed login
        with self.app as client:
            with client.session_transaction() as sess:
                self.assertNotIn('Loggedin', sess)

        # Check if the response contains a message indicating incorrect email/password
        self.assertIn(b'Incorrect Email/password', response.data)

if __name__ == '__main__':
    unittest.main()
