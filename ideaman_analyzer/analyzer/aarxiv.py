import sys, os

sys.path.append("../../")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../") for name in dirs])
from gensim import corpora, models, similarities
from gensim.parsing.preprocessing import stem
import re
from math import log
import numpy as np
from ideaman_analyzer.textteaser import TextTeaser
from ideaman_analyzer.model.paper import *
from ideaman_mail.MailSender import *
from datetime import datetime
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARNING)


def labelling(tweet: str, topics) -> bool:
    """
    打标签,如果文本中包含上述,则打上标签
    """
    tweet = " ".join([t for t in tweet_preprocess(tweet.lower()) if not deprecate_words(t)])
    for topic in topics:
        if topic in tweet:
            return True
    return False


def deprecate_words(word: str) -> bool:
    """
        文本预处理,去除stopword 并进行分词
    """
    if word.endswith('…'):
        return True
    stop_list = 'a an the of at on upon in to from out as so such or and those this these that for is was am are been ' \
                'were what when where who will with the www by ? ! : . , … -'.split()
    stop_start_with = ['goo.gl', 't.co', 'http://', 'https://', 'g.co', 'msft.social', 'bit.ly', 't.cn', "@",
                       '(http://', '(https://']
    if word in stop_list:
        return True
    for stop_word in stop_start_with:
        if word.startswith(stop_word):
            return True
    return False


