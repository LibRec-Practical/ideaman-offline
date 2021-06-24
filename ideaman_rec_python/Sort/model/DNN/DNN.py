import pandas as pd
# 利用 keras 定义深度学习网络
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
import sys, os

sys.path.append("../../../")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../../../") for name in dirs])


def load_dataset(path):
    df = pd.read_csv(path, header=None)
    df = df.dropna()
    X = df.drop([1824], axis=1)
    Y = df[1824]
    return X, Y


def load_model():
    model = Sequential()
    # 添加了输入层的信息
    model.add(Dense(100, activation='sigmoid', input_shape=(1824,)))  # batch_size = 20, 30, 50, ...
    model.add(Dense(128, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(2, activation='softmax'))

    # 目标函数，优化算法，评估方法（准确，AUC）
    model.compile(loss='categorical_crossentropy', optimizer=SGD(), metrics=['accuracy'])

    return model


def train(model, X, Y, batch_size=50, epochs=128):
    model.fit(X, Y, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(X, Y))


def predict(model, X):
    return model.predict(X)


def run():
    # 加载数据
    X, Y = load_dataset()
    # 加载模型
    model = load_dataset()
    # 训练数据
    train(model, X, Y)
