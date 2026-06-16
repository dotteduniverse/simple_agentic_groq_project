from core.llm_client import LLMClientFactory
from core.tool_registry import ToolRegistry
from core.agent import Agent
from tools.math_tool import MathTool
from tools.search_tool import SearchTool
from tools.code_tool import CodeTool

def build_agent():
    # 1. Setup Registry and register tools
    registry = ToolRegistry()
    registry.register(MathTool())
    registry.register(SearchTool())
    registry.register(CodeTool())
    
    # 2. Create LLM client
    llm_client = LLMClientFactory.get_client()
    
    # 3. Build Agent (Dependency Injection)
    return Agent(llm_client=llm_client, tool_registry=registry)

if __name__ == "__main__":
    agent = build_agent()
    print("🧠 Multi‑Tool Agent (Groq). Type 'exit' to quit.")
    while True:
        query = input("\nYou: ")
        if query.lower() in ("exit", "quit"):
            break
        response = agent.run(query)
        print(f"Agent: {response}")