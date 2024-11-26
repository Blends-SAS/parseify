import requests
from parseify import BaseScraper

class ScrapingBeeScraper(BaseScraper):
    """
    Scraper implementation using the ScraperAPI service.
    """

    BASE_URL = "https://app.scrapingbee.com/api/v1/"

    def __init__(self, api_key, render=True):
        """
        Initialize the ScraperAPIScraper with configuration options.

        Args:
            api_key (str): API key for ScraperAPI.
            render (bool): Whether to render JavaScript on the page. Defaults to False.
        """
        self.api_key = api_key
        self.render = render

    def fetch(self, url) -> str:
        """
        Fetch the HTML content of a URL using ScraperAPI.

        Args:
            url (str): The URL to scrape.

        Returns:
            str: The HTML content of the page.

        Raises:
            Exception: If the request fails or returns an error.
        """
        params = {
            "api_key": self.api_key,
            "url": url,
            "render_js": "true" if self.render else "false",
        }

        try:
            # Make the GET request to ScraperAPI
            response = requests.get(
                self.BASE_URL,
                headers={"Content-Type": "application/json"},
                params=params,
            )

            # Handle different response scenarios
            if response.status_code == 404:
                return "404"
            elif response.ok:
                return response.text
            else:
                # Log the error and raise an exception
                error_message = f"Failed to fetch data from ScrapingBee: {response.status_code} - {response.text} on URL: {url}"
                print(error_message)  # Replace with logging if needed
                raise Exception(error_message)

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch URL {url} via ScrapingBee: {e}")
