from django.db import connection

# 使用原生SQL

def sql_select(tables, attr="*", cond="", addition="")->dict:
    """ select attr from tables where cond addition """
    if len(cond) == 0:
        return sql("select {} from {} {}".format(attr, tables, addition))
    else:
        return sql("select {} from {} where {} {}".format(attr, tables, cond, addition))


def sql_insert(table, values, key):
    """ insert into table (key) values (values) """
    return sql("insert into {} ({}) values ({})".format(table, key, values))


def sql(code)->dict:
    print("code:", code)
    cursor = connection.cursor()
    print(cursor)
    cursor.execute(code)
    return getDataAsDict(cursor)


def getDataAsDict(cursor)->dict:

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
