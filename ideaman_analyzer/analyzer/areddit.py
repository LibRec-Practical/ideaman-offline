import tensorflow as tf
import numpy as np
from gensim.models import Word2Vec
from pathlib import Path
import re
from ideaman_analyzer.model.paper import *
from ideaman_mail.MailSender import *
import warnings
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)
# warnings.filterwarnings('ignore')
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
print(tf.__version__)


def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')


class ModelConfig(object):
    num_epochs = 512
    batch_size = 256
    embedding_dim = 100

    seq_length = 32
    num_filters_x = 256
    kernel_size_x = 5

    ht_length = 3
    num_filters_h = 128
    kernel_size_h = 3

    hidden_dim = 128
    learning_rate = 1e-5
    keep_prob = 0.5

    num_classes = 40000
    negative_to_positive_ratio = 5
    negative_before_positive = 20

    parent_path = '.'

    train_report_per_batch = 1
    predict_report_per_batch = 100

    def __init__(self):
        mkdir(self.parent_path + '/w2vmodels')
        mkdir(self.parent_path + '/checkpoints')
        mkdir(self.parent_path + '/summary')
        self.save_embedding_model_path = self.parent_path + '/w2vmodels/w2v_model_fback'
        self.save_checkpoint_dir = self.parent_path + '/checkpoints/checkpoints_fback-1_%d-%.1f' % (
            self.negative_to_positive_ratio, self.keep_prob)
        self.summary_dir = self.parent_path + '/summary/summary_fback-1_%d-%.1f' % (
            self.negative_to_positive_ratio, self.keep_prob)


config = ModelConfig()


def extract_text_from_Paper(b):
    return b.title.lower() + "." + b.description


def deprecate_words(word: str) -> bool:
    """
        文本预处理,去除stopword 并进行分词
    """
    if word.endswith('…'):
        return True
    stop_list = 'a an the of at on upon in to from out as so such or and those this these that for is was am are been were what when where who will with the www by ? ! : . , … -'.split()
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
    tweet_text = re.sub(
        r'(a|an|the|of|at|on|upon|in|to|from|out|as|so|such|or|and|those|this|these|that|for|is|was|am|are|been|were|what|when|where|who|will|with|by|\?|!|:|\.|,|…|-)',
        "", tweet_text)
    tweet_text = re.sub(r"[?!,.#…@:*\"/•]", " ", tweet_text)
    tweet_text = re.sub(r"[()]", " ", tweet_text)
    tweet_text = re.sub(r"\s{2,}", " ", tweet_text)
    tweet_text = re.sub(r"(^\s)|(\s$)", "", tweet_text)
    tweet_text = re.sub(r"\s[–\-|]|(--)\s", " ", tweet_text)
    return tweet_text.split()


class TweetReader(object):
    """
    用于从数据库获得文章信息
    """

    def __init__(self):
        self.papers = Paper.get_classifier_dataset()

    def __iter__(self):
        for p in self.papers:
            yield p

    def __len__(self):
        return len(self.papers)

    def __getitem__(self, item):
        return self.papers[item]


class TweetEmbeddingReader(TweetReader):
    def __iter__(self):
        for t in Paper.get_classifier_dataset():
            yield tweet_preprocess(extract_text_from_Paper(t))


def pad2d(lst, seq_length=config.seq_length, dim=config.embedding_dim):
    a = list(lst)
    if len(a) >= seq_length:
        return np.vstack([np.expand_dims(r, 0) for r in a[:seq_length]])
    else:
        while len(a) < seq_length:
            a.append(np.zeros(shape=dim))
        return np.vstack([np.expand_dims(r, 0) for r in a[:seq_length]])


