# Project1
# 前言
本项目改编自阿里天池学习赛，将主要利用Python进行数据分析以及数据可视化，包含数据集的处理、数据探索与清晰、数据分析、数据可视化四部分，利用pandas、mysql、matplotlib
+ [学习赛事地址](https://tianchi.aliyun.com/competition/entrance/531837/introduction。)

# 1. 数据集说明
#### 1.1 数据集来源介绍
**所有候选人信息** 
</br>该文件为每个候选人提供一份记录，并显示候选人的信息、总收入、从授权委员会收到的转账、付款总额、给授权委员会的转账、库存现金总额、贷款和债务以及其他财务汇总信息。
</br>数据字段描述详细:https://www.fec.gov/campaign-finance-data/all-candidates-file-description/
</br>关键字段说明
- CAND_ID 候选人ID
- CAND_NAME 候选人姓名
- CAND_PTY_AFFILIATION 候选人党派

</br>数据来源:https://www.fec.gov/files/bulk-downloads/2020/weball20.zip

**候选人委员会链接信息** 
</br>该文件显示候选人的身份证号码、候选人的选举年份、联邦选举委员会选举年份、委员会识别号、委员会类型、委员会名称和链接标识号。
</br>信息描述详细:https://www.fec.gov/campaign-finance-data/candidate-committee-linkage-file-description/
</br>关键字段说明
- CAND_ID 候选人ID
- CAND_ELECTION_YR 候选人选举年份
- CMTE_ID 委员会ID

</br>数据来源:https://www.fec.gov/files/bulk-downloads/2020/ccl20.zip

**个人捐款档案信息** 
【注意】由于文件较大，本数据集只包含2020.7.22-2020.8.20的相关数据，如果需要更全数据可以通过数据来源中的地址下载。
</br>该文件包含有关收到捐款的委员会、披露捐款的报告、提供捐款的个人、捐款日期、金额和有关捐款的其他信息。
</br>信息描述详细:[https://www.fec.gov/campaign-finance-data/contributions-individuals-file-description/](https://www.fec.gov/campaign-finance-data/contributions-individuals-file-description/)
</br>关键字段说明
- CMTE_ID  委员会ID
- NAME 捐款人姓名
- CITY 捐款人所在市
- State 捐款人所在州
- EMPLOYER 捐款人雇主/公司
- OCCUPATION 捐款人职业

</br>数据来源:https://www.fec.gov/files/bulk-downloads/2020/indiv20.zip


#### 1.2 需要提前下载好数据集
你无需从以上网页的数据来源去下载数据，数据已上传到百度云中
https://pan.baidu.com/s/1szl7FYwnbzYv3KWwNCimbQ
提取码：akak
+ ccl.txt
+ itcont_2020_20200722_20200820.txt
+ weball20.txt

# 2、数据处理
进行数据处理前，我们需要知道我们最终想要的数据是什么样的，因为我们是想分析候选人与捐赠人之间的关系，所以我们想要一张数据表中有捐赠人与候选人一一对应的关系，所以需要将目前的三张数据表进行一一关联，汇总到需要的数据。

#### 2.1 用python读取数据，并利用pymysql连接python与mysql

```
import pymysql.cursors
import pandas as pd
connection = pymysql.connect(host='127.0.0.1',port=3306,\
                         user='root',password='root',db='test',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
#user和password根据你自己来填，db是你将要在mysql中使用的数据库
```


+ 读取候选人信息，由于原始数据没有表头，需要添加表头
```
candidates = pd.read_csv("weball20.txt", sep = '|',names=['CAND_ID','CAND_NAME','CAND_ICI','PTY_CD','CAND_PTY_AFFILIATION','TTL_RECEIPTS',
                                                          'TRANS_FROM_AUTH','TTL_DISB','TRANS_TO_AUTH','COH_BOP','COH_COP','CAND_CONTRIB',
                                                          'CAND_LOANS','OTHER_LOANS','CAND_LOAN_REPAY','OTHER_LOAN_REPAY','DEBTS_OWED_BY',
                                                      'TTL_INDIV_CONTRIB','CAND_OFFICE_ST','CAND_OFFICE_DISTRICT','SPEC_ELECTION','PRIM_ELECTION','RUN_ELECTION'
                                                          ,'GEN_ELECTION','GEN_ELECTION_PRECENT','OTHER_POL_CMTE_CONTRIB','POL_PTY_CONTRIB', 'CVG_END_DT','INDIV_REFUNDS','CMTE_REFUNDS'])
#读取候选人和委员会的联系信息
ccl = pd.read_csv("ccl.txt", sep = '|',names=['CAND_ID','CAND_ELECTION_YR','FEC_ELECTION_YR','CMTE_ID','CMTE_TP','CMTE_DSGN','LINKAGE_ID'])
# 读取个人捐赠数据，由于原始数据没有表头，需要添加表头
# 提示：读取本文件大概需要5-10s      
itcont = pd.read_csv('itcont_2020_20200722_20200820.txt', sep='|',names=['CMTE_ID','AMNDT_IND','RPT_TP','TRANSACTION_PGI',                                                'IMAGE_NUM','TRANSACTION_TP','ENTITY_TP','NAME','CITY',
                                                                              'STATE','ZIP_CODE','EMPLOYER','OCCUPATION','TRANSACTION_DT',
                                                                                  'TRANSACTION_AMT','OTHER_ID','TRAN_ID','FILE_NUM','MEMO_CD','MEMO_TEXT','SUB_ID'])
```

+ 由于列数过多，我们只提取其中最有用的列
数据字段说明：
- CMTE_ID：委员会ID
- CAND_ID：候选人ID
- CAND_NAME：候选人姓名
- CAND_PTY_AFFILIATION：候选人党派
- NAME – 捐赠人姓名
- STATE – 捐赠人所在州
- EMPLOYER – 捐赠人所在公司
- OCCUPATION – 捐赠人职业
- TRANSACTION_AMT – 捐赠数额（美元）
- TRANSACTION_DT – 收到捐款的日期
```
ccl = ccl[['CMTE_ID','CAND_ID']] 
candidates = candidates[['CAND_ID','CAND_NAME','CAND_PTY_AFFILIATION']]
itcont = itcont[['CMTE_ID','NAME','STATE','EMPLOYER','OCCUPATION',
                                           'TRANSACTION_AMT', 'TRANSACTION_DT']]
```

#### 2.2 将委员会和候选人一一对应，通过`CAND_ID`关联两个表
由于候选人和委员会的联系表中无候选人姓名，只有候选人ID（`CAND_ID`），所以需要通过`CAND_ID`从候选人表中获取到候选人姓名，最终得到候选人与委员会联系表`ccl`。

```ccl=pd.merge(ccl,candidates)```


#### 2.3 将候选人和捐赠人一一对应，通过`CMTE_ID`关联两个表
通过`CMTE_ID`将目前处理好的候选人和委员会关系表与人捐款档案表进行关联，得到候选人与捐赠人一一对应联系表`cil`。

+ 将候选人与委员会关系表ccl和个人捐赠数据表itcont合并，通过 CMTE_ID
```c_itcont =  pd.merge(ccl,itcont)```
+ 丢弃不需要的数据列
```c_itcont.drop(["CMTE_ID","CAND_ID"]axis="columns") ```

#### 2.4、数据探索与清洗

进过数据处理部分，我们获得了可用的数据集，现在我们可以利用调用`shape`属性查看数据的规模，调用`info`函数查看数据信息，调用`describe`函数查看数据分布。

```
# 查看数据规模 多少行 多少列
c_itcont.shape
c_itcont.info()
```

若加载失败可直接访问网页链接
![image](https://gitee.com/liu-guanting/Data-analysis-project/blob/main/photos/info.png)

通过上面的探索我们知道目前数据集的一些基本情况，目前数据总共有756205行，8列，总占用内存51.9+MB，`STATE`、`EMPLOYER`、`OCCUPATION`有缺失值，另外日期列目前为int64类型，需要进行转换为str类型。

```#空值处理，统一填充 NOT PROVIDED
c_itcont['STATE'].fillna('NOT PROVIDED',inplace=True)
c_itcont['EMPLOYER'].fillna('NOT PROVIDED',inplace=True)
c_itcont['OCCUPATION'].fillna('NOT PROVIDED',inplace=True)
```

```
#对日期TRANSACTION_DT列进行处理
c_itcont['TRANSACTION_DT'] = c_itcont['TRANSACTION_DT'] .astype(str)
#将日期格式改为年月日  7242020	
c_itcont['TRANSACTION_DT'] = [i[3:7]+i[0:3] for i in c_itcont['TRANSACTION_DT'] ]
```

+ 查看数据前3行
`c_itcont.head(3)`
![image](https://gitee.com/liu-guanting/Data-analysis-project/blob/main/photos/head(3).png)

+ 查看数据表中数据类型的列的数据分布情况
`c_itcont.describe()`
![image](https://gitee.com/liu-guanting/Data-analysis-project/blob/main/photos/describe.png)

# 3、数据分析

+ 将清洗后数据导入mysql

```
c_itcont_table=[]
for i in c_itcont.values:
    c_itcont_table.append(list(i))#将数据处理成列表嵌套列表的形式才能提交给mysql
cursor = connection.cursor()
sql = "create table c_itcont(CAND_NAME VARCHAR(50),CAND_PTY_AFFILIATION CHAR(5),NAME VARCHAR(50),STATE CHAR(20),EMPLOYER VARCHAR(50),OCCUPATION VARCHAR(50),TRANSACTION_AMT INT,TRANSACTION_DT VARCHAR(50))"
connection.ping(reconnect=True)#没有这一行可能会出错
cursor.execute(sql)
sql2 = "insert into c_itcont values(%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql2,c_itcont_table)
connection.commit()#将数据提交到mysql
cursor.close()
connection.close()
```




#### 以下分析为mysql的执行语句

+ 计算每个党派的所获得的捐款总额，然后排序，取前十位
```select CAND_PTY_AFFILIATION,sum(TRANSACTION_AMT) as total_AMT
from c_itcont
group by CAND_PTY_AFFILIATION
order by sum(TRANSACTION_AMT) desc
limit 10;
```
![image](https://raw.githubusercontent.com/lgt494371725/Data-analysis-project/master/photos/query1.png)

+ 计算每个总统候选人所获得的捐款总额，然后排序，取前十位
```
select CAND_NAME,sum(TRANSACTION_AMT) as total_AMT
from c_itcont
group by CAND_NAME
order by sum(TRANSACTION_AMT) desc
limit 10;
```
![image](https://raw.githubusercontent.com/lgt494371725/Data-analysis-project/master/photos/query2.png)

获得捐赠最多的党派有`DEM(民主党)`、`REP(共和党)`，分别对应`BIDEN, JOSEPH R JR(拜登)`和`TRUMP, DONALD J.(特朗普)`，从我们目前分析的2020.7.22-2020.8.20这一个月的数据来看，在选民的捐赠数据中拜登代表的民主党完胜特朗普代表的共和党，由于完整数据量过大，所以没有对所有数据进行汇总分析，因此也不能确定11月大选公布结果就一定是拜登当选

+ 查看不同职业的人捐款的总额，然后排序，取前十位
```
select OCCUPATION,sum(TRANSACTION_AMT) as total_AMT
from c_itcont
group by OCCUPATION
order by sum(TRANSACTION_AMT) desc
limit 10;
```
![image](https://raw.githubusercontent.com/lgt494371725/Data-analysis-project/master/photos/query3.png)

+ 查看每个职业捐款人的数量
```
select OCCUPATION,count(*) as `number`
from c_itcont
group by OCCUPATION
order by number desc
limit 10;
```
![image]https://raw.githubusercontent.com/lgt494371725/Data-analysis-project/master/photos/query4.png)

从捐款人的职业这个角度分析，我们会发现`NOT EMPLOYED(自由职业)`的总捐赠额是最多，通过查看每个职业捐赠的人数来看，我们就会发现是因为`NOT EMPLOYED(自由职业)`人数多的原因，另外退休人员捐款人数也特别多，所以捐款总数对应的也多，其他比如像：律师、创始人、医生、顾问、教授、主管这些高薪人才虽然捐款总人数少，但是捐款总金额也占据了很大比例。

+ 每个州获捐款的总额，然后排序，取前五位
```
select STATE,sum(TRANSACTION_AMT) as total_AMT
from c_itcont
group by state
order by sum(TRANSACTION_AMT) desc
limit 5;
```
![image](https://raw.githubusercontent.com/lgt494371725/Data-analysis-project/master/photos/query5.png)

+ 查看每个州捐款人的数量
```
select STATE,count(*) as number
from c_itcont
group by state
order by number desc
limit 5
```
![image](https://raw.githubusercontent.com/lgt494371725/Data-analysis-project/master/photos/query6.png)

最后查看每个州的捐款总金额，我们会发现`CA(加利福利亚)`、`NY(纽约)`、`FL(弗罗里达)`这几个州的捐款是最多的，在捐款人数上也是在Top端，另一方面也凸显出这些州的经济水平发达。
大家也可以通过数据查看下上面列举的高端职业在各州的分布情况，进行进一步的分析探索。

### 4、数据可视化
将以上的数据导入python有两种方法:
1 由于之前已经用pymysql建立了连接，可以通过python内输入sql语句来导入
2 在sql中依次执行语句并另存为csv文件，利用pd.read_csv方法读入
由于第二种方法行数更少且容易操作，采用第二种
+ 为了绘图，首先导入相关Python库


```
import matplotlib.pyplot as plt
#为了使matplotlib图形能够内联显示
%matplotlib inline
#读取数据，用dataset列表类型保存query1-6的数据，为保持顺序一致，填充了第一个元素
dataset=[0]
path=r'C:\Users\yukino\Desktop\query'
for i in range(1,7):
    dataset.append(pd.read_csv(path+str(i)+'.csv'))
```

#### 4.1 按州总捐款数和总捐款人数柱状图

```
# 各州总捐款数可视化
plt.bar(dataset[5]['STATE'],dataset[5]['total_AMT'])
plt.xlabel('STATE')
plt.ylabel('total_AMT')
plt.title("total contributions per state")
```
![image](https://raw.githubusercontent.com/lgt494371725/Data-analysis-project/master/photos/graph1.png)

#### 4.2 各州捐款总人数可视化

```
# 各州捐款总人数可视化，取前5个州的数据
plt.bar(dataset[6]['STATE'],dataset[6]['number'])
plt.xlabel('STATE')
plt.ylabel('amount')
plt.title("the total number of donations per state")
```
![image](https://raw.githubusercontent.com/lgt494371725/Data-analysis-project/master/photos/graph2.png)

#### 4.3 热门候选人拜登在总统候选人中获得的捐款总额占比

```
labels = dataset[2]["CAND_NAME"].str.split(',').str.get(0)[:5]
#由于名字过长，只取每个人的lastname，考虑到比例问题，只取候选人中前五名
sizes = dataset[2]["total_AMT"][:5]

plt.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
```
![image](https://raw.githubusercontent.com/lgt494371725/Data-analysis-project/master/photos/graph3.png)
