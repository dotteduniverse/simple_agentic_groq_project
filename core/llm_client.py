from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import groq
from config.settings import settings

class BaseLLMClient(ABC):
    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: str = "auto",
        temperature: float = 0.3,
    ) -> Dict[str, Any]:
        """Send chat request and return the full response dict."""
        pass

class GroqClient(BaseLLMClient):
    def __init__(self, api_key: str = settings.GROQ_API_KEY, model: str = settings.GROQ_MODEL):
        self.client = groq.Groq(api_key=api_key)
        self.model = model

    def chat(self, messages, tools=None, tool_choice="auto", temperature=0.3):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=temperature,
        )
        # Convert to dict for easier serialization
        return response.model_dump()

# Simple Factory
class LLMClientFactory:
    @staticmethod
    def get_client(provider: str = settings.LLM_PROVIDER) -> BaseLLMClient:
        if provider == "groq":
            return GroqClient()
        # elif provider == "openai":
        #     return OpenAIClient()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")