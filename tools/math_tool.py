import math
from typing import Dict, Any
from tools.base import BaseTool

class MathTool(BaseTool):
    @property
    def name(self) -> str:
        return "math_tool"

    @property
    def description(self) -> str:
        return "Evaluate a mathematical expression. Uses safe builtins and math functions."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression, e.g., '2 + 3 * 4' or 'sqrt(16)'.",
                }
            },
            "required": ["expression"],
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        expr = arguments["expression"]
        allowed_builtins = {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow, "int": int, "float": float,
            "len": len, "range": range,
        }
        math_funcs = {
            "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
            "tan": math.tan, "pi": math.pi, "e": math.e,
            "log": math.log, "exp": math.exp,
        }
        allowed_globals = {**allowed_builtins, **math_funcs}
        try:
            result = eval(expr, {"__builtins__": None}, allowed_globals)
            return f"Result: {result}"
        except Exception as e:
            return f"Math error: {str(e)}"