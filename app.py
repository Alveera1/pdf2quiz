# import streamlit as st
# import tempfile
# import os

# from pdf_reader import extract_text
# from text_processor import clean_text
# from quiz_generator import generate_questions
# from output_generator import save_to_txt, save_to_pdf

# st.set_page_config(page_title="PaperMind", page_icon="📚", layout="centered")

# # ---- Custom styling ----
# st.markdown("""
# <style>
#     .main { background-color: #fafafa; }
#     .block-container { padding-top: 2rem; }
#     h1 { color: #2c3e50; font-weight: 700; }
#     .stButton>button {
#         background-color: #4a6fa5;
#         color: white;
#         border-radius: 8px;
#         padding: 0.6em 1.5em;
#         font-weight: 600;
#         border: none;
#     }
#     .stButton>button:hover { background-color: #3a5a85; }
#     .question-card {
#         background-color: white;
#         border-radius: 10px;
#         padding: 1.2em;
#         margin-bottom: 1em;
#         box-shadow: 0 1px 4px rgba(0,0,0,0.08);
#         border-left: 4px solid #4a6fa5;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ---- Header ----
# st.title("📚 PaperMind")
# st.caption("Turn your study material into practice questions — instantly.")
# st.divider()

# # ---- Upload + options ----
# uploaded_file = st.file_uploader("Upload your study material (PDF)", type=["pdf"])

# col1, col2 = st.columns(2)
# with col1:
#     question_type = st.selectbox(
#         "Question Type",
#         ["mcq", "true_false", "fill_blank", "short_answer", "long_answer", "descriptive"],
#         format_func=lambda x: x.replace("_", " ").title(),
#         help="Choose the style of questions you want generated."
#     )
#     num_questions = st.selectbox(
#         "Number of Questions",
#         [2, 3, 5, 10],
#         help="More questions take slightly longer to generate."
#     )

# with col2:
#     difficulty = st.selectbox(
#         "Difficulty",
#         ["easy", "medium", "hard"],
#         format_func=str.title,
#         help="Hard questions require deeper understanding, not just recall."
#     )
#     content_depth = st.select_slider(
#         "How much of the document to use?",
#         options=["Quick skim", "Standard", "Deep dive", "Full document"],
#         value="Standard",
#         help="Quick skim is fastest. Full document gives the most thorough questions but takes longer."
#     )

# # Map friendly labels to actual character limits internally
# DEPTH_MAP = {
#     "Quick skim": 1000,
#     "Standard": 2500,
#     "Deep dive": 5000,
#     "Full document": 8000
# }
# max_chars = DEPTH_MAP[content_depth]

# st.caption("💡 Tip: fewer questions and a shorter 'depth' setting generate faster.")

# generate_btn = st.button("⚡ Generate Questions", type="primary", disabled=(uploaded_file is None))

# # ---- Generate ----
# if generate_btn and uploaded_file is not None:
#     with st.spinner("Reading PDF..."):
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#             tmp.write(uploaded_file.read())
#             tmp_path = tmp.name

#         raw_text = extract_text(tmp_path)
#         cleaned_text = clean_text(raw_text)
#         text_chunk = cleaned_text[:max_chars]
#         os.unlink(tmp_path)

#     with st.spinner(f"Generating {num_questions} {question_type.replace('_',' ')} questions..."):
#         try:
#             questions = generate_questions(
#                 text_chunk,
#                 question_type=question_type,
#                 num_questions=num_questions,
#                 difficulty=difficulty
#             )
#             st.session_state["questions"] = questions
#             st.session_state["question_type"] = question_type
#             st.session_state["difficulty"] = difficulty
#             st.success("Questions generated successfully!")
#         except Exception as e:
#             st.error(f"Generation failed: {e}")
#             st.session_state["questions"] = None

# # ---- Display results ----
# if st.session_state.get("questions"):
#     questions = st.session_state["questions"]
#     qtype = st.session_state["question_type"]
#     diff = st.session_state["difficulty"]

#     st.divider()
#     st.subheader("📝 Generated Questions")

#     for i, q in enumerate(questions, start=1):
#         with st.container():
#             st.markdown(f"""<div class="question-card">
#                 <b>{i}. {q['question']}</b>
#             </div>""", unsafe_allow_html=True)

#             if qtype == "mcq":
#                 for letter, option in q["options"].items():
#                     st.write(f"   **{letter}.** {option}")

#             with st.expander("Show answer"):
#                 st.write(q["correct_answer"])

#     st.divider()

#     # ---- Downloads ----
#     dl_col1, dl_col2 = st.columns(2)

#     with dl_col1:
#         txt_filename = save_to_txt(questions, qtype, diff)
#         with open(txt_filename, "rb") as f:
#             st.download_button(
#                 label="📄 Download as TXT",
#                 data=f,
#                 file_name=txt_filename,
#                 mime="text/plain",
#                 use_container_width=True
#             )

