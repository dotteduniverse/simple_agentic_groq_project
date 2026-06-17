import sys
from core.llm_client import LLMClientFactory
from core.tool_registry import ToolRegistry
from core.agent import Agent
from tools.math_tool import MathTool
from tools.search_tool import SearchTool
from tools.code_tool import CodeTool
from tools.weather_tool import WeatherTool

def build_agent():
    registry = ToolRegistry()
    registry.register(MathTool())
    registry.register(SearchTool())
    registry.register(CodeTool())
    registry.register(WeatherTool())
    llm_client = LLMClientFactory.get_client()
    return Agent(llm_client=llm_client, tool_registry=registry)

if __name__ == "__main__":
    agent = build_agent()
    print("🧠 Multi‑Tool Agent (Groq). Type 'exit' or press Ctrl+C to quit.")
    try:
        while True:
            query = input("\nYou: ")
            if query.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            response = agent.run(query)
            print(f"Agent: {response}")
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        sys.exit(0)