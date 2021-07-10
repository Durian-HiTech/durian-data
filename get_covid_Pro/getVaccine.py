import requests
import json
import os
from urllib import parse
# from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import time
import sched
import pymysql

schedule = sched.scheduler(time.time, time.sleep)

### 认证:获取疫苗数据

def Action(inc):
    headers = {
        'content-type': 'application/json',
    }


    ResultList = {}
    CasesList = {}
    DeathsList = {}
    RecoveredList = {}
    OrResult = {}

    CountryList = []

    data = json.load(open("all_minified.json","r",encoding = "utf-8"))
    for itemT in data:
        if itemT in [ 'confirmedCount', 'curedCount', 'deadCount']:
            continue
        CountryList.append(data[itemT]["ENGLISH"])

    ####vaccine 
    URL = 'https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=all'
    response = requests.get(URL, headers=headers)

    type1 = 'vaccine'
    OrResult[type1]={}
    for term in json.loads(response.content):
        countryname = term['country']
        if countryname == "UK":
            countryname = "United Kingdom"
        if countryname == "USA":
            countryname = "United States of America"
        if countryname == "UAE":
            countryname = "United Arab Emirates"
        if countryname == "S. Korea":
            countryname = "South Korea"
        
        if countryname not in CountryList:
            continue
        
        for date in term['timeline']:
            if date not in OrResult[type1]:
                OrResult[type1][date] = {}
            if countryname not in OrResult[type1][date]:
                OrResult[type1][date][countryname] = {}
            OrResult[type1][date][countryname] = term['timeline'][date]

    ####    
    

    ##### 数据库操作
    
    conn = pymysql.connect(
        host="rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com",
        port=3306,
        user="buaase2021",password="buaase(2021)",
        database="durian",
        charset="utf8")

    cursor = conn.cursor() 

    for type1 in OrResult:
        try:
            cursor.execute('drop table Covid_%s'%(type1))
            print('数据库已删除',type1)
        except:
            print('数据库不存在！',type1)

    for type1 in OrResult:
        try:
            cursor.execute('create table Covid_%s(date datetime,country_name varchar(1000),info int,primary key(date,country_name))'%(type1))
            print('数据库创建',type1)
        except:
            print('数据库已存在！',type1)
    
    
    for type1 in OrResult:
        print(type1)
        for date in OrResult[type1]:
            day = date.split('/')
            # print(date)
            print("20%s-%s-%s"%(day[2],day[0],day[1]))
            for countryname in OrResult[type1][date]:
                # print(date,countryname,type1)
                # print("\'20%s-%s-%s\'  \'%s\',%s"%(day[2],day[0],day[1],countryname,type1))
                try:
                    cursor.execute('insert into Covid_%s(date,country_name,info) values (\'20%s-%s-%s\',\'%s\',%d)'%(type1,day[2],day[0],day[1],countryname,OrResult[type1][date][countryname]))
                    conn.commit()
                except:
                    print('插入错误',type1,countryname,date)      
                        

    cursor.close()
    conn.close()

    ##### 数据库操作  

    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # schedule.enter(inc, 0, Action, (inc,))

def timeAct(inc=60):
    schedule.enter(0,0,Action,(inc,))
    schedule.run()

if __name__=="__main__":
    timeAct(300) #18000 5小时
        