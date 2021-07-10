import requests
import json
import os
from urllib import parse
from datetime import datetime
import time
import sched
import pymysql

### 认证 vaccine 补〇

schedule = sched.scheduler(time.time, time.sleep)

def Action(inc):
    headers = {
        'content-type': 'application/json',
    }

    url = 'https://disease.sh/v3/covid-19/historical/'
    datecontrol = '?lastdays=all'

    countryList = ['China']
    #countryList = ['China','India']
    #countryList = ['China','India','Afghanistan','Argentina','Australia','Belgium']
    '''
    countryList = []
    countryURL = 'https://disease.sh/v3/covid-19/countries'
    response = requests.get(countryURL, headers=headers)
    for i in json.loads(response.content):
        countryList.append(i['country'])
    '''
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
    ####vaccine 
    URL = 'https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=all'
    response = requests.get(URL, headers=headers)

    type1 = 'vaccine'
    OrResult[type1]={}
    for term in json.loads(response.content):
        countryname = term['country']
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
    try:
        cursor.execute('create table Covid_%s(date datetime,country_name varchar(255),info int,primary key(date,country_name))'%("test"))
        print('数据库创建',type1)
    except:
        print('数据库已存在！',type1)

    for date in OrResult["cases"]:
        if date=="12/1/20":
            break
        day = date.split('/')
        for countryname in OrResult["vaccine"]["12/1/20"]:
            try:
                cursor.execute('insert into Covid_%s(date,country_name,info) values (\'20%s-%s-%s\',\'%s\',%d)'%("vaccine",day[2],day[0],day[1],countryname,0))
                conn.commit()
            except:
                print("插入失败",date,countryname)
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
        