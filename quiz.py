import streamlit as st
from openai_utils import get_quiz_data
from openai_utils import string_to_list, get_randomized_options
from youtube_utils import extract_video_id_from_url, get_transcript_text
from PyPDF2 import PdfReader
from pptx import Presentation
import time

# API Key
OPENAI_API_KEY = "REDACTED"

# Page configuration
st.set_page_config(
    page_title="eduALNEL",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Title and description
st.title(":orange[eduALNEL] - Obejrzyj 💻 - Naucz się 📖 - Sprawdź się! 📝", anchor=False)
st.write("""
**Jak działamy?** 🤔

👉 Wybierz źródło materiału (filmik YouTube, plik PDF, prezentacja PowerPoint lub własny pomysł), a my wygenerujemy Quiz, abyś mógł sprawdzić swoją wiedzę!

❗ Nasza aplikacja jest w fazie testów, więc prosimy o wyrozumiałość w przypadku błędów. Dziękujemy! 🙏
""")

# Initialize session state
if "quiz_data_list" not in st.session_state:
    st.session_state.quiz_data_list = []
    st.session_state.correct_answers = []
    st.session_state.randomized_options = []
    st.session_state.user_answers = []

# Function definitions
def process_pdf(file):
    reader = PdfReader(file)
    return "\n".join(page.extract_text() for page in reader.pages)

def process_pptx(file):
    presentation = Presentation(file)
    return "\n".join(
        shape.text for slide in presentation.slides for shape in slide.shapes if hasattr(shape, "text")
    )

# Source selection
source_option = st.radio("Wybierz źródło danych:", ["YouTube", "PDF", "PowerPoint (pptx)", "TXT", "Własny pomysł"])
input_text = ""

if source_option == "YouTube":
    youtube_url = st.text_input("Wprowadź link filmiku YouTube:", value="https://www.youtube.com/watch?v=RRubcjpTkks")
    if youtube_url:
        video_id = extract_video_id_from_url(youtube_url)
        input_text = get_transcript_text(video_id)

elif source_option == "PDF":
    pdf_file = st.file_uploader("Wgraj plik PDF:", type="pdf")
    if pdf_file:
        input_text = process_pdf(pdf_file)

elif source_option == "PowerPoint (pptx)":
    pptx_file = st.file_uploader("Wgraj plik PPTX:", type="pptx")
    if pptx_file:
        input_text = process_pptx(pptx_file)

elif source_option == "TXT":
    txt_file = st.file_uploader("Wgraj plik TXT:", type="txt")
    if txt_file:
        input_text = txt_file.read().decode("utf-8")

elif source_option == "Własny pomysł":
    input_text = st.text_area("Wpisz pomysł:", value="np. z książki \"Zemsta\" Aleksandra Fredry..")

# Difficulty and language selection
difficulty = st.selectbox("Wybierz poziom trudności:", ["Easy", "Medium", "Hard", "Expert"])
num_questions = st.slider("Liczba pytań:", min_value=1, max_value=20, value=5)
language = st.selectbox("Wybierz język pytań:", ["English", "Polish", "German", "French"])

# Quiz creation
if st.button("Stwórz Quiz"):
    if not input_text.strip():
        st.warning("Podaj dane wejściowe.")
        st.stop()

    with st.spinner("Trwa tworzenie quizu..."):
        quiz_data_str = get_quiz_data(input_text, OPENAI_API_KEY, difficulty=difficulty, num_questions=num_questions, language=language)
        st.session_state.quiz_data_list = string_to_list(quiz_data_str)

        st.session_state.correct_answers = []
        st.session_state.randomized_options = []
        st.session_state.user_answers = [None] * len(st.session_state.quiz_data_list)

        for q in st.session_state.quiz_data_list:
            options, correct_answer = get_randomized_options(q[1:])
            st.session_state.randomized_options.append(options)
            st.session_state.correct_answers.append(correct_answer)

# Quiz display
if st.session_state.quiz_data_list:
    st.subheader("Quiz: Przetestuj swoją wiedzę!")
    for i, q in enumerate(st.session_state.quiz_data_list):
        options = st.session_state.randomized_options[i]
        response = st.radio(q[0], options, key=f"question_{i}")
        st.session_state.user_answers[i] = response

    if st.button("Zobacz wyniki"):
        score = sum(
            user_ans == correct_ans
            for user_ans, correct_ans in zip(st.session_state.user_answers, st.session_state.correct_answers)
        )
        st.success(f"Wynik: {score}/{len(st.session_state.quiz_data_list)}")

        for i, (q, correct_ans, user_ans, options) in enumerate(zip(
                st.session_state.quiz_data_list,
                st.session_state.correct_answers,
                st.session_state.user_answers,
                st.session_state.randomized_options,
        )):
            with st.expander(f"Pytanie {i + 1}"):
                if user_ans != correct_ans:
                    st.info(f"Pytanie: {q[0]}")
                    st.error(f"Twoja odpowiedź: {user_ans}")
                    st.success(f"Prawidłowa odpowiedź: {correct_ans}")