import requests
import json
import os
from urllib import parse
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
    totalPerHundred = {}
    dailyPerMillion = {}

    CountryList = []

    AtLastCountryList = []

    data = json.load(open("all_minified.json","r",encoding = "utf-8"))
    for itemT in data:
        if itemT in [ 'confirmedCount', 'curedCount', 'deadCount']:
            continue
        CountryList.append(data[itemT]["ENGLISH"])

    ####vaccine 
    URL = 'https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=all&fullData=true'
    response = requests.get(URL, headers=headers)

    type1 = 'vaccine'
    OrResult[type1]={}
    totalPerHundred[type1] = {}
    dailyPerMillion[type1] = {}
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
        
        AtLastCountryList.append(countryname)
        
        for DArea in term['timeline']:
            date = DArea["date"]
        # for date in term['timeline']:
            if date not in OrResult[type1]:
                OrResult[type1][date] = {}
            if countryname not in OrResult[type1][date]:
                OrResult[type1][date][countryname] = {}
            # OrResult[type1][date][countryname] = term['timeline'][date]
            OrResult[type1][date][countryname] = DArea["total"]

            if date not in totalPerHundred[type1]:
                totalPerHundred[type1][date] = {}
            if countryname not in totalPerHundred[type1][date]:
                totalPerHundred[type1][date][countryname] = {}
            # totalPerHundred[type1][date][countryname] = term['timeline'][date]
            totalPerHundred[type1][date][countryname] = DArea["totalPerHundred"]

            if date not in dailyPerMillion[type1]:
                dailyPerMillion[type1][date] = {}
            if countryname not in dailyPerMillion[type1][date]:
                dailyPerMillion[type1][date][countryname] = {}
            # dailyPerMillion[type1][date][countryname] = term['timeline'][date]
            dailyPerMillion[type1][date][countryname] = DArea["dailyPerMillion"]

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
            cursor.execute('create table Covid_%s(date datetime,country_name varchar(1000),info int,totalPerHundred int,dailyPerMillion int,primary key(date,country_name))'%(type1))
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
                    cursor.execute('insert into Covid_%s(date,country_name,info,totalPerHundred,dailyPerMillion) values (\'20%s-%s-%s\',\'%s\',%d,%d,%d)'%(type1,day[2],day[0],day[1],countryname,OrResult[type1][date][countryname],totalPerHundred[type1][date][countryname],dailyPerMillion[type1][date][countryname]))
                    conn.commit()
                except:
                    print('插入错误',type1,countryname,date)      
                    

    for date in data["全球"]["confirmedCount"]:
        for countryname in AtLastCountryList:
            print(date,countryname)
            try:
                cursor.execute('insert into Covid_vaccine(date,country_name,info,totalPerHundred,dailyPerMillion) values (\'%s\',\'%s\',%d,%d,%d)'%(date,countryname,0,0,0))
                conn.commit()
            except:
                print('插入错误',"vaccine0",countryname,date)                

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
        