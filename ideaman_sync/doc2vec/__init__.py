import sys, os

sys.path.append("../../")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../../") for name in dirs])

import time
from datetime import datetime
import logging
import re
import gensim
import smart_open
import jieba
from milvus import Milvus, DataType
from stop_words import safe_get_stop_words
from ideaman_util.paper import Paper
from ideaman_util.config import *

stop_words = safe_get_stop_words('en')
stopwords = {}.fromkeys(stop_words)
logging.basicConfig(filename='./doc2vec.txt',
                    filemode='w',
                    level=logging.DEBUG,
                    format='[%(asctime)s] - [%(levelname)s] - [PID:%(process)d] - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'  # 注意月份和天数不要搞乱了，这里的格式化符与time模块相同
                    )


def cut_stopwords(line):
    """
    去除停用词
    :param line: 输入 str
    :return: final: 去除停用词后的 str
    """
    segs = jieba.cut(clean_text(line), cut_all=False)
    final = ""
    for seg in segs:
        if seg not in stopwords:
            final += seg
    return final


def clean_text(text):
    """
    Clean text
    :param text: the string of text
    :return: text string after cleaning
    """
    # unit
    text.replace("$$", "")

    text = re.sub(r"(\d+)kgs ", lambda m: m.group(1) + ' kg ', text)  # e.g. 4kgs => 4 kg
    text = re.sub(r"(\d+)kg ", lambda m: m.group(1) + ' kg ', text)  # e.g. 4kg => 4 kg
    text = re.sub(r"(\d+)k ", lambda m: m.group(1) + '000 ', text)  # e.g. 4k => 4000
    text = re.sub(r"\$(\d+)", lambda m: m.group(1) + ' dollar ', text)
    text = re.sub(r"(\d+)\$", lambda m: m.group(1) + ' dollar ', text)

    # acronym
    text = re.sub(r"can\'t", "can not", text)
    text = re.sub(r"cannot", "can not ", text)
    text = re.sub(r"what\'s", "what is", text)
    text = re.sub(r"What\'s", "what is", text)
    text = re.sub(r"\'ve ", " have ", text)
    text = re.sub(r"n\'t", " not ", text)
    text = re.sub(r"i\'m", "i am ", text)
    text = re.sub(r"I\'m", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"c\+\+", "cplusplus", text)
    text = re.sub(r"c \+\+", "cplusplus", text)
    text = re.sub(r"c \+ \+", "cplusplus", text)
    text = re.sub(r"c#", "csharp", text)
    text = re.sub(r"f#", "fsharp", text)
    text = re.sub(r"g#", "gsharp", text)
    text = re.sub(r" e mail ", " email ", text)
    text = re.sub(r" e \- mail ", " email ", text)
    text = re.sub(r" e\-mail ", " email ", text)
    text = re.sub(r",000", '000', text)
    text = re.sub(r"\'s", " ", text)

    # spelling correction
    text = re.sub(r"ph\.d", "phd", text)
    text = re.sub(r"PhD", "phd", text)
    text = re.sub(r"pokemons", "pokemon", text)
    text = re.sub(r"pokémon", "pokemon", text)
    text = re.sub(r"pokemon go ", "pokemon-go ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" 9 11 ", " 911 ", text)
    text = re.sub(r" j k ", " jk ", text)
    text = re.sub(r" fb ", " facebook ", text)
    text = re.sub(r"facebooks", " facebook ", text)
    text = re.sub(r"facebooking", " facebook ", text)
    text = re.sub(r"insidefacebook", "inside facebook", text)
    text = re.sub(r"donald trump", "trump", text)
    text = re.sub(r"the big bang", "big-bang", text)
    text = re.sub(r"the european union", "eu", text)
    text = re.sub(r" usa ", " america ", text)
    text = re.sub(r" us ", " america ", text)
    text = re.sub(r" u s ", " america ", text)
    text = re.sub(r" U\.S\. ", " america ", text)
    text = re.sub(r" US ", " america ", text)
    text = re.sub(r" American ", " america ", text)
    text = re.sub(r" America ", " america ", text)
    text = re.sub(r" quaro ", " quora ", text)
    text = re.sub(r" mbp ", " macbook-pro ", text)
    text = re.sub(r" mac ", " macbook ", text)
    text = re.sub(r"macbook pro", "macbook-pro", text)
    text = re.sub(r"macbook-pros", "macbook-pro", text)
    text = re.sub(r" 1 ", " one ", text)
    text = re.sub(r" 2 ", " two ", text)
    text = re.sub(r" 3 ", " three ", text)
    text = re.sub(r" 4 ", " four ", text)
    text = re.sub(r" 5 ", " five ", text)
    text = re.sub(r" 6 ", " six ", text)
    text = re.sub(r" 7 ", " seven ", text)
    text = re.sub(r" 8 ", " eight ", text)
    text = re.sub(r" 9 ", " nine ", text)
    text = re.sub(r"googling", " google ", text)
    text = re.sub(r"googled", " google ", text)
    text = re.sub(r"googleable", " google ", text)
    text = re.sub(r"googles", " google ", text)
    text = re.sub(r" rs(\d+)", lambda m: ' rs ' + m.group(1), text)
    text = re.sub(r"(\d+)rs", lambda m: ' rs ' + m.group(1), text)
    text = re.sub(r"the european union", " eu ", text)
    text = re.sub(r"dollars", " dollar ", text)

    # punctuation
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"-", " - ", text)
    text = re.sub(r"/", " / ", text)
    text = re.sub(r"\\", " \ ", text)
    text = re.sub(r"=", " = ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r"", " . ", text)
    text = re.sub(r",", " , ", text)
    text = re.sub(r"\?", " ? ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\"", " \" ", text)
    text = re.sub(r"&", " & ", text)
    text = re.sub(r"\|", " | ", text)
    text = re.sub(r";", " ; ", text)
    text = re.sub(r"\(", " ( ", text)
    text = re.sub(r"\)", " ) ", text)

    # symbol replacement
    text = re.sub(r"&", " and ", text)
    text = re.sub(r"\|", " or ", text)
    text = re.sub(r"=", " equal ", text)
    text = re.sub(r"\+", " plus ", text)
    text = re.sub(r"₹", " rs ", text)  # 测试！
    text = re.sub(r"\$", " ", text)
    text = re.sub(r"  ", " ", text)
    text = re.sub(r"   ", " ", text)
    text = re.sub(r"    ", " ", text)
    # remove extra space
    text = ' '.join(text.split())

    return text


def read_file(fname, tokens_only=False):
    with smart_open.open(fname, encoding="utf-8") as f:
        for i, line in enumerate(f):
            print(line)
            print(cut_stopwords(line))
            return 0
            tokens = gensim.utils.simple_preprocess(cut_stopwords(line))
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


def read_mysql(start_date_str, end_date_str, tokens_only=False):
    ONE_DAY = 86400000
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').timestamp() * 1000
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').timestamp() * 1000
    res = Paper.query_by_time_interval(start_date, end_date)
    for index, item in enumerate(res):
        line = item.title + " . " + item.description
        tokens = gensim.utils.simple_preprocess(cut_stopwords(line))
        if tokens_only:
            yield tokens
        else:
            # For training data, add tags
            yield gensim.models.doc2vec.TaggedDocument(tokens, [index])


def train(start_date_str, end_date_str):
    logging.info("读取文件中。。。")
    train_corpus = list(read_mysql(start_date_str, end_date_str))
    print(len(train_corpus))
    logging.info("生成模型")
    model = gensim.models.doc2vec.Doc2Vec(vector_size=128, min_count=32, epochs=512)
    model.build_vocab(train_corpus)
    logging.info("训练模型开始")
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    logging.info("保存模型")
    model.save("./doc2vec.model")


def incremental_train(start_date_str, end_date_str):
    logging.info("读取文件中。。。")
    train_corpus = list(read_mysql(start_date_str, end_date_str))
    print(len(train_corpus))
    logging.info("加载模型")
    model = gensim.models.doc2vec.Doc2Vec.load("./doc2vec.model")
    total_examples = model.corpus_count + len(train_corpus)
    logging.info("训练模型开始")
    model.train(train_corpus, total_examples=total_examples, epochs=512)
    logging.info("保存模型")
    model.save("./doc2vec.model")


def get_vector(model, line):
    """
    获得文章的向量
    :param final: list
    :return: final: list
    """

    vec = model.infer_vector(line)
    return vec


def predict(start_date_str, end_date_str):
    print("加载模型")
    model = gensim.models.doc2vec.Doc2Vec.load("./doc2vec.model")
    print("建立milvus链接")
    client = Milvus(host=milvus_ip, port='19530')
    print("读取数据ing")
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').timestamp() * 1000
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').timestamp() * 1000
    res = Paper.query_by_time_interval(start_date, end_date)

    num = 0
    start = time.time()
    id_list = []
    user_id_list = []
    vecs = []

    for i in res:
        paper_id = i.id
        paper_user_id = i.user_id
        paper_str = i.title + " . " + i.description
        vec = get_vector(model, [paper_str])
        # 将词向量写入到Milvus
        id_list.append(paper_id)
        user_id_list.append(paper_user_id)
        vecs.append(list(vec))
        # 将词向量写入数据库
        paper_vec = str(vec).replace('\n', '').replace('[', '').replace(']', '').replace("  ", " ").replace(" ",
                                                                                                            ",")[1:]
        paper_vec = paper_vec.replace(",,", ",0,")
        Paper.update_SQL('doc_vector', paper_vec, paper_user_id)

        num += 1
        if num % 200 == 0:
            print("完成了", num, '篇', '--用时:', time.time() - start)
            start = time.time()
            # hybrid_entities = [
            #     {"name": "id", "values": id_list, "type": DataType.INT32},
            #     {"name": "Vec", "values": vecs, "type": DataType.FLOAT_VECTOR}
            # ]
            client.insert('ideaman', records=vecs, ids=id_list)
            client.flush(collection_name_array=["ideaman"])
            user_id_list.clear()
            id_list.clear()
            vecs.clear()


if __name__ == '__main__':
    predict(start_date_str, end_date_str)
