"""
    @Desc:
        SQL语言的基础包装
    @Func:
        getTupleByKey
        sql_select
        sql_insert
        sql
        getDataAsDict
"""

from django.db import connection


def getLastRecord(_table, _order_id):
    code = "select * from {} order by {} desc LIMIT 1".format(
        _table, _order_id)
    return sql(code)[0]


def getTuplesByEqualCond(_table: str, _key: list, _value: list) -> list:
    """
        get records by key or a=1 b=1... this format condition
    """
    cond = ""
    for i in range(len(_key)):
        cond += " {}='{}' ".format(_key[i], _value[i])
        if i < len(_key) - 1:
            cond += ' and '
    res = sql_select(_table, cond=cond)
    return res


def deleteByEqualCond(_table, _key, _value) -> list:
    cond = ""
    for i in range(len(_key)):
        cond += " {}='{}' ".format(_key[i], _value[i])
        if i < len(_key) - 1:
            cond += ' and '
    res = sql_delete(_table, cond=cond)


def sql_delete(_table, cond):
    """ delete from _table where cond """
    sql("delete from {} where {}".format(_table, cond))


def sql_select(tables, attr="*", cond="", addition="") -> list:
    """ select attr from tables where cond addition """
    if len(cond) == 0:
        return sql("select {} from {} {}".format(attr, tables, addition))
    else:
        return sql("select {} from {} where {} {}".format(attr, tables, cond, addition))


def sql_insert(table, values: str, key: str):
    """ insert into table (key) values (values) """
    return sql("insert into {} ({}) values ({})".format(table, key, values))


def sql_update(table, cond, **kwargs):
    """  
        @Desc:
            UPDATE table_name SET field1=new-value1, field2=new-value2 [WHERE Clause]
        @Param:
            table: table name
            kwargs: the key-value of field-value
    """
    code = "update {} set ".format(table)
    length = len(kwargs)
    i = 0
    for field, value in kwargs.items():
        code += " {}='{}' ".format(field, value)
        if i != length-1:
            code += ','
        i += 1
    code += "where {}".format(cond)
    sql(code)


def sql(code) -> list:
    """ 执行原始SQL代码 """
    print("code:", code)
    cursor = connection.cursor()
    print(cursor)
    cursor.execute(code)
    return getDataAsDict(cursor)


def getDataAsDict(cursor) -> list:
    """ 将表信息包装成列表字典  """
    rows = cursor.fetchall()
    if cursor.description == None:
        return {}
    cols = [desc[0] for desc in cursor.description]
    result = []
    for row in rows:
        tempDict = {}
        for index, value in enumerate(row):
            tempDict[cols[index]] = value
        result.append(tempDict)
    return result
