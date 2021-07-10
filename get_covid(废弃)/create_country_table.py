import pymysql

conn = pymysql.connect( host='rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com',
                        port=3306,
                        user='buaase2021',
                        passwd='buaase(2021)',
                        charset='utf8',
                        db='durian'
                        )

cursor = conn.cursor()


###############     创建country表       #####################
cursor.execute('CREATE TABLE `country`( \
               `country_name` VARCHAR(255) NOT NULL,\
               PRIMARY KEY (`country_name`),\
               INDEX `ID` USING BTREE (`country_name`))\
               ENGINE = InnoDB,\
               DEFAULT CHARACTER SET = utf8mb4',)
conn.commit()

###############     插入数据       #####################
country_list=[]
with open('./get_covid/country_list.txt','r',encoding='UTF-8') as f:
    for line in f:
        country_list.append(line[:-1])

for country in country_list:
    print(country)
    cursor.execute('INSERT INTO country VALUES (%s)', (country))

conn.commit()