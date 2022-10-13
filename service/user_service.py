from config.config import start_step
from dao.steps_history_dao import StepsHistoryDao
from dao.user_dao import UserDao
from dao.user_text_dao import UserTextDao


class UserService:
    @staticmethod
    def is_user_exists(id):
        if UserDao.get_user_by_id(id) is None:
            return False
        else:
            return True

    @staticmethod
    def get_user_by_id(id):
        return UserDao.get_user_by_id(id)

    @staticmethod
    def create_user(user_id):
        start_step_id = StepsHistoryDao.create_step(start_step, 'NULL')
        UserDao.create_user(user_id, start_step_id)

    @staticmethod
    def delete_user(user_id):
        UserService.delete_all_step_history(user_id)
        UserDao.delete_user(user_id)

    @staticmethod
    def get_user_step(user_id):
        step_id = UserDao.get_user_step_by_id(user_id)
        return StepsHistoryDao.get_step_by_id(step_id)

    @staticmethod
    def set_user_step(user_id, step):
        prev_step = UserDao.get_user_step_by_id(user_id)
        step_id = StepsHistoryDao.create_step(step, prev_step)
        UserDao.update_user_step_by_id(user_id, step_id)

    @staticmethod
    def set_user_step_id(user_id, step_id):
        UserDao.update_user_step_by_id(user_id, step_id)

    @staticmethod
    def get_next_step(user_id):
        step = UserService.get_user_step(user_id)
        return UserTextDao().get_next_step(step)

    @staticmethod
    def get_step_type_by_step(step, admin=False):
        return UserTextDao().get_step_type(step)

    @staticmethod
    def go_to_prev_step(user_id):
        curr_step_id = UserDao.get_user_step_by_id(user_id)
        prev_step_id = StepsHistoryDao.get_prev_step_id_by_id(curr_step_id)
        step = UserService.get_user_step(user_id)
        is_admin = False
        curr_step_type = UserService.get_step_type_by_step(step, is_admin)
        first_it = True
        while ((
                       curr_step_type == 'skip' or
                       'sleep' in curr_step_type or
                       's_fun' in curr_step_type)
               and prev_step_id is not None) or (
                first_it and prev_step_id is not None):
            first_it = False
            UserDao.update_user_step_by_id(user_id, prev_step_id)
            StepsHistoryDao.delete_step_by_id(curr_step_id)
            curr_step_id = prev_step_id
            prev_step_id = StepsHistoryDao.get_prev_step_id_by_id(curr_step_id)
            step = UserService.get_user_step(user_id)
            curr_step_type = UserService.get_step_type_by_step(step, is_admin)
        return StepsHistoryDao.get_step_by_id(curr_step_id)

    @staticmethod
    def no_prev_action_step(user_id):
        curr_step_id = UserDao.get_user_step_by_id(user_id)
        prev_step_id = StepsHistoryDao.get_prev_step_id_by_id(curr_step_id)
        step = UserService.get_user_step(user_id)
        is_admin =  False
        DaoModel = UserTextDao
        curr_step_type = UserService.get_step_type_by_step(step, is_admin)
        first_it = True
        while ((
                       curr_step_type == 'skip' or
                       'sleep' in curr_step_type or
                       's_fun' in curr_step_type)
               and prev_step_id is not None) or (
                first_it and prev_step_id is not None):
            first_it = False
            curr_step_id = prev_step_id
            prev_step_id = StepsHistoryDao.get_prev_step_id_by_id(curr_step_id)
            curr_step = StepsHistoryDao.get_step_by_id(curr_step_id)
            curr_step_type = DaoModel().get_step_type(curr_step)
        return True if prev_step_id is None else False

    @staticmethod
    def delete_all_step_history(user_id):
        curr_step_id = UserDao.get_user_step_by_id(user_id)
        curr_step = StepsHistoryDao.get_step_by_id(curr_step_id)
        prev_step_id = curr_step_id
        while prev_step_id is not None:
            curr_step_id = UserDao.get_user_step_by_id(user_id)
            curr_step = StepsHistoryDao.get_step_by_id(curr_step_id)
            prev_step_id = StepsHistoryDao.get_prev_step_id_by_id(curr_step_id)
            UserDao.update_user_step_by_id(user_id, prev_step_id)
            StepsHistoryDao.delete_step_by_id(curr_step_id)
        UserDao.update_user_step_by_id(user_id, None)
        StepsHistoryDao.delete_step_by_id(curr_step_id)
        return curr_step