import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import metrics
iris = datasets.load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = \
         train_test_split(X, y, test_size=0.2,random_state=20)
clf = KNeighborsClassifier(n_neighbors=5, p=2, metric="minkowski")
#参数 weights:是否需要加权系数，metric:minkowski即pnorm,当p=2时，就是欧式距离，p=1就是曼哈顿距离
clf.fit(X_train, y_train)
X_pred = clf.predict(X_test)
acc = metrics.accuracy_score(y_test,X_pred)
print("预测的准确率ACC: %.3f" % acc)

#回归器的用法
from sklearn.neighbors import KNeighborsRegressor
np.random.seed(0)
# 随机生成40个(0, 1)之前的数，乘以5，再进行升序
X = np.sort(5 * np.random.rand(40, 1), axis=0)
# 创建[0, 5]之间的500个数的等差数列, 作为测试数据
T = np.linspace(0, 5, 500).reshape(-1,1)
# 使用sin函数得到y值，并拉伸到一维
y = np.sin(X).ravel()
# Add noise to targets[y值增加噪声]
y[::5] += 1 * (0.5 - np.random.rand(8))
# Fit regression model
# 设置多个k近邻进行比较
n_neighbors = [1, 3, 5, 8, 10, 40]
# 设置图片大小
plt.figure(figsize=(10,20))
for i, k in enumerate(n_neighbors):
    # 默认使用加权平均进行计算predictor
    clf = KNeighborsRegressor(n_neighbors=k, p=2, metric="minkowski")
    # 训练
    clf.fit(X, y)#总是X，y就是任意生成的随机数
    # 预测
    y_ = clf.predict(T)
    plt.subplot(6, 1, i + 1)
    plt.scatter(X, y, color='red', label='data')
    plt.plot(T, y_, color='navy', label='prediction')
    plt.axis('tight')
    plt.legend()
    plt.title("KNeighborsRegressor (k = %i)" % (k))

plt.tight_layout()
plt.show()
#可见k=1的时候过拟合，k=40的时候欠拟合，一般来说k从3，20之间尝试