#     with dl_col2:
#         pdf_filename = save_to_pdf(questions, qtype, diff)
#         with open(pdf_filename, "rb") as f:
#             st.download_button(
#                 label="📕 Download as PDF",
#                 data=f,
#                 file_name=pdf_filename,
#                 mime="application/pdf",
#                 use_container_width=True
#             )

import streamlit as st
import tempfile
import os

from pdf_reader import extract_text
from text_processor import clean_text
from quiz_generator import generate_questions
from output_generator import save_to_txt, save_to_pdf

st.set_page_config(page_title="PaperMind", page_icon=":books:", layout="centered")

# ---- Custom styling ----
st.markdown("""
<style>
    .main { background-color: #f7f8fa; }
    .block-container { padding-top: 3rem; max-width: 760px; }

    h1 {
        color: #1a1a2e;
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.5px;
    }

    .subtitle {
        color: #6b7280;
        font-size: 1.05rem;
        margin-top: -0.5rem;
        margin-bottom: 1.5rem;
    }

    .section-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #374151;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }

    .stButton>button {
        background-color: #2b3a67;
        color: white;
        border-radius: 6px;
        padding: 0.65em 2em;
        font-weight: 600;
        font-size: 0.95rem;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1f2a4d;
    }
    .stButton>button:disabled {
        background-color: #d1d5db;
        color: #9ca3af;
    }

    .question-card {
        background-color: white;
        border-radius: 8px;
        padding: 1.3em 1.5em;
        margin-bottom: 0.9em;
        border: 1px solid #e5e7eb;
    }

    .question-number {
        color: #2b3a67;
        font-weight: 700;
        margin-right: 0.4em;
    }

    hr { margin: 1.8rem 0; border-color: #e5e7eb; }
</style>
""", unsafe_allow_html=True)

# ---- Header ----
st.title("PaperMind")
st.markdown('<p class="subtitle">Turn your study material into practice questions.</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload a PDF of your notes or textbook, choose how you want to be tested, and get instant practice questions generated from your own material.</p>', unsafe_allow_html=True)
st.divider()

# ---- Upload ----
st.markdown('<p class="section-label">Study Material</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], label_visibility="collapsed")

st.write("")

# ---- Options ----
col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="section-label">Question Type</p>', unsafe_allow_html=True)
    question_type = st.selectbox(
        "Question Type",
        ["mcq", "true_false", "fill_blank", "short_answer", "long_answer", "descriptive"],
        format_func=lambda x: x.replace("_", " ").title(),
        label_visibility="collapsed"
    )

    st.markdown('<p class="section-label" style="margin-top: 1rem;">Number of Questions</p>', unsafe_allow_html=True)
    num_questions = st.selectbox(
        "Number of Questions",
        [2, 3, 5, 10],
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<p class="section-label">Difficulty</p>', unsafe_allow_html=True)
    difficulty = st.selectbox(
        "Difficulty",
        ["easy", "medium", "hard"],
        format_func=str.title,
        label_visibility="collapsed"
    )

# Fixed internal setting — not exposed to the user
max_chars = 2500

st.write("")
generate_btn = st.button("Generate Questions", type="primary", disabled=(uploaded_file is None))

# ---- Generate ----
if generate_btn and uploaded_file is not None:
    with st.spinner("Reading document..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        raw_text = extract_text(tmp_path)
        cleaned_text = clean_text(raw_text)
        text_chunk = cleaned_text[:max_chars]
        os.unlink(tmp_path)

    with st.spinner("Generating questions..."):
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
        except Exception as e:
            st.error(f"Generation failed: {e}")
            st.session_state["questions"] = None

# ---- Display results ----
if st.session_state.get("questions"):
    questions = st.session_state["questions"]
    qtype = st.session_state["question_type"]
    diff = st.session_state["difficulty"]

    st.divider()
    st.markdown('<p class="section-label">Generated Questions</p>', unsafe_allow_html=True)

    for i, q in enumerate(questions, start=1):
        st.markdown(f"""
        <div class="question-card">
            <span class="question-number">{i}.</span>{q['question']}
        </div>
        """, unsafe_allow_html=True)

        if qtype == "mcq":
            for letter, option in q["options"].items():
                st.write(f"&nbsp;&nbsp;&nbsp;**{letter}.** {option}", unsafe_allow_html=True)

        with st.expander("Show answer"):
            st.write(q["correct_answer"])

    st.divider()

    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        txt_filename = save_to_txt(questions, qtype, diff)
        with open(txt_filename, "rb") as f:
            st.download_button(
                label="Download as TXT",
                data=f,
                file_name=txt_filename,
                mime="text/plain",
                use_container_width=True
            )

    with dl_col2:
        pdf_filename = save_to_pdf(questions, qtype, diff)
        with open(pdf_filename, "rb") as f:
            st.download_button(
                label="Download as PDF",
                data=f,
                file_name=pdf_filename,
                mime="application/pdf",
                use_container_width=True
            )