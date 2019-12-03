"""
    @Name: 
        card.py
    @Desc:
        this file is used to do sql operations about cards
    @Class:
        P_Card: Personal..
        T_Card: Team...
"""

from .sql import *


class P_Card:
    """
        个人列表
    """
    table_name = "p_card"


class T_Card:
    """
        团队列表
    """
    table_name = "t_card"

class Card:
    """
        包含上面两个表
        _card_obj: 看板种类 P_List T_List
    """
    cid = "CID" # primary
    name = "name"
    desc = "description"
    lid = "LID" # foreign
    due_time = "due_time"

    @staticmethod
    def getCardsByLid(_card_obj, _lid):
        return getTuplesByEqualCond(_card_obj.table_name, [Card.lid], [_lid])

    @staticmethod
    def insert(_card_obj, _lid, _name, _desc=""):
        values = "{},'{}','{}'".format(_lid, _name, _desc)
        keys = "{},{}".format(Card.lid, Card.name, Card.desc)
        sql_insert(_card_obj.table_name, values, keys)

    @staticmethod
    def deleteByCid(_card_obj, _cid):
        deleteByEqualCond(_card_obj.table_name, [_card_obj.cid], [_cid])