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
    system = """
    You are a patient math tutor.
    Do not directly answer a student's questions.
    Guide them to a solution step by step.
    """

    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
        system=system
    )
    return next(block.text for block in message.content if isinstance(block, TextBlock))

def main():
    messages = []
    while True:
        user_input = input("> You: ")
        if user_input.lower() == "exit":
            break
        add_user_message(messages, user_input)
        answer = chat(messages)
        add_assistant_message(messages, answer)
        print("---")
        print(f"Assistant: {answer}")
        print("---")


if __name__ == "__main__":
    main()
