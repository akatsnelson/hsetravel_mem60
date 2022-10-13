import pandas as pd

from config.config import user_file_path, constructor_error


class UserTextDao(object):
    def __new__(cls):
        """
        метод добавляет классу свойства синглетона и инициализирует его
        """
        if not hasattr(cls, 'instance'):
            cls.df = pd.read_csv(user_file_path, na_filter=False)
            cls.instance = super(UserTextDao, cls).__new__(cls)
        return cls.instance

    def update(cls):
        cls.df = pd.read_csv(user_file_path, na_filter=False)

    def get_step_type(self, step):
        return self.df[self.df['step'] == step]['type'].values[0]

    def get_step_answer(self, step):
        answer = self.df[self.df['step'] == step]['answer'].values

        return answer[
            0] if list(answer) != [] else constructor_error

    def get_next_step(self, step):
        return self.df[self.df['step'] == step]['next_step'].values[0]

    def get_step_buttons(self, step):
        return self.df[self.df['step'] == step]['buttons'].values[0]

    def get_step_save_to(self, step):
        return self.df[self.df['step'] == step]['save_to'].values[0]
