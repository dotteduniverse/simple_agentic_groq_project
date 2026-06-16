from typing import Dict, Any
from tools.base import BaseTool
from duckduckgo_search import DDGS

class SearchTool(BaseTool):
    @property
    def name(self) -> str:
        return "search_tool"

    @property
    def description(self) -> str:
        return "Search the internet using DuckDuckGo and return top 3 snippets."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query."}
            },
            "required": ["query"],
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        query = arguments["query"]
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
            if not results:
                return "No results found."
            snippets = [f"{i}. {r.get('title','No title')}\n   {r.get('body','No snippet')}" 
                        for i, r in enumerate(results, 1)]
            return "\n\n".join(snippets)
        except Exception as e:
            return f"Search error: {str(e)}"