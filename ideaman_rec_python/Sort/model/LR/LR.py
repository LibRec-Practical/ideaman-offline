import pandas as pd
from sklearn.linear_model import LogisticRegression
from DataSet import get_total_recall, cur, getPredictData
import sys, os

sys.path.append("../../../")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../../../") for name in dirs])


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
    X, Y = load_dataset("dataset/tensor.csv")
    # 加载模型
    model = load_model()
    # 训练数据
    train(model, X, Y)
    dic = get_total_recall()
    for i in dic:
        u_id = i
        i_ids = dic[i].split(",")
        for i_id in i_ids:
            x_prev = getPredictData(int(u_id), int(i_id))
            y_prev = predict(model,x_prev)
            print(y_prev)
if __name__ == '__main__':
    run()