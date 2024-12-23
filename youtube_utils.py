import streamlit as st
from youtube_transcript_api import (
    YouTubeTranscriptApi, YouTubeRequestFailed, VideoUnavailable, InvalidVideoId, TooManyRequests,
    TranscriptsDisabled, NoTranscriptAvailable, NotTranslatable, TranslationLanguageNotAvailable,
    CookiePathInvalid, CookiesInvalid, FailedToCreateConsentCookie, NoTranscriptFound
)

proxies = {
    "http": "http://brd-customer-hl_4dd03e87-zone-residential_proxy1-country-pl:o692i4vz45iv@brd.superproxy.io:33335",
    "https": "https://brd-customer-hl_4dd03e87-zone-residential_proxy1-country-pl:o692i4vz45iv@brd.superproxy.io:33335",
}

def extract_video_id_from_url(url):
    """Extracts video ID from YouTube URL."""
    from pytube import extract
    try:
        return extract.video_id(url)
    except Exception:
        st.error("Proszę podać prawidłowy format linku url YouTube.")
        example_urls = [
            'http://youtu.be/SA2iWivDJiE',
            'http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu',
            'http://www.youtube.com/embed/SA2iWivDJiE',
            'http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US',
            'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
            'https://www.youtube.com/watch?time_continue=9&v=n0g-Y0oo5Qs&feature=emb_logo'
        ]
        st.info("Przykładowe formaty: " + " ,".join(example_urls))
        st.stop()

def get_transcript_text(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pl', 'en', 'de'])
        return " ".join([item["text"] for item in transcript])
    except (YouTubeRequestFailed, VideoUnavailable, InvalidVideoId, TooManyRequests, NoTranscriptAvailable, NotTranslatable,
            TranslationLanguageNotAvailable, CookiePathInvalid, CookiesInvalid, FailedToCreateConsentCookie):
        st.error("Spróbuj z innym filmem, wykryliśmy nieznany problem.")
        st.stop()
    except TranscriptsDisabled:
        st.error("Chwilowo przekroczyłeś dopuszczalną ilość zapytań YouTube, spróbuj ponownie za chwilę z innym filmem.")
        st.stop()
    except NoTranscriptFound:
        st.error("Film nie posiada napisów w języku polskim, angielskim ani niemieckim :(")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}. Please try again.")
        st.stop()
