import datetime

from telebot import TeleBot

from dao.db_connection import DBConnect
from service.sender_service import SenderService
from service.user_service import UserService


def c_answer(bot: TeleBot, user_id, answer, params):
    score = int(DBConnect.get_custom_user_field(user_id, 'users', 'score'))
    if answer.lower() == params[1].lower():
        score = score + 1
        DBConnect.update_custom_user_filed(user_id, 'users', 'score', score)
        bot.send_message(user_id, f"Верно!\nУ тебя {score} баллов")
    else:
        bot.send_message(user_id, f"Ошибка!\nУ тебя {score} баллов")
    return params[0]
