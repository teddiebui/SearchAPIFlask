import aiohttp
import asyncio
from bs4 import BeautifulSoup
from flask import jsonify, Response

# Service class that can be called by the main controller
# Used to make search requests to Google
class GoogleFetchService:
    GOOGLE_SEARCH_URL = "https://www.google.com/search?q={}"
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
        Private method to perform the HTTP GET request to Google Search.
        Parameters:
            session: The aiohttp client session to make the request.
            keyword: The search keyword to query Google with.
        Returns:
            The raw HTML response text or a JSON response if an error occurs.
        """
        url = self.GOOGLE_SEARCH_URL.format(keyword)
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
            html: The raw HTML content returned from Google Search.
        Returns:
            A list of dictionaries containing the title and description of each search result.
        """
        if isinstance(html, dict) and "error" in html:
            # Return the error if the HTML is actually an error response
            return html

        soup = BeautifulSoup(html, 'lxml')
        results = []

        # Inspecting Google HTML shows that each search result is within a div with class "g"
        # Each result has 3 direct child divs
        # Loop through each result to extract the `title` and `description`
        for item in soup.select('div.g'):
            title_container = item.find_all('div')[1] if len(item.find_all('div')) > 1 else None
            title_tag = title_container.find('span') if title_container else None
            description_container = item.find_all('div')[1] if len(item.find_all('div')) > 1 else None
            description_tag = description_container.find('span') if description_container else None
            
            if title_tag and description_tag:
                title = title_tag.text
                description = description_tag.text
                results.append({"title": title, "description": description})

        return results

    async def fetch_results(self, keyword):
        """
        Public method to initiate the fetch process and parse the results.
        Parameters:
            keyword: The search keyword to query Google with.
        Returns:
            A Flask JSON response with the search results or an error message.
        """
        async with aiohttp.ClientSession() as session:
            google_html = await self._fetch(session, keyword)
            if isinstance(google_html, Response):  # If the result is already a response, return it
                return google_html
            
            google_results = self._parse_results(google_html)
            return self._create_response({"google": google_results}, 200)

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
