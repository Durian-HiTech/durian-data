import requests
import json
import os
from urllib import parse
from datetime import datetime
import time
import sched
import pymysql

### 认证: Global 疫苗数据

headers = {
    'content-type': 'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
}

url = 'https://disease.sh/v3/covid-19/vaccine/coverage?lastdays=all&fullData=true'

response = requests.get(url, headers=headers)

data = json.load(open("all_minified.json","r",encoding = "utf-8"))

print(json.loads(response.content)[0])

##### 数据库操作
    
conn = pymysql.connect(
    host="rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com",
    port=3306,
    user="buaase2021",password="buaase(2021)",
    database="durian",
    charset="utf8")

cursor = conn.cursor() 

try:
    cursor.execute('drop table Covid_Global_vaccine')
    print('数据库已删除')
except:
    print('数据库不存在！')


try:
    cursor.execute('create table Covid_Global_vaccine(date datetime,total bigint,daily bigint,totalPerHundred bigint,dailyPerMillion bigint,primary key(date))')
    print('数据库创建')
except:
    print('数据库已存在！')
    
for term in json.loads(response.content):
    date = term["date"]
    day = date.split('/')
    print("20%s-%s-%s"%(day[2],day[0],day[1]))
    try:
        cursor.execute('insert into Covid_Global_vaccine(date,total,daily,totalPerHundred,dailyPerMillion) values (\'20%s-%s-%s\',%d,%d,%d,%d)'%(day[2],day[0],day[1],term["total"],term["daily"],term["totalPerHundred"],term["dailyPerMillion"]))
        conn.commit()
    except:
        print('插入错误',date)  
        print(term["total"],term["daily"],term["totalPerHundred"],term["dailyPerMillion"])   


for date in data["全球"]["confirmedCount"]:
    print("补0",date)
    try:
        cursor.execute('insert into Covid_Global_vaccine(date,total,daily,totalPerHundred,dailyPerMillion) values (\'%s\',%d,%d,%d,%d)'%(date,0,0,0,0))
        conn.commit()
    except:
        print('补0 插入错误',date)                

cursor.close()
conn.close()