import datetime
from ideaman_util.db import *
import sys, os

sys.path.append("../../")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../") for name in dirs])


class Paper:

    def __init__(self, user_id=None, title=None, authors=None, description=None, link=None, tags=None, doc_vector=None,
                 pwc_tasks=None):
        self.user_id = user_id
        self.link = link
        self.title = title
        self.description = description
        self.authors = authors

        self.tags = tags
        self.doc_vector = doc_vector
        self.pwc_tasks = pwc_tasks

    @staticmethod
    def count_by_time_interval(start_timestamp, end_timestamp=None):
        SQL = ""
        if end_timestamp == None:
            SQL = "SELECT count(1) FROM paper WHERE published >= {}".format(
                start_timestamp)
        if end_timestamp:
            SQL = "SELECT count(1) FROM paper WHERE published >= {} AND published <= {};".format(
                start_timestamp, end_timestamp)
        cur.execute(SQL)
        res = cur.fetchone()
        if res is None:
            return 0
        return res[0]

    @staticmethod
    def query_by_time_interval(start_timestamp, end_timestamp=None, key_words=None):
        """
        查询某段时间的所有论文，用于每周报告。
        :param start_timestamp: 开始的时间戳
        :param end_timestamp: 结束的时间戳，可选
        :return: .Paper 的生成器
        """
        SQL = ""
        if end_timestamp == None:
            SQL = "SELECT user_id,title,authors,description,link FROM paper WHERE add_time >= '{}'".format(
                start_timestamp)
        if end_timestamp:
            SQL = "SELECT user_id,title,authors,description,link FROM paper WHERE add_time >= {} AND add_time <= {};".format(
                start_timestamp, end_timestamp)
        if key_words:
            SQL = "SELECT user_id,title,authors,description,link FROM paper WHERE add_time >= '{}' AND title LIKE '%%{}%%'".format(
                start_timestamp, key_words)
        cur.execute(SQL)
        res = cur.fetchall()
        papers = []
        for i in res:
            author_names = []
            for author_id in i[2].split(","):
                if author_id is None or author_id == "" or author_id == 'None':
                    author_name = ' '
                else:
                    author_name = get_name("authors", "id", author_id, "author")
                    if author_name is None:
                        author_name = ' '
                author_names.append(author_name)
            author_names_str = ", ".join(author_names)
            p = Paper(i[0], i[1], author_names_str, i[3], i[4])
            papers.append(p)
        return papers

    @staticmethod
    def query_by_user_id(u_id):
        """
        查询某段时间的所有论文，用于每周报告。
        :param start_timestamp: 开始的时间戳
        :param end_timestamp: 结束的时间戳，可选
        :return: .Paper 的生成器
        """
        SQL = "SELECT user_id,title,authors,description,link FROM paper WHERE  user_id LIKE '%%{}%%'".format(
            u_id)

        cur.execute(SQL)
        res = cur.fetchall()
        papers = []
        for i in res:
            author_names = []
            for author_id in i[2].split(","):
                author_name = get_name("authors", "id", author_id, "author")
                if author_name is None:
                    author_name = ' '
                author_names.append(author_name)
            author_names_str = ", ".join(author_names)
            p = Paper(i[0], i[1], author_names_str, i[3], i[4])
            papers.append(p)
        return papers

    @staticmethod
    def update_SQL(col_name, col_value, user_id):
        SQL = "UPDATE paper SET %s = '%s' WHERE user_id = %s" % (col_name, col_value, user_id)
        try:
            cur.execute(SQL)
            conn.commit()
        except:
            conn.rollback()

    @staticmethod
    def get_classifier_dataset():
        sql = """SELECT
                    title,
                    description,
                    tags,
                    `authors`,
                    doc_vector,
                    pwc_tasks 
                FROM
                    paper 
                WHERE
                    pwc_tasks <> '' 
                    AND doc_vector IS NOT NULL
                """
        cur.execute(sql)
        res = cur.fetchall()
        papers = []
        for i in res:
            title = i[0]
            description = i[1]
            tags = i[2]
            authors = i[3]
            doc_vector = i[4]
            pwc_tasks = i[5]
            p = Paper(title=title, description=description, tags=tags, authors=authors, doc_vector=doc_vector,
                      pwc_tasks=pwc_tasks
                      )
            papers.append(p)
        return papers


if __name__ == '__main__':
    # authors_ids = "10958,10959,1351"
    # authors_ids = authors_ids.split(",")
    # print(authors_ids)
    # print(",".join(['aaa']))
    for i in Paper.query_by_user_id(0, "arXiv:1501.00960v4"):
        print(i.user_id)
    print()
