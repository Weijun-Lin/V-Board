"""
    @Name: 
        attachment.py
    @Desc:
        this file is used to do sql operations about attachments
    @Class:
        P_Attachment: Personal..
        T_Attachment: Team...
"""

from .sql import *

class P_Attachment:
    """
        个人卡片的附件
    """
    table_name = "p_attachment"


class T_Attachment:
    """
        团卡片的附件
    """
    table_name = "t_attachment"

class Attachment:
    """
        包含上面两个表
        _attachment_obj: 看板种类 P_Attachment T_Attachment
    """
    fid = "FID" # primary
    path = "path"
    cid = "CID" # foreign
    uid = "UID" # foreign

    @staticmethod
    def getAttachmentsByCid(_attachment_obj, _cid):
        return getTuplesByEqualCond(_attachment_obj.table_name, [Attachment.cid], [_cid])

    @staticmethod
    def insert(_attachment_obj, _path, _cid, _uid):
        values = "'{}','{}','{}'".format(_path, _cid, _uid)
        keys = "{},{},{}".format(Attachment.path, Attachment.cid, Attachment.uid)
        sql_insert(_attachment_obj.table_name, values, keys)

    @staticmethod
    def deleteByfid(_attachment_obj, _fid):
        deleteByEqualCond(_attachment_obj.table_name, [Attachment.fid], [_fid])

    @staticmethod
    def getAttachmentByFid(_attachment_obj, _fid):
        return getTuplesByEqualCond(_attachment_obj.table_name, [Attachment.fid], [_fid])

    @staticmethod
    def getLast(_attachment_obj):
        return getLastRecord(_attachment_obj.table_name, Attachment.fid)
