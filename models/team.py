"""
    @Name: 
        team.py
    @Desc:
        this file is used to do sql operations about teams and teamates
    @Class:
        Team: table of team
        Team_Member: table of teammates
"""

class Team:
    """
        记录团队信息的表
    """
    tid = "TID"
    name = "name"
    uid = "UID"


class Team_Member:
    """
        团队成员表
    """
    tid = "TID",
    uid = "UID"