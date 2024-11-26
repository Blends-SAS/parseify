from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def parse(self, content: str, schema: dict) -> dict:
        """Parse the content using AI and fill the given schema."""
        pass
