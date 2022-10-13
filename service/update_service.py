import pandas as pd

from config.config import doc_id, user_sheet_id, user_file_path
from dao.user_text_dao import UserTextDao


class UpdateService:
    @staticmethod
    def update():
        """
        метод скачивает гугл таблицу работы бота и обновляет ее локально
        """
        sheet_url = UpdateService.build_sheet_url(doc_id, user_sheet_id)
        print(sheet_url)
        df = pd.read_csv(sheet_url)
        UpdateService.write_df_to_local(df, user_file_path)

        UserTextDao().update()

    @staticmethod
    def build_sheet_url(doc_id, sheet_id):
        """
        метод енерирует ссылку на гугл таблицу
        :param doc_id:
        :param sheet_id:
        :return:
        """
        return f'https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&gid={sheet_id}'

    @staticmethod
    def write_df_to_local(df, file_path):
        """
        метод сохраняет новую таблицу
        :param df:
        :param file_path:
        """
        df.to_csv(file_path)


UpdateService.update()
