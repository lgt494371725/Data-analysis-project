-- 计算每个党派的所获得的捐款总额，然后排序，取前十位
select CAND_PTY_AFFILIATION,sum(TRANSACTION_AMT) as total_AMT
from c_itcont
group by CAND_PTY_AFFILIATION
order by sum(TRANSACTION_AMT) desc
limit 10;

-- 计算每个总统候选人所获得的捐款总额，然后排序，取前十位

select CAND_NAME,sum(TRANSACTION_AMT) as total_AMT
from c_itcont
group by CAND_NAME
order by sum(TRANSACTION_AMT) desc
limit 10;

-- 查看不同职业的人捐款的总额，然后排序，取前十位
select OCCUPATION,sum(TRANSACTION_AMT) as total_AMT
from c_itcont
group by OCCUPATION
order by sum(TRANSACTION_AMT) desc
limit 10;

-- 查看每个职业的捐款人数
select OCCUPATION,count(*) as `number`
from c_itcont
group by OCCUPATION
order by number desc
limit 10;
-- 每个州获捐款的总额，然后排序，取前五位
select STATE,sum(TRANSACTION_AMT) as total_AMT
from c_itcont
group by state
order by sum(TRANSACTION_AMT) desc
limit 5;

-- 查看每个州捐款人的数量
select STATE,count(*) as number
from c_itcont
group by state
order by number desc
limit 5






