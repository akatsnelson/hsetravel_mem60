import sqlite3

from dao.db_connection import DBConnect


class UserDao:
    @staticmethod
    def create_user(tg_id, step):
        conn = DBConnect().getConnection()
        cur = conn.cursor()
        try:
            q = f'insert into users (tg_id, step) values ({tg_id}, \'{step}\')'
            cur.execute(q)
            conn.commit()
        except sqlite3.Error as e:
            raise e
        finally:
            if cur:
                cur.close()

    @staticmethod
    def get_user_by_id(tg_id):
        q = f'select * from main.users where tg_id = {tg_id}'
        cur = DBConnect().getCursor()
        try:
            cur.execute(q)
            o = cur.fetchone()
            if o is not None:
                o = o
            return o
        except sqlite3.Error as e:
            raise e
        finally:
            if cur:
                cur.close()

    @staticmethod
    def get_users():
        q = f'select * from main.users'
        cur = DBConnect().getCursor()
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
    def get_user_step_by_id(tg_id):
        q = f'select step from users where tg_id = {tg_id}'
        return DBConnect().do_select_query(q)

    @staticmethod
    def update_user_step_by_id(tg_id, step):
        conn = DBConnect().getConnection()
        cur = conn.cursor()
        try:
            q = f'update users set step = \'{step}\' where tg_id = {tg_id}'
            cur.execute(q)
            conn.commit()
        except sqlite3.Error as e:
            raise e
        finally:
            if cur:
                cur.close()

    @staticmethod
    def delete_user(tg_id):
        conn = DBConnect().getConnection()
        cur = conn.cursor()
        try:
            q = f'delete from users where tg_id = {tg_id}'
            cur.execute(q)
            conn.commit()
        except sqlite3.Error as e:
            raise e
        finally:
            if cur:
                cur.close()
