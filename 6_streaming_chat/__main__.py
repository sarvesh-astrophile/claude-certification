from anthropic import Anthropic
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


def chat(messages, system=""):
    print("Assistant: ", end="", flush=True)
    with client.messages.stream(
        model=model,
        max_tokens=1000,
        messages=messages,
        system=system
    ) as stream:
        answer = ""
        for text in stream.text_stream:
            print(text, end="", flush=True)
            answer += text
    print()
    return answer

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


if __name__ == "__main__":
    main()
