# Claude Certification

This codebase is for practice and learning the **Claude Architect Foundation** course.

It contains hands-on examples that follow along with the course material, so you can
experiment with the Anthropic API and refer to working code as you go.

## Setup

This project uses a virtual environment with `uv`.

```bash
uv venv
source .venv/bin/activate
uv pip install anthropic python-dotenv
```

Create a `.env` file in the project root with your API key:

```
ANTHROPIC_API_KEY=your-api-key-here
```

## Running the examples

Always activate the virtual environment first, then run a lesson file:

```bash
source .venv/bin/activate
python 1_first_request/__init__.py
```

## Structure

| Path | Description |
| --- | --- |
| `1_first_request/` | First request to the Claude API |
| `example.py` | Scratch file for experimenting |
| `.` |
