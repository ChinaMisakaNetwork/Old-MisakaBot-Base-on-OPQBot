import requests
import json
import qrcode
from urllib import parse
import re
import io
import base64

# 定义一个快速提取参数的函数


def getcansu(url):

    urldata = parse.unquote(url)
    result = parse.urlparse(urldata)
    query_dict = parse.parse_qs(result.query)

    cachesessdata = query_dict.get('SESSDATA', [])[0]
    a = re.split('[,]', cachesessdata)
    SESSDATA = a[0]+'%2C'+a[1]+'%2C'+a[2]

    csrf = query_dict.get('bili_jct', [])[0]

    return({"csrf": csrf, "sessdata": SESSDATA})


class Login:
    def __init__(self):
        self.oauthKey = ''

    def newlogin(self):
        loginurlre = requests.get(
            'https://passport.bilibili.com/qrcode/getLoginUrl')
        redata = json.loads(loginurlre.text)
        self.oauthKey = redata['data']['oauthKey']
        loginurl = redata['data']['url']

        img = qrcode.make(data=loginurl, version=1)
        # loginqrcode.save('LoginQRcode.png')

        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        image_stream = buf.getvalue()
        heximage = base64.b64encode(image_stream)
        # 'data:image/jpeg;base64,' +
        return(heximage.decode())

    def chaxunlogin(self):
        data = {
            "oauthKey": self.oauthKey
        }
        chaxun = requests.post(
            'https://passport.bilibili.com/qrcode/getLoginInfo', data)
        logindata = json.loads(chaxun.text)

        if logindata['status'] == False:
            return('Not Logined')
        else:
            loginedurl = logindata['data']['url']
            return(getcansu(loginedurl))
