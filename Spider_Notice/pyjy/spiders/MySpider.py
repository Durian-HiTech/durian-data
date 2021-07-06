import scrapy
from pyjy.items import PyjyItem
import json
import time
import requests
import re
import datetime
class MySpider(scrapy.Spider):

    name = "MySpider"
    # allowed_domains = ["www.gov.cn"]
    # start_urls = [
    #     # 'http://www.gov.cn/zhengce/zhengceku/2021-04/13/content_5599299.htm'
    # ]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': 'http://www.gov.cn/fuwu/zt/yqfwzq/yqfkblt.htm',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55',
        },
    }

    def start_requests(self):
        requests = []
        f = open('record.json')
        for x in f.readlines():
            print(eval(x))
            request = scrapy.Request(eval(x), method='GET')
            requests.append(request)
        # request = scrapy.Request("http://www.gov.cn/zhengce/zhengceku/2020-04/23/content_5505441.htm", method='GET')
        # requests.append(request)
        return requests


    def parse(self,response):
        content=[]
        tit=[]

        notices_title =response.xpath('//div[@class="share-title"]/text()').extract()
        content=response.xpath('//div[@class="pages_content"]/p/text()').extract()
        notices_time = response.xpath('//div[@class="pages-date"]/text()').extract()
        notices_content=""
        for i in content:
            notices_content += i
        # notices_title = tit[0]
        # notices_time = tit[2]
        
        #print("!!!!!!!!!!!!")
        
        pattern=r"肺炎疫情最新情况"
        matchObj = re.search(pattern,notices_title[0])
        if matchObj :
            
            print(notices_title[0])
            print(notices_time[0])
            print(notices_content)
            item = PyjyItem()
            item["title"]=notices_title[0]
            item["content"]=notices_content
            item["time"]=datetime.datetime.strptime(notices_time[0].strip()+":00", "%Y-%m-%d %H:%M:%S")
            yield item
        #print("eeeeeeeeennnnnnnndddddddddd")
        # print(notices_time)
        
        

