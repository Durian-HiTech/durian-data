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
    #     'https://huoche.tuniu.com/tn?r=train/trainTicket/getTickets&primary%5BdepartureDate%5D=2021-7-12&primary%5BdepartureCityName%5D=大理&primary%5BarrivalCityName%5D=贵阳'
    #     # 'http://www.gov.cn/zhengce/zhengceku/2021-04/13/content_5599299.htm'
    # ]

    # custom_settings = {
    #     "DEFAULT_REQUEST_HEADERS": {
    #         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #         'referer': 'http://www.gov.cn/fuwu/zt/yqfwzq/yqfkblt.htm',
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55',
    #     },
    # }

    def start_requests(self):
        requests = []
        start=[]
        end=[]
        train=[]
        with open('train_info.json') as f:
            trainlist = json.load(f)
        for i in trainlist:
            train.append(i['train_num'])
            # start.append(i['city'])
            # end.append(i['city'])
        # print(train)
        # print("aa")
        for i in train:
            #print(i)
            url = "https://huoche.tuniu.com/tn?r=train/trainTicket/getTrainInfo&id="+i+"&departDate=2021-07-14"
            #url = "https://huoche.tuniu.com/tn?r=train/trainTicket/getTickets&primary%5BdepartureDate%5D=2021-7-14&primary%5BdepartureCityName%5D="+i+"&primary%5BarrivalCityName%5D="+j
            
            request = scrapy.Request(url, method='GET')
            #time.sleep(0.002)
            #print(request.data)
            requests.append(request)
            # request = scrapy.Request("http://www.gov.cn/zhengce/zhengceku/2020-04/23/content_5505441.htm", method='GET')
            # requests.append(request)
        return requests


    def parse(self,response):
        train_pass = []
        
        ff = json.loads(response.body.decode())
        
        train_id= ff['trainInfo']['id']
        #print(json.loads(response.body.decode()))
        # lo = json.loads(ff)
        
        for i in ff['stationList']:
            # print("车号:",i['trainNum'],
            #     " 始发地:",i['departureCityName'],
            #     " 终点:",i['arrivalCityName'],
            #     " 始发站:",i['departStationName'],
            #     " 终点站:",i['destStationName'],
            #     " 日期:",i['trainStartDate'],
            #     " 出发时间:",i['departDepartTime'],
            #     " 到达时间:",i['destArriveTime'],
            #     " 用时:",i['durationStr'])
            if len(i['cityName'] )!= 0:
                train_pass.append(i['cityName'])
        print(train_id)
        print(train_pass)
        item = PyjyItem()
        item["train_num"] = train_id
        item["train_pass"] = ','.join(train_pass)
        yield item
                    
                # temp_dict = {
                #     'train_id':i['trainNum'],
                #     'departure_city':i['departureCityName'],
                #     'arrival_city':i['arrivalCityName'],
                #     'departure_station':i['departStationName'],
                #     'arrival_station':i['destStationName'],
                #     'train_start_date':i['trainStartDate'],
                #     'departure_time':i['departDepartTime'],
                #     'arrival_time':i['destArriveTime'],
                #     'duration_time':i['durationStr'],
                #     'pass_city':[]
                # }
                # train.append(temp_dict)
            
        # except:
        #     pass
        # new_list =[]
        # try:
        #     with open('火json数据.json', 'r') as f:
        #         new_list = json.load(f)
        #         #print(new_list)
        #         new_list.append(train) # 依据列表的append对文件进行追加

        # except:
        #     pass
        # with open( '火json数据.json', 'w') as fp:
        #     fp.write( json.dumps(new_list,ensure_ascii=False))
            
        # notices_title =response.xpath('//div[@class="share-title"]/text()').extract()
        # content=response.xpath('//div[@class="pages_content"]/p/text()').extract()
        # notices_time = response.xpath('//div[@class="pages-date"]/text()').extract()
        # notices_content=""
        # for i in content:
        #     notices_content += i
        # notices_title = tit[0]
        # notices_time = tit[2]
        
        #print("!!!!!!!!!!!!")
        
        # pattern=r"肺炎疫情最新情况"
        # matchObj = re.search(pattern,notices_title[0])
        # if matchObj :
            
        #     print(notices_title[0])
        #     print(notices_time[0])
        #     print(notices_content)
        
    
