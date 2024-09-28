import streamlit as st
from openai_utils import get_quiz_data
from quiz_utils import string_to_list, get_randomized_options
from youtube_utils import extract_video_id_from_url, get_transcript_text

OPENAI_API_KEY = "REDACTED"

st.set_page_config(
    page_title="eduALNEL",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title(":orange[eduALNEL] - Obejrzyj 💻 - Naucz się 📖 - Sprawdź się! 📝", anchor=False)
st.write("""

**Jak działamy?** 🤔

👉 Wklejasz nam link do filmiku na YouTube, z którego się ostatnio uczyłeś, a my wygenerujemy Ci Quiz na jego podstawie, abyś mógł sprawdzić swoją wiedze!

❗ Pamiętaj, aby filmik miał włączone angielskie napisy, lub był po angielsku! (większość filmików edukacyjnych ma)

""")

with st.form("user_input"):
    YOUTUBE_URL = st.text_input("Wprowadź link filmiku YouTube:", value="https://www.youtube.com/watch?v=RRubcjpTkks")
    submitted = st.form_submit_button("Stwórz Quiz i sprawdź moją wiedze!")

if submitted or ('quiz_data_list' in st.session_state):
    if not YOUTUBE_URL:
        st.info("Podaj prawidłowy format linku do filmiku na YouTube [YouTube](https://www.youtube.com/)")
        st.stop()

    with st.spinner("Trwa tworzenie quizu..."):
        if submitted:
            video_id = extract_video_id_from_url(YOUTUBE_URL)
            video_transcription = get_transcript_text(video_id)
            quiz_data_str = get_quiz_data(video_transcription, OPENAI_API_KEY)
            st.session_state.quiz_data_list = string_to_list(quiz_data_str)

            if 'user_answers' not in st.session_state:
                st.session_state.user_answers = [None for _ in st.session_state.quiz_data_list]
            if 'correct_answers' not in st.session_state:
                st.session_state.correct_answers = []
            if 'randomized_options' not in st.session_state:
                st.session_state.randomized_options = []

            for q in st.session_state.quiz_data_list:
                options, correct_answer = get_randomized_options(q[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)

        with st.form(key='quiz_form'):
            st.subheader("Quiz: Przetestuj swoją wiedze!", anchor=False)
            for i, q in enumerate(st.session_state.quiz_data_list):
                options = st.session_state.randomized_options[i]
                default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
                response = st.radio(q[0], options, index=default_index)
                user_choice_index = options.index(response)
                st.session_state.user_answers[i] = user_choice_index


            results_submitted = st.form_submit_button(label='Zobacz wyniki!')

            if results_submitted:
                score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                st.success(f"Wynik: {score}/{len(st.session_state.quiz_data_list)}")

                if score == len(st.session_state.quiz_data_list):
                    st.balloons()
                else:
                    incorrect_count = len(st.session_state.quiz_data_list) - score
                    if incorrect_count == 1:
                        st.warning(f"Prawie idealnie! Popełniłeś tylko jeden błąd! Zobacz odpowiedzi:")
                    else:
                        st.warning(f"Prawie! Popełniłeś {incorrect_count} błędów. Zobacz odpowiedzi:")

                for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers, st.session_state.quiz_data_list, st.session_state.randomized_options)):
                    with st.expander(f"Pytanie {i + 1}", expanded=False):
                        if ro[ua] != ca:
                            st.info(f"Pytanie: {q[0]}")
                            st.error(f"Twoja odpowiedź: {ro[ua]}")
                            st.success(f"Prawidłowa odpowiedź: {ca}")