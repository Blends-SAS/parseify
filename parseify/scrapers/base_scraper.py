from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def fetch(self, url: str) -> str:
        """Fetch the raw HTML content of the given URL."""
        pass
