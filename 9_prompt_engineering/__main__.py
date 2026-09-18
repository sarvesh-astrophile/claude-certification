from client import add_user_message, chat
from evaluator import PromptEvaluator

# Create an instance of PromptEvaluator
# Increase `max_concurrent_tasks` for greater concurrency, but beware of rate limit errors!
evaluator = PromptEvaluator(max_concurrent_tasks=1)
dataset = evaluator.generate_dataset(
    # Describe the purpose or goal of the prompt you're trying to test
    task_description="",
    # Describe the different inputs that your prompt requires
    prompt_inputs_spec={},
    # Where to write the generated dataset
    output_file="dataset.json",
    # Number of test cases to generate (recommend keeping this low if you're getting rate limit errors)
    num_cases=3,
)

# Define and run the prompt you want to evaluate, returning the raw model output
# This function is executed once for each test case
def run_prompt(prompt_inputs):
    prompt = f"""

    """

    messages = []
    add_user_message(messages, prompt)
    return chat(messages)


results = evaluator.run_evaluation(
    run_prompt_function=run_prompt, dataset_file="dataset.json"
)
