from anthropic import Anthropic
from anthropic._types import omit
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5-20250929"  # supports assistant prefill (claude-sonnet-5 does not)


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


def chat(messages, system="", stop_sequences: list[str] | None = None):
    print("Assistant: ", end="", flush=True)
    with client.messages.stream(
        model=model,
        max_tokens=1000,
        messages=messages,
        system=system,
        stop_sequences=stop_sequences if stop_sequences is not None else omit
    ) as stream:
        answer = ""
        for text in stream.text_stream:
            print(text, end="", flush=True)
            answer += text
    print()
    return answer

def main():
    messages = []
    user_input = "Generate a very short event bride rule as json"
    print("---")
    add_user_message(messages, user_input)
    add_assistant_message(messages, "```json")
    answer = chat(messages, stop_sequences=["```"])
    add_assistant_message(messages, answer)
    print("---")


if __name__ == "__main__":
    main()
