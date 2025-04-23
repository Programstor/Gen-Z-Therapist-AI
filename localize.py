# Всички поддържани езици на сайта
translations = {
    'en': {
        'page': "Therapist AI",
        'title': "Gen Z Therapist AI",
        'placeholder': "Type something here...",
        'new': "💬  New chat  🗨️",
        'load': "Previous convos:"
    },
    'bg': {
        'page': "Терапевт AI",
        'title': "Gen Z Терапевт AI",
        'placeholder': "Напиши нещо тук...",
        'new': "💬  Нов чат  🗨️",
        'load': "Предишни разговори:"
    },
    'es': {
        'page': "Terapeuta IA",
        'title': "Terapeuta IA de la Gen Z",
        'placeholder': "Escribe algo aquí...",
        'new': "💬  Nuevo chat  🗨️",
        'load': "Conversaciones anteriores:"
    },
    'fr': {
        'page': "IA Thérapeute",
        'title': "Thérapeute IA de la Gen Z",
        'placeholder': "Tapez quelque chose ici...",
        'new': "💬  Nouveau chat  🗨️",
        'load': "Conversations précédentes:"
    }
}

# Връщане на преведен текст по език и ключ
def get_translation(language, key):
    return translations.get(language, translations['en']).get(key, key)
