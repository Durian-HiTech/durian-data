from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import json
class LinkSpider(CrawlSpider):
    name = 'LinkSpider'
    allowed_domains = ['www.gov.cn']

    start_urls = ['http://www.gov.cn/fuwu/zt/yqfwzq/yqfkblt.htm']

    # custom_settings = {
    #     "DEFAULT_REQUEST_HEADERS": {
    #         # 'HTTPERROR_ALLOWED_CODES' : [412],
    #         'Cookie': 'sVoELocvxVW0S=5gzGO8lfWV2KSu5QCk4QJosLWC3rlagA8b.mbBIbphM8IgnLzqB9azc5yufhcIjWv0VEkSprPVzJbzt6Je.OWLA; yfx_c_g_u_id_10006654=_ck21070216014219710350299561137; _gscu_2059686908=25216302g63xjr12; yfx_key_10006654=; yfx_mr_10006654=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10006654=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; insert_cookie=97324480; yfx_f_l_v_t_10006654=f_t_1625212902971__r_t_1625968941179__v_t_1625987583559__r_c_2; security_session_verify=285fb39a72d56ac08a339ffaf745d73d; sVoELocvxVW0T=53ijRHDkjbIZqqqm_2DN20aDbaxnySDb5s_9AMgfo0KFu_Z1rTVignb2Z1uLDxRfadS5HEP5IKAC39xtFooUcdshBUUn0.bBz3XacopKpsO7rjx_vM6FrL2lv_MqwEQ1mnckYiQsHGwK3U_7G5CEUpBhJqyK8r73qixRB8QpkqV1.aFRlXXWcElNJPEyXkB.o.ZfBJlFZPbgLQOumvl3evF7WKDkKky9mj5wtNQvMi.OcYccCrZT9dDdKxuNykrVKrQHFxukkOTiJqQewmW8LP3D2UZBC5B044vnJTVwFuSzCVyXGts_dV48unOckKAfgwGqV9dISPOzpd9e2l_4R9T',
    #         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #         'referer': 'http://www.nhc.gov.cn/xcs/kpzs/list_gzbd_6.shtml',
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    #     },
    # }

    rules = (Rule(
        LinkExtractor(allow=('^http://www.gov.cn/fuwu/.')),
        callback='parse_item',
        follow=True),)
    
    # custom_settings = {
    #     "DEFAULT_REQUEST_HEADERS": {
    #         # 'HTTPERROR_ALLOWED_CODES' : [412],
    #         'referer': 'http://www.gov.cn/',
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    #     },
    # }

    def parse_item(self, response):

        # link = LinkExtractor(allow=('^http://www.gov.cn/fuwu/.'))
        # links = link.extract_links(response)
        
        # for x in links:
        #     print(x)

        print(response.url)
        with open("record.json", "a") as f:

            # json.dump(response.url, f)

            line = json.dumps(response.url) + "\n"
            # 写入文件
            f.write(line)

        # print("加载入文件完成...")