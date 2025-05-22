import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

# Load Gemini API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing.")
genai.configure(api_key=GEMINI_API_KEY)

# Gemini wrapper
class GeminiLLMWrapper:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def generate(self, prompt: str) -> str:
        response = await asyncio.to_thread(self.model.generate_content, prompt)
        return response.text

# RAG Retriever
class RAGRetriever:
    def __init__(self, collection):
        self.collection = collection

    async def retrieve(self, query: str) -> str:
        print("[RAGRetriever] Querying ChromaDB...")
        results = await asyncio.to_thread(
            self.collection.query,
            query_texts=[query],
            n_results=3
        )
        documents = results.get("documents", [[]])[0]
        return "\n\n".join(documents) if documents else ""

# Query Handler
class QueryHandler:
    def __init__(self, llm: GeminiLLMWrapper):
        self.llm = llm

    async def answer(self, query: str, context: str) -> str:
        if not context:
            return "Sorry, I couldn't find relevant information to answer your question."

        prompt = (
            f"You are an FAQ assistant. Use the following context to answer the user's question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{query}"
        )
        print("[QueryHandler] Generating answer...")
        return await self.llm.generate(prompt)

class SelectorGroupChat:
    def __init__(self, retriever: RAGRetriever, handler: QueryHandler):
        self.retriever = retriever
        self.handler = handler

    async def run(self, query: str):
        context = await self.retriever.retrieve(query)
        response = await self.handler.answer(query, context)
        return response

# Load data into ChromaDB
def load_documents():
    client = chromadb.PersistentClient(path="chroma_db")
    embedding_func = GoogleGenerativeAiEmbeddingFunction(api_key=GEMINI_API_KEY, model_name="models/embedding-001")
    collection = client.get_or_create_collection(name="faq_collection", embedding_function=embedding_func)

    if collection.count() == 0:
        print("[Init] Loading documents into ChromaDB...")
        with open("faq.txt", "r", encoding="utf-8") as f:
            docs = f.read().split("\n\n")
        for i, doc in enumerate(docs):
            collection.add(
                documents=[doc],
                metadatas=[{"source": f"faq{i}"}],
                ids=[f"doc{i}"]
            )
        print("[Init] Documents added.")

    return collection

async def main():
    collection = load_documents()
    retriever = RAGRetriever(collection)
    llm = GeminiLLMWrapper()
    handler = QueryHandler(llm)
    chat = SelectorGroupChat(retriever, handler)

    print("\n=== FAQ Chatbot with RAG is ready ===")
    while True:
        query = input("\nAsk a question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        try:
            answer = await chat.run(query)
            print(f"\n💬 Answer:\n{answer}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
