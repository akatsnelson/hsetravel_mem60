import re
from time import sleep

from config.config import if_answer_err, finish, answer_err, back_btn
from dao.db_connection import DBConnect
from dao.user_text_dao import UserTextDao
from service.keyboard_service import KeyboardService
from service.user_service import UserService
from custom_functions.custom_analyzers import *
from custom_functions.custom_answers import *



class TextService:

    @staticmethod
    def analyzer_and_sender(user_id, bot, answer='', photo=None, repeat=False):
        """
        метод анализирует текущий шаг и в случае успеха отправляет на следующий
        :param repeat:
        :param photo:
        :param user_id:
        :param bot:
        :param answer:
        """
        freeze = DBConnect.get_custom_user_field(user_id, 'users',
                                                 'user_freeze')
        if freeze == True:
            return

        step = UserService.get_user_step(user_id)
        if step == finish:
            return
        DaoModel = UserTextDao

        step_type = UserService().get_step_type_by_step(step, False)
        next_step = ''
        if repeat == True:
            TextService.send_next_step(user_id, bot, step)
            next_step = UserService.get_user_step(user_id)
        elif step_type == 'skip':
            next_step = UserService.get_next_step(user_id)
            UserService.set_user_step(user_id, next_step)
            TextService.send_next_step(user_id, bot, next_step)

        elif step_type == 'answer':
            if answer == '':
                TextService.send_next_step(user_id, bot, answer_err)
                next_step = step
                TextService.send_next_step(user_id, bot, step)
            else:
                table, filed = DaoModel().get_step_save_to(step).split('.')
                split = filed.split(':')
                if len(split) == 2:
                    filed, size = split
                    if len(answer) > int(size):
                        TextService.send_next_step(user_id, bot, answer_err)
                        TextService.send_next_step(user_id, bot, step)
                        return
                DBConnect.update_custom_user_filed(user_id, table, filed,
                                                   answer)

                next_step = UserService.get_next_step(user_id)
                UserService.set_user_step(user_id, next_step)
                TextService.send_next_step(user_id, bot, next_step)

        elif 'function' in step_type or 'fun' in step_type:
            function_name = step_type.split(':')[1]
            function_name, params = function_name.split('(')
            params = params.replace(')', '').split(', ')
            params.append(TextService)
            next_step = globals()[function_name](bot, user_id, answer, params)
            UserService.set_user_step(user_id, next_step)
            if DaoModel().get_step_save_to(step) != '':
                table, filed = DaoModel().get_step_save_to(step).split('.')
                split = filed.split(':')
                if len(split) == 2:
                    filed, size = split
                    if len(answer) > int(size):
                        TextService.send_next_step(user_id, bot, answer_err)
                        TextService.send_next_step(user_id, bot, step)
                        return
                DBConnect.update_custom_user_filed(user_id, table, filed,
                                                   answer)
            TextService.send_next_step(user_id, bot, next_step)

        elif 'sleep' in step_type:
            sleep_time = step_type.split(':')[1]
            DBConnect.update_custom_user_filed(user_id, 'users', 'user_freeze',
                                               True)
            sleep(sleep_time)
            DBConnect.update_custom_user_filed(user_id, 'users', 'user_freeze',
                                               False)
            next_step = UserService.get_next_step(user_id)
            UserService.set_user_step(user_id, next_step)
            TextService.send_next_step(user_id, bot, next_step)

        elif step_type == 'ifanswer':
            future_issue = TextService.parse_ifanswer(step, False)
            for f in future_issue:
                if answer.lower() in future_issue[f]:
                    if DaoModel().get_step_save_to(step) != '':
                        table, filed = DaoModel().get_step_save_to(
                            step).split(
                            '.')
                        split = filed.split(':')
                        if len(split) == 2:
                            filed, size = split
                            if len(answer) > int(size):
                                TextService.send_next_step(user_id, bot,
                                                           answer_err)
                                TextService.send_next_step(user_id, bot, step)
                                return
                        DBConnect.update_custom_user_filed(user_id, table,
                                                           filed,
                                                           answer)

                    next_step = f
                    UserService.set_user_step(user_id, next_step)
                    TextService.send_next_step(user_id, bot, next_step)

            if next_step is None:
                TextService.send_next_step(user_id, bot, if_answer_err)
                next_step = step
                TextService.send_next_step(user_id, bot, step)

        elif step_type == 'photo':
            if photo is None:
                TextService.send_next_step(user_id, bot, answer_err)
                next_step = step
                TextService.send_next_step(user_id, bot, step)
            else:
                table, filed = DaoModel().get_step_save_to(step).split('.')
                DBConnect.update_custom_user_photo_filed(user_id, table, filed,
                                                         photo)

                next_step = UserService.get_next_step(user_id)
                UserService.set_user_step(user_id, next_step)
                TextService.send_next_step(user_id, bot, next_step)
        is_admin = False
        if next_step == '':
            return
        next_step_type = UserService().get_step_type_by_step(next_step,
                                                             is_admin)
        if next_step_type == 'skip' or 'sleep' in next_step_type or 's_fun' in next_step_type:
            TextService.analyzer_and_sender(user_id, bot)

    @staticmethod
    def send_next_step(user_id, bot, step):
        """
        метод отправляет сообщения для след шага или ошибки
        :param user_id:
        :param bot:
        :param step:
        """
        DaoModel = UserTextDao
        msg = DaoModel().get_step_answer(step)
        if msg != '':
            find_fun = re.compile(r'\B@\w+')
            if find_fun.match(msg) is not None:
                fun_name = find_fun.findall(msg)[0].replace('@', '')
                globals()[fun_name](bot, user_id)
            else:
                msg = TextService.fill_text(user_id, msg)
                buttons = DaoModel().get_step_buttons(step)
                find_fun = re.compile(r'\B@\w+')
                if find_fun.match(buttons) is not None:
                    fun_name = find_fun.findall(buttons)[0].replace('@', '')
                    buttons = globals()[fun_name](user_id)
                else:
                    if buttons != '':
                        buttons = buttons.split('; ')
                    else:
                        buttons = []
                kb = KeyboardService.generate_inline_keyboard(buttons)
                bot.send_message(user_id, msg, reply_markup=kb)

    @staticmethod
    def parse_ifanswer(step, admin=False):
        """
         метод разбирает конструкцию ifanswer, для дальнейшей обработки
        :param step:
        :return:
        """

        next_steps_text = UserTextDao().get_next_step(step).lower().split(
            '; ')
        future_issue = {}
        for next_step_text in next_steps_text:
            next_steps, text_answers = next_step_text.split(':')
            answers = text_answers.split(', ')
            future_issue[next_steps] = answers
        return future_issue

    @staticmethod
    def fill_text(user_id, text):
        """
        метод обрабатывает шаблонные ответы и заполняет их данными из бд
        :param user_id:
        :param text:
        :return:
        """
        templates = re.findall(r'{([\s\S]+?)}', text)
        text = ''.join(re.split(r'{([\s\S]+?)}', text))
        for t in templates:
            fill = TextService.fill_field(user_id, t)
            text = text.replace(t, fill)
        return text

    @staticmethod
    def fill_field(user_id, query):
        """
        метод находит заполнение для одного поля
        :param user_id:
        :param query:
        :return:
        """
        table, filed = query.split('.')
        return DBConnect.get_custom_user_field(user_id, table, filed)
