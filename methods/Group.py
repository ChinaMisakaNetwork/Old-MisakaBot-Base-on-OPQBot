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


def ShutUp(msg,QQ,GroupID):
    import json
    if '#禁言' in msg:
        Adminer = sql.read('SELECT * FROM Admin;')
        if str(QQ) in str(Adminer):
            try:
                shutupuserid = json.loads(msg)['UserID'][0]
                time = json.loads(msg)['Content'].split(' ')[2]
            except:
                POST.GroupMsg(msg='缺少参数',groupid=GroupID,picurl=0,picbase=0,atUser=0)
                return
            POST.SetShutUpUser(qq=shutupuserid,time=time,groupid=GroupID)
            POST.GroupMsg(msg='操作成功',groupid=GroupID,picurl=0,picbase=0,atUser=0)
        else:
            POST.GroupMsg(msg='非许可用户,不可使用该命令',groupid=GroupID,picurl=0,picbase=0,atUser=0)
def LoginBilibili(msg,QQ,GroupID):
    if msg == '#御坂登录':
        POST.GroupMsg(msg='请私聊我发送“#御坂登录”登录哦',groupid=GroupID,picurl=0,picbase=0,atUser=0)

def Block(Type,GroupID,MsgSeq,MsgRandom,QQ):
    Adminer = sql.read('SELECT * FROM Admin;')
    if str(QQ) in str(Adminer):
        return
    else:
        POST.CheHui(GroupID=GroupID,MsgSeq=MsgSeq,MsgRandom=MsgRandom)
        POST.GroupMsg(msg=f'监测到违规信息,已经撤回,类型为{Type}',groupid=GroupID,picurl=0,picbase=0,atUser=0)
        POST.SetShutUpUser(qq=QQ,time=config['TextShutupTime'],groupid=GroupID)
    

def Group(msg,QQ,GroupID):
    ShutUp(msg,QQ,GroupID)
    LoginBilibili(msg,QQ,GroupID)

