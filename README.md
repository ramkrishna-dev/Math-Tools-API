# Math Tools API

This API provides a set of advanced math tools.

## Getting Started

### Prerequisites

- Python 3
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/math-tools-api.git
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python math_tools_api/main.py
   ```

## Usage

### Generate an API Key

To use the math tool endpoints, you first need to generate an API key.

**Endpoint:** `POST /generate_key`

**Request Body:**

To generate a key with access to all features, use the `*` wildcard:

```json
{
  "features": ["*"]
}
```

To generate a key with specific features, provide a list of feature names:

```json
{
  "features": ["factorial", "fibonacci"]
}
```

## Security Warning

This API stores API keys in a plaintext JSON file (`api_keys.json`). This is not a secure practice and should not be used in a production environment.

**Response:**

```json
{
  "api_key": "your-new-api-key",
  "features": ["factorial", "fibonacci", "is_prime"]
}
```

### Math Tool Endpoints

**Factorial**

**Endpoint:** `GET /math/factorial/<n>`

**Headers:**

- `x-api-key`: `your-api-key`

**Fibonacci**

**Endpoint:** `GET /math/fibonacci/<n>`

**Headers:**

- `x-api-key`: `your-api-key`

**Is Prime**

**Endpoint:** `GET /math/is_prime/<n>`

**Headers:**

- `x-api-key`: `your-api-key`
