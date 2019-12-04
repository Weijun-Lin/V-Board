"""
    @Name: 
        team.py
    @Desc:
        this file is used to do sql operations about teams and teamates
    @Class:
        Team: table of team
        Team_Member: table of teammates
"""

from .sql import *

class Team:
    """
        记录团队信息的表
    """
    table_name = "team"
    tid = "TID" # primary
    name = "name"
    uid = "UID" # foreign

    @staticmethod
    def getRecordsByUid(_uid):
        return getTuplesByEqualCond(Team.table_name, [Team.uid], [_uid])

    @staticmethod
    def getRecordsByTid(_tid):
        return getTuplesByEqualCond(Team.table_name, [Team.tid], [_tid])
    
    @staticmethod
    def insert(_name, _uid):
        sql_insert(Team.table_name,"'{}', {}".format(_name, _uid), "{}, {}".format(Team.name, Team.uid))
    
    @staticmethod
    def isLegalName(_uid, _name)->bool:
        records = Team.getRecordsByUid(_uid)
        for item in records:
            if _name == item[Team.name]:
                return False
        return True

    @staticmethod
    def deleteByTid(_tid):
        deleteByEqualCond(Team.table_name, [Team.tid], [_tid])

    @staticmethod
    def createTeam(_uid, _name, _members:list):
        """
            @Desc:
                新建团队
            @Param:
                _uid: 创建者
                _name: 团队名字
                _members: 队员 uid 集合
        """
        # 创建团队
        Team.insert(_name, _uid)
        # 获取此时的tid 就是最后一个
        tid = getLastRecord(Team.table_name, Team.tid)[Team.tid]
        # 队员加入到Team_Member中
        for member in _members:
            Team_Member.insert(tid, member)

    @staticmethod
    def changeTeamName(_tid, _name):
        sql_update(Team.table_name, "{}={}".format(Team.tid, _tid), **{Team.name:_name})


        
class Team_Member:
    """
        团队成员表
    """
    table_name = "team_member"
    tid = "TID" # primary
    uid = "UID" # primary

    @staticmethod
    def getTeams(_uid):
        """ 获取用户所属团队tid """
        return sql_select(Team_Member.table_name, Team_Member.tid, "{}={}".format(Team_Member.uid, _uid))

    @staticmethod
    def getTeammates(_tid):
        """ 获取一个队伍的成员uid """
        return sql_select(Team_Member.table_name, Team_Member.uid, "{}={}".format(Team_Member.tid, _tid))

    @staticmethod
    def insert(_tid, _uid):
        sql_insert(Team_Member.table_name, "{},{}".format(_tid, _uid), "{},{}".format(Team_Member.tid, Team_Member.uid))

    @staticmethod
    def deleteMember(_tid, _uid):
        deleteByEqualCond(Team_Member.table_name, [Team_Member.tid, Team_Member.uid], [_tid, _uid])
