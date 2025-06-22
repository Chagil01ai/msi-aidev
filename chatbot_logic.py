from dotenv import load_dotenv
import os
import time
from anthropic import Anthropic, APIStatusError

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")
if not my_api_key:
    raise ValueError("ANTHROPIC_API_KEY is not set in the environment variables.")

client = Anthropic(api_key=my_api_key)

def retry_with_backoff(func, max_retries=5, backoff_factor=2, *args, **kwargs):
    """
    Generic retry helper with exponential backoff.
    """
    delay = 1  # start with 1 second
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except APIStatusError as e:
            if "Overloaded" in str(e) and attempt < max_retries - 1:
                print(f"Retrying after {delay}s due to overload...")
                time.sleep(delay)
                delay *= backoff_factor
            else:
                raise e

def stream_claude_response(history):
    stream = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=history,
        stream=True
    )
    for chunk in stream:
        if chunk.type == "content_block_delta":
            yield chunk.delta.text

    # Call with retry wrapper
    try:
        return retry_with_backoff(stream_claude_response, history=history)
    except APIStatusError as e:
        if "Overloaded" in str(e):
            return "Claude is still busy or currently overloaded. Please try again shortly."
        else:
            return f"API error: {str(e)}"