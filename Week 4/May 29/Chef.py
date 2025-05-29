import os
import json
import re
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# LLM config
llm_config = {
    "seed": 42,
    "config_list": [{
        "model": "gemini-1.5-flash",
        "api_key": api_key,
        "api_type": "google"
    }],
    "temperature": 0
}

# Load ingredients
with open("ingredients.json") as f:
    ingredients_data = json.load(f)

# ===== Tool Functions =====
def generate_recipe(preferences: str, servings: int):
    matching = [
        name for name, props in ingredients_data.items()
        if preferences.lower() in props.get("tags", [])
    ]
    if len(matching) < 3:
        return {
            "title": "Not enough ingredients",
            "servings": servings,
            "ingredients": [],
            "steps": ["Please add more ingredients matching the preference."]
        }

    import random
    selected = random.sample(matching, 3)
    return {
        "title": f"{preferences.title()} Stir-Fry",
        "servings": servings,
        "ingredients": [{"name": ing, "quantity": 1} for ing in selected],
        "steps": ["Chop ingredients", "Cook in pan", "Serve warm"]
    }

def check_nutrition(recipe: dict):
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    for item in recipe["ingredients"]:
        name = item["name"]
        qty = item["quantity"]
        data = ingredients_data.get(name, {})
        for key in totals:
            totals[key] += data.get(key, 0) * qty

    per_serving = {k: round(v / recipe["servings"], 2) for k, v in totals.items()}
    balanced = (
        400 <= per_serving["calories"] <= 600 and
        per_serving["protein"] >= 15 and
        per_serving["fat"] <= 30
    )

    return {
        "nutrition": per_serving,
        "balanced": balanced,
        "message": (
            "This recipe is nutritionally balanced. TERMINATE"
            if balanced else
            "This recipe is not balanced. Please regenerate."
        )
    }

# ===== Formatting Functions =====
def format_ingredients(ingredients):
    if not ingredients:
        return "No ingredients listed."
    max_name_len = max(len(item["name"]) for item in ingredients)
    lines = []
    for item in ingredients:
        # quantity might be int or str, convert to str for uniformity
        qty_str = str(item["quantity"])
        lines.append(f"name: {item['name']:<{max_name_len}} , quantity: {qty_str}")
    return "\n".join(lines)

def format_recipe(recipe_json):
    title = recipe_json.get("title", "No Title")
    servings = recipe_json.get("servings", "N/A")
    ingredients = recipe_json.get("ingredients", [])
    steps = recipe_json.get("steps", [])

    formatted_ingredients = format_ingredients(ingredients)
    formatted_steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])

    return (
        f"Recipe: {title}\n"
        f"Servings: {servings}\n\n"
        f"Ingredients:\n{formatted_ingredients}\n\n"
        f"Steps:\n{formatted_steps}"
    )

def extract_json_from_response(text):
    # Extract JSON block between ```json ... ```
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    return None

# ===== Agents =====
recipe_creator = AssistantAgent(
    name="RecipeCreator",
    llm_config=llm_config,
    system_message=(
        "You are a chef who creates recipes using the 'generate_recipe' tool. "
        "Always return a full recipe with title, servings, ingredients (list of {name, quantity}), and steps."
    ),
    function_map={"generate_recipe": generate_recipe}
)

nutrition_checker = AssistantAgent(
    name="NutritionChecker",
    llm_config=llm_config,
    system_message=(
        "You are a nutritionist. Use 'check_nutrition' to evaluate the recipe. "
        "If balanced, say 'This recipe is nutritionally balanced. TERMINATE'. Otherwise ask to regenerate."
    ),
    function_map={"check_nutrition": check_nutrition}
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    code_execution_config={"use_docker": False},
    system_message="You are a user requesting recipes and reviewing results."
)

# ===== Custom RoundRobinGroupChat =====
class RoundRobinGroupChat:
    def __init__(self, agents):
        self.agents = agents

    def run(self, initial_message):
        current_message = initial_message
        turn = 0

        print("🟢 Starting Round-Robin Recipe Chat\n")

        while True:
            agent = self.agents[turn % len(self.agents)]
            print(f"🔁 Round {turn + 1} | {agent.name}'s Turn")

            if isinstance(agent, UserProxyAgent):
                user_input = input("Replying as User. Provide feedback to the sender. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: ")
                if user_input.strip().lower() == "exit":
                    print("User requested exit. Terminating chat.")
                    break
                if user_input.strip() == "":
                    print("\n>>>>>>>> NO HUMAN INPUT RECEIVED.\n")
                    print(">>>>>>>> USING AUTO REPLY...")
                    current_message = ""
                else:
                    current_message = user_input
                print(f"{agent.name}: {current_message}")
            else:
                response = agent.generate_reply(messages=[{"role": "user", "content": current_message}])

                # If response is dict, get content key
                content = response.get("content") if isinstance(response, dict) else response

                # Try to detect and format JSON recipe output from RecipeCreator
                if agent.name == "RecipeCreator" and isinstance(content, str):
                    json_str = extract_json_from_response(content)
                    if json_str:
                        try:
                            recipe_data = json.loads(json_str)
                            formatted = format_recipe(recipe_data)
                            print(f"{agent.name}:\n{formatted}")
                            content = formatted  # update content to formatted for next agent if needed
                        except Exception as e:
                            # fallback to raw content on JSON parse error
                            print(f"{agent.name}: {content}")
                    else:
                        print(f"{agent.name}: {content}")
                else:
                    print(f"{agent.name}: {content}")

                if isinstance(content, str) and "TERMINATE" in content:
                    print(f"{agent.name} requested termination. Ending chat.")
                    break

                current_message = content
            turn += 1

chat = RoundRobinGroupChat([user_proxy, recipe_creator, nutrition_checker])
chat.run("Generate a vegan dinner recipe for 2 people.")
