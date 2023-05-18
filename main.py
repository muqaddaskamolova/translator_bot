import sqlite3
import telebot.types
from telebot import TeleBot
from telebot.types import Message
from keyboards import generate_languages
from googletrans import Translator
import urllib.request
from bs4 import BeautifulSoup
bot = TeleBot('5705930722:AAFJTCEh5zXzBbyFzC_0XkaR21FBkWk657I')


@bot.message_handler(commands=['start', 'translates'])
def welcome(message: Message):
    user_id = message.from_user.id
    if message.text == '/start':
        bot.send_message(user_id, f"""Hello, Welcome to our Translator Bot!!!""")
        choose_first_language(message)
    elif message.text == '/translates':
        show_history(message)


# bot.send_sticker(user_id, 'CAACAgIAAxkBAAEIq0hkQnYGwWYYqeikoi_5CaytxioSmgACdQADQbVWDMJ9HiaPIEMuLwQ')
def show_history(message: Message):
    user_id = message.from_user.id

    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute(
        """
    SELECT from_lang, to_lang, original_lang, translated_lang
    FROM translates
    WHERE telegram_id = ?
    """, (user_id,))
    translations = cursor.fetchall()
    database.close()

    for translate in translations[:3]:
        bot.send_message(user_id,
                         f"""First language: {translate[0]} , 
                          Second language: {translate[1]},
                          Original Text: {translate[2]}  ,
                          Translated text: {translate[3]}                   
""")
    choose_first_language(message)


def choose_first_language(message: Message):
    user_id = message.from_user.id

    msg = bot.send_message(user_id, f"""Dear User, please choose which langauge to translate from : """,
                           reply_markup=generate_languages())
    bot.register_next_step_handler(msg, choose_second_language)


def choose_second_language(message: Message):
    if message.text in ['/start', '/translates']:
        welcome(message)
    else:
        user_id = message.from_user.id
        first_language = message.text
        msg = bot.send_message(user_id, f"""Dear User, please choose which langauge to translate to : """,
                               reply_markup=generate_languages())
        bot.register_next_step_handler(msg, ask_text, first_language)


def ask_text(message: Message, first_language):
    if message.text in ['/start', '/translates']:
        welcome(message)
    else:
        user_id = message.from_user.id
        second_language = message.text
        msg = bot.send_message(user_id, f"""Write down your text... """,
                               reply_markup=telebot.types.ReplyKeyboardRemove())

        bot.register_next_step_handler(msg, translate, first_language, second_language)


def translate(message: Message, first_language, second_language):
    if message.text in ['/start', '/translates']:
        welcome(message)
    else:
        user_id = message.from_user.id
        text = message.text
        source_text = BeautifulSoup(text, 'html.parser')
        paragraphs = ""
        for text in source_text.find_all("p"):
            paragraphs += text.text + "\n\n"
        paragraphs += "\n\nall complete"
        translator = Translator()
        translated_text = translator.translate(src=first_language.split(' ')[0],
                                               dest=second_language.split(' ')[0],
                                               text=text).text

        bot.send_message(user_id, translated_text)
        choose_first_language(message)

        database = sqlite3.connect('database.db')
        cursor = database.cursor()

        cursor.execute("""INSERT INTO translates(telegram_id, from_lang, to_lang, original_lang, translated_lang)
        VALUES(?,?,?,?,?)""", (user_id, first_language, second_language, text, translated_text))
        database.commit()
        database.close()


bot.polling(non_stop=True)
