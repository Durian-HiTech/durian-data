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

    countryList = ['China','India']
    '''
    countryList = []
    countryURL = 'https://disease.sh/v3/covid-19/countries'
    response = requests.get(countryURL, headers=headers)
    for i in json.loads(response.content):
        countryList.append(i['country'])
    '''
    ResultList = {}
    OrResult = {}

    for countryname in countryList:
        URL = parse.urljoin(url,countryname)
        URL = parse.urljoin(URL,datecontrol) # 从2020年开始的日期
        print(URL)
        
        response = requests.get(URL, headers=headers)

        if "timeline"not in json.loads(response.content):
            print("Country not found or doesn't have any historical data")
            continue

        for type1 in json.loads(response.content)["timeline"]:
            for date in json.loads(response.content)["timeline"][type1]:
                if date not in OrResult:
                    OrResult[date]={}
                if countryname not in OrResult[date]:
                    OrResult[date][countryname] = {}
                OrResult[date][countryname][type1] = (int)(json.loads(response.content)["timeline"][type1][date])
        
    
    for date in OrResult:
        ResultList[date] = []
        for countryname in OrResult[date]:
            dict1 = {}
            dict1['name'] = countryname
            dict1['values'] = OrResult[date][countryname]
            ResultList[date].append(dict1)
    
    file = open("./Result2.json",'w')
    print(json.dumps(ResultList),file=file)
    file.close()

    ##### 数据库操作
    
    conn = pymysql.connect(
        host="rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com",
        port=3306,
        user="buaase2021",password="buaase(2021)",
        database="durian",
        charset="utf8")

    cursor = conn.cursor() 

    try:
        cursor.execute('create table Covid_Times(date varchar(255) primary key,info text)')
    except:
        print('数据库已存在！')

    for date in ResultList.keys():
        # print(json.dumps(ResultList[date]),type(json.dumps(ResultList[date])))
        print(date)
        try:
            cursor.execute('insert into Covid_Times(date,info) values (\'%s\',\'%s\')'%(date,json.dumps(ResultList[date])))
            conn.commit()
        except:
            print('插入错误')     


    cursor.close()
    conn.close()

    ##### 数据库操作  
    # print("hello: %s , %s "%("5/1/12","hello:1/3"))
    #insert into Covid_Times(date,info) values ('5/1/21','5/1/21')

    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # schedule.enter(inc, 0, Action, (inc,))

def timeAct(inc=60):
    schedule.enter(0,0,Action,(inc,))
    schedule.run()

if __name__=="__main__":
    timeAct(10) #18000 5小时
        