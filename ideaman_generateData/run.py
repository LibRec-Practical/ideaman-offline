import sys
import random
import os
sys.path.append("../../")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../../") for name in dirs])


from ideaman_util.db import conn, cur

interest_tags = ["1", "2", "3", "4", "5", "6", "8", "9", "10", "11", "12", "13", "16", "18", "20", "23", "24", "25",
                 "29", "34", "37",
                 "38", "39", "44", "45", "54", "56", "60", "61", "62", "63", "64", "65", "75", "78", "83", "92",
                 "126", "132", "157"]  # 常用的paper分类

id2tags = {}


def click(user_id, paper_id, flag=1):
    """
    将点击信息写入到mysql中
    :param user_id: 用户id
    :param paper_id:点击的论文id
    :return: null
    """
    SQL = 'INSERT INTO click_log(u_id,item_id,event_type) VALUES("{}","{}","{}")'.format(user_id, paper_id, flag)
    try:
        cur.execute(SQL)
        conn.commit()
    except:
        conn.rollback()


def get_user(u_id):
    """
    根据u_id,生成用户,如果该用户的所有感兴趣的tags交集中很少或者没有论文,重新生成.
    :param u_id: 用户id
    :return: name:用户名
    :return: tags:用户感兴趣的tags,格式为list
    :return: tag:用户感兴趣的tags,格式为字符串,如"1,2,3"
    :return SQL_2:用于获得该用户感兴趣tags的论文
    """
    # 创建用户
    name = "tmp_%05d" % u_id
    tags = random.sample(interest_tags, random.randint(1, 3))
    tag = ",".join(tags)
    id = u_id + 7015
    id2tags[id] = tag

    # 2，随机为每一位用户的第一个个标签点击随机（2，5）篇的论文。
    conditions = []
    for t_id in tags:
        conditions.append('FIND_IN_SET("{}",tags)'.format(t_id))
    condition = " AND ".join(conditions)

    SQL_2 = 'SELECT id FROM paper WHERE ' + condition + ' ORDER BY RAND() LIMIT {}'.format(random.randint(2, 8))
    cur.execute(SQL_2)
    if len(cur.fetchall()) <= 4:
        return get_user(u_id)
    else:
        return name, tags, tag, id, SQL_2


def main(user_number=8000):
    """
    用于生成用户点击论文数据，
        1.生产指定数量的用户,指定每一位用户的感兴趣的标签[1,3]。将deleted位置设置为1
        2.随机为每一位用户的每个标签点击随机（2，8）篇的论文。
        3.随机选择用户，85%的概率对相应感兴趣的便签进行点击，15%的概率随机点击其他的论文，执行 8w,平均每个用户执行10次
    """

    # 1 生产指定数量的用户,指定每一位用户的感兴趣的标签，将deleted位置设置为1
    for u_id in range(1, user_number + 1):
        name, tags, tag, id, SQL_2 = get_user(u_id)
        cur.execute(SQL_2)
        paper_list = list(cur.fetchall())

        SQL_1 = 'INSERT INTO `user`(username,deleted,interest_tags) VALUES("{}", 1,"{}")'.format(name, tag)
        cur.execute(SQL_1)
        conn.commit()
        for paper_id in paper_list:
            click(id, paper_id[0])
        if u_id % 100 == 0:
            print("已经完成用户数量:", u_id)

    SQL_5 = "SELECT id,interest_tags FROM `user` WHERE id >= 10;"
    cur.execute(SQL_5)
    for u_item in cur.fetchall():
        id2tags[u_item[0]] = u_item[1].split(",")
    # 3.随机选择用户，
    # 随机选择用户
    for num in range(user_number * 10):
        id = random.sample(id2tags.keys(), 1)[0]
        rand_num = random.random()
        if rand_num < 0.55:
            # 55%生成正样本
            t_id = random.sample(id2tags.get(id), 1)[0]
            SQL_3 = 'SELECT id FROM paper WHERE FIND_IN_SET("{}",tags) ORDER BY RAND() LIMIT {}'.format(t_id, 1)
            cur.execute(SQL_3)
            paper_item = cur.fetchall()[0]
            paper_id = paper_item[0]
            click(id, paper_id)
        elif 0.55 <= rand_num <= 0.9:
            # 45%生成负样本
            t_id = random.sample(id2tags.get(id), 1)[0]
            SQL_3 = 'SELECT id FROM paper WHERE NOT FIND_IN_SET("{}",tags) ORDER BY RAND() LIMIT {}'.format(t_id, 1)
            cur.execute(SQL_3)
            paper_item = cur.fetchall()[0]
            paper_id = paper_item[0]
            click(id, paper_id, 0)
        else:
            # 5 % 的概率随机点击其他的论文
            SQL_4 = 'SELECT id FROM paper ORDER BY RAND() LIMIT 1'
            cur.execute(SQL_4)
            paper_item = cur.fetchall()[0]
            paper_id = paper_item[0]
            click(id, paper_id)
        if num % 1000 == 0:
            print("已经完成点击数量：%d", num)


if __name__ == '__main__':
    main(user_number = 35000)
