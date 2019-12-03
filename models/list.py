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

    @staticmethod
    def getListsByBid(_list_obj, _bid):
        return getTuplesByEqualCond(_list_obj.table_name, [List.bid], [_bid])

    @staticmethod
    def insert(_list_obj, _bid, _name):
        values = "{}, '{}'".format(_bid, _name)
        keys = "{},{}".format(List.bid, List.name)
        sql_insert(_list_obj.table_name, values, keys)

    @staticmethod
    def deleteByLid(_list_obj, _cid):
        deleteByEqualCond(_list_obj.table_name, [List.cid], [_cid])