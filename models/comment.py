"""
    @Name: 
        Comment.py
    @Desc:
        this file is used to do sql operations about Comments
    @Class:
        P_Comment: Personal..
        T_Comment: Team...
"""

from .sql import *

class P_Comment:
    """
        个人评论
    """
    table_name = "p_comment"


class T_Comment:
    """
        团队评论
    """
    table_name = "t_comment"

class Comment:
    """
        包含上面两个表
        _comment_obj: 看板种类 P_Comment T_Comment
    """
    cm_id = "cm_id" # primary
    val = "val"
    cid = "CID" # foreign
    uid = "UID" # foreign

    @staticmethod
    def getCommentsByCid(_comment_obj, _cid):
        return getTuplesByEqualCond(_comment_obj.table_name, [Comment.cid], [_cid])

    @staticmethod
    def insert(_comment_obj, _val, _cid, _uid):
        values = "'{}','{}','{}'".format(_val, _cid, _uid)
        keys = "{},{},{}".format(Comment.val, Comment.cid, Comment.uid)
        sql_insert(_comment_obj.table_name, values, keys)

    @staticmethod
    def deleteBycm_id(_comment_obj, _cm_id):
        deleteByEqualCond(_comment_obj.table_name, [Comment.cm_id], [_cm_id])

    @staticmethod
    def getCommentBycm_id(_comment_obj, _cm_id):
        return getTuplesByEqualCond(_comment_obj.table_name, [Comment.cm_id], [_cm_id])

    @staticmethod
    def getLast(_comment_obj):
        return getLastRecord(_comment_obj.table_name, Comment.cm_id)