def input_fn(embedding_model, ratio_control,
             batch_size=config.batch_size, produce_id=False):
    def word_vector(w):
        try:
            return np.array(embedding_model[w])
        except KeyError:
            return np.zeros(config.embedding_dim)

    # count_positive = 0
    # count_negative = 0
    reader = TweetReader()
    # 输出 (-1, seq_length, embedding_dim)
    raw_list = []
    for i in reader:
        text = extract_text_from_Paper(i)
        tasks = [eval(_id) for _id in (i.pwc_tasks).split(",")]
        input_matrix = pad2d([word_vector(w) for w in tweet_preprocess(text)])
        hashtag_matrix = pad2d([word_vector(w) for w in text.split() if w.startswith('#')],
                               seq_length=config.ht_length)
        # 加载label
        label = [0] * ModelConfig.num_classes
        for _id in tasks:
            label[_id] = 1

        if produce_id:
            raw_list.append([input_matrix, hashtag_matrix, label, i.title])
        else:
            raw_list.append([input_matrix, hashtag_matrix, label])

        if len(raw_list) >= batch_size:
            np.random.shuffle(raw_list)
            transpose_arr = np.transpose(raw_list)
            X = transpose_arr[0]
            X = np.expand_dims(np.vstack([np.expand_dims(row, 0) for row in X]), -1)
            h = transpose_arr[1]
            h = np.expand_dims(np.vstack([np.expand_dims(row, 0) for row in h]), -1)
            y = transpose_arr[2]
            y = np.vstack([np.expand_dims(row, 0) for row in y])
            if produce_id:
                title = transpose_arr[3]
                yield X, h, y, title
            else:
                yield X, h, y
            raw_list = []


def embedding_fn():
    print("embeddeding_fn开始")
    reader = TweetEmbeddingReader()

    if Path(config.save_embedding_model_path).is_file():
        embedding_model = Word2Vec.load(config.save_embedding_model_path)
    else:
        embedding_model = Word2Vec(reader, workers=4, size=config.embedding_dim)
        embedding_model.init_sims(replace=True)
        embedding_model.save(config.save_embedding_model_path)

    return embedding_model


def model_fn(input_x, input_h, input_y, global_step):
    tf.summary.image('input_x', input_x)
    tf.summary.image('input_h', input_h)

    with tf.name_scope("cnn_x_1"):
        # CNN layer
        conv_x = tf.layers.conv2d(
            input_x,
            config.num_filters_x,
            kernel_size=(1, config.kernel_size_x),
            name='conv_x',
            padding='same',
            kernel_regularizer=tf.contrib.layers.l2_regularizer(0.0)
        )

        # global max pooling layer
        gmp_x = tf.reduce_max(conv_x, reduction_indices=[1], name='gmp_x')

    with tf.name_scope("cnn_h_1"):
        # CNN layer
        conv_h = tf.layers.conv2d(
            input_h,
            config.num_filters_h,
            kernel_size=(1, config.kernel_size_h),
            name='conv_h',
            padding='same',
            kernel_regularizer=tf.contrib.layers.l2_regularizer(0.0)
        )
        # global max pooling layer
        gmp_h = tf.reduce_max(conv_h, reduction_indices=[1], name='gmp_h')

    with tf.name_scope("score"):
        # 全连接层，后面接dropout以及relu激活
        reshape_x = tf.reshape(gmp_x, shape=[-1, config.num_filters_x * config.embedding_dim])
        reshape_h = tf.reshape(gmp_h, shape=[-1, config.num_filters_h * config.embedding_dim])
        flatten = tf.concat([reshape_x, reshape_h], axis=1)
        fc = tf.layers.dense(
            flatten,
            config.hidden_dim,
            name='fc1',
            kernel_regularizer=tf.contrib.layers.l2_regularizer(0.004)
        )
        fc = tf.layers.dropout(fc, rate=config.keep_prob)
        fc = tf.nn.relu(fc)

        # 分类器
        logits = tf.layers.dense(
            fc,
            config.num_classes,
            name='fc2',
            kernel_regularizer=tf.contrib.layers.l2_regularizer(0.004)
        )
        smx_res = tf.nn.sigmoid(logits)
        y_pred_cls = smx_res  # 预测类别

    with tf.name_scope("optimize"):
        # 损失函数，交叉熵
        cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=input_y)
        loss = tf.reduce_mean(cross_entropy)
        # 优化器
        optim = tf.train.AdamOptimizer(learning_rate=config.learning_rate).minimize(loss, global_step=global_step)

    tf.summary.scalar('loss', loss)

    with tf.name_scope("accuracy"):
        # 准确率

        # correct_pred = tf.equal(tf.argmax(y_pred_cls.logits_class, 1), tf.argmax(input_y, 1))
        # acc = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
        correct_attrs_op = tf.equal(tf.cast(tf.greater_equal(tf.sigmoid(y_pred_cls), 0.5), tf.int32),
                                    tf.cast(input_y, tf.int32))
        acc = tf.reduce_mean(tf.reduce_min(tf.cast(correct_attrs_op, tf.float32), 1))
    tf.summary.scalar('accuracy', acc)

    return loss, optim, acc, smx_res