def tweet_preprocess(tweet_text: str):
    """
    文本预处理,去除特殊符号
    """
    tweet_text = tweet_text.lower()
    tweet_text = re.sub(
        r"(?:https?://)?(?:(?:0rz\.tw)|(?:1link\.in)|(?:1url\.com)|(?:2\.gp)|(?:2big\.at)|(?:2tu\.us)|(?:3\.ly)|(?:307\.to)|(?:4ms\.me)|(?:4sq\.com)|(?:4url\.cc)|(?:6url\.com)|(?:7\.ly)|(?:a\.gg)|(?:a\.nf)|(?:aa\.cx)|(?:abcurl\.net)|(?:ad\.vu)|(?:adf\.ly)|(?:adjix\.com)|(?:afx\.cc)|(?:all\.fuseurl.com)|(?:alturl\.com)|(?:amzn\.to)|(?:ar\.gy)|(?:arst\.ch)|(?:atu\.ca)|(?:azc\.cc)|(?:b23\.ru)|(?:b2l\.me)|(?:bacn\.me)|(?:bcool\.bz)|(?:binged\.it)|(?:bit\.ly)|(?:bizj\.us)|(?:bloat\.me)|(?:bravo\.ly)|(?:bsa\.ly)|(?:budurl\.com)|(?:canurl\.com)|(?:chilp\.it)|(?:chzb\.gr)|(?:cl\.lk)|(?:cl\.ly)|(?:clck\.ru)|(?:cli\.gs)|(?:cliccami\.info)|(?:clickthru\.ca)|(?:clop\.in)|(?:conta\.cc)|(?:cort\.as)|(?:cot\.ag)|(?:crks\.me)|(?:ctvr\.us)|(?:cutt\.us)|(?:dai\.ly)|(?:decenturl\.com)|(?:dfl8\.me)|(?:digbig\.com)|(?:digg\.com)|(?:disq\.us)|(?:dld\.bz)|(?:dlvr\.it)|(?:do\.my)|(?:doiop\.com)|(?:dopen\.us)|(?:easyuri\.com)|(?:easyurl\.net)|(?:eepurl\.com)|(?:eweri\.com)|(?:fa\.by)|(?:fav\.me)|(?:fb\.me)|(?:fbshare\.me)|(?:ff\.im)|(?:fff\.to)|(?:fire\.to)|(?:firsturl\.de)|(?:firsturl\.net)|(?:flic\.kr)|(?:flq\.us)|(?:fly2\.ws)|(?:fon\.gs)|(?:freak\.to)|(?:fuseurl\.com)|(?:fuzzy\.to)|(?:fwd4\.me)|(?:fwib\.net)|(?:g\.ro.lt)|(?:gizmo\.do)|(?:gl\.am)|(?:go\.9nl.com)|(?:go\.ign.com)|(?:go\.usa.gov)|(?:goo\.gl)|(?:goshrink\.com)|(?:gurl\.es)|(?:hex\.io)|(?:hiderefer\.com)|(?:hmm\.ph)|(?:href\.in)|(?:hsblinks\.com)|(?:htxt\.it)|(?:huff\.to)|(?:hulu\.com)|(?:hurl\.me)|(?:hurl\.ws)|(?:icanhaz\.com)|(?:idek\.net)|(?:ilix\.in)|(?:is\.gd)|(?:its\.my)|(?:ix\.lt)|(?:j\.mp)|(?:jijr\.com)|(?:kl\.am)|(?:klck\.me)|(?:korta\.nu)|(?:krunchd\.com)|(?:l9k\.net)|(?:lat\.ms)|(?:liip\.to)|(?:liltext\.com)|(?:linkbee\.com)|(?:linkbun\.ch)|(?:liurl\.cn)|(?:ln-s\.net)|(?:ln-s\.ru)|(?:lnk\.gd)|(?:lnk\.ms)|(?:lnkd\.in)|(?:lnkurl\.com)|(?:lru\.jp)|(?:lt\.tl)|(?:lurl\.no)|(?:macte\.ch)|(?:mash\.to)|(?:merky\.de)|(?:migre\.me)|(?:miniurl\.com)|(?:minurl\.fr)|(?:mke\.me)|(?:moby\.to)|(?:moourl\.com)|(?:mrte\.ch)|(?:myloc\.me)|(?:myurl\.in)|(?:n\.pr)|(?:nbc\.co)|(?:nblo\.gs)|(?:nn\.nf)|(?:not\.my)|(?:notlong\.com)|(?:nsfw\.in)|(?:nutshellurl\.com)|(?:nxy\.in)|(?:nyti\.ms)|(?:o-x\.fr)|(?:oc1\.us)|(?:om\.ly)|(?:omf\.gd)|(?:omoikane\.net)|(?:on\.cnn.com)|(?:on\.mktw.net)|(?:onforb\.es)|(?:orz\.se)|(?:ow\.ly)|(?:ping\.fm)|(?:pli\.gs)|(?:pnt\.me)|(?:politi\.co)|(?:post\.ly)|(?:pp\.gg)|(?:profile\.to)|(?:ptiturl\.com)|(?:pub\.vitrue.com)|(?:qlnk\.net)|(?:qte\.me)|(?:qu\.tc)|(?:qy\.fi)|(?:r\.im)|(?:rb6\.me)|(?:read\.bi)|(?:readthis\.ca)|(?:reallytinyurl\.com)|(?:redir\.ec)|(?:redirects\.ca)|(?:redirx\.com)|(?:retwt\.me)|(?:ri\.ms)|(?:rickroll\.it)|(?:riz\.gd)|(?:rt\.nu)|(?:ru\.ly)|(?:rubyurl\.com)|(?:rurl\.org)|(?:rww\.tw)|(?:s4c\.in)|(?:s7y\.us)|(?:safe\.mn)|(?:sameurl\.com)|(?:sdut\.us)|(?:shar\.es)|(?:shink\.de)|(?:shorl\.com)|(?:short\.ie)|(?:short\.to)|(?:shortlinks\.co.uk)|(?:shorturl\.com)|(?:shout\.to)|(?:show\.my)|(?:shrinkify\.com)|(?:shrinkr\.com)|(?:shrt\.fr)|(?:shrt\.st)|(?:shrten\.com)|(?:shrunkin\.com)|(?:simurl\.com)|(?:slate\.me)|(?:smallr\.com)|(?:smsh\.me)|(?:smurl\.name)|(?:sn\.im)|(?:snipr\.com)|(?:snipurl\.com)|(?:snurl\.com)|(?:sp2\.ro)|(?:spedr\.com)|(?:srnk\.net)|(?:srs\.li)|(?:starturl\.com)|(?:su\.pr)|(?:surl\.co.uk)|(?:surl\.hu)|(?:t\.cn)|(?:t\.co)|(?:t\.lh.com)|(?:ta\.gd)|(?:tbd\.ly)|(?:tcrn\.ch)|(?:tgr\.me)|(?:tgr\.ph)|(?:tighturl\.com)|(?:tiniuri\.com)|(?:tiny\.cc)|(?:tiny\.ly)|(?:tiny\.pl)|(?:tinylink\.in)|(?:tinyuri\.ca)|(?:tinyurl\.com)|(?:tl\.gd)|(?:tmi\.me)|(?:tnij\.org)|(?:tnw\.to)|(?:tny\.com)|(?:to\.ly)|(?:togoto\.us)|(?:totc\.us)|(?:toysr\.us)|(?:tpm\.ly)|(?:tr\.im)|(?:tra\.kz)|(?:trunc\.it)|(?:twhub\.com)|(?:twirl\.at)|(?:twitclicks\.com)|(?:twitterurl\.net)|(?:twitterurl\.org)|(?:twiturl\.de)|(?:twurl\.cc)|(?:twurl\.nl)|(?:u\.mavrev.com)|(?:u\.nu)|(?:u76\.org)|(?:ub0\.cc)|(?:ulu\.lu)|(?:updating\.me)|(?:ur1\.ca)|(?:url\.az)|(?:url\.co.uk)|(?:url\.ie)|(?:url360\.me)|(?:url4\.eu)|(?:urlborg\.com)|(?:urlbrief\.com)|(?:urlcover\.com)|(?:urlcut\.com)|(?:urlenco\.de)|(?:urli\.nl)|(?:urls\.im)|(?:urlshorteningservicefortwitter\.com)|(?:urlx\.ie)|(?:urlzen\.com)|(?:usat\.ly)|(?:use\.my)|(?:vb\.ly)|(?:vgn\.am)|(?:vl\.am)|(?:vm\.lc)|(?:w55\.de)|(?:wapo\.st)|(?:wapurl\.co.uk)|(?:wipi\.es)|(?:wp\.me)|(?:x\.vu)|(?:xr\.com)|(?:xrl\.in)|(?:xrl\.us)|(?:xurl\.es)|(?:xurl\.jp)|(?:y\.ahoo.it)|(?:yatuc\.com)|(?:ye\.pe)|(?:yep\.it)|(?:yfrog\.com)|(?:yhoo\.it)|(?:yiyd\.com)|(?:youtu\.be)|(?:yuarel\.com)|(?:z0p\.de)|(?:zi\.ma)|(?:zi\.mu)|(?:zipmyurl\.com)|(?:zud\.me)|(?:zurl\.ws)|(?:zz\.gd)|(?:zzang\.kr)|(?:›\.ws)|(?:✩\.ws)|(?:✿\.ws)|(?:❥\.ws)|(?:➔\.ws)|(?:➞\.ws)|(?:➡\.ws)|(?:➨\.ws)|(?:➯\.ws)|(?:➹\.ws)|(?:➽\.ws))/[a-z0-9]*/?",
        "", tweet_text)
    tweet_text = re.sub(r"[?!,.#…@:*\"/•]", " ", tweet_text)
    tweet_text = re.sub(r"[()]", " ", tweet_text)
    tweet_text = re.sub(r"\s{2,}", " ", tweet_text)
    tweet_text = re.sub(r"(^\s)|(\s$)", "", tweet_text)
    tweet_text = re.sub(r"\s[–\-|]|(--)\s", " ", tweet_text)

    return [stem(t) for t in tweet_text.split()]


