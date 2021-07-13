#引入文件
from scrapy.exceptions import DropItem
import json
import pymysql

class MyPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(host = "rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com",port=3306,user = "buaase2021",passwd = "buaase(2021)",db = "durian")
        self.cursor = self.connect.cursor()
        print("连接数据库成功")
        #打开文件
        self.file = open('data.json', 'a', encoding='utf-8')
    #该方法用于处理数据
    def process_item(self, item, spider):
        self.cursor.execute(
            """update  train_info2 set pass_city=%s where train_num =%s and pass_city =''
            """,  # 纯属python操作mysql知识，不熟悉请恶补
            (item['train_pass'],
            item['train_num'],
            ))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回

        #读取item中的数据
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        #写入文件
        self.file.write(line)
        #返回item
        return item
    #该方法在spider被开启时被调用。
    def open_spider(self, spider):
        pass
    #该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        pass