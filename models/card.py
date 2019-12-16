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
        个人卡片
    """
    table_name = "p_card"


class T_Card:
    """
        团队卡片
    """
    table_name = "t_card"

class Card:
    """
        包含上面两个表
        _card_obj: 看板种类 P_Card T_Card
    """
    cid = "CID" # primary
    name = "name"
    desc = "description"
    lid = "LID" # foreign
    uid = "UID" # foreign
    due_time = "due_time"

    @staticmethod
    def getCardsByLid(_card_obj, _lid):
        return getTuplesByEqualCond(_card_obj.table_name, [Card.lid], [_lid])

    @staticmethod
    def insert(_card_obj, _lid, _name, _uid, _desc=""):
        values = "{},'{}',{},'{}'".format(_lid, _name, _uid, _desc)
        keys = "{},{},{},{}".format(Card.lid, Card.name, Card.uid, Card.desc)
        sql_insert(_card_obj.table_name, values, keys)

    @staticmethod
    def deleteByCid(_card_obj, _cid):
        deleteByEqualCond(_card_obj.table_name, [Card.cid], [_cid])

    @staticmethod
    def setName(_card_obj, _cid, _name):
        sql_update(_card_obj.table_name, "{}={}".format(Card.cid, _cid), **{Card.name:_name})

    @staticmethod
    def getCardByCid(_card_obj, _cid):
        return getTuplesByEqualCond(_card_obj.table_name, [Card.cid], [_cid])

    @staticmethod
    def setDescByCid(_card_obj, _cid, _desc):
        sql_update(_card_obj.table_name, "{}={}".format(Card.cid, _cid), **{Card.desc:_desc})