class FullTweets(object):
    """
    用于从数据库获得文章信息
    """

    def __init__(self, start, end=None, key_words=None):
        self.start = start
        self.end = end
        self.papers = Paper.query_by_time_interval(self.start, self.end)

    def __iter__(self):
        for p in self.papers:
            yield p

    def __len__(self):
        return len(self.papers)

    def __getitem__(self, item):
        return self.papers[item]


class FullTweetTextSplit(object):
    """
        进行文本预处理和分词
    """

    def __init__(self, start, end=None):
        self.s = FullTweets(start, end)

    def __iter__(self):
        for p in self.s:
            # + "." + p.description
            yield [t for t in tweet_preprocess(p.title.lower()) if not deprecate_words(t)]

    def __len__(self):
        return len(self.s)

    def __getitem__(self, item):
        # + "." + self.s[item].description
        return [t for t in tweet_preprocess(self.s[item].title.lower()) if
                not deprecate_words(t)]


class TweetSplitStemmed(object):
    """
        进行词干提取
    """

    def __init__(self, start_timestamp_ms: int, end_timestamp_ms):
        self.full_tweet_split = FullTweetTextSplit(start_timestamp_ms, end_timestamp_ms)

    def __iter__(self):
        for tweet in self.full_tweet_split:
            yield [stem(w) for w in tweet]

    def __len__(self):
        return len(self.full_tweet_split)

    def __getitem__(self, item):
        return [stem(w) for w in self.full_tweet_split[item]]


