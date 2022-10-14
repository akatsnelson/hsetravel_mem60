from telebot import TeleBot

from service.user_service import UserService


def get_stat(bot: TeleBot, user_id):
    msg = f'Статистика:\n'
    users = UserService.get_users()
    for u in users:
        msg += f'Имя: {u[1]}: Тест1-{u[2]}б; Тест2-{u[3]}б; Тест3-{u[4]}б'
    bot.send_message(user_id, msg)
