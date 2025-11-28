import json
import uuid
from functools import wraps
from flask import Flask, jsonify, request

app = Flask(__name__)

API_KEYS_FILE = 'api_keys.json'

def load_api_keys():
    try:
        with open(API_KEYS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_api_keys(api_keys):
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(api_keys, f, indent=2)

api_keys = load_api_keys()

AVAILABLE_FEATURES = ['factorial', 'fibonacci', 'is_prime']

@app.route('/')
def home():
    return "Welcome to the Math Tools API!"

@app.route('/generate_key', methods=['POST'])
def generate_key():
    data = request.get_json()
    if not data or 'features' not in data:
        return jsonify({'error': 'Features not provided'}), 400

    features = data['features']
    if features == ['*']:
        features = AVAILABLE_FEATURES
    else:
        for feature in features:
            if feature not in AVAILABLE_FEATURES:
                return jsonify({'error': f'Invalid feature: {feature}'}), 400

    api_key = str(uuid.uuid4())
    api_keys[api_key] = features
    save_api_keys(api_keys)
    return jsonify({'api_key': api_key, 'features': features})


def require_api_key(feature):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('x-api-key')
            if not api_key or api_key not in api_keys:
                return jsonify({'error': 'Invalid or missing API key'}), 401

            user_features = api_keys.get(api_key, [])
            if feature not in user_features:
                return jsonify({'error': f'Your API key does not have access to the {feature} feature'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

@app.route('/math/factorial/<int:n>', methods=['GET'])
@require_api_key('factorial')
def get_factorial(n):
    if n > 1000:
        return jsonify({'error': 'Input number is too large'}), 400
    try:
        result = factorial(n)
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

def fibonacci(n):
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@app.route('/math/fibonacci/<int:n>', methods=['GET'])
@require_api_key('fibonacci')
def get_fibonacci(n):
    if n > 1000:
        return jsonify({'error': 'Input number is too large'}), 400
    try:
        result = fibonacci(n)
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

def is_prime(n):
  if n <= 1:
    return False
  for i in range(2, int(n**0.5) + 1):
    if n % i == 0:
      return False
  return True

@app.route('/math/is_prime/<int:n>', methods=['GET'])
@require_api_key('is_prime')
def get_is_prime(n):
    if n > 1000:
        return jsonify({'error': 'Input number is too large'}), 400
    return jsonify({'result': is_prime(n)})

if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode)
