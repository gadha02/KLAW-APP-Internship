import os
import asyncio
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import google.generativeai as genai
import aiofiles

# Load Gemini API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function: Fetch visible content from a webpage
def fetch_web_content(url: str) -> str:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    content = driver.find_element("tag name", "body").text
    driver.quit()
    return content[:10000]  # limit to 10k characters

# Function: Summarize text using Gemini
async def summarize_text(text: str) -> str:
    prompt = f"Summarize the following webpage content clearly and concisely:\n\n{text}"
    response = await model.generate_content_async(prompt)
    return response.text

# Main async flow
async def main():
    url = input("🔗 Enter the webpage URL to summarize: ").strip()

    print("\n🔍 Fetching webpage content...")
    content = fetch_web_content(url)

    print("🧠 Summarizing content using Gemini...\n")
    summary = await summarize_text(content)

    # Display summary
    print("📄 Summary:\n")
    print(summary)

    # Save to file
    async with aiofiles.open("final_summary.txt", "w") as f:
        await f.write(summary)

    print("\n✅ Summary saved to final_summary.txt")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
