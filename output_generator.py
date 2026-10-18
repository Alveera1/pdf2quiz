
from fpdf import FPDF
from datetime import datetime


def sanitize_text(text):
    """Replace Unicode characters FPDF's default font can't handle."""
    replacements = {
        "\u2014": "-",   # em-dash —
        "\u2013": "-",   # en-dash –
        "\u2018": "'",   # left single quote '
        "\u2019": "'",   # right single quote '
        "\u201c": '"',   # left double quote "
        "\u201d": '"',   # right double quote "
        "\u2026": "...", # ellipsis …
        "\u2022": "-",   # bullet •
    }
    for unicode_char, replacement in replacements.items():
        text = text.replace(unicode_char, replacement)
    # Catch-all: strip any remaining non-latin-1 characters
    return text.encode("latin-1", "ignore").decode("latin-1")


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


def save_to_pdf(questions, question_type, difficulty, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"questions_{question_type}_{timestamp}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_x(pdf.l_margin)
    pdf.cell(0, 10, "PaperMind - Generated Questions", ln=True, align="C")
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_x(pdf.l_margin)
    pdf.cell(0, 8, sanitize_text(f"Type: {question_type} | Difficulty: {difficulty}"), ln=True, align="C")
    pdf.ln(5)
    pdf.set_draw_color(180, 180, 180)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    for i, q in enumerate(questions, start=1):
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 7, sanitize_text(f"{i}. {q['question']}"))
        pdf.ln(1)

        if question_type == "mcq" and "options" in q:
            pdf.set_font("Helvetica", "", 11)
            for letter, option in q["options"].items():
                pdf.set_x(pdf.l_margin + 5)
                pdf.multi_cell(0, 6, sanitize_text(f"{letter}. {option}"))
            pdf.ln(1)

        pdf.set_font("Helvetica", "I", 11)
        pdf.set_text_color(0, 100, 0)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 6, sanitize_text(f"Answer: {q['correct_answer']}"))
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

    pdf.output(filename)
    return filename