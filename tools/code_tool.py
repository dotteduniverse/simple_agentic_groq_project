from typing import Dict, Any
from tools.base import BaseTool
from core.llm_client import LLMClientFactory
from utils.sandbox import validate_and_execute
from config.settings import settings

class CodeTool(BaseTool):
    @property
    def name(self) -> str:
        return "code_tool"

    @property
    def description(self) -> str:
        return "Generate, validate, and execute Python code based on a task description."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_description": {
                    "type": "string",
                    "description": "Describe what the Python code should do.",
                }
            },
            "required": ["task_description"],
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        task = arguments["task_description"]
        
        # 1. Generate code using the same LLM (or a dedicated one)
        llm = LLMClientFactory.get_client()  # re-use
        gen_prompt = f"Write Python code for: {task}. Return only code, no markdown."
        response = llm.chat(
            messages=[{"role": "user", "content": gen_prompt}],
            tools=None,  # no tools for generation
            temperature=0.2,
        )
        generated_code = response["choices"][0]["message"]["content"].strip()

        # 2. Validate & Execute via sandbox
        execution_output = validate_and_execute(generated_code)

        return (
            f"Generated code:\n```python\n{generated_code}\n```\n\n"
            f"Execution result:\n{execution_output}"
        )