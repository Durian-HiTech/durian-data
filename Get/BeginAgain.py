import requests
import json
import os
from urllib import parse
from datetime import datetime
import time
import sched
import pymysql

###本程序是从all_minified中获取数据的办法

### 读入信息
data = json.load(open("all_minified.json","r",encoding = "utf-8"))
typeType = ["cases","deaths","recovered"]
typeType2 = ["confirmedCount", "deadCount", "curedCount"]
###

### 处理信息

###

### 数据库操作
conn = pymysql.connect(
    host="rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com",
    port=3306,
    user="",password="",
    database="durian",
    charset="utf8")

cursor = conn.cursor() 

for type1 in typeType:
    '''
    try:
        cursor.execute('drop table Covid_New_%s'%type1)
    except:
        print("删除失败")
    '''
    try:
        cursor.execute('create table Covid_New_%s(date datetime,country_name varchar(1000),info int,primary key(date,country_name))'%type1)
    except:
        print("创建失败")

for countryname in data:
    if countryname in ["confirmedCount", "deadCount", "curedCount","ENGLISH"]:
        continue
    ### 中国特判
    if countryname == "中国":
        for countrysmall in data[countryname]:
            if countrysmall in ["confirmedCount", "deadCount", "curedCount","ENGLISH"]:
                continue
            
            for date in data["全球"]["confirmedCount"]:
                if date not in data[countryname][countrysmall]["confirmedCount"]:
                    print(date,countrysmall,0,"confirmed")
                    try:
                        if countrysmall == "中国大陆":
                            cursor.execute('insert into Covid_New_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                        else:
                            cursor.execute('insert into Covid_New_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],0))
                        conn.commit()   
                    except:
                        print("插入失败")
                else:
                    print(date,countrysmall,data[countryname]["confirmedCount"][date],"confirmed")
                    try:
                        if countrysmall == "中国大陆":
                            cursor.execute('insert into Covid_New_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname][countrysmall]["confirmedCount"][date]))
                        else:
                            cursor.execute('insert into Covid_New_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],data[countryname][countrysmall]["confirmedCount"][date]))
                        conn.commit()   
                    except:
                        print("插入失败")     
            

            for date in data["全球"]["confirmedCount"]:
                if date not in data[countryname][countrysmall]["deadCount"]:
                    print(date,countrysmall,0,"dead")
                    try:
                        if countrysmall == "中国大陆":
                            cursor.execute('insert into Covid_New_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                        else:
                            cursor.execute('insert into Covid_New_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],0))
                        conn.commit()   
                    except:
                        print("插入失败")
                else:
                    print(date,countrysmall,data[countryname]["deadCount"][date],"dead")
                    try:
                        if countrysmall == "中国大陆":
                            cursor.execute('insert into Covid_New_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname][countrysmall]["deadCount"][date]))
                        else:
                            cursor.execute('insert into Covid_New_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],data[countryname][countrysmall]["deadCount"][date]))
                        conn.commit()   
                    except:
                        print("插入失败")       

            for date in data["全球"]["confirmedCount"]:
                if date not in data[countryname][countrysmall]["curedCount"]:
                    print(date,countrysmall,0,"cured")
                    try:
                        if countrysmall == "中国大陆":
                            cursor.execute('insert into Covid_New_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                        else:
                            cursor.execute('insert into Covid_New_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],0))
                        conn.commit()   
                    except:
                        print("插入失败")
                else:
                    print(date,countrysmall,data[countryname]["curedCount"][date],"cured")
                    try:
                        if countrysmall == "中国大陆":
                            cursor.execute('insert into Covid_New_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname][countrysmall]["curedCount"][date]))
                        else:
                            cursor.execute('insert into Covid_New_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname][countrysmall]["ENGLISH"],data[countryname][countrysmall]["curedCount"][date]))
                        conn.commit()   
                    except:
                        print("插入失败")       
        continue
    ###
'''

    for date in data["全球"]["confirmedCount"]:
        # print(data[countryname]["ENGLISH"])
        if date not in data[countryname]["confirmedCount"]:
            print(date,countryname,0,"confirmed")
            try:
                cursor.execute('insert into Covid_New_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                conn.commit()   
            except:
                print("插入失败")
        else:
            print(date,countryname,data[countryname]["confirmedCount"][date],"confirmed")
            try:
                cursor.execute('insert into Covid_New_cases(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname]["confirmedCount"][date]))
                conn.commit()   
            except:
                print("插入失败")    
       

    for date in data["全球"]["confirmedCount"]:
        if date not in data[countryname]["deadCount"]:
            print(date,countryname,0,"dead")
            try:
                cursor.execute('insert into Covid_New_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                conn.commit()   
            except:
                print("插入失败")
        else:
            print(date,countryname,data[countryname]["deadCount"][date],"dead")
            try:
                cursor.execute('insert into Covid_New_deaths(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname]["deadCount"][date]))
                conn.commit()   
            except:
                print("插入失败")     

    for date in data["全球"]["confirmedCount"]:
        if date not in data[countryname]["curedCount"]:
            print(date,countryname,0,"cured")
            try:
                cursor.execute('insert into Covid_New_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],0))
                conn.commit()   
            except:
                print("插入失败")
        else:
            print(date,countryname,data[countryname]["curedCount"][date],"cured")
            try:
                cursor.execute('insert into Covid_New_recovered(date,country_name,info) values (\'%s\',\'%s\',%d)'%(date,data[countryname]["ENGLISH"],data[countryname]["curedCount"][date]))
                conn.commit()   
            except:
                print("插入失败")    
'''

cursor.close()
conn.close()               
        
###
'''
print(data["英国"].keys())
for date in data["英国"]["confirmedCount"]:
    print(date,data["英国"]["confirmedCount"][date])
    break
'''