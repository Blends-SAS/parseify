from parseify import DomExtractor, OpenAIService
import json
import logging

logger = logging.getLogger(__name__)







class WebsiteAnalyzer:
    def __init__(self, scraper_engine, parser_engine, extractor_engine=DomExtractor, max_links=3,  translate = 'english'):
        self.scraper = scraper_engine
        self.parser = parser_engine
        self.extractor = extractor_engine()
        self.max_links = max_links  # Limit the number of links to explore
        self.translate = translate


    def analyze(self, url, schema):
        visited_links = [url]
        results = {key: None for key in schema.keys()}

        def process_page(link, current_results):
            try:
                raw_html = self.scraper.fetch(link)
                page_extracted_content = self.extractor.extract(raw_html, base_url=link)
                new_results = self.fill_json_schema(
                    ' / '.join(page_extracted_content['text_contents']),
                    schema,
                    current_results
                )
                updated_results = self._merge_results(current_results, new_results)

                return updated_results, page_extracted_content
            except Exception as e:
                logger.error(f"Error processing page {link}: {e}")
                return current_results, None

        # Step 1: Process the main page

        results, extracted_content = process_page(url, results)

        # Rise and exception for when the first web page fails to load
        if extracted_content is None:
            raise Exception("Invalid URL provided, or scraper could not access requested URL")

        images = {
            "logos": extracted_content["logos"],
            "favicon": extracted_content["favicon"]
        }

        # Step 2: Handle missing fields and explore next links
        missing_fields = {key: value for key, value in results.items() if value is None}

        if missing_fields and extracted_content:
            try:
                next_links = extracted_content["links"]
                
                filtered_links = self._filter_next_links(next_links, missing_fields)
                filtered_links = filtered_links[:self.max_links]

                for link in filtered_links:
                    if link in visited_links:
                        continue

                    visited_links.append(link)
                    results, _ = process_page(link, results)

                    missing_fields = {key: value for key, value in results.items() if value is None}
                    if not missing_fields:
                        break
            except Exception as e:
                logger.error(f"Error during link exploration: {e}")

        results["visited_links"] = visited_links
        results.update(images)

        # Translate the results

        if self.translate:
            results = OpenAIService(api_key= self.parser.api_key).translate(results=results, language=self.translate) # Take the key of OpenAIParser

        return results

    def fill_json_schema(self, page_content, information_requested, results):
        """
        Fills the provided schema using AI-driven parsing.

        Args:
            page_content (list): The content found on the page (text).
            information_requested (dict): Descriptions of the details to extract.
            results (dict): The current results to update.

        Returns:
            dict: Updated results with extracted data or None for missing values.
        """
        # Identify missing fields in the schema
        missing_fields = {key: value for key, value in results.items() if value is None}

        if not missing_fields:
            return {}  # No missing fields, nothing to do

        # Prepare the messages for the LLM
        messages = [
            {
                "role": "user",
                "content": (
                    "We are gathering information for a startup. We are looking for the following missing details: "
                    f"{json.dumps(missing_fields)}.\n"
                    "Here is the content found on this page: "
                    f"{json.dumps(page_content)}.\n"
                    "For each missing detail, please provide both the value and a boolean indicating if the information "
                    "was found. Return an empty string for missing values."
                )
            }
        ]

        # Define the schema for the GPT response
        response_schema = {
            key: {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "string",
                        "description": information_requested[key]  # Ensure this is a string
                    },
                    "found": {
                        "type": "boolean",
                        "description": "Indicates if the information was found on the page"
                    }
                },
                "required": ["value", "found"],
                "additionalProperties": False
            }
            for key in missing_fields.keys()
        }

        try:
            # Request completion from the parser (LLM)
            response = self.parser.parse(messages, response_schema)

            # Update the results based on the response
            for key, details in response.items():
                # Handle cases where the LLM returns "Not found" or empty strings
                if details["found"] and details["value"].strip().lower() != "not found":
                    results[key] = details["value"]
                else:
                    results[key] = None  # Mark as None if not found or explicitly "Not found"

            return results

        except Exception as e:
            logger.error(f"Error during parsing: {e}")
            return {}

    def _merge_results(self, current_results, new_results):
        """
        Merge new results into the current results, prioritizing existing values.

        Args:
            current_results (dict): Current results with potential missing fields.
            new_results (dict or None): New results to merge into current results.

        Returns:
            dict: Merged results.
        """
        if not new_results:
            return current_results  # Return current results if new_results is None

        for key, value in new_results.items():
            if current_results.get(key) is None:  # Only update missing fields
                current_results[key] = value
        return current_results

    def _filter_next_links(self, possible_links, missing_fields):
        """
        Filters the most relevant links to explore for missing schema fields.

        Args:
            possible_links (list): List of links to evaluate.
            missing_fields (dict): Missing fields in the schema.

        Returns:
            list: Selected links to explore.
        """
        # Define the message for the AI parser
        messages = [
            {
                "role": "user",
                "content": f"We are trying to gather the following information: {json.dumps(missing_fields)}."
                           f"Here are the available links: {json.dumps(possible_links)}."
                           f"Please suggest the most relevant links to explore. Do not suggest link with fragment identifiers (#)"
            }
        ]

        # Call the parser to filter links
        response = self.parser.parse(
            messages=messages,
            json_schema={
                "links": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        )

        return response.get("links", [])


