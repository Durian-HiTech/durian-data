import argparse
import datetime
import json
import os
import time
import pymysql
import requests
from requests.exceptions import Timeout
from tqdm import tqdm

from utils.cast import cur_time
from utils.logger import create_logger

URL = 'http://train.qunar.com/qunar/checiInfo.jsp'
DEFAULT_DATE = datetime.datetime.now()
#DEFAULT_DATE_STR = DEFAULT_DATE.strftime('%Y-%m-%d')  # 默认查询当天的
DEFAULT_DATE_STR = "2021-07-13"
mingming = [('G', 2899),
            ('C', 9999),
            ('Z', 9999),
            ('T', 9999),
            ('K', 9999),
            ('L', 9999),
            ('Y', 999)]


def getinfo(logger,cursorx,db,train_number='G2850', date=DEFAULT_DATE_STR):
    # logger.info('getinfo')
    params = {
        'method_name': 'buy',
        'ex_track': '',
        'q': train_number,
        'date': date.replace('-', ''),
        'format': 'json',
        'cityname': 123456,
        'ver': int(time.time() * 1000),
    }
    url = URL
    try:
        response = requests.get(url=url, params=params, headers={'Content-Type': 'application/json'}, timeout=10)
    except Timeout:
        logger.error('无法从服务器获取数据')
        logger.error('url: ' + url)
        logger.error(params)
        return None
    result = json.loads(response.text)
    print(result)
    # for i in result['trainInfo']:
    #     # print(i)
    #     print("班次:",result['trainInfo'][i]['code'])
    #     print("出发日期:",result['trainInfo'][i]['dptDate'])
    #     print("到达日期:",result['trainInfo'][i]['arrDate'])
    #     print("始发地:",result['trainInfo'][i]['deptCity'])
    #     print("始发站:",result['trainInfo'][i]['deptStation'])
    #     print("目的地:",result['trainInfo'][i]['arriCity'])
    #     print("到达站:",result['trainInfo'][i]['arriStation'])
    #     print("出发时间:",result['trainInfo'][i]['deptTime'])
    #     print("到达时间:",result['trainInfo'][i]['arriTime'])
    try:
        for i in result['trainInfo']:
            cursorx.execute(
            """insert into train_domestic(departure_city, departure_time,arrival_city,arrival_time,train_number,departure_station,arrival_station)
            value (%s,%s,%s,%s,%s,%s,%s)""",  # 纯属python操作mysql知识，不熟悉请恶补
            (result['trainInfo'][i]['deptCity'],
            result['trainInfo'][i]['dptDate']+' '+result['trainInfo'][i]['deptTime'],
            result['trainInfo'][i]['arriCity'],
            result['trainInfo'][i]['arrDate']+' '+result['trainInfo'][i]['arriTime'],
            result['trainInfo'][i]['code'],
            result['trainInfo'][i]['deptStation'],
            result['trainInfo'][i]['arriStation'],
            ))

            db.commit()
    except:
        pass        


def main(verbose, path, index=0, st=0):
    if not os.path.exists(path):
        os.makedirs(path)

    logger = create_logger(logger_name=os.path.basename(path), log_path=os.path.join(path, f'log.log'), to_stdout=False)

    for current_index in range(index, len(mingming)):
        if verbose:
            bar = tqdm(range(st, mingming[current_index][1]), dynamic_ncols=True)
        else:
            bar = range(st, mingming[current_index][1])
        for current_st in bar:
            if 0 <= datetime.datetime.now().hour <= 6:
                time.sleep(0.5)
            else:
                time.sleep(1)
            name = mingming[current_index][0] + str(current_st)
            result = getinfo(logger=logger, train_number=name,db=db,cursorx=cursor)  # result是json
            # print(result)
            if result:
                data = list(result['trainInfo'].values())[0]
                if verbose:
                    bar.set_description(f'[{name}]')
                    bar.set_postfix_str(f'{data["deptCity"]} => {data["arriCity"]}')
                with open(os.path.join(path, '火车班次爬到哪了.txt'), 'w', encoding='utf-8') as fp:
                    fp.write(f'index={current_index}, st={current_st+1}\n')
                with open(os.path.join(path, '火车班次json数据.json'), 'a', encoding='utf-8') as fp:
                    fp.write(json.dumps(result,ensure_ascii=False) + '\n')
                with open(os.path.join(path, '火车班次列表.json'), 'a', encoding='utf-8') as fp:
                    fp.write(name + '\n')
            else:
                if verbose:
                    bar.set_description(f'[{name}]: failed')
                    bar.set_postfix_str('failed')


def local_main():
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--verbose', required=False, default=True, type=bool)
    parser.add_argument('--path', required=False, default=os.path.join('spider_train', 'train_spider'), type=str)
    parser.add_argument('--index', required=False, default=0, type=int)
    parser.add_argument('--st', required=False, default=2850, type=int)
    args = parser.parse_args()
    
    start = datetime.datetime.now().strftime('[%m-%d %H:%M:%S]')
    args.path += f'_index{args.index}_st{args.st}'
    print(f'{start} 开始爬！path={args.path}, index={args.index}, st={args.st}...')
    try:
        main(args.verbose, args.path, args.index, args.st)
    except:
        with open(os.path.join(args.path, '火车班次爬到哪了.txt'), 'r', encoding='utf-8') as fp:
            s = fp.read()
            print(f'爬失败了，请你下次从 {s} 再开始爬！')
    else:
        print(f'爬完了！')

if __name__ == '__main__':
    db = pymysql.connect(host = "rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com",port=3306,user = "buaase2021",passwd = "buaase(2021)",db = "durian")
    cursor = db.cursor()
    local_main()

    # res = getinfo('G1317')
    # print(res)

    # url = 'http://train.qunar.com/qunar/checiSuggest.jsp?callback=jQuery17208000492092391186_1460000280989&include_coach_suggest=true&lang=zh&q=G1316&sa=true&format=js&_=1460000429009'
    # try:
    #     response = requests.get(url=url, timeout=10)
    # except Timeout:
    #     logger.error('无法从服务器获取数据')
    #     logger.error('url: '+url)
    # results=json.loads('{'+response.text.split('({')[1].split('})')[0]+'}')['result']
    # print(results[0].get('key'))
