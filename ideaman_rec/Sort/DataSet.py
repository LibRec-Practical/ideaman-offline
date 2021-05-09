"""
数据生成有两种格式:
1. UserID - ItemID - Rating （- TimeStamp）
2. TenSor
"""
import sys, os

sys.path.append("../")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../") for name in dirs])

import datetime
from util.db import cur
from transformers import BertTokenizer, BertConfig, BertForMaskedLM, BertForNextSentencePrediction
from transformers import BertModel


def add2Map(map: dict, key):
    if map.__contains__(key):
        return map.get(key)
    else:
        id = str(len(map))
        map[key] = id
        return id


def map2file(map: dict, filename: str):
    f = open(filename, 'w', encoding='utf-8')
    for key in map:
        f.write("{key}:{value}\n".format(key=key, value=map[key]))
    f.close()


def file2map(map: dict, filename: str):
    f = open(filename, 'r', encoding='utf-8')
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip().split(':')
        key, value = line[0], line[1]
        map[key] = value
    f.close()


tags2idx, authors2idx, pwc_tasks2idx = {}, {}, {}
file2map(authors2idx, 'dataset/authors2idx')
file2map(tags2idx, 'dataset/tags2idx')


def gen_UIR():
    # 写入正样本
    cur.execute("SELECT u_id,item_id,event_type,add_time FROM click_log where event_type = 1")
    res = cur.fetchall()
    file = open("dataset/UIR.csv", "w", encoding='utf-8')
    for item in res:
        uid = item[0]
        itemid = item[1]
        rating = item[2]
        timestamp = item[3].timestamp()
        file.write(",".join([str(i) for i in [uid, itemid, rating, timestamp]]) + "\n")
    file.close()

    # 写入负样本
    cur.execute("""SELECT
        u_id,
        GROUP_CONCAT(DISTINCT item_id ORDER BY item_id ASC SEPARATOR ' ') as neg
    FROM
        click_log 
    WHERE
        event_type = 0 
    GROUP BY
      u_id
    ORDER BY
        LENGTH(neg) DESC""")
    res = cur.fetchall()
    file = open("dataset/UIR_negative.csv", "w", encoding='utf-8')
    for item in res:
        uid = item[0]
        negs = item[1]
        file.write(" ".join([str(i) for i in [uid, negs]]) + "\n")
    file.close()


def gen_Tensor():
    """
    第一步：下载数据
    1. 从相邻主机的Mysql中下载数据，格式：userid , user_interest_tags , paper_id ,title , description ,tags , authors ,
    doc_vector , add_time ,label
    2. 原文文本中包含逗号，都用|代替
    3. 将作者转换为独热编码，并补齐
    4. 将tags转换为独热编码并补齐
    5. 将pwc_tasks转换为独热编码并补齐
    """
    model_name = 'bert-base-uncased'
    MODEL_PATH = './bert-base-uncased/'
    # 通过词典导入分词器
    tokenizer = BertTokenizer.from_pretrained(model_name)
    # 导入配置文件
    model_config = BertConfig.from_pretrained(model_name)
    # 通过配置和路径导入模型
    bert_model = BertModel.from_pretrained(MODEL_PATH, config=model_config)
    sql = """SELECT
        log.u_id AS userid,
        USER.interest_tags AS user_interest_tags,
        paper.id AS paperid,
        paper.title AS title,
        paper.description AS description,
        paper.tags AS tags,
        paper.`AUTHORS` AS `authors`,
        paper.doc_vector AS doc_vector,
        log.add_time AS add_time,
        log.event_type AS label 
    FROM
        ( SELECT u_id, item_id, event_type, add_time FROM click_log where u_id <= 10000) AS log
        INNER JOIN ( SELECT id, interest_tags FROM `user` ) AS `user`
        INNER JOIN (
        SELECT
            id,
            title,
            description,
            tags,
            AUTHORS,
            doc_vector 
        FROM
            paper 
        WHERE
            pwc_tasks <> '' 
            AND doc_vector IS NOT NULL 
            AND `authors` NOT LIKE '%one%' 
            AND tags NOT LIKE '%one%' 
        ) AS paper ON log.u_id = `user`.id 
        AND log.item_id = paper.id"""

    cur.execute(sql)
    res = cur.fetchall()

    tags2idx, authors2idx, pwc_tasks2idx = {}, {}, {}
    tags_pad, author_pad, doc2vec_pad = 16, 100, 160
    user_interest_tags_pad = 10
    f = open('dataset/tensor.csv', 'w', encoding='utf-8')

    for index, item in enumerate(res):
        userid = [str(item[0])]
        user_interest_tags = str(item[1]).split(",")
        user_interest_tags += ['0'] * (user_interest_tags_pad - len(user_interest_tags))

        paper_id = [str(item[2])]
        title = item[3]
        description = item[4]
        tags = item[5]
        authors = item[6]
        doc2vec = item[7]
        label = [str(item[9])]

        # title转换为vec
        encoded_input = tokenizer(title, return_tensors='pt')
        title = bert_model(**encoded_input)['pooler_output'].tolist()[0]
        title = [str(i) for i in title]

        # description转换为vec
        encoded_input = tokenizer(description, return_tensors='pt')
        description = bert_model(**encoded_input)['pooler_output'].tolist()[0]
        description = [str(i) for i in description]

        # tags转换为idx
        tags = [add2Map(tags2idx, i) for i in tags.split(",")]
        tags += ['0'] * (tags_pad - len(tags))

        # authors 转换为idx
        authors = [add2Map(authors2idx, i) for i in authors.split(",")]
        authors += ['0'] * (author_pad - len(authors))

        doc2vec = doc2vec.split(",")
        doc2vec += ['0'] * (doc2vec_pad - len(doc2vec))

        line = ",".join(userid + user_interest_tags + paper_id + title + description + tags + authors + doc2vec + label)
        f.write(line + '\n')
    f.close()

    map2file(authors2idx, 'dataset/authors2idx')
    map2file(tags2idx, 'dataset/tags2idx')
    map2file(pwc_tasks2idx, 'dataset/pwc_task2idx')


