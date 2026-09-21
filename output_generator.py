from datetime import datetime

def save_to_txt(questions, question_type, difficulty, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"questions_{question_type}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("PDF2QUIZ - Generated Questions\n")
        f.write(f"Type: {question_type} | Difficulty: {difficulty}\n")
        f.write("-" * 40 + "\n\n")

        for i, q in enumerate(questions, start=1):
            f.write(f"{i}. {q['question']}\n")
            if question_type == "mcq":
                for letter, option in q['options'].items():
                    f.write(f"   {letter}. {option}\n")
            f.write(f"   Answer: {q['correct_answer']}\n\n")

    return filename