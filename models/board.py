"""
    @Name: 
        board.py
    @Desc:
        this file is used to do sql operations about boards
    @Class:
        Person_Board
        Team_Board
"""

from .sql import *


class Person_Board:
    """
        个人看板表
    """
    table_name = "personal_board"
    bid = "BID" # primary
    name = "name"
    desc = "description"
    is_public = "is_public"
    owner_id = "UID" # foreign
    is_star = "is_star"


class Team_Board:
    """
        团队看板表
    """
    table_name = "team_board"
    bid = "BID" # primary
    name = "name"
    desc = "description"
    is_public = "is_public"
    is_star = "is_star"
    owner_id = "TID" # foreign


# 是不是工厂模式 ?
class Board:
    """
        包含上面两个表
        _board_obj: 看板种类 Personal_Board Team_Board
    """

    @staticmethod
    def getBoardsByOwner(_board_obj, _owner_id):
        return getTuplesByEqualCond(_board_obj.table_name, [_board_obj.owner_id], [_owner_id])

    @staticmethod
    def getBoardByBid(_board_obj, _bid):
        return getTuplesByEqualCond(_board_obj.table_name, [_board_obj.bid], [_bid])

    @staticmethod
    def insert(_board_obj, _name, _desc, _owner_id, _is_public = 0):
        values = "'{}','{}',{},{}".format(_name, _desc, _owner_id, _is_public)
        keys = "{},{},{},{}".format(_board_obj.name, _board_obj.desc, _board_obj.owner_id, _board_obj.is_public)
        sql_insert(_board_obj.table_name, values, keys)

    @staticmethod
    def deleteByBid(_board_obj, _bid):
        deleteByEqualCond(_board_obj.table_name, [_board_obj.bid], [_bid])
    
    @staticmethod
    def getLastByBid(_board_obj):
        return getLastRecord(_board_obj.table_name, _board_obj.bid)

    @staticmethod
    def setInfo(_board_obj, _bid, _name, _desc):
        newValues = {_board_obj.name:_name, _board_obj.desc:_desc}
        sql_update(_board_obj.table_name, "{}='{}'".format(_board_obj.bid, _bid),**newValues)

