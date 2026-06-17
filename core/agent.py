import json
import re
import groq
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
        debug: bool = True,          # <-- added debug flag
    ):
        self.llm_client = llm_client
        self.tool_registry = tool_registry
        self.max_iterations = max_iterations
        self.debug = debug

    def _log(self, msg: str):
        if self.debug:
            print(f"[DEBUG] {msg}")

    def run(self, user_query: str) -> str:
        self._log(f"🟢 New query: {user_query}")
        messages = [
            {"role": "system", "content": (
                "You are a helpful assistant with access to tools. "
                "You MUST use the provided tool functions exclusively by calling them via the function-calling interface. "
                "Do NOT output function calls as plain text, markdown, or XML tags. "
                "If you need to call a tool, do it only via the tool_choice mechanism."
            )},
            {"role": "user", "content": user_query}
        ]

        for iteration in range(self.max_iterations):
            self._log(f"🔄 Iteration {iteration + 1}/{self.max_iterations}")

            try:
                response = self.llm_client.chat(
                    messages=messages,
                    tools=self.tool_registry.get_all_schemas(),
                    tool_choice="auto",
                )
            except groq.BadRequestError as e:
                error_body = e.response.json() if hasattr(e, 'response') else {}
                if error_body.get('error', {}).get('code') == 'tool_use_failed':
                    self._log("⚠️ Tool use failed – retrying with hint")
                    if messages and messages[-1]['role'] == 'assistant':
                        messages.pop()
                    messages.append({
                        "role": "user",
                        "content": "You must call the tool using the proper function-calling interface. Do not output raw XML or text. Call the tool correctly."
                    })
                    continue
                else:
                    raise

            assistant_message = response["choices"][0]["message"]
            content = assistant_message.get("content", "")
            self._log(f"💬 LLM response: {content[:100] + '...' if content and len(content) > 100 else content}")

            # --- Manual fallback for malformed function calls ---
            if not assistant_message.get("tool_calls") and '<function=' in content:
                self._log("🔧 Detected malformed tool call – attempting to parse manually")
                match = re.search(r'<function=(\w+)\s*({.*?})>', content, re.DOTALL)
                if match:
                    tool_name = match.group(1)
                    try:
                        args = json.loads(match.group(2))
                        self._log(f"📞 Parsed tool: {tool_name}({args})")
                        try:
                            result = self.tool_registry.execute(tool_name, args)
                        except KeyError:
                            result = f"Error: Tool '{tool_name}' does not exist. Available tools: {', '.join(self.tool_registry.list_tools())}"
                            self._log(f"❌ {result}")
                        except Exception as e:
                            result = f"Error executing tool '{tool_name}': {str(e)}"
                            self._log(f"❌ {result}")
                        self._log(f"📦 Tool result: {result[:200] + '...' if len(result) > 200 else result}")
                        messages.append({
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [{"id": "manual", "function": {"name": tool_name, "arguments": json.dumps(args)}}]
                        })
                        messages.append({"role": "tool", "tool_call_id": "manual", "content": result})
                        continue
                    except Exception:
                        self._log("⚠️ Could not parse malformed call – treating as normal content")
                        pass

            # --- Sanitize assistant message ---
            cleaned = {"role": assistant_message.get("role", "assistant")}
            if assistant_message.get("content") is not None:
                cleaned["content"] = assistant_message["content"]
            if "tool_calls" in assistant_message:
                cleaned["tool_calls"] = assistant_message["tool_calls"]
            cleaned.pop("function_call", None)
            messages.append(cleaned)

            tool_calls = assistant_message.get("tool_calls")
            if not tool_calls:
                self._log("✅ Final answer received")
                return assistant_message.get("content", "No answer provided.")

            self._log(f"🔧 LLM requested {len(tool_calls)} tool call(s)")

            for tool_call in tool_calls:
                func_name = tool_call["function"]["name"]
                try:
                    args = json.loads(tool_call["function"]["arguments"])
                except json.JSONDecodeError:
                    args = {}
                self._log(f"📞 Calling tool: {func_name} with args: {args}")

                try:
                    result = self.tool_registry.execute(func_name, args)
                except KeyError:
                    result = f"Error: Tool '{func_name}' does not exist. Available tools: {', '.join(self.tool_registry.list_tools())}"
                    self._log(f"❌ {result}")
                except Exception as e:
                    result = f"Error executing tool '{func_name}': {str(e)}"
                    self._log(f"❌ {result}")
                else:
                    self._log(f"📦 Tool result: {result[:200] + '...' if len(result) > 200 else result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result,
                })

        return "Agent reached maximum iterations without concluding."