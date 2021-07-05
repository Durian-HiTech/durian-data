from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import json
class LinkSpider(CrawlSpider):
    name = 'LinkSpider'
    allowed_domains = ['www.gov.cn']
    start_urls = ['http://www.gov.cn/fuwu/zt/yqfwzq/yqfkblt.htm#1']

    rules = (Rule(
        LinkExtractor(allow=('^http://www.gov.cn/zhengce/zhengceku/.')),
        callback='parse_item',
        follow=True),)

    def parse_item(self, response):
        print(response.url)
        with open("record.json", "a") as f:

            # json.dump(response.url, f)

            line = json.dumps(response.url) + "\n"
            # 写入文件
            f.write(line)

        print("加载入文件完成...")