class TweetStemmed(object):
    """
    应用层
    """

    def __init__(self, start_timestamp_ms: int, end_timestamp_ms):
        self.full_tweet_split = TweetSplitStemmed(start_timestamp_ms, end_timestamp_ms)

    def __iter__(self):
        for tweet in self.full_tweet_split:
            yield ' '.join(tweet)

    def __len__(self):
        return len(self.full_tweet_split)

    def __getitem__(self, item):
        return ' '.join(self.full_tweet_split[item])


class TFIDFCorpus(object):
    """
    使用doc2bow 切换为词袋模型
    Bag-of-words model (BoW model) 最早出现在自然语言处理（Natural Language Processing）和信息检索（Information Retrieval）领域.。该模型忽略掉文本的语法和语序等要素，将其仅仅看作是若干个词汇的集合，文档中每个单词的出现都是独立的。BoW使用一组无序的单词(words)来表达一段文字或一个文档
    """
    full_tweets = None
    dictionary = None

    def __init__(self, full_tweets, dictionary: corpora.Dictionary):
        self.full_tweets = full_tweets
        self.dictionary = dictionary

    def __iter__(self):
        for item in self.full_tweets:
            yield self.dictionary.doc2bow(item.lower().split())

    def __len__(self):
        return len(self.full_tweets)


