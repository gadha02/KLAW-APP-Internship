import os
import asyncio
import tempfile
import subprocess
from dotenv import load_dotenv
import google.generativeai as genai
import re

# Load Gemini API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

genai.configure(api_key=GEMINI_API_KEY)


class CodeGenerator:
    def __init__(self):
        self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    async def run(self, prompt_text):
        print("\n[Generating Python code...]\n")
        prompt = f"Create Python code for the following requirement:\n{prompt_text}"
        response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
        content = response.text

        # Extract code blocks with ```python ... ```
        code_segments = re.findall(r"```python(.*?)```", content, re.DOTALL)

        if code_segments:
            output_code = "\n\n".join(code_segments[:2]).strip()
        else:
            funcs = re.split(r"(?=def\s)", content)
            funcs = [f.strip() for f in funcs if f.strip()]
            if len(funcs) >= 2:
                output_code = "\n\n".join(funcs[:2])
            else:
                output_code = content[:1000].strip()

        print("[Generated Code]\n", output_code)
        return output_code


class CodeDebugger:
    async def run(self, source_code):
        print("\n[Running static analysis and executing code...]\n")
        # Replace input(...) calls with a default string "7" to avoid waiting for input
        sanitized_code = re.sub(r'input\([^)]+\)', '"7"', source_code)

        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as temp_file:
            temp_file.write(sanitized_code)
            temp_path = temp_file.name

        try:
            lint_report = subprocess.check_output(
                ["pylint", temp_path, "--disable=all", "--enable=E,F"],
                stderr=subprocess.STDOUT,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            lint_report = exc.output

        try:
            exec_output = subprocess.check_output(
                ["python", temp_path],
                stderr=subprocess.STDOUT,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            exec_output = exc.output

        # Clean up temp file
        os.unlink(temp_path)

        combined_result = f"Pylint Report:\n{lint_report}\n\nExecution Output:\n{exec_output}"
        print(combined_result)
        return combined_result


class AgentCoordinator:
    def __init__(self, agents_list):
        self.agents = agents_list

    async def process(self, input_data):
        current_data = input_data
        for agent in self.agents:
            current_data = await agent.run(current_data)
        return current_data


async def main():
    print("=== Gemini Powered Python Code Generator & Analyzer ===")

    generator = CodeGenerator()
    debugger = CodeDebugger()
    coordinator = AgentCoordinator([generator, debugger])

    user_request = input("\nEnter a description for the Python code you want:\n> ")
    await coordinator.process(user_request)

    print("\n✅ Task finished: code generation and analysis complete!")


if __name__ == "__main__":
    asyncio.run(main())
