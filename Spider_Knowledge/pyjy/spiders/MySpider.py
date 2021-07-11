import scrapy
from pyjy.items import PyjyItem
import json
import time
import requests
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
        news_title =response.xpath('//title/text()').extract()
        content=response.xpath('//div[@class="pages_content"]/p/text()').extract()
        # for selector in response.xpath('//div[@class="pages_content"]//p'):
        #     print(selector.xpath('/text()').extract())
        #     title += selector.xpath('/text()').extract()
        # data=""
        # for i in title:
        #     data += i.data
        # tit = response.xpath('//div[@class="pages_content"]/p/span/text()').extract()
        #print(tit)
        news_content=""
        for i in content:
            news_content += i
        # news_title = tit[0]
        # news_time = tit[2]
        print(news_content)
        print(news_title) #不能保证 time 和title 匹配正确
        # print(news_time)
        item = PyjyItem()
        item["title"]=news_title
        item["content"]=news_content
        yield item
        

