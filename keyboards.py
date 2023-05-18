from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from utils import LANGUAGES


def generate_languages():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    languages = []
    for language in LANGUAGES.values():
        lang_button = KeyboardButton(text=language)
        languages.append(lang_button)

    markup.add(*languages)
    return markup

