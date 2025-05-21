import asyncio
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Avoid GUI backend issues
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env file")
genai.configure(api_key=GEMINI_API_KEY)

class GeminiLLMWrapper:
    def __init__(self):
        self.model = genai.GenerativeModel(model_name="models/gemini-pro")


    async def generate_summary(self, prompt: str) -> str:
        response = await asyncio.to_thread(self.model.generate_content, prompt)
        return response.text

# Agent: Data Fetcher
class DataFetcher:
    async def fetch(self, csv_path: str) -> pd.DataFrame:
        print("[DataFetcher] Loading CSV data...")
        df = await asyncio.to_thread(pd.read_csv, csv_path)
        print("[DataFetcher] Data loaded.")
        return df

# Agent: Analyst
class Analyst:
    def __init__(self, llm: GeminiLLMWrapper):
        self.llm = llm

    async def analyze(self, df: pd.DataFrame, column: str):
        print(f"[Analyst] Generating visualizations for: {column}")
        
        # Line Chart
        line_file = "linechart.png"
        await asyncio.to_thread(self.plot_linechart, df, column, line_file)

        # Bar Chart
        bar_file = "barchart.png"
        await asyncio.to_thread(self.plot_barchart, df, column, bar_file)

        # Histogram
        hist_file = "histogram.png"
        await asyncio.to_thread(self.plot_histogram, df, column, hist_file)


        prompt = f"Summarize the data distribution and pattern for the column '{column}'."
        summary = await self.llm.generate_summary(prompt)
        print("[Analyst] Summary generated via Gemini.")
        return hist_file, line_file, bar_file, summary


    def plot_linechart(self, df, column, file):
        plt.figure()
        df[column].plot(kind='line')
        plt.title(f"Line Chart of {column}")
        plt.savefig(file)
        plt.close()

    def plot_barchart(self, df, column, file):
        plt.figure()
        df[column].head(10).plot(kind='bar')  # limit to first 10 for clarity
        plt.title(f"Bar Chart of {column} (Top 10 rows)")
        plt.savefig(file)
        plt.close()

    def plot_histogram(self, df, column, file):
        plt.figure()
        df[column].hist()
        plt.title(f"Histogram of {column}")
        plt.savefig(file)
        plt.close()

# Group Chat: Round Robin
class RoundRobinGroupChat:
    def __init__(self, agents):
        self.agents = agents
        self.index = 0

    async def run(self, csv_path):
        fetcher = self.agents[self.index]
        self.index = (self.index + 1) % len(self.agents)

        df = await fetcher.fetch(csv_path)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if not numeric_cols:
            raise ValueError("No numeric columns found in the CSV file.")

        print("Available numeric columns:")
        for col in numeric_cols:
            print(f" - {col}")

        selected_col = None
        while selected_col not in numeric_cols:
            selected_col = input("Enter a column name to analyze: ").strip()
            if selected_col not in numeric_cols:
                print("Invalid column name. Try again.")

        analyst = self.agents[self.index]
        self.index = (self.index + 1) % len(self.agents)

        hist_file, line_file, bar_file, summary = await analyst.analyze(df, selected_col)
        return line_file, bar_file,hist_file, summary

# Main async function
async def main():
    csv_path = "dataset.csv"  # Replace with your file name

    llm = GeminiLLMWrapper()
    data_fetcher = DataFetcher()
    analyst = Analyst(llm)

    chat = RoundRobinGroupChat([data_fetcher, analyst])

    try:
        hist, line, bar, summary = await chat.run(csv_path)
        print("\nPipeline complete!")
        print(f"Line chart saved to: {line}")
        print(f"Bar chart saved to: {bar}")
        print(f"Histogram saved to: {hist}")
        print(f"\nGemini Summary:\n{summary}")
    except Exception as e:
        print(f"Pipeline error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
