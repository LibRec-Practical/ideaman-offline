"""
    用于与Mysql数据库相连,配置在util.config文件内,使用时,直接使用cur执行命令.
"""
import happybase
import pymysql
from hbase import Hbase
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from util.config import *

conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_pwd, db=mysql_db,
                       charset='utf8')
cur = conn.cursor()


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


def get_name(table_name, col_name, value_name, need_name):
    """
        判断是否有col_name字段中有value_name的值
        :param table_name: 表名
        :param col_name: 列名s
        :param value_name: 值
        :return:
        """
    sql = "SELECT %s from `%s` where %s = %s " % (need_name, table_name, col_name, value_name)
    cur.execute(sql)
    res = cur.fetchone()
    if res:
        return res[0]
    else:
        return None


# hbase_conn = happybase.Connection(host=mysql_host, port=9090, timeout=120000)
# hbase_conn.open()
# hbase_tableName = 'user_rec'


# def Get_By_rowkey(rowkey, family_name, col_name=None):
#     # if col_name:
#     #     family_name = family_name + ":" + col_name
#     # print(hbase_tableName)
#     # print(rowkey)
#     # print(family_name)
#     # result = client.get(tableName=hbase_tableName, row=rowkey, column=family_name)
#     # print(result)
#     table = hbase_conn.table(hbase_tableName)
#     rows = table.scan()



