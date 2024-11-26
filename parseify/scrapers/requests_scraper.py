import requests
from parseify import BaseScraper

class RequestsScraper(BaseScraper):
    """
    A scraper implementation using the requests library.
    """

    def __init__(self, headers=None, timeout=10):
        """
        Initialize the scraper with optional headers and timeout.

        Args:
            headers (dict): Custom headers for the requests. Defaults to a common User-Agent.
            timeout (int): Request timeout in seconds. Defaults to 10.
        """
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        self.timeout = timeout

    def fetch(self, url: str) -> str:
        """
        Fetch the raw HTML content of the given URL using the requests library.

        Args:
            url (str): The URL to scrape.

        Returns:
            str: The HTML content of the page.

        Raises:
            Exception: If the request fails or returns a non-200 status code.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
            return response.text  # Return the raw HTML content
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch URL {url}: {e}")
