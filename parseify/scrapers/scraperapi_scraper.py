import requests
from parseify import BaseScraper

class ScraperAPIScraper(BaseScraper):
    """
    Scraper implementation using the ScraperAPI service.
    """

    BASE_URL = "https://api.scraperapi.com"

    def __init__(self, api_key, default_tld="fr", default_country="fr", timeout=100, render=True, premium_level="none"):
        """
        Initialize the ScraperAPIScraper with configuration options.

        Args:
            api_key (str): API key for ScraperAPI.
            default_tld (str): Default top-level domain (e.g., 'fr').
            default_country (str): Default country code (e.g., 'fr').
            timeout (int): Timeout for HTTP requests in seconds. Defaults to 100.
            render (bool): Whether to render JavaScript on the page. Defaults to False.
            premium_level (str): Premium level ('none', 'premium', 'ultra'). Defaults to 'none'.
        """
        self.api_key = api_key
        self.default_tld = default_tld
        self.default_country = default_country
        self.timeout = timeout
        self.render = render
        self.premium_level = premium_level

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
            "tld": self.default_tld,
            "country_code": self.default_country,
            "render": "true" if self.render else "false",
            "premium": "true" if self.premium_level != "none" else "false",
            "ultra_premium": "true" if self.premium_level == "ultra" else "false",
        }

        try:
            # Make the GET request to ScraperAPI
            response = requests.get(
                self.BASE_URL,
                headers={"Content-Type": "application/json"},
                params=params,
                timeout=self.timeout,
            )

            # Handle different response scenarios
            if response.status_code == 404:
                return "404"
            elif response.ok:
                return response.text
            else:
                # Log the error and raise an exception
                error_message = f"Failed to fetch data from ScraperAPI: {response.status_code} - {response.text} on URL: {url}"
                print(error_message)  # Replace with logging if needed
                raise Exception(error_message)

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch URL {url} via ScraperAPI: {e}")
