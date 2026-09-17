import json
from pathlib import Path
from anthropic import Anthropic
from anthropic._types import omit
from dotenv import load_dotenv
from statistics import mean
import ast
import re

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


def run_prompt(test_case):
    """Merge the test case into the prompt and run it."""
    prompt = f"""
    Please solve the following task:
    {test_case["task"]}

    * Respond in {test_case["format"]} format.
    * Do not include any explanations or additional text in your response.
    """
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```code")
    output = chat(messages, stop_sequences=["```"])
    return output

def validate_json(text):
    """Validates that the text is valid JSON."""
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0

def validate_python(text):
    """Validates that the text is valid Python code."""
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    """Validates that the text matches the given regex pattern."""
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0

def grade_syntax(response, test_case):
    """Programmatically grades the syntax of the response."""
    format = test_case["format"]
    if format == "json":
        return validate_json(response)
    elif format == "python":
        return validate_python(response)
    elif format == "regex":
        return validate_regex(response)
    else:
        return 0



def run_test_case(test_case):
    """Calls run_prompt and grades the output result."""
    output = run_prompt(test_case)

    # TODO: Grading
    model_grade = grade_by_model(test_case, output)
    reasoning = model_grade["reasoning"]
    model_score = model_grade["score"]
    syntax_score = grade_syntax(output, test_case)

    return {
        "output": output,
        "test_case": test_case,
        "model_score": model_score,
        "reasoning": reasoning,
        "syntax_score": syntax_score,
    }

def run_eval(test_cases):
    """Loads the dataset and calls run_test_case for each test case."""
    results = []
    for test_case in test_cases:
        results.append(run_test_case(test_case))

    average_score = mean([r["model_score"] for r in results])
    print(f"Average score: {average_score}")
    return results

def grade_by_model(test_case, output):
    eval_prompt = f"""
        You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

        Original Task:
        <task>
        {test_case["task"]}
        </task>

        Solution to Evaluate:
        <solution>
        {output}
        </solution>

        Output Format
        Provide your evaluation as a structured JSON object with the following fields, in this specific order:
        - "strengths": An array of 1-3 key strengths
        - "weaknesses": An array of 1-3 key areas for improvement
        - "reasoning": A concise explanation of your overall assessment
        - "score": A number between 1-10

        Respond with JSON. Keep your response concise and direct.
        Example response shape:
        {{
            "strengths": string[],
            "weaknesses": string[],
            "reasoning": string,
            "score": number
        }}
    """

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)


def load_test_cases():
    """Loads the test cases from the dataset."""
    with open(Path(__file__).parent / "sample_dataset.json", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    test_cases = load_test_cases()
    results = run_eval(test_cases)
    print(json.dumps(results, indent=2))
