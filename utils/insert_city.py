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

with open('./utils/Center.json','r',encoding='utf8') as f:
    city_dict = json.load(f)
    # print(city_dict)

for city in city_dict:
    print(city['name'], city['center'])
    # print(str(city['center']))
    cursor.execute('INSERT INTO center_city VALUES (%s, %s, %s)', (city['name'],city['center'][0], city['center'][1]))

conn.commit()