import argparse
from pdf_reader import extract_text
from text_processor import clean_text
from quiz_generator import generate_questions, print_questions
from output_generator import save_to_txt

def main():
    parser = argparse.ArgumentParser(description="PDF2Quiz - Generate questions from a study PDF")
    parser.add_argument("--pdf", required=True, help="Path to the PDF file")
    parser.add_argument("--type", default="mcq",
                         choices=["mcq", "true_false", "fill_blank", "short_answer", "long_answer", "descriptive"],
                         help="Type of questions to generate")
    parser.add_argument("--num", type=int, default=5, help="Number of questions")
    parser.add_argument("--difficulty", default="medium",
                         choices=["easy", "medium", "hard"], help="Difficulty level")
    parser.add_argument("--chars", type=int, default=4000,
                         help="How many characters of cleaned text to use (limits prompt size)")

    args = parser.parse_args()

    print(f"\n>>> Reading {args.pdf}...")
    raw = extract_text(args.pdf)
    cleaned = clean_text(raw)
    text_chunk = cleaned[:args.chars]

    print(f">>> Generating {args.num} {args.type} questions at {args.difficulty} difficulty...\n")
    questions = generate_questions(text_chunk, question_type=args.type,
                                    num_questions=args.num, difficulty=args.difficulty)

    print_questions(questions, args.type)

    filename = save_to_txt(questions, args.type, args.difficulty)
    print(f"\n>>> Saved to {filename}")


if __name__ == "__main__":
    main()