def analyze(topics, start_prediction=int(time.time() * 1000 - 604800000), end_prediction=None, select_top=10,
            print_select_tops=True, key_words=None):
    start_time = time.time()
    tt = TextTeaser()  # 用于提取摘要
    print("开始日期：", start_prediction)
    print("全文本")
    full_tweets = FullTweets(start_prediction, end_prediction, key_words)  # 全文本
    print("去处理后")
    full_split = FullTweetTextSplit(start_prediction, end_prediction)  # 去处理后
    print("提取词干")
    full_stemmed = TweetStemmed(start_prediction, end_prediction)  # 提取词干
    print("论文数量", len(full_tweets))
    # 构造字典 并且处理字典中的停用词
    dictionary = corpora.Dictionary(tweet_preprocess(item) for item in full_stemmed)
    print("initialization finished")
    stop_list = set(
        'a an the of at on upon in to from out as so such or and those this these that for is was am are \'s been were what when where who will with the www'.split())
    stop_ids = [dictionary.token2id[stop_word] for stop_word in stop_list if stop_word in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
    dictionary.filter_tokens(stop_ids + once_ids)
    dictionary.compactify()
    print("dictionary finished")

    # 建立 tfidf模型
    corpus = TFIDFCorpus(full_stemmed, dictionary)
    print('corpus finished')
    # noinspection PyPep8Naming
    tfIdfModel = models.TfidfModel(corpus)
    print('TF-IDF finished')

    # 建立 词袋模型
    topics_bow = dictionary.doc2bow([stem(t.replace(' ', '_')) for t in topics])
    topics_tfidf = tfIdfModel[topics_bow]
    print("related topics finished")

    # 建立矩阵相似度index
    print(len(dictionary))
    index = similarities.MatrixSimilarity(tfIdfModel[corpus])
    print("similarity index finished")
    sims0 = index[topics_tfidf]
    sims = sorted(enumerate(sims0), key=lambda item: -item[1])
    print("similarity sorting finished")

    # remove duplicates
    print(len(full_tweets))
    tweet_texts = [' '.join(t) for t in full_split]
    current_pointer = 0
    while current_pointer < len(sims) - 1:
        this_index = sims[current_pointer][0]
        next_index = sims[current_pointer + 1][0]
        this_text = re.sub('rt \S* ', '', tweet_texts[this_index]).strip()
        next_text = re.sub('rt \S* ', '', tweet_texts[next_index]).strip()
        if this_text[0:32] == next_text[0:32]:
            del sims[current_pointer + 1]
        else:
            current_pointer += 1
    existing = [False] * len(full_tweets)
    for i in sims:
        existing[i[0]] = True
    print(len(sims))
    print(sims[0:select_top])

    result_str_list = []
    if print_select_tops:
        final_result = sims[0:select_top]
        increment_flag = 1
        for item in final_result:
            t = full_tweets[item[0]]
            result_str = """{increment_flag}.\n{title}\n{authors}\nhttps://arxiv.org/abs/{arxiv_id}\n{abstract}""".format(
                increment_flag=increment_flag,
                title=t.title.replace('\n ', ''),
                authors=t.authors,
                arxiv_id=t.user_id.replace('arXiv:', ''),
                abstract=t.description
            )
            result_str_list.append(result_str)

            increment_flag += 1
    print(str(time.time() - start_time))

    # send email
    result_email_text = '论文' + '\n\n\n'.join(result_str_list)
    if end_prediction is None:
        end_prediction = int(time.time() * 1000)
    start_prediction = int(time.time() * 1000 - 604800000)
    subject = '本周' + topics[0] + '领域论文推荐: {start_date}-{end_date}'.format(
        start_date=datetime.fromtimestamp(start_prediction / 1000).strftime("%Y.%m.%d"),
        end_date=datetime.fromtimestamp(end_prediction / 1000).strftime("%Y.%m.%d")
    )
    sendEmail(subject, result_email_text)
    #
    # calculate accuracy
    acc_count = 0
    top_indexes = [i[0] for i in sims[0:select_top]]
    for _idx, tweet in enumerate(full_tweets):
        if _idx in top_indexes:
            t = tweet.description
            if labelling(t, topics):
                acc_count += 1
    hit = acc_count / select_top

    # calculate loss (cross entropy)
    q = []
    p = []
    for _idx, tweet in enumerate(full_tweets):
        if not existing[_idx]:
            continue
        q.append(log(sims0[_idx] if sims0[_idx] > 0 else 1e-20))
        p.append(1.0 if labelling(tweet.description, topics) else 0.0)
    loss = -np.dot(p, q)

    # calculate precision & recall
    pr_counter = [0, 0, 0, 0]
    for _idx, tweet in enumerate(full_tweets):
        if not existing[_idx]:
            continue
        t = tweet.title.lower() + "." + tweet.description
        if _idx in top_indexes and labelling(t, topics):
            pr_counter[0] += 1
        elif _idx in top_indexes and not labelling(t, topics):
            pr_counter[1] += 1
        elif _idx not in top_indexes and labelling(t, topics):
            pr_counter[2] += 1
        elif _idx not in top_indexes and not labelling(t, topics):
            pr_counter[3] += 1
    accuracy = (pr_counter[0] + pr_counter[3]) / len(sims)

    print(hit)
    print(loss)
    print(acc_count)
    print(accuracy)


if __name__ == '__main__':
    # related_topics = [
    #     "recommendations",
    #     'recommender systems',
    #     'recommendation algorithms',
    #     'collaborative filtering',
    #     'matrix factorization',
    #     'probabilistic graphical models',
    #     'recommender',
    #     'recommendation',
    #     'cold start',
    #     'factorization machine',
    #     'tensor factorization',
    #     'sparse matrix',
    #     'data sparsity',
    #     "recall",
    #     "click prediction",
    #     "predicting clicks",
    #     "interest network",
    #     "ctr",
    #     "explainable recommendation",
    #     'recsys',
    #     'recsys2017',
    #     'recsys2018',
    #     'recsys2019',
    #     'recsys2020',
    #     "similarity",
    #     "interaction sequences",
    #     "matrix factorization",
    #     "implicit feedback"
    # ]
    # analyze(related_topics, start_prediction="2021-03-27 00:00:00.000")
    QA_topics = [
        "qa",
        "question answering",
        "question-answer",
        "retriever reader",
        "question generation",
        "question answer",
        "answering dataset",
        "comprehension task",
        "step reasoning",
        "text comprehension",
        "answering using",
        "answering challenge",
        "open domain",
        "answer context",
        "reader reformulated",
        "reformulated query",
        "query used",
        "paragraphs retriever"
    ]
    analyze(QA_topics, start_prediction="2021-03-27 00:00:00.000", key_words="nswer")
