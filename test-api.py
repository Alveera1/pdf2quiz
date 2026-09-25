import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
def generate_mcqs(text, num_questions=5, difficulty="medium"):
    prompt = f"""You are a question generator. Based ONLY on the study material below, generate exactly {num_questions} multiple-choice questions at {difficulty} difficulty.

Rules:
- Questions must be answerable using only the material provided.
- Do not use outside knowledge.
- Each question must have exactly 4 options (A, B, C, D).
- Only one option is correct.

Return ONLY valid JSON, in this exact format, with no extra text, no markdown, no explanation:

{{
  "questions": [
    {{
      "question": "...",
      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
      "correct_answer": "A"
    }}
  ]
}}

Study material:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=4096,
        timeout=60
    )

    raw_output = response.choices[0].message.content

    # Clean up in case the model wraps output in markdown fences
    cleaned = raw_output.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        data = json.loads(cleaned)
        return data["questions"]
    except (json.JSONDecodeError, KeyError) as e:
        print("Failed to parse JSON. Raw output was:")
        print(raw_output)
        raise e


def print_questions(questions):
    for i, q in enumerate(questions, start=1):
        print(f"\n{i}. {q['question']}")
        for letter, option in q['options'].items():
            print(f"   {letter}. {option}")
        print(f"   Answer: {q['correct_answer']}")


if __name__ == "__main__":
    from pdf_reader import extract_text
    from text_processor import clean_text

    raw = extract_text("sample.pdf")
    cleaned = clean_text(raw)

    # Small slice for a fast first test
    sample_chunk = cleaned[:800]

    print("\n>>> Sending request to Nvidia API, please wait (may take up to a minute)...\n")
    questions = generate_mcqs(sample_chunk, num_questions=2, difficulty="medium")
    print(">>> Response received!\n")
    print_questions(questions)