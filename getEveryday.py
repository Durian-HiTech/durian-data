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
                '''       
    for date in OrResult:
        ResultList[date] = []
        for countryname in OrResult[date]:
            dict1 = {}
            dict1['name'] = countryname
            dict1['values'] = OrResult[date][countryname]
            ResultList[date].append(dict1)
            '''
    
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

    try:
        cursor.execute('drop table Covid_Cases')
        cursor.execute('drop table Covid_Deaths')
        cursor.execute('drop table Covid_Recovered')
        print('数据库已删除')
    except:
        print('数据库不存在！')

    try:
        cursor.execute('create table Covid_cases(date varchar(255),countryname varchar(255),info int,primary key(date,countryname))')
        cursor.execute('create table Covid_Deaths(date varchar(255),countryname varchar(255),info int,primary key(date,countryname))')
        cursor.execute('create table Covid_Recovered(date varchar(255),countryname varchar(255),info int,primary key(date,countryname))')
    except:
        print('数据库已存在！')

    for date in OrResult['cases']:
        print(date,'cases')
        for countryname in OrResult['cases'][date]:
            print(date,countryname,'cases')
            try:
                cursor.execute('insert into Covid_Cases(date,countryname,info) values (\'%s\',\'%s\',%d)'%(date,countryname,OrResult['cases'][date][countryname]))
                conn.commit()
            except:
                print('插入错误1')

    for date in OrResult['deaths']:
        print(date,'deaths')
        for countryname in OrResult['deaths'][date]:
            print(date,countryname,'deaths')
            try:
                cursor.execute('insert into Covid_deaths(date,countryname,info) values (\'%s\',\'%s\',%d)'%(date,countryname,OrResult['deaths'][date][countryname]))
                conn.commit()
            except:
                print('插入错误2')
    
    for date in OrResult['recovered']:
        print(date,'recovered')
        for countryname in OrResult['recovered'][date]:
            print(date,countryname,'recovered')
            try:
                cursor.execute('insert into Covid_recovered(date,countryname,info) values (\'%s\',\'%s\',%d)'%(date,countryname,OrResult['recovered'][date][countryname]))
                conn.commit()
            except:
                print('插入错误3')
    '''
    for date in ResultList['cases'].keys():
        # print(json.dumps(ResultList[date]),type(json.dumps(ResultList[date])))
        print(date,"cases")
        try:
            cursor.execute('insert into Covid_Cases(date,info) values (\'%s\',\'%s\')'%(date,json.dumps(ResultList['cases'][date])))
            conn.commit()
        except:
            print('插入错误')     

    for date in ResultList['deaths'].keys():
        # print(json.dumps(ResultList[date]),type(json.dumps(ResultList[date])))
        print(date,"deaths")
        try:
            cursor.execute('insert into Covid_deaths(date,info) values (\'%s\',\'%s\')'%(date,json.dumps(ResultList['deaths'][date])))
            conn.commit()
        except:
            print('插入错误')     

    
    for date in ResultList['recovered'].keys():
        # print(json.dumps(ResultList[date]),type(json.dumps(ResultList[date])))
        print(date,"recovered")
        try:
            cursor.execute('insert into Covid_Recovered(date,info) values (\'%s\',\'%s\')'%(date,json.dumps(ResultList['recovered'][date])))
            conn.commit()
        except:
            print('插入错误')   
    '''

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
        