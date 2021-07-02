# coding=utf-8
import socketio
import json
import time
import logging
import re
import Group
import User
import sql
import random


f = open('./config.json')
config = json.loads(f.read())['BotConfig']
f.close()

robotqq = config['botqq']  # 机器人QQ号
webapi = config['server']  # Webapi接口
MasterGroup = config['MasterGroup']
sio = socketio.Client()

# 检测数据库中是表是不是完整
print('开始检查数据库')
for i in range(len(MasterGroup)):
    GroupID = MasterGroup[i]
    try:
        sql.read(f'SELECT * FROM Admin_{GroupID};')
        sql.read(f'SELECT * FROM log_{GroupID};')
        sql.read(f'SELECT * FROM ShutUplog_{GroupID};')
        sql.read(f'SELECT * FROM Violation_{GroupID};')
        print(f'{GroupID}的群数据库检查PASS')
    except:
        raise Exception(f'群{GroupID}缺少数据库表,请检查')
try:
    sql.read(f'SELECT * FROM eventlog;')
except:
    raise Exception(f'EventLog数据表丢失')


class GMess:
    # QQ群消息类型
    def __init__(self, message1):
        # print(message1)
        self.FromQQG = message1['FromGroupId']  # 来源QQ群
        self.QQGName = message1['FromGroupName']  # 来源QQ群昵称
        self.FromQQID = message1['FromUserId']  # 来源QQ
        self.FromQQName = message1['FromNickName']  # 来源QQ名称
        self.Content = message1['Content']  # 消息内容
        self.MsgSeq = message1['MsgSeq']  # 消息ID
        self.MsgRandom = message1['MsgRandom']  # 消息随机


class Mess:
    def __init__(self, message1):
        self.FromQQ = message1['FromUin']
        self.ToQQ = message1['ToUin']
        self.Content = message1['Content']


def beat():
    while (1):
        sio.emit('GetWebConn', robotqq)
        time.sleep(60)


@sio.event
def connect():
    print('已连接到服务器', config['server'], '正在运行的QQ', config['botqq'])
    sio.emit('GetWebConn', robotqq)  # 取得当前已经登录的QQ链接
    beat()  # 心跳包，保持对服务器的连接


