from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's parameters."""
        pass

    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> str:
        """Execute the tool with the given arguments and return a string result."""
        pass

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert the tool to OpenAI/Groq function-calling schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }