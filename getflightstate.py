
from datetime import datetime
import pymysql
import requests
from bs4 import BeautifulSoup

def get_flight_info_by_code(code, date=datetime.now().strftime('%Y-%m-%d')):
    url = f'http://www.umetrip.com/mskyweb/fs/fc.do?flightNo={code}&date={date}&channel='
    fail_num = 0
    while True:
        if fail_num > 50:
            return '暂无'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        state = soup.find(attrs={'class': 'state'})
        if state is not None:
            condition = state.text.strip()[:2]
            return condition
        fail_num += 1

if __name__ == '__main__':
    db = pymysql.connect(host="rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com", port=3306, user="buaase2021",
                         passwd="buaase(2021)", db="durian")
    cursor = db.cursor()
    cursor2 =db.cursor()
    print("link success")
    cursor.execute("select * from flight_domestic;")
    for res in cursor.fetchall():
        print(res[1],res[2].strftime("%Y-%m-%d"))
        temp =get_flight_info_by_code(res[1],res[2].strftime("%Y-%m-%d"))
        todo = ' update flight_domestic set state = "'+temp+'" where (flight_number ="'+res[1]+'")and(departure_date ="'+res[2].strftime("%Y-%m-%d %H:%M:%S")+'")'
        print(todo)
        cursor2.execute(todo)
        db.commit()
        # cursor.execute("update user set name='xiaoxiaoxiaoxiaoren' where id=5")

    # print(get_flight_info_by_code('ZH1516','2021-07-13'))