def getPredictData(user_id: int, paper_id: int):
    # 初始化
    tags_pad, author_pad, doc2vec_pad = 16, 100, 160
    user_interest_tags_pad = 10

    model_name = 'bert-base-uncased'
    MODEL_PATH = './bert-base-uncased/'
    # 通过词典导入分词器
    tokenizer = BertTokenizer.from_pretrained(model_name)
    # 导入配置文件
    model_config = BertConfig.from_pretrained(model_name)
    # 通过配置和路径导入模型
    bert_model = BertModel.from_pretrained(MODEL_PATH, config=model_config)

    # 获取用户数据
    cur.execute("SELECT id, interest_tags FROM `user` WHERE id = %d" % (user_id,))
    res = cur.fetchone()
    userid = [str(res[0])]
    user_interest_tags = str(res[1]).split(",")
    user_interest_tags += ['0'] * (user_interest_tags_pad - len(user_interest_tags))

    # 获取论文数据
    cur.execute("""
        SELECT
            id,
            title,
            description,
            tags,
            AUTHORS,
            doc_vector 
        FROM
            paper 
        WHERE
            pwc_tasks <> '' 
            AND doc_vector IS NOT NULL 
            AND `authors` NOT LIKE '%one%' 
        AND tags NOT LIKE '%one%' 
        AND id = {}
	""".format(paper_id))
    item = cur.fetchone()

    paper_id = [str(item[0])]
    title = item[1]
    description = item[2]
    tags = item[3]
    authors = item[4]
    doc2vec = item[5]

    # title转换为vec
    encoded_input = tokenizer(title, return_tensors='pt')
    title = bert_model(**encoded_input)['pooler_output'].tolist()[0]
    title = [str(i) for i in title]

    # description转换为vec
    encoded_input = tokenizer(description, return_tensors='pt')
    description = bert_model(**encoded_input)['pooler_output'].tolist()[0]
    description = [str(i) for i in description]

    # tags转换为idx
    tags = [add2Map(tags2idx, i) for i in tags.split(",")]
    tags += ['0'] * (tags_pad - len(tags))

    # authors 转换为idx
    authors = [add2Map(authors2idx, i) for i in authors.split(",")]
    authors += ['0'] * (author_pad - len(authors))

    doc2vec = doc2vec.split(",")
    doc2vec += ['0'] * (doc2vec_pad - len(doc2vec))

    line = userid + user_interest_tags + paper_id + title + description + tags + authors + doc2vec
    line = [eval(i) for i in line]

    return line


if __name__ == '__main__':
    # gen_UIR()
    # gen_Tensor()
    print(getPredictData(1, 14363))
