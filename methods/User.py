#-*- coding: UTF-8 -*-

if __name__ != '__main__':
    from methods import api
else:
    import api
import json
from module import sql

f = open('./config.json')
config = json.loads(f.read())
f.close()
POST = api.PostMsg(url=config['server'],botqq=config['botqq'])
#初始化#

def LoginBilibili(msg,QQ):
    from module import login
    import time
    a = login.Login()
    if msg == '#御坂登录':
        base = a.newlogin()
        POST.UserMsg(msg='请在150秒内使用哔哩哔哩客户端扫描登录二维码',to=QQ,picurl=0,picbase=base)
        print(QQ)
        for i in range(150):
            text = a.chaxunlogin()
            if text == 'Not Logined':
                #print('没登录')
                pass
            else:
                POST.UserMsg(msg='登录成功',to=QQ,picurl=0,picbase=0)
                csrf = text['csrf']
                cookie = text['sessdata']
                from module import sql
                try:
                    sql.write(f'insert into bilibili(QQ,csrf,cookie) values("{QQ}","{csrf}","{cookie}");')
                except:
                    pass
                break
            time.sleep(1)


def User(msg,QQ):
    LoginBilibili(msg,QQ)
    