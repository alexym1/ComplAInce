"""Monitor AI agents steps by steps."""


import functools
import os
import sys
from datetime import datetime
from io import StringIO


def tracing_messages(func):
    """Record messages for easy tracing/debugging."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        os.makedirs("logs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"logs/tracing_message_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            for m in result['messages']:
                content = m.pretty_print()
                if content is None:
                    old_stdout = sys.stdout
                    sys.stdout = mystdout = StringIO()
                    m.pretty_print()
                    sys.stdout = old_stdout
                    f.write(mystdout.getvalue() + "\n")
                else:
                    f.write(str(content) + "\n")

        return result

    return wrapper
