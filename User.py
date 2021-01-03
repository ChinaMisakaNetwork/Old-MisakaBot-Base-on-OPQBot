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
    if msg == '/御坂登录':
        base = a.newlogin()
        POST.UserMsg(msg='请在提示登录请求过期前(最少150秒)内使用哔哩哔哩客户端扫描登录二维码',to=QQ,picurl=0,picbase=base)
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
                return
            time.sleep(1)
        POST.UserMsg(msg='您的登录请求已经过期',to=QQ,picurl=0,picbase=0)


def User(msg,QQ):
    LoginBilibili(msg,QQ)
    