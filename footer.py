import streamlit as st

class Footer:
    """
    Klasa odpowiedzialna za generowanie stopki dla aplikacji Streamlit.
    """
    @staticmethod
    def render():
        """
        Metoda renderująca stopkę z dowolną treścią.
        """
        st.markdown(
            """
            ---
            <div style="text-align: center; font-size: 14px; color: #888;">
                📢 <strong>QuizCraft</strong> | Wersja Beta 3.1 | Copyright &copy; QuizCraft Wszystkie prawa zastrzeżone.
            </div>
            """,
            unsafe_allow_html=True
        )