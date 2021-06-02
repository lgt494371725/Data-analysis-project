import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

mac2id=dict()
onlinetimes=[]
f=open('TestData.txt',encoding='utf-8')
for line in f:
    mac=line.split(',')[2]  #每条数据的mac地址
    onlinetime=int(line.split(',')[6])#上网时长
    starttime=int(line.split(',')[4].split(' ')[1].split(':')[0])#开始上网时间
    if mac not in mac2id:
        mac2id[mac]=len(onlinetimes)#key:mac,value:对应mac地址的上网时长及开始上网时间
        onlinetimes.append((starttime,onlinetime))
    else:
        onlinetimes[mac2id[mac]]=[(starttime,onlinetime)]
real_X=np.array(onlinetimes).reshape((-1,2))

X=real_X[:,0:1]

db=DBSCAN(eps=0.01,min_samples=20).fit(X)
#eps:两个样本被看作邻居节点的最大距离，min_samples:每个簇的样本数,metric:距离计算方式,如metric='euclidean'即欧式距离
labels = db.labels_  #每个数据的簇标签

print('Labels:')
print(labels)
raito=len(labels[labels[:] == -1]) / len(labels) #计算标签为-1，即噪声数据的比例
print('Noise raito:',format(raito, '.2%'))

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0) #计算簇的个数

print('Estimated number of clusters: %d' % n_clusters_)
print("Silhouette Coefficient: %0.3f"% metrics.silhouette_score(X, labels))

for i in range(n_clusters_):  #打印各簇标号及各簇内数据
    print('Cluster ',i,':')
    print(list(X[labels == i].flatten()))
    
plt.hist(X,24)
