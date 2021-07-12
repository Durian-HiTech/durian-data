import requests
import json
import time
import pymysql


def getinfo(d,a,date,cursorx,db):


    url = "https://flights.ctrip.com/itinerary/api/12808/products"
    # Referer = "https://flights.ctrip.com/itinerary/oneway/bjs-sha?date=2019-07-18"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Referer": "https://flights.ctrip.com/itinerary/oneway/bjs-sha?date=" + date,
        "Content-Type": "application/json"
    }
    request_payload = {
        "flightWay": "Oneway",
        "classType": "ALL",
        "hasChild": False,
        "hasBaby": False,
        "searchIndex": 1,
        "airportParams": [
            {"dcity": d, "acity": a, "date": date}
        ]
    }

    # post请求
    response = requests.post(url, data=json.dumps(request_payload), headers=headers).text
    print(response)
    # 很多航班信息在此分一下
    routeList = json.loads(response).get('data').get('routeList')
    # print(routeList)
    # 依次读取每条信息
    for route in routeList:
        # 判断是否有信息，有时候没有会报错
        if len(route.get('legs')) == 1:
            legs = route.get('legs')
            flight = legs[0].get('flight')
            # print(flight)
            # 提取想要的信息
            # airlineName = flight.get('airlineName')
            # flightNumber = flight.get('flightNumber')
            # departureDate = flight.get('departureDate')
            # arrivalDate = flight.get('arrivalDate')
            # departureCityName = flight.get('departureAirportInfo').get('cityName')
            # departureAirportName = flight.get('departureAirportInfo').get('airportName')
            # arrivalCityName = flight.get('arrivalAirportInfo').get('cityName')
            # arrivalAirportName = flight.get('arrivalAirportInfo').get('airportName')
            #
            # print(airlineName, "\t",
            #       flightNumber, "\t",
            #       departureDate, "\t",
            #       arrivalDate, "\t",
            #       departureCityName, "\t",
            #       departureAirportName, "\t",
            #       arrivalCityName, "\t",
            #       arrivalAirportName)


if __name__ == "__main__":

    db = pymysql.connect(host = "rm-uf6ji600qianqe6921o.mysql.rds.aliyuncs.com",port=3306,user = "buaase2021",passwd = "buaase(2021)",db = "durian")
    cursor = db.cursor()
    print("link success")
    NOW = time.strftime("%Y-%m-%d", time.localtime())
    # getinfo("AAT", "ACX", NOW)
    # for x in city:
    #     for y in city:
    #         if x!=y:
    #             print(x+" "+y)
    #             getinfo(x,y,"2021-07-09")
    # getinfo("AAT", "KRY", NOW, cursor,db)

    getinfo("SHA","BJS",NOW,cursor,db)
    #
    # with open('./flights_data/'+NOW+"_flightinfo.json", 'w') as file_object:
    #     json.dump(jdata, file_object)