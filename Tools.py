from requests import get
from json import loads


def GetCityWeatherCode(city):
    """
    :param city: 地区名
    :return: ['101050703', 'heilongjiang', '漠河', 'Mohe', '漠河', 'Mohe', '457', '165300', 'MH', '黑龙江']
    """
    data = loads(str(get("http://toy1.weather.com.cn/search?cityname={}".format(city)).content, "utf8")[1:-1])
    if len(data):
        return data[0]["ref"].split("~")
    return None


def Weather(city):
    """
    :param city: 城市
    :return_sample: {'nameen': 'xiamen', 'cityname': '厦门', 'city': '101230201', 'temp': '25', 'tempf': '77', 'WD': '东风', 'wde': 'E', 'WS': '2级', 'wse': '8km/h', 'SD': '95%', 'sd': '95%','qy': '992', 'njd': '15km', 'time': '22:10', 'rain': '0', 'rain24h': '0', 'aqi': '23', 'aqi_pm25': '23', 'weather': '多云', 'weathere': 'Cloudy', 'weathercode': 'd01', 'limitnumber': '', 'date': '06月25日(星期五)'}
    """
    code = GetCityWeatherCode(city)
    if code:
        return loads(str(get("http://d1.weather.com.cn/sk_2d/{}.html".format(code[0])).content, "utf8").replace(
            "var dataSK=", ""))
    return None


"""
#Test
if __name__ == "__main__":
    print(GetCityWeatherCode("厦门"))
"""
