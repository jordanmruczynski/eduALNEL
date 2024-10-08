import streamlit as st
from youtube_transcript_api import (
    YouTubeTranscriptApi, YouTubeRequestFailed, VideoUnavailable, InvalidVideoId, TooManyRequests,
    TranscriptsDisabled, NoTranscriptAvailable, NotTranslatable, TranslationLanguageNotAvailable,
    CookiePathInvalid, CookiesInvalid, FailedToCreateConsentCookie, NoTranscriptFound
)

from pytube import extract



def extract_video_id_from_url(url):
    try:
        return extract.video_id(url)
    except Exception:
        st.error("Please provide a valid YouTube URL.")
        example_urls = [
            'http://youtu.be/SA2iWivDJiE',
            'http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu',
            'http://www.youtube.com/embed/SA2iWivDJiE',
            'http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US',
            'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
            'https://www.youtube.com/watch?time_continue=9&v=n0g-Y0oo5Qs&feature=emb_logo'
        ]
        st.info("Here are some valid formats: " + " ,".join(example_urls))
        st.stop()


def get_transcript_text(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item["text"] for item in transcript])
    except (YouTubeRequestFailed, VideoUnavailable, InvalidVideoId, TooManyRequests, NoTranscriptAvailable, NotTranslatable,
            TranslationLanguageNotAvailable, CookiePathInvalid, CookiesInvalid, FailedToCreateConsentCookie):
        st.error("Spróbuj z innym filmem, wykryliśmy nieznany problem.")
        st.stop()
    except TranscriptsDisabled:
        st.error("Film ma wyłączone napisy. Wprowadź proszę inny.")
        st.stop()
    except NoTranscriptFound:
        st.error("Film ma wyłączone angielskie napisy. Upewnij się, że film jest po angielsku, lub ma włączone angielskie napisy.")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}. Please try again.")
        st.stop()