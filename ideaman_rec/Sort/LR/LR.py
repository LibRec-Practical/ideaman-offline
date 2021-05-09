import pandas as pd
from sklearn.linear_model import LogisticRegression
import sys, os

sys.path.append("../../")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../../") for name in dirs])


def load_dataset(path):
    df = pd.read_csv(path, header=None)
    df = df.dropna()
    X = df.drop([1824], axis=1)
    Y = df[1824]
    return X, Y


def load_model(*args, **kwargs):
    lr = LogisticRegression(*args, **kwargs)
    return lr


def train(model, X, Y):
    model.fit(X, Y)


def predict(model, X):
    return model.predict(X)


def run():
    # 加载数据
    X, Y = load_dataset()
    # 加载模型
    model = load_dataset()
    # 训练数据
    train(model, X, Y)
