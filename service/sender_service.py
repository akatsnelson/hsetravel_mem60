from telebot import TeleBot


class SenderService:

    @staticmethod
    def send_to_users(bot: TeleBot, users_id, message):
        for u in users_id:
            bot.send_message(u, message)

    @staticmethod
    def send_to_user(bot: TeleBot, user_id, message):
        bot.send_message(user_id, message)
