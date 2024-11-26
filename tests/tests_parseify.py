import os
from parseify import OpenAIParser, RequestsScraper, ScraperAPIScraper, ScrapingBeeScraper, WebsiteAnalyzer

import dotenv
dotenv.load_dotenv()

OPEN_AI_KEY = os.environ.get("OPENAI_API_KEY")
SCRAPER_API_SCRAPER_KEY = os.environ.get("SCRAPER_API_SCRAPE_KEY")
SCRAPINGBEE_API_SCRAPER_KEY = os.environ.get("SCRAPINGBEE_API_SCRAPER_KEY")

def test_parseify():

    # All scraper
    scraper = ScraperAPIScraper(api_key=SCRAPER_API_SCRAPER_KEY)
    scraper = RequestsScraper()
    scraper = ScrapingBeeScraper(api_key= SCRAPINGBEE_API_SCRAPER_KEY, render=False)

    # All parsers
    parser = OpenAIParser(api_key=OPEN_AI_KEY)

    analyzer = WebsiteAnalyzer(scraper_engine=scraper, parser_engine=parser)


    # Define schema
    schema = {
        "mission": "La mission de l'entreprise",
        "news": "Actualités de l'entreprise",
    }

    # Analyze a website
    results = analyzer.analyze("https://mistral.ai/fr/", schema)

    # Assert that every key is in restult
    for key in list(schema.keys()):
        assert key in results
