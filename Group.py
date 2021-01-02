#-*- coding: UTF-8 -*-

import api
import json
import sql
import itertools


f = open('./config.json')
config = json.loads(f.read())
f.close()
POST = api.PostMsg(url=config['server'],botqq=config['botqq'])
#初始化#


def ShutUp(msg,QQ,GroupID):
    import json
    if '#禁言' in msg:
        Adminer = sql.read('SELECT * FROM Admin;')
        if str(QQ) in list(itertools.chain.from_iterable([list(x) for x in Adminer])):
            try:
                shutupuserid = json.loads(msg)['UserID'][0]
                time = json.loads(msg)['Content'].split(' ')[2]
            except:
                POST.GroupMsg(msg='缺少参数',groupid=GroupID,picurl=0,picbase=0)
                return
            POST.SetShutUpUser(qq=shutupuserid,time=time,groupid=GroupID)
            POST.GroupMsg(msg='操作成功',groupid=GroupID,picurl=0,picbase=0)
        else:
            POST.GroupMsg(msg='非许可用户,不可使用该命令',groupid=GroupID,picurl=0,picbase=0)
def LoginBilibili(msg,QQ,GroupID):
    if msg == '#御坂登录':
        POST.GroupMsg(msg='请私聊我发送“#御坂登录”登录哦',groupid=GroupID,picurl=0,picbase=0)

def Block(Type,GroupID,MsgSeq,MsgRandom,QQ):
    Adminer = sql.read('SELECT * FROM Admin;')
    if str(QQ) in str(Adminer):
        return
    else:
        POST.CheHui(GroupID=GroupID,MsgSeq=MsgSeq,MsgRandom=MsgRandom)
        POST.GroupMsg(msg=f'监测到违规信息,已经撤回,类型为{Type}',groupid=GroupID,picurl=0,picbase=0)
        POST.SetShutUpUser(qq=QQ,time=config['TextShutupTime'],groupid=GroupID)
    
def Weather(msg, QQ, GroupID):
    if msg.split()[0] == "#查询天气" and len(msg.split()) == 2:
        city = zhconv.convert(msg.split()[1], "zh-hans").replace("'","").lower().replace(' ','')
        if '#' in city or '--' in city or '"' in city:
            POST.GroupMsg(msg = "请不要尝试进行SQL注入。\n怀疑违规行为已经向所有风纪委员通报。", groupid = GroupID, picurl = 0, picbase = 0, atUser = QQ)
            POST.GroupMsg(msg = "QQ号为"+str(QQ)+"的用户怀疑正在进行SQL注入，请注意且自行判断其违规行为并予以惩罚。\n消息内容: \n"+msg, groupid = 835021978, picurl = 0, picbase = 0, atUser = 0)
        else:
            sqlr = sql.read('SELECT * FROM city WHERE cityZh = '+city+' or cityEn = '+city)
            if len(sqlr) == 0:
                sqlr2 = sql.read('SELECT * FROM city WHERE provinceZh = '+city+' or provinceEn = '+city)
                if len(sqlr2) > 0:
                    POST.GroupMsg(msg = "请输入具体城市名作为参数。属于"+city[0][4]+"省的城市有: \n"+"\n".join([x[2] for x in read('SELECT * FROM city WHERE provinceZh="'+city+'" or provinceEn="'+city+'"')])+"\n。", groupid = GroupID, picurl = 0, picbase = 0, atUser = QQ)
                else:
                    POST.GroupMsg(msg = "无查询结果。\n请确认是否有错别字或者拼写错误。", groupid = GroupID, picurl = 0, picbase = 0, atUser = QQ)
            else:
                raw = json.loads(urllib.request.urlopen("https://tianqiapi.com/api?version=v6&appid=18224395&appsecret=lgCc5VqI&cityid="+str(sqlr[0][0])).read())
                rtst = sqlr[0][2]+"的天气状况: \n"
                rtst+= "温度: "+str(raw['tem'])+"℃ ("+str(raw['tem2'])+"℃-"+str(raw['tem1'])+"℃)\n"
                rtst+= "湿度："+raw['humidity']+'\n'
                rtst+= raw['wea']+'\n'
                rtst+= "吹"+raw['win']+' '+raw['win_speed']+'[PICFLAG]'
                try:
                    picf = open('./plugin/weather/'+raw['wea_img']+'.png', 'rb').read()
                    pbase = "data:image/jpeg;base64,"+base64.b64encode(picf).decode()
                except:
                    pbase = 0
                POST.GroupMsg(msg = rtst, groupid = GroupID, picurl = 0, picbase = pbase, atUser = QQ)

def Group(msg,QQ,GroupID):
    ShutUp(msg,QQ,GroupID)
    LoginBilibili(msg,QQ,GroupID)
    Weather(msg, QQ, GroupID)
