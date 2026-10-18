import fitz

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num, page in enumerate(doc, start=1): #numbering of the page!!
        page_text = page.get_text()
        full_text += page_text
        print(f"--- Page {page_num} extracted ({len(page_text)} chars) ---")
    doc.close()
    return full_text

if __name__ == "__main__":
    text = extract_text("sample.pdf")
    print("\n===== FIRST 1000 CHARS =====\n")
    print(text[:1000])
    print(f"\nTotal length: {len(text)} characters")