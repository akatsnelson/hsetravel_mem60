import telebot

from config.config import bot_id, answer_err
from custom_functions.custom_answers import get_stat
from service.text_service import TextService
from service.update_service import UpdateService
from service.user_service import UserService

UpdateService.update()
bot = telebot.TeleBot(bot_id)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if not UserService.is_user_exists(user_id):
        UserService.create_user(user_id)
    TextService.analyzer_and_sender(user_id, bot)


@bot.message_handler(commands=['top'])
def stat(message):
    user_id = message.from_user.id
    if not UserService.is_user_exists(user_id):
        UserService.create_user(user_id)
    get_stat(bot, user_id)


@bot.message_handler(commands=['restart'])
def send_message_again(message):
    user_id = message.from_user.id
    if not UserService.is_user_exists(user_id):
        UserService.create_user(user_id)
    TextService.analyzer_and_sender(user_id, bot, repeat=True)


# @bot.message_handler(commands=['update'])
# def update_req(message):
#     user_id = message.from_user.id
#     if not UserService.is_user_exists(user_id):
#         UserService.create_user(user_id)
#


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_id = message.from_user.id
    if not UserService.is_user_exists(user_id):
        UserService.create_user(user_id)
    TextService.analyzer_and_sender(user_id, bot, message.text)


@bot.message_handler(content_types=['photo'])
def photo(message):
    user_id = message.from_user.id
    if not UserService.is_user_exists(user_id):
        UserService.create_user(user_id)
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    photo = bot.download_file(file_info.file_path)
    TextService.analyzer_and_sender(user_id, bot, photo=photo)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    if not UserService.is_user_exists(user_id):
        UserService.create_user(user_id)
    mes_id = call.message.message_id
    bot.edit_message_reply_markup(user_id, message_id=mes_id, reply_markup=None)
    TextService.analyzer_and_sender(user_id, bot, call.data)


bot.polling(none_stop=True, interval=0)
