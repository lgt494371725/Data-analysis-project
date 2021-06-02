import numpy as np 

import matplotlib.pyplot as plt
import seaborn as sns

## 导入逻辑回归模型函数
from sklearn.svm  import SVC

## 构造数据集
x_fearures = np.array([[-1, -2], [-2, -1], [-3, -2], [1, 3], [2, 1], [3, 2]])
y_label = np.array([0, 0, 0, 1, 1, 1])

## 调用SVC模型 （支持向量机分类）
svc = SVC(kernel='linear')
#参数：C：正则化参数，C越小包容性越高，容易欠拟合，C越大，敏感度越高，容易过拟合
#选择核函数kernel='rbf' 高斯核函数

svc = svc.fit(x_fearures, y_label)
## 查看其对应模型的w
print('the weight of svc:',svc.coef_)
## 查看其对应模型的w0
print('the intercept(w0) of svc:',svc.intercept_)
y_train_pred = svc.predict(x_fearures)
# 最佳函数
x_range = np.linspace(-3, 3)

w = svc.coef_[0]
a = -w[0] / w[1]#参数向量和决策边界90度正交
y_3 = a*x_range - (svc.intercept_[0]) / w[1]#这个边界线怎么来的？

# 可视化决策边界
plt.figure()
plt.scatter(x_fearures[:,0],x_fearures[:,1], c=y_label, s=50, cmap='viridis')
plt.plot(x_range, y_3, '-c')
#-c只是一个线的风格
plt.show()
