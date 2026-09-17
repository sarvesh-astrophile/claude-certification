import json
from pathlib import Path

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


def generate_sample_dataset():
    prompt = """
Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
    {
        "task": "Description of task",
        "format": "python" or "json" or "regex",
    },
    ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""

    messages = []
    print("---")
    add_user_message(messages, prompt)
    add_assistant_message(messages, "[")
    answer = chat(messages, stop_sequences=["]"])
    dataset = json.loads("[" + answer + "]")

    output_file = Path(__file__).parent / "sample_dataset.json"
    output_file.write_text(json.dumps(dataset, indent=2))
    print(f"Dataset written to {output_file}")
    print("---")
    return dataset


if __name__ == "__main__":
    generate_sample_dataset()
