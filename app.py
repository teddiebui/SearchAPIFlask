from flask import Flask, request, jsonify
from flask_cors import CORS
from service.GoogleFetchService import GoogleFetchService
from service.CoccocFetchService import CoccocFetchService
import asyncio

# Initialize the Flask application
app = Flask(__name__)

# Instantiate the services
google_service = GoogleFetchService()
coccoc_service = CoccocFetchService()

# Configure CORS to accept all requests from any domain
CORS(app)

@app.route('/')
def home():
    """Simple home endpoint to check if the server is running."""
    return 'Hello World!'

@app.route('/search', methods=['GET'])
async def search():
    """
    Search endpoint that fetches results from both Google and Cốc Cốc.
    This endpoint accepts a 'keyword' parameter and returns search results
    from both search engines in a JSON format.
    """
    # Get the search keyword from the query parameters
    keyword = request.args.get('keyword')
    
    # If 'keyword' is missing, return a 400 Bad Request response
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    
    # Initiate asynchronous tasks to fetch results from both services concurrently
    google_task = asyncio.create_task(google_service.fetch_results(keyword))
    coccoc_task = asyncio.create_task(coccoc_service.fetch_results(keyword))
    
    # Await the completion of both tasks
    google_results, coccoc_results = await asyncio.gather(google_task, coccoc_task)
    
    # Construct the final response with results from both services
    result = {
        "google": google_results[0].json['google'],
        "coccoc": coccoc_results[0].json['coccoc']
    }
    
    # Return the JSON response
    return result

# After each request, set the Content-Type header to ensure responses are returned as JSON with UTF-8 encoding
@app.after_request
def setResponseHeaders(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# Start the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
