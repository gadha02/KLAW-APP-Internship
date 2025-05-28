import os
from dotenv import load_dotenv
from sympy import symbols, Eq, solve, diff, sympify
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

config_list = [
    {
        "model": "gemini-1.5-flash",
        "api_key": api_key,
        "api_type": "google"
    }
]

llm_config = {
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}


def solve_math_problem(problem: str) -> str:
    x = symbols('x')
    try:
        if 'differentiate' in problem.lower():
            expr = sympify(problem.lower().replace('differentiate', '').strip())
            result = diff(expr, x)
        elif '=' in problem:
            lhs, rhs = problem.split('=')
            equation = Eq(sympify(lhs), sympify(rhs))
            result = solve(equation, x)
        else:
            result = eval(problem)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def verify_solution(problem: str, solution: str) -> str:
    x = symbols('x')
    try:
        if '=' in problem:
            lhs, rhs = problem.split('=')
            lhs_expr = sympify(lhs)
            rhs_expr = sympify(rhs)
            solutions = eval(solution)
            if not isinstance(solutions, list):
                solutions = [solutions]
            for sol in solutions:
                if lhs_expr.subs(x, sol) != rhs_expr.subs(x, sol):
                    return "Incorrect"
            return "Correct. TERMINATE"
        return "Cannot verify without equation form"
    except Exception as e:
        return f"Error in verification: {str(e)}"


problem_solver = AssistantAgent(
    name="ProblemSolver",
    llm_config=llm_config,
    system_message="You solve math problems using the 'solve_math_problem' tool.",
    function_map={"solve_math_problem": solve_math_problem}
)

verifier = AssistantAgent(
    name="Verifier",
    llm_config=llm_config,
    system_message="You verify math solutions using 'verify_solution'. If correct, say 'Correct. TERMINATE'.",
    function_map={"verify_solution": verify_solution}
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    code_execution_config={"use_docker": False},
    system_message="You are the user providing math problems."
)


group_chat = GroupChat(
    agents=[user_proxy, problem_solver, verifier],
    messages=[],
    max_round=10,
    allow_repeat_speaker=True
)

chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config
)


if __name__ == "__main__":
    user_input = input("Enter a math problem to solve and verify (e.g., x**2 - 4 = 0): ")
    user_proxy.initiate_chat(chat_manager, message=f"Solve and verify: {user_input}")
