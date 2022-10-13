import sqlite3

from dao.db_connection import DBConnect


class StepsHistoryDao:

    @staticmethod
    def create_step(curr_step, prev_step):
        conn = DBConnect().getConnection()
        cur = conn.cursor()
        try:
            q = f'insert into steps_history (curr_step, prev_step)' \
                f' values (\'{curr_step}\', {prev_step})'
            cur.execute(q)
            conn.commit()
            id = cur.lastrowid
        except sqlite3.Error as e:
            raise e
        finally:
            if cur:
                cur.close()
        return id

    @staticmethod
    def delete_step_by_id(step_id):
        conn = DBConnect().getConnection()
        cur = conn.cursor()
        try:
            q = f'delete from steps_history where id = {step_id}'
            cur.execute(q)
            conn.commit()
        except sqlite3.Error as e:
            raise e
        finally:
            if cur:
                cur.close()

    @staticmethod
    def get_step_by_id(step_id):
        q = f'select curr_step from steps_history where id = {step_id}'
        return DBConnect().do_select_query(q)

    @staticmethod
    def get_prev_step_id_by_id(step_id):
        q = f'select prev_step from steps_history where id = {step_id}'
        return DBConnect().do_select_query(q)
