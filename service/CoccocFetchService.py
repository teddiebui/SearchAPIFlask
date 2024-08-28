import aiohttp
import asyncio
from flask import jsonify, Response
import json
import re

# Service class that can be called by the main controller
# Used to make search requests to Cốc Cốc
class CoccocFetchService:
    COCCOC_SEARCH_URL = "https://coccoc.com/search?query={}"
    TIMEOUT_SECONDS = 10
    
    # Simulate a browser to ensure search results are more easily parsed
    HEADERS = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    def __init__(self):
        # Initialize the service with a timeout configuration for HTTP requests
        self.timeout = aiohttp.ClientTimeout(total=self.TIMEOUT_SECONDS)

    async def _fetch(self, session, keyword):
        """
        Private method to perform the HTTP GET request to Cốc Cốc Search.
        Parameters:
            session: The aiohttp client session to make the request.
            keyword: The search keyword to query Cốc Cốc with.
        Returns:
            The raw HTML response text or a JSON response if an error occurs.
        """
        url = self.COCCOC_SEARCH_URL.format(keyword)
        try:
            # Perform the GET request with a simulated browser header
            async with session.get(url, headers=self.HEADERS, timeout=self.timeout) as response:
                response.raise_for_status()  # Raise an error for bad HTTP status codes
                return await response.text()  # Return the HTML text
        except asyncio.TimeoutError:
            # Handle timeout errors
            return self._create_response({"error": "Connection timeout"}, 500)
        except aiohttp.ClientError as e:
            # Handle other HTTP client errors
            return self._create_response({"error": f"HTTP error occurred: {str(e)}"}, 500)

    def _parse_results(self, html):
        """
        Private method to parse the HTML content and extract search results.
        Parameters:
            html: The raw HTML content returned from Cốc Cốc Search.
        Returns:
            A list of dictionaries containing the title and description of each search result.
        """
        if isinstance(html, dict) and "error" in html:
            # Return the error if the HTML is actually an error response
            return html

        results = []
        
        # Find the <script> tag within <head> containing the JSON search results
        json_data = re.findall(r"<script.*?window\.composerResponse\s*=\s*(.*?);</script>", html, re.S|re.I)[0]
        if len(json_data) > 0:
            try:
                # Load the JSON data from the <script> tag
                json_data = json.loads(json_data)
                # Filter search results with type 'search'
                for item in json_data['search']['search_results']:
                    try:
                        if item['type'] != 'search':
                            continue
                        title = item['title']
                        description = item['content']
                        results.append({"title": title, "description": description})
                    except KeyError as e:
                        # If a key error occurs, save the HTML to a file and return an error response
                        with open("result.html", "w", encoding="utf-8") as f:
                            f.write(html)
                        return self._create_response({"error": "Coccoc error."}, 500)
                    
            except json.JSONDecodeError:
                # Handle JSON parsing errors
                return self._create_response({"error": "Failed to parse JSON"}, 500)

        return results

    async def fetch_results(self, keyword):
        """
        Public method to initiate the fetch process and parse the results.
        Parameters:
            keyword: The search keyword to query Cốc Cốc with.
        Returns:
            A Flask JSON response with the search results or an error message.
        """
        async with aiohttp.ClientSession() as session:
            coccoc_html = await self._fetch(session, keyword)
            if isinstance(coccoc_html, Response):  # If the result is already a response, return it
                return coccoc_html
            
            coccoc_results = self._parse_results(coccoc_html)
            return self._create_response({"coccoc": coccoc_results}, 200)

    def _create_response(self, data, status_code):
        """
        Private method to create a Flask JSON response.
        Parameters:
            data: The data to be included in the response body.
            status_code: The HTTP status code for the response.
        Returns:
            A Flask response object with the JSON data and status code.
        """
        return jsonify(data), status_code
