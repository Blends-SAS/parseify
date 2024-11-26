from lxml import html
from urllib.parse import urljoin


class DomExtractor:
    """
    Extractor for structured data from HTML content using lxml.
    """

    def __init__(self):
        pass

    def extract(self, html_content, base_url):
        """
        Extract structured content from the HTML page.

        Args:
            html_content (str): Raw HTML content of the page.
            base_url (str): The base URL of the page for resolving relative links.

        Returns:
            dict: A dictionary containing extracted text, links, and logo.
        """
        tree = html.fromstring(html_content)

        # Extract text content
        text_content = self._extract_text(tree)

        # Extract links
        links = self._extract_links(tree, base_url)

        # Extract logo
        logos = self._extract_logo(tree, base_url)

        # Extract favicon
        favicon = self.extract_favicon(tree, base_url)

        return {
            "text_contents": text_content,
            "links": links,
            "logos": logos,
            "favicon": favicon,
        }

    def _extract_text(self, tree):
        text_elements = tree.xpath("//p | //h1 | //h2 | //h3 | //span")
        text_content = [
            element.text_content().strip()
            for element in text_elements if element.text_content().strip()
        ]
        return list(set(text_content))  # Remove duplicates

    def _extract_links(self, tree, base_url):
        links = []
        for element in tree.xpath("//a[@href]"):
            href = element.get("href").strip()
            title = element.text_content().strip()

            if href and title:
                absolute_link = urljoin(base_url, href)  # Convert relative URL to absolute
                links.append({"title": title, "link": absolute_link})

        return links


    def _extract_logo(self, tree, base_url):
        logo_elements = tree.xpath(
            "//img[contains(translate(@alt, 'LOGO', 'logo'), 'logo') "
            "or contains(translate(@class, 'LOGO', 'logo'), 'logo') "
            "or contains(translate(@id, 'LOGO', 'logo'), 'logo')] "
            "| //svg[contains(translate(@class, 'LOGO', 'logo'), 'logo') "
            "or contains(translate(@id, 'LOGO', 'logo'), 'logo')]"
        )
        logos = []
        for element in logo_elements:
            if element.tag == "img":
                logo_src = element.get("src")
                if logo_src:
                    logos.append(urljoin(base_url, logo_src.strip()))
            elif element.tag == "svg":
                logos.append(html.tostring(element, encoding='unicode'))
        return logos


    def extract_favicon(self, tree, base_url):
        """
        Extract the favicon URL from the HTML tree.

        Args:
            tree (lxml.html.HtmlElement): Parsed HTML tree of the page.
            base_url (str): The base URL of the page for resolving relative links.

        Returns:
            str: The URL of the favicon, or None if not found.
        """
        # Search for the favicon in the <head> section
        favicon_elements = tree.xpath(
            "//link[contains(translate(@rel, 'ICON', 'icon'), 'icon')]"
        )

        for element in favicon_elements:
            href = element.get("href")
            if href:
                # Resolve relative URL to absolute
                return urljoin(base_url, href.strip())

        # If no favicon is explicitly defined, return the default favicon path
        return urljoin(base_url, "/favicon.ico")