def generate_placeholder():
    input_x = tf.placeholder(shape=[None, config.seq_length, config.embedding_dim, 1], dtype=tf.float32)
    input_h = tf.placeholder(shape=[None, config.ht_length, config.embedding_dim, 1], dtype=tf.float32)
    input_y = tf.placeholder(shape=[None, config.num_classes], dtype=tf.float32)

    return input_x, input_h, input_y


def train(first_run=False, save_path=None):
    print('开始训练')
    embedding_model = embedding_fn()
    print("embedding模型运行完成")

    input_x, input_h, input_y = generate_placeholder()
    print("生成占位后的tensor")

    global_step = tf.Variable(0, name='global_step', trainable=False)
    loss, optim, acc, _ = model_fn(input_x, input_h, input_y, global_step)
    # 计算loss
    summary = tf.summary.merge_all()
    gen = []
    for i in range(config.num_epochs):
        gen.append(input_fn(embedding_model, ratio_control=True))
    saver = tf.train.Saver()
    with tf.Session() as sess:
        train_writer = tf.summary.FileWriter(config.summary_dir, sess.graph)
        sess.run(tf.global_variables_initializer())
        if first_run == False:
            saver.restore(sess, save_path=save_path)

        epoch_count = 0
        for ds in gen:
            epoch_count += 1

            step = 0
            for X, h, y in ds:
                step += 1

                run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
                run_metadata = tf.RunMetadata()
                summ, l, o, a, g = sess.run([summary, loss, optim, acc, global_step], feed_dict={
                    input_x: X,
                    input_h: h,
                    input_y: y
                }, run_metadata=run_metadata, options=run_options)
                train_writer.add_run_metadata(run_metadata, 'step%d' % g)
                train_writer.add_summary(summ, g)

                if step % config.train_report_per_batch == 0:
                    saver.save(sess, config.save_checkpoint_dir + 'model.ckpt', global_step=g)
                    print('[%s] epoch %d/%d, batch %d, training accuracy %f, loss %f' % (
                        datetime.now().strftime('%b-%d-%y %H:%M:%S'), epoch_count, config.num_epochs, step, a, l))
            print('[%s] epoch %d/%d, batch %d finished' % (
                datetime.now().strftime('%b-%d-%y %H:%M:%S'), epoch_count, config.num_epochs, step))
    print("all finished")
    train_writer.close()
    print('train writer closed')


def predict(save_path=None):
    print('start prediction')

    embedding_model = embedding_fn()
    input_x, input_h, input_y = generate_placeholder()

    global_step = tf.Variable(0, name='global_step', trainable=False)

    loss, _, acc, res = model_fn(input_x, input_h, input_y, global_step)
    gen = input_fn(embedding_model, ratio_control=False,
                   batch_size=1,
                   produce_id=True)

    acc_list = []
    loss_list = []
    id_list = []
    res_list = []

    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, save_path=save_path)

        step = 0

        aaa = 1
        for X, h, y, title in gen:
            step += 1
            l, a, r = sess.run([loss, acc, res], feed_dict={
                input_x: X,
                input_h: h,
                input_y: y
            })
            loss_list.append(l)
            res_list.append(r[0][0])
            lis = r.tolist()[0]
            after_sort_lis = sorted(lis.copy() , reverse=True)
            num = 1
            print(title)
            for v in after_sort_lis:
                i = lis.index(v)
                print(i , v)
                num += 1;
                if num >= 10:
                    break
            a += 1
            if aaa > 10:
                return
            # if step % config.predict_report_per_batch == 0:
            #     print(
            #         '[%s] batch %d, accuracy %f, loss %f' % (datetime.now().strftime('%b-%d-%y %H:%M:%S'), step, a, l))
        # print('[%s] batch %d finished' % (datetime.now().strftime('%b-%d-%y %H:%M:%S'), step))

    # print("all finished")


if __name__ == '__main__':
    # train(first_run=True)
    predict(save_path="./checkpoints/checkpoints_fback-1_5-0.5model.ckpt-3158")
