import sqlite3

from config.config import db_path


class DBConnect(object):

    def __new__(cls):
        """
        метод добавляет классу свойства синглетона и инициализирует его
        """
        if not hasattr(cls, 'instance'):
            try:
                cls.conn = sqlite3.connect(db_path, check_same_thread=False)
            except Exception as e:
                raise e

            cls.instance = super(DBConnect, cls).__new__(cls)
        return cls.instance

    def getConnection(self):
        return self.conn

    def getCursor(self):
        return self.conn.cursor()

    def do_select_query(self, q):
        cur = self.getCursor()
        try:
            cur.execute(q)
            o = cur.fetchone()
            if o is not None:
                o = o[0]
            return o
        except sqlite3.Error as e:
            raise e
        finally:
            if cur:
                cur.close()

    def do_selects_query(self, q):
        cur = self.getCursor()
        try:
            cur.execute(q)
            o = cur.fetchall()
            return o
        except sqlite3.Error as e:
            raise e
        finally:
            if cur:
                cur.close()

    @staticmethod
    def get_custom_user_field(tg_id, table, field):
        """
        метод получает сложное поле из db
        :param tg_id:
        :param table:
        :param field:
        :return:
        """
        cur = DBConnect().getCursor()
        try:
            q = f'select {field} from {table} where tg_id = {tg_id}'
            cur.execute(q)
            step = cur.fetchone()[0]
            return step
        except sqlite3.Error as e:
            raise e
        finally:
            if cur:
                cur.close()

    @staticmethod
    def update_custom_user_filed(tg_id, table, filed, val):
        """
        метод обновляет сложное поле из db
        :param tg_id:
        :param table:
        :param filed:
        :param val:
        """
        conn = DBConnect().getConnection()
        cur = conn.cursor()
        try:
            if val is None:
                q = f'update {table} set {filed} = NULL where tg_id = {tg_id}'
            else:
                q = f'update {table} set {filed} = \'{val}\' where tg_id = {tg_id}'
            cur.execute(q)
            conn.commit()
        except sqlite3.Error as e:
            raise e
        finally:
            if cur:
                cur.close()

    @staticmethod
    def update_custom_user_photo_filed(tg_id, table, filed, photo):
        """
        метод обновляет фото произвольного поля из db
        :param tg_id:
        :param table:
        :param filed:
        :param photo:
        """
        conn = DBConnect().getConnection()
        cur = conn.cursor()
        try:
            q = f'update {table} set {filed} = ? where tg_id = {tg_id}'
            cur.execute(q, [photo])
            conn.commit()
        except sqlite3.Error as e:
            raise e
        finally:
            if cur:
                cur.close()
