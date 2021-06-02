
#划分测试训练
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = \
         train_test_split(X, y, test_size=0.2,random_state=20)

#各种指标
from sklearn import metrics
准确度 metrics.accuracy_score(y_test,X_pred)
混淆矩阵 metrics.confusion_matrix(test_predict,y_test)
#利用热力图对于结果进行可视化
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix_result, annot=True, cmap='Blues')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.show()

#利用数据库的实例
from sklearn import datasets
iris=datasets.load_iris()
X=iris.data
y=iris.target

# 交叉验证
from sklearn.model_selection import cross_val_score

cross_val_score(regressor,boston.data,bonston.target,cv=10,scoring="neg_mean_squared_error")
#第一个是回归器/分类器，第二个是data,第三个是label，第四个是划分10份循环10次，scoring是衡量指标，此处为负均方误差
# KFlod的函数
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import Pipeline




#通常用于训练分类算法
from sklearn.datasets.samples_generator import make_blobs
x,y=make_blobs(n_samples=60, centers=2, random_state=0, cluster_std=0.4)


#选择参数的好办法
from sklearn.model_selection import GridSearchCV
# 存在缺点，因为网格搜索无法舍去参数，所以如果有些实际上多余的参数也被输入，得到的结果可能会更差
parameters={"希望参数":["取值范围"]}
GS = GridSearchCV(clf,parameters,cv=10)#交叉检证次数为10
GS.fit(Xtrain,Ytrain)
GS.best_params_#返回最佳组合
GS.best_score_ #在最佳组合下的精确性

#填充缺失参数
#使用均值填补
from sklearn.impute import SimpleImputer
imp_mean=SimpleImputer(missing_values=np.nan,strategy='mean')
#strategy还有'median'，‘most_frequent’
X_missing_mean=imp_mean.fit_transform(X_missing)
# 使用0填补
imp_zero=SimpleImputer(missing_values=np.nan,strategy='constant',fill_value=0)
X_missing_zero=imp_zero.fit_transform(X_missing)
















