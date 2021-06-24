import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import sys, os

from sklearn.preprocessing import OneHotEncoder

sys.path.append("../../../")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../../../") for name in dirs])


class GBDTLR:
    def __init__(self, lr, gbdt, gbdt_enc):
        self.lr = lr
        self.gbdt = gbdt
        self.gbdt_enc = gbdt_enc


def load_dataset(path):
    df = pd.read_csv(path, header=None)
    df = df.dropna()
    X = df.drop([1824], axis=1)
    Y = df[1824]
    return X, Y


def load_model(*args, **kwargs):
    gbdt = GradientBoostingClassifier(n_estimators=10)
    """
    n_estimators,最大的弱学习器的个数，即有多少个回归树
    max_depth : int, default=3。每个回归树的的深度
    """
    gbdt_enc = OneHotEncoder()
    lr = LogisticRegression(max_iter=1000)
    model = GBDTLR(lr, gbdt, gbdt_enc)
    return model


def train(model: GBDTLR, X, Y):
    model.gbdt.fit(X, Y)
    model.gbdt_enc.fit(model.gbdt.apply(X)[:, :, 0])
    model.lr.fit(model.gbdt_enc.transform(model.gbdt.apply(X)[:, :, 0]), Y)


def predict(model, X):
    y_pred_gbdt_lr = model.lr.predict_proba(
        model.gbdt_enc.transform(model.gbdt.apply(X)[:, :, 0]))[:, 1]
    return y_pred_gbdt_lr


def run():
    # 加载数据
    X, Y = load_dataset()
    # 加载模型
    model = load_model()
    # 训练数据
    train(model, X, Y)
