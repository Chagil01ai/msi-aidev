from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")

if not my_api_key:
    raise ValueError("ANTHROPIC_API_KEY is not set in the environment variables.")

#Initialize Anthropic event
client = Anthropic(
    api_key=my_api_key
)

# ANSI color codes
BLUE = "\033[94m"
GREEN = "\033[92m"
RESET = "\033[0m"

def chat_with_claude():
    print("Welcome to the Claude Chatbot!")
    print("Type 'exit' or 'quit' to end the chat.")

    conversation_history = []

    while True:
        user_input = input(f"{BLUE}You: {RESET}")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break

        conversation_history.append({"role": "user", "content": user_input})

        print(f"{GREEN}Claude is thinking...{RESET}", end="", flush=True)
        # Simulate thinking time
        import time
        time.sleep(1)
        print("\r", end="")
        print(f"{GREEN}Claude: {RESET}", end="", flush=True)

        # Call the Claude model with the conversation history
        # You can change the model to "claude-3-haiku-20240307" if you want to use a different version
        
        stream = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            # model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=conversation_history,
            stream=True
        )

        bot_reply = ""
        for chunk in stream:
            if chunk.type == "content_block_delta":
                content = chunk.delta.text
                print(f"{GREEN}{content}{RESET}", end="", flush=True)
                bot_reply += content

        print() # New line after bot reply

        conversation_history.append({"role": "assistant", "content": bot_reply})

if __name__ == "__main__":
    chat_with_claude()
# This script allows you to chat with the Claude model in a terminal interface.