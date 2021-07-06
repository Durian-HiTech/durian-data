import time
import os

while True:
    file = open("log.txt","r")
    day =[]
    day = file.readlines()
    now = time.strftime('%Y-%m-%d',time.localtime(time.time()))+"\n"
    file.close()
    #当今天不在日志中，才说明数据为被爬取过
    if now not in day:
        os.system("scrapy crawl MySpider")
        #完成爬取后，将今天写入日志
        file = open("log.txt", "a")
        file.write(now)
        file.close()
    else :
        print("We've already got the data.")
    time.sleep(86400)  # 每隔一天运行一次 24*60*60=86400s