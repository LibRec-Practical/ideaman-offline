"""
    用于与Mysql数据库相连,配置在util.config文件内,使用时,直接使用cur执行命令.
"""
import pymysql
from .config import *

conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_pwd, db=mysql_db,
                       charset='utf8')
cur = conn.cursor()


def ignore_insert(table_name, col_name, value_name):
    """
    判断是否有col_name字段中有value_name的值,如果有直接返回,如果没有插入到table_name中
    :param table_name: 表名
    :param col_name: 列名
    :param value_name: 值
    :return:
    """
    if get_id(table_name, col_name, value_name):
        return
    else:
        sql = "insert into `%s` (`%s`) values (\"%s\")" % (table_name, col_name, str(value_name))
        try:
            cur.execute(sql)
            conn.commit()
        except:
            conn.rollback()


def get_id(table_name, col_name, value_name):
    """
    判断是否有col_name字段中有value_name的值
    :param table_name: 表名
    :param col_name: 列名
    :param value_name: 值
    :return:
    """
    sql = "SELECT id from `%s` where %s = \"%s\" " % (table_name, col_name, str(value_name))
    cur.execute(sql)
    res = cur.fetchone()
    if res:
        return res[0]
    else:
        return None

def get_name(table_name, col_name, value_name,need_name):
    """
        判断是否有col_name字段中有value_name的值
        :param table_name: 表名
        :param col_name: 列名s
        :param value_name: 值
        :return:
        """
    sql = "SELECT %s from `%s` where %s = %s " % (need_name,table_name, col_name, value_name)
    cur.execute(sql)
    res = cur.fetchone()
    if res:
        return res[0]
    else:
        return None