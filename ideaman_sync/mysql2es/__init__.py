import sys, os

sys.path.append("../../")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../") for name in dirs])

from datetime import datetime
from elasticsearch import Elasticsearch
from ideaman_util.db import *
from ideaman_util.paper import Paper
from ideaman_util.config import *

# 链接es服务
host = es_ip + ':9200'
es = Elasticsearch([host])

# 索引名称
index_name = 'papers'

# 指定mappings和settings
request_body = {
    "mappings": {
        "properties": {
            "authors": {
                "type": "text"
            },
            "title": {
                "type": "text"
            },
            "description": {
                "type": "text",
                "analyzer": "standard"
            }
        }
    }
}


def create(index, body=None):
    """
    创建索引
    :param index: 索引名称
    :return: {'acknowledged': True, 'shards_acknowledged': True, 'index': 'student1'}
    """
    if es.indices.exists(index=index):
        es.indices.delete(index=index)  # 删除索引
    res = es.indices.create(index=index, body=body)
    return res


def delete(index):
    """
    删除索引
    :param index: 索引名称
    :return: True 或 False
    """
    if not es.indices.exists(index):
        return False
    else:
        res = es.indices.delete(index=index)
        return res['acknowledged']


def add(index, body, id=None):
    """
    (单条数据添加或更新)添加或更新文档记录，更新文档时传对应的id即可
    使用方法：
    `
    body = {"name": "long", "age": 11,"height": 111}
    add(index=index_name,body=body)
    或
    body = {"name": "long", "age": 11,"height": 111}
    add(index=index_name,body=body,id=1)
    `
    :param index: 索引名称
    :param body:文档内容
    :param id: 是否指定id,如不指定就会使用生成的字符串
    :return:{'_index': 'student1', '_type': '_doc', '_id': 'nuwKDXIBujABphC4rbcq', '_version': 1, 'result': 'created', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}
    """
    res = es.index(index=index, body=body, id=id)
    return res['_id']  # 返回 id


def search(index=None):
    """
    查询记录：如果没有索引名称的话默认就会查询全部的索引信息
    :param index:查询的索引名称
    :return:
    """
    if not index:
        return es.search()
    else:
        return es.search(index=index)


def get_maxid():
    """
    获得最大的论文id
    :return: maxid:
    """
    maxid = 0
    sql = "Select max(id) as maxid from paper"
    cur.execute(sql)
    maxid = cur.fetchone()[0]
    return maxid


def run(start_date_str, end_date_str):
    ONE_DAY = 86400000
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').timestamp() * 1000
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').timestamp() * 1000
    tmp_date = start_date
    while tmp_date <= end_date:
        res = Paper.query_by_time_interval(tmp_date, tmp_date + ONE_DAY)
        for i in res:
            body = {"authors": i.authors, "title": i.title, "description": i.description}
            add(index_name, body, id=i.user_id)
        tmp_date += ONE_DAY
        print("mysql2ex同步，完成日期：", datetime.fromtimestamp(tmp_date))


if __name__ == '__main__':
    print(run("2021-01-01", "2021-01-05"))
