from telebot import types


class KeyboardService:

    @staticmethod
    def generate_keyboard_inline_(keys):
        """
        метод генерирует клавиатуру в тг из массива
        :param keys:
        :return:
        """
        if len(keys) == 0:
            return None
        else:
            markup = types.InlineKeyboardMarkup()
            for key in keys:
                btn = types.InlineKeyboardButton(key, callback_data=key)
                markup.add(btn)
            return markup

    @staticmethod
    def generate_inline_keyboard(keys):
        """
        метод генерирует клавиатуру в тг из массива
        :param keys:
        :return:
        """
        if len(keys) == 0:
            return types.ReplyKeyboardRemove()
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for key in keys:
                btn = types.KeyboardButton(key)
                markup.add(btn)
            return markup
