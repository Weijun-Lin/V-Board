"""
    @Name: 
        list.py
    @Desc:
        this file is used to do sql operations about lists
    @Class:
        P_List: Personal..
        T_List: Team...
"""

from .sql import *


class P_List:
    """
        个人列表
    """
    table_name = "p_list"


class T_List:
    """
        团队列表
    """
    table_name = "t_list"


class List:
    """
        包含上面两个表
        _list_obj: 看板种类 P_List T_List
    """
    lid = "LID" # primary
    name = "name"
    bid = "BID" # foreign
    uid = "UID" # foreign

    @staticmethod
    def getListsByBid(_list_obj, _bid):
        return getTuplesByEqualCond(_list_obj.table_name, [List.bid], [_bid])

    @staticmethod
    def getListByLid(_list_obj, _lid):
        return getTuplesByEqualCond(_list_obj.table_name, [List.lid], [_lid])

    @staticmethod
    def insert(_list_obj, _bid, _name, _uid):
        values = "{}, '{}', {}".format(_bid, _name, _uid)
        keys = "{},{},{}".format(List.bid, List.name, List.uid)
        sql_insert(_list_obj.table_name, values, keys)

    @staticmethod
    def deleteByLid(_list_obj, _lid):
        deleteByEqualCond(_list_obj.table_name, [List.lid], [_lid])

    @staticmethod
    def setNameByLid(_list_obj, _lid, _name):
        sql_update(_list_obj.table_name, "{}={}".format(List.lid, _lid), **{List.name:_name})
    
    @staticmethod
    def getLast(_list_obj):
        return getLastRecord(_list_obj.table_name, List.lid)