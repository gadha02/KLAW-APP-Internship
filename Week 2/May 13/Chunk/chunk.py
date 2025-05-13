import fitz

def extract_text_from_pdf(file_path):

    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks


if __name__ == "__main__":
    pdf_path = "Prompt Engineering.pdf"
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=800, overlap=100)
    
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1}\n{chunk}")

