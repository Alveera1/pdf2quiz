import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

# Prompt instructions specific to each question type
FORMAT_INSTRUCTIONS = {
    "mcq": """Each question must have exactly 4 options (A, B, C, D), with only one correct.
Return JSON in this format:
{
  "questions": [
    {"question": "...", "options": {"A": "...", "B": "...", "C": "...", "D": "..."}, "correct_answer": "A"}
  ]
}""",

    "true_false": """Each question must be a statement the user judges as True or False.
Return JSON in this format:
{
  "questions": [
    {"question": "...", "correct_answer": "True"}
  ]
}""",

    "fill_blank": """Each question must be a sentence with a blank shown as ______.
Return JSON in this format:
{
  "questions": [
    {"question": "...", "correct_answer": "..."}
  ]
}""",

    "short_answer": """Each question expects a 1-2 sentence answer.
Return JSON in this format:
{
  "questions": [
    {"question": "...", "correct_answer": "..."}
  ]
}""",

    "long_answer": """Each question expects a detailed, multi-sentence answer.
Return JSON in this format:
{
  "questions": [
    {"question": "...", "correct_answer": "..."}
  ]
}""",

    "descriptive": """Each question should ask the user to explain or describe a concept in depth (essay-style).
Return JSON in this format:
{
  "questions": [
    {"question": "...", "correct_answer": "..."}
  ]
}"""
}


def generate_questions(text, question_type="long_answer", num_questions=5, difficulty="medium"):
    if question_type not in FORMAT_INSTRUCTIONS:
        raise ValueError(f"Unknown question_type '{question_type}'. Choose from: {list(FORMAT_INSTRUCTIONS.keys())}")

    format_instruction = FORMAT_INSTRUCTIONS[question_type]

    prompt = f"""You are a question generator. Based ONLY on the study material below, generate exactly {num_questions} {question_type.replace('_', ' ')} questions at {difficulty} difficulty.

Rules:
- Questions must be answerable using only the material provided.
- Do not use outside knowledge.
- Return ONLY valid JSON, no extra text, no markdown, no explanation.

{format_instruction}

Study material:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=4096,
        timeout=120
    )

    raw_output = response.choices[0].message.content
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


def print_questions(questions, question_type):
    for i, q in enumerate(questions, start=1):
        print(f"\n{i}. {q['question']}")
        if question_type == "mcq":
            for letter, option in q['options'].items():
                print(f"   {letter}. {option}")
        print(f"   Answer: {q['correct_answer']}")


if __name__ == "__main__":
    from pdf_reader import extract_text
    from text_processor import clean_text

    raw = extract_text("sample.pdf")
    cleaned = clean_text(raw)
    sample_chunk = cleaned[:800]

    # 👇 Change this to whatever type you want to test: mcq, true_false, fill_blank, short_answer, long_answer, descriptive
    qtype = "long_answer"

    print(f"\n>>> Generating {qtype} questions...\n")
    questions = generate_questions(sample_chunk, question_type=qtype, num_questions=3, difficulty="medium")
    print_questions(questions, qtype)