"""
    @Name: 
        board.py
    @Desc:
        this file is used to do sql operations about boards
    @Class:
        User_Login: table of users login information
        User_Info: table of users themselves information
"""

class Board:
    """
        看板表
    """
    table_name = "board"
    bid = "BID"
    name = "name"
    desc = "description"
    uid = "uid"
    p_or_t = "p_or_t"
    ispublic = "ispublic"