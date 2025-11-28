import json
import os
import unittest
from math_tools_api.main import app, API_KEYS_FILE, save_api_keys

class MathToolsAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.api_keys = {}
        save_api_keys(self.api_keys)

    def tearDown(self):
        if os.path.exists(API_KEYS_FILE):
            os.remove(API_KEYS_FILE)

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Welcome to the Math Tools API!')

    def test_generate_key(self):
        response = self.app.post('/generate_key',
                                 data=json.dumps({'features': ['factorial', 'fibonacci']}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('api_key', data)
        self.assertEqual(data['features'], ['factorial', 'fibonacci'])

    def test_math_endpoints_without_api_key(self):
        response = self.app.get('/math/factorial/5')
        self.assertEqual(response.status_code, 401)
        response = self.app.get('/math/fibonacci/5')
        self.assertEqual(response.status_code, 401)
        response = self.app.get('/math/is_prime/5')
        self.assertEqual(response.status_code, 401)

    def test_math_endpoints_with_invalid_api_key(self):
        response = self.app.get('/math/factorial/5', headers={'x-api-key': 'invalid-key'})
        self.assertEqual(response.status_code, 401)

    def test_math_endpoints_with_unauthorized_api_key(self):
        response = self.app.post('/generate_key',
                                 data=json.dumps({'features': ['factorial']}),
                                 content_type='application/json')
        api_key = json.loads(response.data.decode())['api_key']
        response = self.app.get('/math/fibonacci/5', headers={'x-api-key': api_key})
        self.assertEqual(response.status_code, 403)

    def test_factorial_endpoint(self):
        response = self.app.post('/generate_key',
                                 data=json.dumps({'features': ['factorial']}),
                                 content_type='application/json')
        api_key = json.loads(response.data.decode())['api_key']
        response = self.app.get('/math/factorial/5', headers={'x-api-key': api_key})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode())['result'], 120)

    def test_fibonacci_endpoint(self):
        response = self.app.post('/generate_key',
                                 data=json.dumps({'features': ['fibonacci']}),
                                 content_type='application/json')
        api_key = json.loads(response.data.decode())['api_key']
        response = self.app.get('/math/fibonacci/5', headers={'x-api-key': api_key})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode())['result'], 5)

    def test_is_prime_endpoint(self):
        response = self.app.post('/generate_key',
                                 data=json.dumps({'features': ['is_prime']}),
                                 content_type='application/json')
        api_key = json.loads(response.data.decode())['api_key']
        response = self.app.get('/math/is_prime/5', headers={'x-api-key': api_key})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode())['result'], True)
        response = self.app.get('/math/is_prime/4', headers={'x-api-key': api_key})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode())['result'], False)

    def test_generate_key_with_wildcard(self):
        response = self.app.post('/generate_key',
                                 data=json.dumps({'features': ['*']}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('api_key', data)
        self.assertEqual(data['features'], ['factorial', 'fibonacci', 'is_prime'])
        api_key = data['api_key']
        response = self.app.get('/math/factorial/5', headers={'x-api-key': api_key})
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/math/fibonacci/5', headers={'x-api-key': api_key})
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/math/is_prime/5', headers={'x-api-key': api_key})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
