import fitz  

def extract_pdf_text(filepath):
    
    text = ""
    try:
        with fitz.open(filepath) as doc:
            for page_num, page in enumerate(doc, start=1):
                page_text = page.get_text()
                text += page_text
    except Exception as e:
        print(f"Error reading PDF")
    
    return text

def main():
    filepath = input("Enter the path to the PDF file : ").strip()
    pdf_text = extract_pdf_text(filepath)

    if pdf_text:
        print("\nExtracted Text: \n")
        print(pdf_text)
    else:
        print("No text could be extracted.")

if __name__ == "__main__":
    main()
