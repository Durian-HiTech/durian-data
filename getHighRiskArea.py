from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import json
import os
from urllib import parse
from datetime import datetime
import time
import sched
import pymysql

schedule = sched.scheduler(time.time, time.sleep)

def Action(inc):
    url ='http://www.gd.gov.cn/gdywdt/zwzt/yqfk/content/post_3021711.html'
    data = urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')
    result = soup.find_all("div", class_='zw')
    print(result)
    schedule.enter(inc, 0, Action, (inc,))

def timeAct(inc=60):
    schedule.enter(0,0,Action,(inc,))
    schedule.run()

if __name__=="__main__":
    timeAct(30) #18000 5小时