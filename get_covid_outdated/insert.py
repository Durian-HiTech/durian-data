import pymysql

conn = pymysql.connect( host='rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com',
                        port=3306,
                        user='buaase2021',
                        passwd='buaase(2021)',
                        charset='utf8',
                        db='durian'
                        )

cursor = conn.cursor()

###############     插入数据       #####################
data_list=[]
with open('./get_covid/vaccinetoday.txt','r',encoding='UTF-8') as f:
    for line in f:
        li=line.split('\t')
        data={
            'date': '2021-07-06',
            'country_name': li[0],
            'info': int(li[1])
        }
        data_list.append(data)

for data in data_list:
    print(data)
    cursor.execute('INSERT INTO covid_vaccine VALUES (%s, %s, %s)', (data['date'],data['country_name'],data['info']))

conn.commit()