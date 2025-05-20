import os
import asyncio
import tempfile
import subprocess
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")
genai.configure(api_key=api_key)

# Coder Agent
class Coder:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def run(self, task: str) -> str:
        print("\n[Coder generating code...]\n")
        prompt = f"Write short, functional Python code for:\n{task}"
        response = await asyncio.to_thread(self.model.generate_content, prompt)
        code = self._extract_code(response.text)
        print("[Generated Code]:\n", code[:300], "...\n")  # Show only first 300 chars
        return code

    def _extract_code(self, text: str) -> str:
        blocks = re.findall(r"```python(.*?)```", text, re.DOTALL)
        return "\n".join(blocks[:1]).strip() if blocks else text[:300].strip()

# Debugger Agent
class Debugger:
    async def run(self, code: str) -> str:
        print("\n[Debugger analyzing code...]\n")
        sanitized = re.sub(r'input\([^)]+\)', '"5"', code)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as f:
            f.write(sanitized)
            path = f.name

        try:
            lint = subprocess.check_output(
                ["pylint", path, "--disable=all", "--enable=E,F"],
                stderr=subprocess.STDOUT, universal_newlines=True
            )
        except subprocess.CalledProcessError as e:
            lint = e.output

        try:
            output = subprocess.check_output(
                ["python", path],
                stderr=subprocess.STDOUT, universal_newlines=True
            )
        except subprocess.CalledProcessError as e:
            output = e.output

        result = f"Lint Errors:\n{lint.strip()[:100]}...\n\nOutput:\n{output.strip()[:100]}..."

        print(result)
        return result

# Round Robin Controller
class RoundRobinGroupChat:
    def __init__(self, agents):
        self.agents = agents

    async def run(self, input_data):
        for agent in self.agents:
            input_data = await agent.run(input_data)
        return input_data

# Main Runner
async def main():
    print("=== Gemini Code Debugging Helper ===")
    task = input("\n Describe the Python coding task:\n> ")
    
    coder = Coder()
    debugger = Debugger()
    chat = RoundRobinGroupChat([coder, debugger])

    # Run generation and debugging
    await chat.run(task)


if __name__ == "__main__":
    asyncio.run(main())
