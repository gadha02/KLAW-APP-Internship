import chromadb

def main():
    # Task 1: Initialize Chroma instance
    client = chromadb.PersistentClient(path="chroma_db") 

    collection = client.get_or_create_collection(name="sample_collection")

    # Task 2: Adding sample document
    collection.add(
        documents=["ChromaDB is an open-source embedding database designed for LLM applications."],
        metadatas=[{"source": "introduction"}],
        ids=["doc1"]
    )

    results = collection.query(
        query_texts=["What is ChromaDB?"],
        n_results=1
    )

    print("\nQuery Results:")
    print(results)

if __name__ == "__main__":
    main()