@sio.on('OnGroupMsgs')
def OnGroupMsgs(message):
    ''' 监听群组消息'''

    tmp1 = message
    tmp2 = tmp1['CurrentPacket']
    tmp3 = tmp2['Data']
    a = GMess(tmp3)
    '''
    a.FrQQ 消息来源
    a.QQGName 来源QQ群昵称
    a.FromQQG 来源QQ群
    a.FromNickName 来源QQ昵称
    a.Content 消息内容
    a.MsgSeq 消息ID
    '''
    # ————————违规消息检测部分分割线————————
    '''
    import sql
    import itertools
    Adminer = sql.read('SELECT * FROM Admin;')
    if 'GroupPic' in str(a.Content):
        # Group.Group(msg=a.Content,QQ=a.FromQQID,GroupID=a.FromQQG)
        picurl = json.loads(a.Content)['GroupPic'][0]['Url']
        reason = json.loads(Text.CheckPic(picurl))
        if reason['Label'] != 'Normal':
            Type1 = reason['Label']
            try:
                Type2 = reason['LabelResults'][0]['SubLabel']
            except:
                Type2 = 'None'
            Type = f'{Type1}图片--{Type2}图片'
            Group.Block(Type=Type, GroupID=a.FromQQG, MsgSeq=a.MsgSeq,
                        MsgRandom=a.MsgRandom, QQ=a.FromQQID, NickName=a.FromQQName)
    else:
        Jiance = Text.Check(msg=a.Content)
        if Jiance['Data']['DetailResult'] == None:
            Group.Group(msg=a.Content, QQ=a.FromQQID, GroupID=a.FromQQG)
        else:
            if '/禁言' in a.Content and str(a.FromQQID) in list(itertools.chain.from_iterable([list(x) for x in Adminer])):
                Group.Group(msg=a.Content, QQ=a.FromQQID, GroupID=a.FromQQG)
            else:
                Group.Block(Jiance['Data']['DetailResult'][0]['EvilLabel'], GroupID=a.FromQQG,
                            MsgSeq=a.MsgSeq, MsgRandom=a.MsgRandom, QQ=a.FromQQID, NickName=a.FromQQName)
        '''
    # ————————违规消息检测部分分割线————————
    # 如果不需要此部分就删掉分割线内内容,并且把下一行取消注释

    if str(a.FromQQG) in MasterGroup and a.FromQQID != robotqq:
        import time, sql
        time = time.strftime("%Y%m%d%H%M%S", time.localtime())

        try:
            msg = json.loads(a.Content)
            if msg['Tips'] == '[回复]':
                replyseq = msg['MsgSeq']
                msg = a.Content.replace('"', r'\"').replace("'", "\'")
                sqlcode = f'INSERT INTO {a.FromQQG}_log (time,type,msg,QQ,msgseq,msgran,Replyseq) VALUES ("{time}","message",\"{msg}\","{a.FromQQID}",{int(a.MsgSeq)},{int(a.MsgRandom)},{int(replyseq)});'
                sql.write(sqlcode)
            else:
                msg = a.Content.replace('"', r'\"').replace("'", "\'")
                sqlcode = f'INSERT INTO {a.FromQQG}_log (time,type,msg,QQ,msgseq,msgran) VALUES ("{time}","message",\"{msg}\","{a.FromQQID}",{int(a.MsgSeq)},{int(a.MsgRandom)});'
                sql.write(sqlcode)
        except:
            try:
                msg = a.Content.replace('"', r'\"').replace("'", "\'")
                sqlcode = f'INSERT INTO {a.FromQQG}_log (time,type,msg,QQ,msgseq,msgran) VALUES ("{time}","message",\'{msg}\',"{a.FromQQID}",{int(a.MsgSeq)},{int(a.MsgRandom)});'
                sql.write(sqlcode)
            except:
                print(f'尝试写消息到数据库时出错,现Print出该消息\n \n {a.Content}')

        f = open('./plugin/settings.json',encoding = 'utf-8')
        settingjson = json.loads(f.read())['menu']
        f.close()

        cmdlist = []
        for i in range(len(settingjson)):#遍历json以获得已经知道的命令列表
            cmd = settingjson[i]['cmd']
            cmdlist.append(cmd)

        if a.Content.split()[0] in cmdlist: #消息首位是命令时，交给功能函数处理
            Group.Group(msg=a.Content, QQ=a.FromQQID, GroupID=a.FromQQG)
            return
        else:#不是时，交给聊天函数处理
            if random.randint(1, 40)==5:  #40分之一的概率
                Group.TencentTalk(msg=a.Content, QQ=a.FromQQID, GroupID=a.FromQQG)
                return
        

    te = re.search(r'\#(.*)', str(a.Content))
    if te == None:
        return


@sio.on('OnFriendMsgs')
def OnFriendMsgs(message):
    ''' 监听好友消息 '''
    tmp1 = message
    tmp2 = tmp1['CurrentPacket']
    tmp3 = tmp2['Data']
    a = Mess(tmp3)

    User.User(msg=a.Content, QQ=a.FromQQ)


@sio.on('OnEvents')
def OnEvents(message):
    ''' 监听相关事件'''
    try:
        if message['CurrentPacket']['Data']["EventMsg"]["Content"] == '群成员撤回消息事件':
            GroupID = message['CurrentPacket']['Data']["EventData"]["GroupID"]
            msgseq = message['CurrentPacket']['Data']['EventData']['MsgSeq']
            msgran = message['CurrentPacket']['Data']['EventData']['MsgRandom']
            sql.write(f'UPDATE {GroupID}_log SET Chehui=1 WHERE msgseq={msgseq} and msgran={msgran};')
            return
    except:
        pass
    message1 = str(message).replace('"', r'\"')
    sql.write(f'INSERT INTO eventlog (text) VALUES (\"{message1}\");')
    print(message)


def main():
    try:
        sio.connect(webapi, transports=['websocket'])
        sio.wait()
    except BaseException as e:
        logging.info(e)
        print(e)


if __name__ == '__main__':
    main()
