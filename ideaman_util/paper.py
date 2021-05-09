from ideaman_util.db import *
from pymysql.converters import escape_string

class Paper:

    def __init__(self, user_id, title, authors, description, link, id):
        self.user_id = user_id
        self.link = link
        self.title = title
        self.description = description
        self.authors = authors
        self.id = id
    def generate_SQL(self):
        sql = "REPLACE INTO `paper`( `user_id`, `authors`, `type`,  `tags`,   `version`, `link`, `title`, `updated`, `published`, `pdf_link`, `description`,`add_time`) " \
              "VALUES (\"%s\" ,\"%s\" ,\"%s\" ,\"%s\" ,\"%s\" ,\"%s\" ,\"%s\" ,\"%s\" ,\"%s\" ,\"%s\" ,\"%s\",str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%S'));" % (
                  self.user_id[0], self.authors, "1", self.tags, self.version, self.link, self.title, str(self.updated),
                  str(self.published), self.pdf_link, self.description, self.add_time)
        return sql

    @staticmethod
    def update_SQL(col_name, col_value, arxiv_id):
        sql = "UPDATE paper SET `%s`='%s' WHERE user_id like '%%%s%%'" % (
            col_name, escape_string(col_value), arxiv_id)
        # 插入到数据库
        # 执行sql语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()

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
    def query_by_time_interval(start_timestamp, end_timestamp=None):
        """
        查询某段时间的所有论文，用于每周报告。
        :param start_timestamp: 开始的时间戳
        :param end_timestamp: 结束的时间戳，可选
        :return: .Paper 的生成器
        """
        SQL = ""
        if end_timestamp == None:
            SQL = "SELECT user_id,title,authors,description,link , id FROM paper WHERE published >= {}".format(
                start_timestamp)
        if end_timestamp:
            SQL = "SELECT user_id,title,authors,description,link , id FROM paper WHERE published >= {} AND published <= {};".format(
                start_timestamp, end_timestamp)
        cur.execute(SQL)
        res = cur.fetchall()
        papers = []
        for i in res:
            author_names = []
            for author_id in i[2].split(","):

                if author_id is None or author_id == 'None':
                    author_name = ' '
                else:
                    author_name = get_name("authors", "id", author_id, "author")
                if author_name is None:
                    author_name = ' '
                author_names.append(author_name)
            author_names_str = ", ".join(author_names)
            p = Paper(i[0], i[1], author_names_str, i[3], i[4], i[5])
            papers.append(p)
        return papers

    @staticmethod
    def query_by_index(start_index, end_index):

        sql = "SELECT user_id,title,authors,description,link, id FROM paper  where id >= {} and id < {}".format(
            start_index,
            end_index)

        cur.execute(sql)
        res = cur.fetchall()
        papers = []
        for i in res:
            author_names = []
            for author_id in i[2].split(","):
                if author_id is None:
                    author_name = ' '
                else:
                    author_name = get_name("authors", "id", author_id, "author")
                if author_name is None:
                    author_name = ' '
                author_names.append(author_name)
            author_names_str = ", ".join(author_names)
            p = Paper(i[0], i[1], author_names_str, i[3], i[4], i[5])
            papers.append(p)
        return papers


if __name__ == '__main__':
    # authors_ids = "10958,10959,1351"
    # authors_ids = authors_ids.split(",")
    # print(authors_ids)
    print(",".join(['aaa']))
