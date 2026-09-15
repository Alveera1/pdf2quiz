import re

def clean_text(raw_text):
    text = raw_text

    # Replace multiple newlines with a single space or paragraph break
    text = re.sub(r'\n{3,}', '\n\n', text)   # collapse 3+ newlines to 2
    text = re.sub(r'\n{2}', '\n', text)      # collapse remaining double newlines

    # Replace multiple spaces/tabs with a single space
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove standalone page numbers (lines that are just digits)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)

    # Fix common broken quote/dash characters from PDF extraction
    text = text.replace('―', '"').replace('‖', '"')
    text = text.replace('–', '-').replace('—', '-')

    # Strip leading/trailing whitespace on each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(line for line in lines if line)  # drop empty lines

    return text.strip()


def chunk_text(text, max_words=3000):
    """Split text into chunks so it fits within LLM context limits."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = ' '.join(words[i:i + max_words])
        chunks.append(chunk)
    return chunks


if __name__ == "__main__":
    from pdf_reader import extract_text

    raw = extract_text("sample.pdf")
    cleaned = clean_text(raw)

    print("===== BEFORE (first 500 chars) =====")
    print(raw[:500])
    print("\n===== AFTER (first 500 chars) =====")
    print(cleaned[:500])
    print(f"\nOriginal length: {len(raw)} | Cleaned length: {len(cleaned)}")

    chunks = chunk_text(cleaned)
    print(f"\nSplit into {len(chunks)} chunk(s) for LLM processing")