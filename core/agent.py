import json
from typing import List, Dict, Any
from core.llm_client import BaseLLMClient
from core.tool_registry import ToolRegistry
from config.settings import settings

class Agent:
    def __init__(
        self,
        llm_client: BaseLLMClient,
        tool_registry: ToolRegistry,
        max_iterations: int = settings.MAX_ITERATIONS,
    ):
        self.llm_client = llm_client
        self.tool_registry = tool_registry
        self.max_iterations = max_iterations

    def run(self, user_query: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant with access to tools. Use them when necessary."},
            {"role": "user", "content": user_query}
        ]

        for _ in range(self.max_iterations):
            # 1. Call LLM with tools
            response = self.llm_client.chat(
                messages=messages,
                tools=self.tool_registry.get_all_schemas(),
                tool_choice="auto",
            )
            assistant_message = response["choices"][0]["message"]

            # 2. Sanitize the assistant message to avoid unsupported fields (like 'annotations')
            cleaned = {"role": assistant_message.get("role", "assistant")}
            if assistant_message.get("content") is not None:
                cleaned["content"] = assistant_message["content"]
            if "tool_calls" in assistant_message:
                cleaned["tool_calls"] = assistant_message["tool_calls"]
            # Remove any deprecated field that might slip through
            cleaned.pop("function_call", None)

            messages.append(cleaned)

            # 3. Check for tool calls
            tool_calls = assistant_message.get("tool_calls")
            if not tool_calls:
                # Final answer
                return assistant_message.get("content", "No answer provided.")

            # 4. Execute tool calls
            for tool_call in tool_calls:
                func_name = tool_call["function"]["name"]
                try:
                    args = json.loads(tool_call["function"]["arguments"])
                except json.JSONDecodeError:
                    args = {}

                result = self.tool_registry.execute(func_name, args)

                # Append tool result (this format is already correct)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result,
                })

        return "Agent reached maximum iterations without concluding."