🧠 Multi‑Tool AI Agent with Groq
https://img.shields.io/badge/python-3.9+-blue.svg
https://img.shields.io/badge/Groq-API-black?logo=groq
https://img.shields.io/badge/License-MIT-yellow.svg

A production‑ready, extensible AI agent that uses Groq’s free API to power tool‑calling capabilities: math operations, internet search, and Python code generation & validation.

📌 Features
🤖 ReAct‑style agent – iteratively decides which tool to call based on user input.

🧮 Math Tool – safely evaluates arithmetic and mathematical functions (sqrt, sin, cos, …).

🌐 Search Tool – queries DuckDuckGo (no API key needed) and returns top snippets.

💻 Code Tool – generates Python code via the LLM, validates syntax, checks for dangerous imports, and executes it in a sandboxed subprocess with timeout.

🔧 Modular & Extensible – built with design patterns (Strategy, Registry, Factory, Template Method) for easy maintenance and expansion.

🔁 Conversation memory – retains full chat history (can be extended to summarization).

⚡ Fast & Free – uses Groq’s high‑throughput inference, perfect for prototyping.

🏗️ Architecture
The agent is split into clear layers:

Core – LLM client abstraction, tool registry, and the main agent loop.

Tools – each tool is a standalone class implementing a common interface.

Utils – sandboxed code execution.

Config – centralized environment settings.









📁 Project Structure
text
agent_project/
├── config/
│   └── settings.py                 # Configuration via environment variables
├── core/
│   ├── __init__.py
│   ├── llm_client.py               # Abstract + Groq implementation (Factory)
│   ├── tool_registry.py            # Singleton Registry for tools
│   └── agent.py                    # Main Agent orchestrator
├── tools/
│   ├── __init__.py
│   ├── base.py                     # Abstract BaseTool (Strategy)
│   ├── math_tool.py
│   ├── search_tool.py
│   └── code_tool.py
├── utils/
│   ├── __init__.py
│   └── sandbox.py                  # Safe code execution
├── main.py                         # Composition root / REPL entry
├── requirements.txt
└── README.md
🚀 Getting Started
Prerequisites
Python 3.9+

A Groq API key (free tier available)

Installation
bash
# Clone the repository
git clone https://github.com/yourusername/agent-project.git
cd agent-project

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Configuration
Create a .env file in the project root:

env
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL=llama3-70b-8192    # or mixtral-8x7b-32768
MAX_ITERATIONS=5
CODE_TIMEOUT=5
LLM_PROVIDER=groq             # currently supports 'groq'
All settings are loaded via config/settings.py.

🖥️ Usage
Run the interactive REPL:

bash
python main.py
Example session:

text
🧠 Multi‑Tool Agent (Groq). Type 'exit' to quit.

You: What is the square root of 144 plus 5?
Agent: The square root of 144 is 12, plus 5 equals 17.

You: Search for the latest news about AI.
Agent: 1. AI News: Breakthrough in language models...
   ...

You: Write a Python function that returns the nth Fibonacci number.
Agent: Generated code:
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
Execution result: (no output, but the code is valid)

text

---

## 🧰 Tools Overview

| Tool | Description | Safety Features |
| :--- | :--- | :--- |
| **Math** | Evaluates arithmetic and math functions. | Uses restricted `eval` with whitelisted built‑ins. |
| **Search** | Performs web search via DuckDuckGo. | Returns only top snippets – no external API key. |
| **Code** | Generates code, validates syntax, checks for dangerous imports/functions, executes in subprocess with timeout. | AST‑based validation, forbidden imports (`os`, `sys`, `subprocess`, …), isolated subprocess, resource timeout. |

---

## 🧩 Design Patterns in Action

To make the code reusable and extendable, we applied:

| Pattern | Location | Benefit |
| :--- | :--- | :--- |
| **Strategy** | `BaseTool` and tool implementations | New tools can be added without changing the agent. |
| **Registry** | `ToolRegistry` (singleton) | Centralizes tool management; tools are discoverable by name. |
| **Abstract Factory** | `LLMClientFactory` | Allows switching LLM providers (Groq, OpenAI, etc.) with a single config change. |
| **Dependency Injection** | `Agent` receives its clients via constructor | Makes testing and swapping dependencies trivial. |
| **Template Method** | `Agent.run()` defines the fixed loop skeleton | The loop logic is reused; only tool execution is delegated. |

---

## 🔧 Extending the Agent

### Adding a New Tool

1. Create a new file in `tools/`, e.g., `weather_tool.py`.
2. Implement a class inheriting `BaseTool`:
   ```python
   from tools.base import BaseTool
   from typing import Dict, Any

   class WeatherTool(BaseTool):
       @property
       def name(self) -> str:
           return "weather_tool"

       @property
       def description(self) -> str:
           return "Get current weather for a city."

       @property
       def parameters(self) -> Dict[str, Any]:
           return {
               "type": "object",
               "properties": {
                   "city": {"type": "string", "description": "City name"}
               },
               "required": ["city"],
           }

       def execute(self, arguments: Dict[str, Any]) -> str:
           city = arguments["city"]
           # ... call weather API ...
           return f"Weather in {city}: Sunny, 25°C"
Register it in main.py:

python
from tools.weather_tool import WeatherTool
registry.register(WeatherTool())
Done! The agent will now have access to the new tool.

Changing the LLM Provider
Create a new class (e.g., OpenAIClient) that implements BaseLLMClient.

Update LLMClientFactory.get_client() to return it based on LLM_PROVIDER.

🤝 Contributing
Contributions are welcome! Please:

Fork the repository.

Create a feature branch.

Write clear, documented code.

Add tests (if applicable).

Submit a pull request.

For major changes, open an issue first to discuss what you’d like to change.

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

🙏 Acknowledgements
Groq for providing fast, free inference.

DuckDuckGo Search library for web search.

The open‑source community for inspiration.