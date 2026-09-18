from pathlib import Path

from client import add_user_message, chat
from evaluator import PromptEvaluator

DATASET_FILE = Path(__file__).parent / "dataset.json"

# Create an instance of PromptEvaluator
# Increase `max_concurrent_tasks` for greater concurrency, but beware of rate limit errors!
prompt_evaluator = PromptEvaluator(max_concurrent_tasks=1)

# # Create the dataset (uncomment to regenerate)
# dataset = prompt_evaluator.generate_dataset(
#     # Describe the purpose or goal of the prompt you're trying to test
#     task_description="Write a compact, concise 1 day meal plan for a single athlete",
#     # Describe the different inputs that your prompt requires
#     prompt_inputs_spec={
#         "height": "The athlete's height in cm",
#         "weight": "The athlete's weight in kg",
#         "goal": "The athlete's goal",
#         "restrictions": "dietary restrictions",
#     },
#     # Where to write the generated dataset
#     output_file=str(DATASET_FILE),
#     # Number of test cases to generate (recommend keeping this low if you're getting rate limit errors)
#     num_cases=3,
# )

# Define and run the prompt you want to evaluate, returning the raw model output
# This function is executed once for each test case
def run_prompt(prompt_inputs):
    prompt = f"""
    Generate a 1 day meal plan for a single athlete that meets the following criteria:

    <athlete_information>
    -Height: {prompt_inputs["height"]}
    -Weight: {prompt_inputs["weight"]}
    -Goal: {prompt_inputs["goal"]}
    -Restrictions: {prompt_inputs["restrictions"]}
    </athlete_information>

    Guidelines:
    1. Include accurate daily calorie amounts
    2. Show protein, fat and carbohydrate amounts
    3. Specify when to eat each meal
    4. Use only foods that fits the athlete's dietary restrictions
    5. List all portions sizes in grams
    6. Keep budget-friendly if mentioned

    Here is an example of a sample input and ideal output:
    <sample_input>
    height: 178
    weight: 68
    goal: Marathon training - maximize carbohydrate intake and energy around 15-mile training run scheduled for 10am
    restrictions: None
    </sample_input>
    <ideal_output>
    # 1-Day Marathon Training Meal Plan
    **Athlete: 178cm, 68kg | 15-mile run at 10:00 AM**

    ---

    ## Daily Nutrition Targets
    - **Calories:** 3,200 kcal
    - **Carbohydrates:** 520g (65% of calories)
    - **Protein:** 110g (14% of calories)
    - **Fat:** 80g (22% of calories)

    ---

    ## Meal Schedule

    ### **6:00 AM - Pre-Run Breakfast**
    *Light, easily digestible carbs*
    - Bagel with honey: 1 bagel (85g) + 1 tbsp honey (20g)
    - Banana: 150g
    - Water: 500ml

    **Macros:** 400 cal | 92g carbs | 10g protein | 1g fat

    ---

    ### **During Run (10:00-11:45 AM)**
    *Consumed while running*
    - Sports drink (6% carbs): 500ml
    - Energy gel: 1 packet (34g)

    **Macros:** 220 cal | 55g carbs | 0g protein | 0g fat

    ---

    ### **11:45 AM - Post-Run Recovery (within 30 min)**
    *Fast carbs + protein to replenish glycogen*
    - Chocolate milk (2%): 400ml
    - White bread: 2 slices (56g)
    - Peanut butter: 25g
    - Apple: 150g

    **Macros:** 540 cal | 65g carbs | 18g protein | 18g fat

    ---

    ### **1:30 PM - Lunch**
    *Balanced carb-protein meal*
    - Pasta (cooked): 250g
    - Grilled chicken breast: 150g
    - Olive oil: 1 tbsp (15ml)
    - Steamed broccoli: 150g
    - Parmesan cheese: 20g

    **Macros:** 680 cal | 75g carbs | 45g protein | 18g fat

    ---

    ### **4:00 PM - Snack**
    *Pre-dinner energy boost*
    - Oatmeal with berries: 50g oats + 150g mixed berries
    - Low-fat yogurt: 150g
    - Granola: 30g

    **Macros:** 380 cal | 70g carbs | 14g protein | 5g fat

    ---

    ### **6:30 PM - Dinner**
    *Substantial carb-based meal*
    - White rice (cooked): 300g
    - Lean ground turkey: 180g
    - Tomato-based sauce: 150ml
    - Olive oil: 1 tbsp (15ml)
    - Mixed salad: 100g
    - Balsamic vinegar: 10ml

    **Macros:** 680 cal | 85g carbs | 35g protein | 18g fat

    ---

    ### **8:30 PM - Evening Snack (Optional)**
    *Light, carb-based before bed*
    - Rice cakes: 3 cakes (30g)
    - Jam: 2 tbsp (40g)
    - Chamomile tea: 250ml

    **Macros:** 200 cal | 48g carbs | 2g protein | 0.5g fat

    ---

    ## Daily Totals
    | Nutrient | Amount |
    |----------|--------|
    | **Calories** | 3,100 kcal |
    | **Carbohydrates** | 490g |
    | **Protein** | 124g |
    | **Fat** | 60.5g |

    ---

    ## Key Notes
    ✅ **Timing:** Pre-run meal is light and fast-digesting; recovery meal prioritizes carbs + protein within 30 minutes
    ✅ **Hydration:** Drink 3-4L water throughout the day (more during/after run)
    ✅ **Budget-friendly:** Uses affordable staples (pasta, rice, chicken, oats)
    ✅ **Glycogen focus:** 65% calories from carbs supports marathon training adaptations
    </ideal_output>
    This example comprehensively addresses all mandatory requirements with well-structured meal planning that strategically leverages timing around the 10am training session. The carbohydrate-focused approach (65%) is appropriate for marathon training, and meals are specific with exact portions and timings. However, there is a minor mathematical inconsistency between stated targets and actual totals, and the calorie/macro calculations lack transparent basis. Despite these secondary issues, the solution is practical, concise, budget-conscious, and directly applicable. The formatting is clear and professional. These minor deficiencies do not violate mandatory requirements but represent room for precision.
    """

    messages = []
    add_user_message(messages, prompt)
    return chat(messages)


results = prompt_evaluator.run_evaluation(
    run_prompt_function=run_prompt,
    dataset_file=str(DATASET_FILE),
    extra_criteria="""
    The output should include:
    - Daily Calorie Total
    - Macro Nutrient Breakdown
    - Meals with exact foods, portions, and timings
    """,
)
