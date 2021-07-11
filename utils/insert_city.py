import json
import pymysql

conn = pymysql.connect( host='rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com',
                        port=3306,
                        user='buaase2021',
                        passwd='buaase(2021)',
                        charset='utf8',
                        db='durian'
                        )

cursor = conn.cursor()

with open('./utils/CityList.json','r',encoding='utf8') as f:
    city_dict = json.load(f)
# print(city_dict)
# print(city_dict['data'])

for city in city_dict['data']:
    # print(city['province'], city['city'])
    cursor.execute('INSERT INTO main_city VALUES (%s, %s)', (city['province'],city['city']))

conn.commit()