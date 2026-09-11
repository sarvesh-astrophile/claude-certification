from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5"

# Making a request
message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[{
        "role": "user",
        "content": "how are you?"
    }]
)

print(message)
