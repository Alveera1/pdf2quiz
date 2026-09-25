import streamlit as st
import tempfile
import os

from pdf_reader import extract_text
from text_processor import clean_text
from quiz_generator import generate_questions
from output_generator import save_to_txt

st.set_page_config(page_title="PDF2Quiz", page_icon="📚")

st.title("PDF2Quiz")
st.caption("Automated Question Generator from Study Materials")

uploaded_file = st.file_uploader("Upload your study material (PDF)", type=["pdf"])

col1, col2 = st.columns(2)
with col1:
    question_type = st.selectbox(
        "Question Type",
        ["mcq", "true_false", "fill_blank", "short_answer", "long_answer", "descriptive"]
    )
    num_questions = st.selectbox("Number of Questions", [2, 3, 5, 10])

with col2:
    difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
    max_chars = st.slider("Amount of PDF text to use (characters)", 500, 8000, 2000, step=500)

st.caption("Tip: fewer questions and shorter text = faster, more reliable generation.")

generate_btn = st.button("⚡ Generate Questions", type="primary", disabled=(uploaded_file is None))

if generate_btn and uploaded_file is not None:
    with st.spinner("Reading PDF..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        raw_text = extract_text(tmp_path)
        cleaned_text = clean_text(raw_text)
        text_chunk = cleaned_text[:max_chars]
        os.unlink(tmp_path)

    with st.spinner(f"Generating {num_questions} {question_type} questions... this can take up to 2 minutes on the free API tier"):
        try:
            questions = generate_questions(
                text_chunk,
                question_type=question_type,
                num_questions=num_questions,
                difficulty=difficulty
            )
            st.session_state["questions"] = questions
            st.session_state["question_type"] = question_type
            st.session_state["difficulty"] = difficulty
            st.success("Questions generated successfully!")
        except Exception as e:
            st.error(f"Generation failed after retries: {e}")
            st.info("This is usually a temporary slowdown on the free API tier. Try again, or reduce the number of questions / text length.")
            st.session_state["questions"] = None

if st.session_state.get("questions"):
    questions = st.session_state["questions"]
    qtype = st.session_state["question_type"]
    diff = st.session_state["difficulty"]

    st.divider()
    st.subheader("Generated Questions")

    for i, q in enumerate(questions, start=1):
        st.markdown(f"**{i}. {q['question']}**")
        if qtype == "mcq":
            for letter, option in q["options"].items():
                st.write(f"   {letter}. {option}")
        with st.expander("Show answer"):
            st.write(q["correct_answer"])
        st.write("")

    filename = save_to_txt(questions, qtype, diff)
    with open(filename, "rb") as f:
        st.download_button(
            label="📥 Download Questions (.txt)",
            data=f,
            file_name=filename,
            mime="text/plain"
        )