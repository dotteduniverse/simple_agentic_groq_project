from typing import Dict, Optional, List, Any
from tools.base import BaseTool

class ToolRegistry:
    _instance: Optional["ToolRegistry"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools: Dict[str, BaseTool] = {}
        return cls._instance

    def register(self, tool: BaseTool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry.")
        return self._tools[name]

    def get_all_schemas(self) -> List[Dict[str, Any]]:
        return [tool.to_openai_schema() for tool in self._tools.values()]

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        tool = self.get(tool_name)
        return tool.execute(arguments)

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())