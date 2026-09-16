from anthropic import Anthropic
from anthropic.types import TextBlock
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5"


def add_user_message(message, content):
    user_message = {
        "role": "user",
        "content": content
    }
    message.append(user_message)


def add_assistant_message(message, content):
    assistant_message = {
        "role": "assistant",
        "content": content
    }
    message.append(assistant_message)


def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages
    )
    return next(block.text for block in message.content if isinstance(block, TextBlock))

def main():
    messages = []
    add_user_message(messages, "Define Quantum Computing in one sentence")
    answer = chat(messages)
    add_assistant_message(messages, answer)
    add_user_message(messages, "What are the main benefits of quantum computing?")
    answer = chat(messages)
    print(answer)

if __name__ == "__main__":
    main()
