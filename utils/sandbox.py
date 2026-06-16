import ast
import subprocess
import sys
import tempfile
import os
from config.settings import settings

FORBIDDEN_IMPORTS = {"os", "sys", "subprocess", "shutil", "importlib", "compile", "eval", "exec", "__import__"}

def validate_and_execute(code: str) -> str:
    # 1. Syntax check
    try:
        parsed = ast.parse(code)
    except SyntaxError as e:
        return f"Syntax error:\n{e}"

    # 2. Safety check (AST walk)
    for node in ast.walk(parsed):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] in FORBIDDEN_IMPORTS:
                    return f"Safety violation: import of '{alias.name}' is not allowed."
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split('.')[0] in FORBIDDEN_IMPORTS:
                return f"Safety violation: import from '{node.module}' is not allowed."
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile"}:
                return f"Safety violation: use of '{node.func.id}' is not allowed."

    # 3. Execute in subprocess with timeout
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=settings.CODE_TIMEOUT,
            env={"PYTHONPATH": ""},
        )
        output = result.stdout
        if result.stderr:
            output += f"\n[stderr]: {result.stderr}"
        return output
    except subprocess.TimeoutExpired:
        return f"Execution timed out after {settings.CODE_TIMEOUT} seconds."
    except Exception as e:
        return f"Execution error: {str(e)}"
    finally:
        os.unlink(temp_file)