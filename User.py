#-*- coding: UTF-8 -*-
import requests
import api
import json
import sql

f = open('./config.json')
config = json.loads(f.read())
f.close()
POST = api.PostMsg(url=config['server'],botqq=config['botqq'])
#初始化#

def LoginBilibili(msg,QQ):
    import login
    import time
    a = login.Login()
    if msg == '#御坂登录':
        base = a.newlogin()
        POST.UserMsg(msg='请在150秒内使用哔哩哔哩客户端扫描登录二维码',to=QQ,picurl=0,picbase=base)
        print(QQ)
        for _ in range(150):
            text = a.chaxunlogin()
            if text == 'Not Logined':
                #print('没登录')
                pass
            else:
                POST.UserMsg(msg='登录成功',to=QQ,picurl=0,picbase=0)
                csrf = text['csrf']
                cookie = text['sessdata']
                try:
                    sql.write(f'insert into bilibili(QQ,csrf,cookie) values("{QQ}","{csrf}","{cookie}");')
                except:
                    pass
                break
            time.sleep(1)

def Telephone(msg,QQ):
    Get = requests.get(f'http://api.cjsrcw.cn/qb-api.php?mod=cha&qq={QQ}').text
    print(Get)

def User(msg,QQ):
    LoginBilibili(msg,QQ)
    