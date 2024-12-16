# Parseify

Get any information from any website you need.

## Installation

```bash
pip install parseify
```

## Usage

Quick notes: 

* You can set the ```max_links```  parameter to restrict the maximum of links that the progran can navigate to find your requested information.  ```
* Set ```translate = None ``` to return the results in the original language! or translate them to the language of your choice.

```python
from parseify import OpenAIParser, RequestsScraper, ScraperAPIScraper, ScrapingBeeScraper, WebsiteAnalyzer

# Initialize the library

scraper = ScrapingBeeScraper(api_key="your-api-key-here")
parser = OpenAIParser(api_key="your-api-key-here")
analyzer = WebsiteAnalyzer(scraper_engine=scraper, parser_engine=parser, max_links=3, translate = 'english')

# Define schema
schema = {
    "mission": "La mission de l'entreprise",
    "news": "Actualités de l'entreprise",
}

# Analyze a website
results = analyzer.analyze("https://mistral.ai/fr/", schema)
print(results)
```


Will return: 
```json
{
  "mission": "We lead the market of open source generative technologies to bring trust and transparency in the field and foster decentralised technology development.",
  "news": "Mistral is introducing new products and services including a free API, improved pricing for their services, and a moderation service for text content detection. They have also announced the Mistral Small and Pixtral Large models, aimed at AI builders.",
  "visited_links": [
    "https://mistral.ai/fr/",
    "https://mistral.ai/news"
  ],
  "logos": [],
  "favicon": "https://mistral.ai/images/favicon/apple-touch-icon.png"
}

```

## Available scrapers

Currently, the library supports the following scrapers:

**ScraperAPI**
``` 
scraper = ScraperAPIScraper(api_key="", render=True)
```

**ScrapingBee**
```
scraper = ScrapingBeeScraper(api_key="", render=True)
```

**Default HTTP request**
```
scraper = RequestsScraper()
```

JS rendering (supported by ScraperAPI and ScrapingBee) is often recommended.