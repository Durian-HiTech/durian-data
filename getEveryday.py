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

def Action(inc):
    headers = {
        'content-type': 'application/json',
    }

    url = 'https://disease.sh/v3/covid-19/historical/'
    datecontrol = '?lastdays=all'

    #countryList = ['China','India']
    #countryList = ['China','India','Afghanistan','Argentina','Australia','Belgium']
    
    countryList = []
    countryURL = 'https://disease.sh/v3/covid-19/countries'
    response = requests.get(countryURL, headers=headers)
    for i in json.loads(response.content):
        countryList.append(i['country'])
    
    ResultList = {}
    CasesList = {}
    DeathsList = {}
    RecoveredList = {}
    OrResult = {}

    for countryname in countryList:
        URL = parse.urljoin(url,countryname)
        URL = parse.urljoin(URL,datecontrol) # 从2020年开始的日期
        print(countryname)
        
        response = requests.get(URL, headers=headers)

        if "timeline"not in json.loads(response.content):
            print("Country not found or doesn't have any historical data")
            continue

        for type1 in json.loads(response.content)["timeline"]:
            if type1 not in OrResult:
                OrResult[type1] = {}
            for date in json.loads(response.content)["timeline"][type1]:
                if date not in OrResult[type1]:
                    OrResult[type1][date]={}
                if countryname not in OrResult[type1][date]:
                    OrResult[type1][date][countryname] = {}
                OrResult[type1][date][countryname] = (int)(json.loads(response.content)["timeline"][type1][date])
        
    for type1 in OrResult:
        ResultList[type1] = {}
        for date in OrResult[type1]:
            ResultList[type1][date] = []
            for countryname in OrResult[type1][date]:
                dict1 = {}
                dict1['name'] = countryname
                dict1['values'] = OrResult[type1][date][countryname]
                ResultList[type1][date].append(dict1)         

    file = open("./Result3.json",'w')
    print(json.dumps(ResultList),file=file)
    file.close()

    ##### 数据库操作
    
    conn = pymysql.connect(
        host="rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com",
        port=3306,
        user="",password="",
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
            cursor.execute('create table Covid_%s(date datetime,country_name varchar(255),info int,primary key(date,country_name))'%(type1))
            print('数据库创建',type1)
        except:
            print('数据库已存在！',type1)
    
    
    for type1 in OrResult:
        print(type1)
        for date in OrResult[type1]:
            day = date.split('/')
            # print(date)
            for countryname in OrResult[type1][date]:
                # print(date,countryname,type1)
                print("\'20%s-%s-%s\'  \'%s\',%s"%(day[2],day[0],day[1],countryname,type1))
                try:
                    cursor.execute('insert into Covid_%s(date,country_name,info) values (\'20%s-%s-%s\',\'%s\',%d)'%(type1,day[2],day[0],day[1],countryname,OrResult[type1][date][countryname]))
                    conn.commit()
                except:
                    print('插入错误',type1)      
                        

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
        