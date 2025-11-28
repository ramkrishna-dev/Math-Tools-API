# Math Tools API

![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple yet powerful Flask-based API for performing advanced mathematical calculations. This API provides endpoints for factorial, Fibonacci, and primality testing, secured by a feature-based API key system.

## Features

- **Factorial Calculation:** Compute the factorial of a non-negative integer.
- **Fibonacci Sequence:** Generate the nth number in the Fibonacci sequence.
- **Primality Test:** Check if a given integer is a prime number.
- **API Key Authentication:** Secure endpoints with a simple and flexible API key system.
- **Persistent Key Storage:** API keys are stored in a local `api_keys.json` file.

## Getting Started

### Prerequisites

- Python 3.12+
- pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/math-tools-api.git
    cd math-tools-api
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    For development, you can run the app directly. Set the `FLASK_ENV` environment variable to enable debug mode.
    ```bash
    export FLASK_ENV=development
    python math_tools_api/main.py
    ```
    For production, it is recommended to use a production-grade WSGI server like Gunicorn:
    ```bash
    gunicorn --bind 0.0.0.0:8000 "math_tools_api.main:app"
    ```

## API Usage

### 1. Generate an API Key

First, you need to generate an API key to access the math tool endpoints.

- **Endpoint:** `POST /generate_key`
- **Content-Type:** `application/json`

#### Request Body

To generate a key with access to **all** features, use the `*` wildcard:

```json
{
  "features": ["*"]
}
```

To generate a key with **specific** features, provide a list of feature names:

```json
{
  "features": ["factorial", "fibonacci"]
}
```

#### Sample Response

```json
{
  "api_key": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "features": ["factorial", "fibonacci"]
}
```

---

### 2. Accessing Math Endpoints

Include your generated key in the `x-api-key` header for all requests to the math endpoints.

#### Factorial

- **Endpoint:** `GET /math/factorial/<n>`
- **Headers:** `x-api-key: your-api-key`

**Example Request:**
```bash
curl -X GET -H "x-api-key: a1b2c3d4-e5f6-7890-1234-567890abcdef" http://127.0.0.1:5000/math/factorial/10
```

**Sample Response:**
```json
{
  "result": 3628800
}
```

#### Fibonacci

- **Endpoint:** `GET /math/fibonacci/<n>`
- **Headers:** `x-api-key: your-api-key`

**Example Request:**
```bash
curl -X GET -H "x-api-key: a1b2c3d4-e5f6-7890-1234-567890abcdef" http://127.0.0.1:5000/math/fibonacci/10
```

**Sample Response:**
```json
{
  "result": 55
}
```

#### Is Prime

- **Endpoint:** `GET /math/is_prime/<n>`
- **Headers:** `x-api-key: your-api-key`

**Example Request:**
```bash
curl -X GET -H "x-api-key: a1b2c3d4-e5f6-7890-1234-567890abcdef" http://127.0.0.1:5000/math/is_prime/13
```

**Sample Response:**
```json
{
  "result": true
}
```

---

### Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request.

- **400 Bad Request:** The request was malformed (e.g., missing `features` in the body, invalid feature name, or input number is too large).
- **401 Unauthorized:** The `x-api-key` header is missing or the provided key is invalid.
- **403 Forbidden:** The API key is valid, but it does not have permission to access the requested feature.

**Example Error Response:**
```json
{
  "error": "Your API key does not have access to the is_prime feature"
}
```

## Security Warning

> **Note:** This API is designed for demonstration purposes. It stores API keys in a plaintext JSON file (`api_keys.json`). This is **not a secure practice** and should not be used in a production environment. For production use, a secure storage solution such as a database or a secrets management service should be implemented.

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please follow these steps:

1.  **Fork the repository.**
2.  **Create a new branch:** `git checkout -b feature/your-feature-name`
3.  **Make your changes and commit them:** `git commit -m 'Add some feature'`
4.  **Push to the branch:** `git push origin feature/your-feature-name`
5.  **Open a pull request.**

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
