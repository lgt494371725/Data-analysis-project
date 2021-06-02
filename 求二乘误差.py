#已知(x,y)=(1,2,-1,1), (2,1,1,0), (-1,1,3,2), (2,1,0,1),
#a=(1,-1,1,2),求二乘误差

#快速方法
data = np.matrix([[1,2,-1,1], [2,1,1,0], [-1,1,3,2], [2,1,0,1]])
a = [1,-1,1,2]

import numpy as np
def SQE(data,a):
    b=np.append(a,0)#0は、bをXにかけたときに、yにかかる
    c=np.ones((data.shape[0],1))
    X=np.hstack((c,data))
    error=np.array(X*b.reshape(-1,1)-data[:,-1])#是矩阵内积，也可以用dot
    error2=sum(error*error) #首先要转换成array类型
    return error2
