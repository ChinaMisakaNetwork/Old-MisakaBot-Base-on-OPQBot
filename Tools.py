import json
import hashlib
import requests
import urllib.parse
import random
import math
import time


def GetCityWeatherCode(city):
    """
    :param city: 地区名
    :return: ['101050703', 'heilongjiang', '漠河', 'Mohe', '漠河', 'Mohe', '457', '165300', 'MH', '黑龙江']
    """
    data = json.loads(
        str(requests.get("http://toy1.weather.com.cn/search?cityname={}".format(city)).content, "utf8")[1:-1])
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
        try:
            return json.loads(
                str(requests.get("http://d1.weather.com.cn/sk_2d/{}.html".format(code[0])).content, "utf8").replace(
                    "var dataSK=", ""))
        except json.decoder.JSONDecodeError:
            return None
    return None


def genSignString(parser, appkey):
    """
    :param parser: params
    :param appkey: AppKey for Tencent Talk
    :return: SignString
    """
    uri_str = ''
    for key in sorted(parser.keys()):
        if parser[key] != '':
            uri_str += "%s=%s&" % (key, urllib.parse.quote(str(parser[key]), safe=''))
    sign_str = uri_str + 'app_key=' + appkey
    hash_md5 = hashlib.md5(sign_str.encode("utf8"))
    return hash_md5.hexdigest().upper()


def TencentTalk(message):
    """
    :param message: str(message)
    :return: str(answer)
    """
    msg = ''
    while msg=='' or msg==" ":
        url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
        appkey = "mqXav84IbUxXK7VI"
        app_id = 2155978988
        params = {
            'app_id': app_id,
            'session': str(random.randint(827333, 102938333312)),
            'question': message,
            'time_stamp': math.floor(time.time()),
            'nonce_str': ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890', 16)),
            'sign': '',
        }
        params["sign"] = genSignString(params, appkey)
        response = requests.post(url, data=params)
        msg = response.json()["data"]["answer"]
    return msg



# Test
if __name__ == "__main__":
    print(TencentTalk("华盛顿"))

