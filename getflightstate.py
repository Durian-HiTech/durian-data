import base64
import re
from datetime import datetime
from io import BytesIO

import pymysql
import requests
from bs4 import BeautifulSoup


def get_num_by_image(url):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=xVaNvyZ45BYWOSUAGqbYHkio&client_secret=MKZmvOt0t3Xr82u80WYpaGh2V2bKFmza'
    response = requests.get(host)
    access_token = response.json()['access_token']
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"
    response = requests.get(url)
    img = base64.b64encode(BytesIO(response.content).read())
    params = {"image": img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    res_time = response.json()['words_result'][0]['words']
    res_time = res_time[:2] + ':' + res_time[2:]
    return res_time

def get_flight_info_by_code(code, date=datetime.now().strftime('%Y-%m-%d')):
    url = f'http://www.umetrip.com/mskyweb/fs/fc.do?flightNo={code}&date={date}&channel='
    fail_num = 0
    while True:
        if fail_num > 50:
            return '暂无'
        res = requests.get(url)
        soup = 
        state = soup.find(attrs={'class': 'state'})
        if state is not None:
            # city_num = len(state.find_all('div'))
            # print(city_num)
            condition = state.text.strip()[:2]
            # city = soup.find_all('h2')
            # dept_airport = re.split('[()]', city[0].text)[1].strip()
            # arri_airport = re.split('[()]', city[-1].text)[1].strip()
            t = soup.find_all(attrs={'class': 'time'})
            # dept_time = get_num_by_image(t[city_num].find('img').get('src'))
            # arri_time = get_num_by_image(t[-1].find('img').get('src'))
            return condition
            # return code, condition, dept_airport, arri_airport, date + ' ' + dept_time + ':00', date + ' ' + arri_time + ':00'
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