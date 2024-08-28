
# Cốc Cốc & Google Search API

This is a Flask-based web application that provides an API to perform keyword searches on both Google and Cốc Cốc simultaneously. The application fetches and returns search results from both search engines in a unified JSON format.

## Features

- **Dual Search Engine Integration**: Fetch search results from both Google and Cốc Cốc.
- **Asynchronous Requests**: Utilizes `aiohttp` and `asyncio` to perform non-blocking, concurrent HTTP requests, ensuring fast and efficient responses.
- **Error Handling**: Includes comprehensive error handling for timeouts, client errors, and JSON parsing issues.
- **CORS Enabled**: Configured to accept requests from any domain using Flask-CORS.
- **Custom Response Structure**: Results are formatted and returned as JSON, including both the title and description of each search result.
- **Unit Testing**: Basic unit tests to ensure the correct functionality of the API endpoints.

## Application Design

### Architecture

- **Flask Framework**: The core web framework for handling HTTP requests and routing.
- **Service Layer**: Encapsulates the logic for interacting with Google and Cốc Cốc, including request handling and response parsing.
- **Asynchronous Fetching**: Uses `asyncio` and `aiohttp` to perform concurrent requests to the search engines, reducing latency.
- **Response Handling**: The service layer is responsible for constructing the HTTP responses, ensuring separation of concerns.

### Project Structure

```
/my_flask_app
│
├── app.py                # Main Flask application entry point
├── /service              # Directory containing service classes
│   ├── __init__.py
│   ├── GoogleFetchService.py   # Service for fetching results from Google
│   └── CoccocFetchService.py   # Service for fetching results from Cốc Cốc
└── /tests                # Directory containing test cases
    ├── __init__.py
    └── test_app.py       # Unit tests for the application
```

### Endpoint Documentation

- **GET `/search`**
  - **Description**: Searches both Google and Cốc Cốc for the provided keyword.
  - **Parameters**: 
    - `keyword` (string): The search term to query.
  - **Response**: JSON containing the search results from both Google and Cốc Cốc.
  - **Example Request**:
    ```
    GET /search?keyword=flask
    ```
  - **Example Response**:
    ```json
    {
      "google": [
        {"title": "Flask - Web Development", "description": "Flask is a micro web framework written in Python."}
      ],
      "coccoc": [
        {"title": "Flask - Web Framework", "description": "Flask is a popular web framework for Python."}
      ]
    }
    ```

## Setup & Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts ctivate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Flask application**:
    ```bash
    python app.py
    ```

5. **Access the application**:
    Open your web browser and go to `http://localhost:5000`.

## Running Tests

1. **Navigate to the tests directory**:
    ```bash
    cd tests
    ```

2. **Run the tests using `unittest`**:
    ```bash
    python -m unittest test_app.py
    ```

## Contributions

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
