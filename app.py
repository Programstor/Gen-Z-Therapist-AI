import streamlit as st
import os
from datetime import datetime
from datetime import timedelta
from gemini import response
import locale
from localize import get_translation

# Разпознаване на език от системата
def get_language():
    lang, _ = locale.getdefaultlocale()  # Връща 'en_US' или 'bg_BG'
    if lang[:2] in ['bg', 'fr', 'es']:
        return lang[:2] # Връща само 'en' или 'bg'
    else:
        return 'en'

lang = get_language()

st.set_page_config(page_title=get_translation(lang,"page"), page_icon="🧑‍⚕️", layout="wide", initial_sidebar_state="expanded")

# Скриване на горния колонтитул и задаване на снимка за фон
st.markdown("""
    <style>
    .stAppHeader {display: none;}
    .stApp {
            background-image: url("https://i.imgur.com/jFXmNPN.png");
            background-size: 90% 100%;
            background-repeat: no-repeat;
            background-position: top right;
        }
    .stBottom,  
.st-emotion-cache-32nds3  {background: transparent !important;}
    </style>
    """, unsafe_allow_html=True)

# Заглавие на сайта
st.title(get_translation(lang,"title"))

# Създаване на папка за записаните чатове
CHAT_DIR = "saved_chats"
os.makedirs(CHAT_DIR, exist_ok=True)

# Функция за логване на грешки в общ файл
def log_error(e):
    with open("error_log.txt", "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now()}] {repr(e)}\n")

# Инициализираме session_state ако не съществуват
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "loaded_file" not in st.session_state:
    st.session_state.loaded_file = None

# Зареждане на чат от файл
def load_chat(file):
    try:
        with open(os.path.join(CHAT_DIR, file), "r", encoding="utf-8") as f:
            lines = f.readlines()
        history = []
        for line in lines[1:]:
            if "::" in line:
                role, msg = line.strip().split("::", 1)
                history.append((role, msg))
        st.session_state.chat_history = history
        st.session_state.loaded_file = file
    except Exception as e:
        log_error(e)

# Запазване на текущия чат
def save_current_chat():
    try:
        if not st.session_state.chat_history:
            return

        content = "\n".join(f"{role}::{msg}" for role, msg in st.session_state.chat_history)

        if st.session_state.loaded_file:
            file_path = os.path.join(CHAT_DIR, st.session_state.loaded_file)
            with open(file_path, "r", encoding="utf-8") as f:
                first_line = f.readline()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(first_line)
                f.write(content)
        else:
            # Създаване на резюме на разговора
            summary = response(f"Summarize me the conversation in 4 words at max, NO emojis and NO quotes from the real conversation, using the language it was mostly written in:\n{content}").strip()
            summary = summary.replace("\n", " ").replace(".", "").replace("\"", "")

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(CHAT_DIR, f"chat_{timestamp}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"summary::{summary}\n")
                f.write(content)
            st.session_state.loaded_file = f"chat_{timestamp}.txt"
    except Exception as e:
        log_error(e)

# Странична лента със бутони и списък със записани чатове
with st.sidebar:
    if st.sidebar.button(f"💬   {get_translation(lang, 'new')}   💬", use_container_width=True):
        save_current_chat()
        st.session_state.chat_history = []
        st.session_state.loaded_file = None
        st.rerun()

    # Бутон за изтриване на всички чатове
    if st.sidebar.button(f"🗑️   {get_translation(lang, 'delete')}   🗑️", use_container_width=True, type="secondary"):
        try:
            for file in os.listdir(CHAT_DIR):
                if file.endswith(".txt"):
                    os.remove(os.path.join(CHAT_DIR, file))
            st.session_state.loaded_file = None
            st.session_state.chat_history = []
            st.rerun()
        except Exception as e:
            log_error(e)

    st.header(f"  💾 {get_translation(lang, 'load')}")
    try:
        shown_labels = []
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        daybefore = yesterday - timedelta(days=1)

        for file in sorted(os.listdir(CHAT_DIR), reverse=True):
            if file.endswith(".txt"):
                try:
                    timestamp_formatted = file.split("_")[1]  # "2025-04-26"
                    chat_date = datetime.strptime(timestamp_formatted, "%Y-%m-%d").date()

                    if chat_date == today:
                        label = get_translation(lang, "today")  # e.g. "Today"
                    elif chat_date == yesterday:
                        label = get_translation(lang, "yesterday")  # e.g. "Yesterday"
                    else:
                        label = chat_date.strftime("%d.%m.%Y")  # EU date format

                    if not label in shown_labels:
                        st.markdown(label)
                        shown_labels.append(label)

                    with open(os.path.join(CHAT_DIR, file), "r", encoding="utf-8") as f:
                        first_line = f.readline()
                        summary = first_line.replace("summary::", "").strip() if first_line.startswith("summary::") else file

                    if st.button(summary, use_container_width=True):
                        load_chat(file)
                except Exception as e:
                    log_error(e)
    except Exception as e:
        log_error(e)

# Контейнер за визуализация на целия разговор
messages = st.container(height=600)
with messages:
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

# Поле за въвеждане на ново съобщение
try:
    prompt = st.chat_input(get_translation(lang, 'placeholder'))
    if prompt:
        st.session_state.chat_history.append(("user", prompt))
        with messages:
            with st.chat_message("user"):
                st.markdown(prompt)

        ai_response = response(prompt)
        st.session_state.chat_history.append(("ai", ai_response))
        with messages:
            with st.chat_message("ai"):
                st.markdown(ai_response)
except Exception as e:
    log_error(e)
