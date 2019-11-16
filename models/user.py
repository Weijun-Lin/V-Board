from django.db import connection
from .sql import sql, sql_select, sql_insert


class Usr_Login:
    """
    用户登录表
    """
    table_name = "usr_login"
    email = "email"
    uid = "UID"
    password = "password"

    @staticmethod
    def show():
        return str(sql("desc {}".format(Usr_Login.table_name)))

    @staticmethod
    def insert(_email, _uid, _password):
        key = "{}, {}, {}".format(Usr_Login.email, Usr_Login.uid, Usr_Login.password)
        values = "'{}', {}, '{}'".format(_email, _uid, _password)
        sql_insert(Usr_Login.table_name, values, key)

    @staticmethod
    def getRecordByKey(_email:str)->dict:
        return sql_select(Usr_Login.table_name, "*", "{}='{}'".format(Usr_Login.email, _email))

    @staticmethod
    def isLegal(_email: str, _password: str) -> bool:
        """
        判断是否是合法账号密码
        """
        record = Usr_Login.getRecordByKey(_email)
        if len(record) == 0:
            return False
        else:
            return record[0][Usr_Login.password] == _password

    @staticmethod
    def register(_name, _email, _password)->bool:
        if len(Usr_Login.getRecordByKey(_email)) != 0:
            return False
        else:
            # insert into usr_info
            Usr_Info.insert(_name)
            uid = sql_select(Usr_Info.table_name)[-1][Usr_Info.uid]
            print(uid)
            Usr_Login.insert(_email, uid, _password)
            return True



class Usr_Info:
    """
    用户信息表
    """
    table_name = "usr_info"
    uid = "UID"
    avatar = "avatar"
    name = "name"
    description = "description"

    @staticmethod
    def show():
        return str(sql("desc {}".format((Usr_Info.table_name))))

    @staticmethod
    def insert(_name, _avatar='', _description=''):
        key = "{}, {}, {}".format(Usr_Info.name, Usr_Info.avatar, Usr_Info.description)
        values = "'{}', '{}', '{}'".format(_name, _avatar, _description)
        sql_insert(Usr_Info.table_name, values, key)
