import streamlit as st
from deep_translator import GoogleTranslator
import pyperclip
import time
import speech_recognition as sr

st.set_page_config(layout="wide", page_title="Language Translator", page_icon="public/icon.jpg")
st.title("Language Translator")

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        body, .stApp {
            background-color: #0a0a0a;
            color: #d0d0d0;
        }
        .stTextArea textarea {
            background-color: #1f1f1f;
            color: #f0f0f0;
            border: 1px solid #00ffff;
            border-radius: 12px;
            height: 240px;
            box-shadow: 0 0 15px #00ffff;
            font-size: 20px;
            transition: all 0.3s ease-in-out;
        }
        .stTextArea textarea:focus {
            box-shadow: 0 0 25px #00ffff;
            border-color: #ffffff;
        }
        .stTextArea textarea:disabled {
            color: #ffffff;
            -webkit-text-fill-color: #ffffff;
        }
        .stSelectbox > div {
            background-color: #1f1f1f;
            border: 1px solid #00ffff;
            border-radius: 10px;
        }
        .stSelectbox [data-baseweb="select"] > div {
            background-color: #1f1f1f;
            color: #f0f0f0;
        }
        div[data-testid="stVirtualDropdown"] ul {
            background-color: #1f1f1f;
            border: 2px solid #00ffff;
        }
        div[data-testid="stVirtualDropdown"] li:hover {
            background-color: #2f2f2f;
        }
        h1 {
            color: #00ffff;
            text-align: center;
            text-shadow: 0 0 36px #00ffff;
            padding-bottom: 20px;
        }
        .icon-bar {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            padding-top: 10px;
        }
        .icon-bar i {
            color: #00ffff;
            font-size: 20px;
            margin-left: 15px;
            cursor: pointer;
        }
        .stButton>button {
            background-color: transparent;
            border: none;
            color: #00ffff;
            font-size: 20px;
            padding: 0;
            margin-left: 15px;
        }
        .stButton>button:hover {
            color: #ffffff;
        }
        [data-testid="stTooltipContent"] {
            width: 120px;
            background-color: #1f1f1f;
            color: #f0f0f0;
            border: 1px solid #00ffff;
            border-radius: 5px;
            padding: 5px;
        }
        [data-testid="stAlert"] {
            width: 300px !important;
        }
        [data-testid="stSpinner"] > div {
            width: auto !important;
            min-width: 200px;
        }
    </style>
""", unsafe_allow_html=True)


lang_map = {
    "English": "en", "Arabic": "ar", "Bengali": "bn", "Bulgarian": "bg",
    "Catalan": "ca", "Chinese (Simplified)": "zh-CN", "Chinese (Traditional)": "zh-TW",
    "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl", "Finnish": "fi",
    "French": "fr", "German": "de", "Greek": "el", "Gujarati": "gu", "Hebrew": "he",
    "Hindi": "hi", "Hungarian": "hu", "Indonesian": "id", "Italian": "it", "Japanese": "ja",
    "Kannada": "kn", "Korean": "ko", "Latvian": "lv", "Lithuanian": "lt", "Malayalam": "ml",
    "Marathi": "mr", "Nepali": "ne", "Norwegian": "no", "Persian": "fa", "Polish": "pl",
    "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro", "Russian": "ru", "Serbian": "sr",
    "Slovak": "sk", "Slovenian": "sl", "Spanish": "es", "Swahili": "sw", "Swedish": "sv",
    "Tagalog": "tl", "Tamil": "ta", "Telugu": "te", "Thai": "th", "Turkish": "tr",
    "Ukrainian": "uk", "Urdu": "ur", "Vietnamese": "vi", "Welsh": "cy"
}
lang_names = list(lang_map.keys())

source_lang_options = ["Detect Language"] + lang_names
target_lang_options = lang_names
lang_codes = list(lang_map.values())
english_index = lang_names.index("English")

def show_alert(message, alert_type="success"):
    if alert_type == "success":
        alert = st.success(message)
    elif alert_type == "warning":
        alert = st.warning(message)
    elif alert_type == "error":
        alert = st.error(message)
    else:
        return

    time.sleep(2)
    alert.empty()

def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            show_alert("⏱️ No voice detected. Please try again.", "warning")
            return ""
        except sr.UnknownValueError:
            show_alert("❌ Could not catch that, Please try again.", "error")
            return ""
        except sr.RequestError:
            show_alert("⚠️ API issue. Check internet.", "error")
            return ""

if "spoken_text_buffer" in st.session_state:
    st.session_state.source_text = st.session_state.spoken_text_buffer
    del st.session_state.spoken_text_buffer

col1, col2, col3 = st.columns([0.475, 0.05, 0.475])

with col1:
    source_lang = st.selectbox("From", source_lang_options, index=0, key="source_lang_select")
    if "source_text" not in st.session_state:
        st.session_state.source_text = ""

    source_text = st.text_area("Enter text to translate", height=300, key="source_text", label_visibility="collapsed", placeholder="Type or paste text here")
    

    icon_spacer, mic_col, copy_col = st.columns([0.95, 0.1, 0.1])

    with mic_col:
        if st.button("🎤", key="mic_input_btn", help="Start voice input"):
            with st.spinner("Listening..."):
                spoken_text = transcribe_audio()
                if spoken_text:
                    st.session_state.spoken_text_buffer = spoken_text
                    st.rerun()

    with copy_col:
        if st.button("📋", key="copy_input_btn", help="Copy to clipboard"):
            pyperclip.copy(source_text)
            show_alert("Text copied!")


with col2:
    st.markdown('<div style="text-align: center; padding-top: 180px; color: #00ffff; font-size: 32px;">&#8596;</div>', unsafe_allow_html=True)

with col3:
    target_lang = st.selectbox("To", target_lang_options, index=english_index, key="target_lang_select")

    if source_text:
        try:
            source_lang_code = 'auto' if source_lang == "Detect Language" else lang_map[source_lang]
            target_lang_code = lang_map[target_lang]
            st.session_state.translated_text = GoogleTranslator(source=source_lang_code, target=target_lang_code).translate(source_text)
        except Exception as e:
            show_alert(f"An error occurred: {e}", "error")
    else:
        st.session_state.translated_text = ""

    st.text_area("Translated Text", value=st.session_state.translated_text, height=300, disabled=True, key="target_text", label_visibility="collapsed", placeholder="Translation will appear here")

    if st.session_state.translated_text:
        icon_spacer_2, copy_col_2, empty_col = st.columns([0.8, 0.1, 0.1])
        with copy_col_2:
            if st.button("📋", key="copy_output_btn", help="Copy to clipboard"):
                pyperclip.copy(st.session_state.translated_text)
                show_alert("Text copied!")