import datetime

from telebot import TeleBot

from dao.db_connection import DBConnect
from service.sender_service import SenderService
from service.user_service import UserService


def c_answer(bot: TeleBot, user_id, answer, params):
    score = int(DBConnect.get_custom_user_field(user_id, 'users', params[0]))
    if (score == -1 and params[4] == 'F') or (score != -1 and params[4] != 'F'):
        if score == -1 and params[4] == 'F':
            score = 0
            DBConnect.update_custom_user_filed(user_id, 'users', params[0], score)
        if answer.lower() == params[3].lower():
            score = score + 1
            DBConnect.update_custom_user_filed(user_id, 'users', params[0], score)
            bot.send_message(user_id, f"Верно!\nУ Вас {score} баллов")
        else:
            bot.send_message(user_id, f"Ошибка!\nУ Вас {score} баллов\nПравильный ответ: {params[3]}")
        return params[1]
    else:
        bot.send_message(user_id, f"Вы уже отвечали на эти вопросы.\nУ Вас {score} баллов")
        return params[2]
