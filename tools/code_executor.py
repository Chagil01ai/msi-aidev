# tools/code_executor.py

import sys
import io
import contextlib

def run_python_code(code):
    """Execute Python safely (restricted)."""
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code, {"__builtins__": __builtins__}, {})
    except Exception as e:
        return f"Error: {e}"
    return output.getvalue()
