from django.db import connection
from .sql import *

def getTupleByKey(_table:str, _key:str, _value)->dict:
    res = sql_select(_table, "*", "{}='{}'".format(_key, _value))
    if len(res) == 0:
        return {}
    return res[0]


class Usr_Login:
    """
    用户登录表
    """
    table_name = "usr_login"
    email = "email" # primary key
    uid = "UID"
    password = "password"

    @staticmethod
    def show():
        return str(sql("desc {}".format(Usr_Login.table_name)))

    @staticmethod
    def getRecordByKey(_email):
        return getTupleByKey(Usr_Login.table_name, Usr_Login.email, _email)

    @staticmethod
    def insert(_email, _uid, _password):
        key = "{}, {}, {}".format(Usr_Login.email, Usr_Login.uid, Usr_Login.password)
        values = "'{}', {}, '{}'".format(_email, _uid, _password)
        sql_insert(Usr_Login.table_name, values, key)

    @staticmethod
    def isLegal(_email: str, _password: str) -> bool:
        """
        判断是否是合法账号密码
        """
        record = Usr_Login.getRecordByKey(_email)
        if record == {}:
            return False
        else:
            return record[Usr_Login.password] == _password

    @staticmethod
    def register(_name, _email, _password)->bool:
        """ 如果存在已注册账号返回 False 否则返回 True """
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
    uid = "UID" # primary key
    avatar = "avatar"
    name = "name"
    description = "description"

    @staticmethod
    def show():
        return str(sql("desc {}".format((Usr_Info.table_name))))

    @staticmethod
    def getRecordByKey(_uid):
        return getTupleByKey(Usr_Info.table_name, Usr_Info.uid, _uid)        

    @staticmethod
    def insert(_name, _avatar='', _description=''):
        key = "{}, {}, {}".format(Usr_Info.name, Usr_Info.avatar, Usr_Info.description)
        values = "'{}', '{}', '{}'".format(_name, _avatar, _description)
        sql_insert(Usr_Info.table_name, values, key)

    @staticmethod
    def update(_uid, _name, _avatar, _desc):
        key_value = {Usr_Info.name:_name, Usr_Info.avatar:_avatar, Usr_Info.description:_desc}
        sql_update(Usr_Info.table_name, "{}='{}'".format(Usr_Info.uid, _uid), **key_value)