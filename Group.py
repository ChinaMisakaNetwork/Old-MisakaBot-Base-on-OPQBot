# -*- coding: UTF-8 -*-

import json
import itertools
import urllib
import base64
import api
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
from sympy import parse_expr,latex,evaluate,latex,Eq,solve,factor,plot
from PIL import Image
from urllib import request
import requests
import io
import glob
import zhconv
import os
import sql
import matplotlib
import threading
import subprocess

f = open('./config.json')
config = json.loads(f.read())
f.close()
POST = api.PostMsg(url=config['server'],botqq=config['botqq'])
loggroup = config['loggroup']

#函数区开始
#Weather死了(数据库没了)

def ShutUp(msg, QQ, GroupID):
    import json
    if "yb.jy" in msg and QQ != config['botqq']:
        Adminer = sql.read('SELECT * FROM Admin;')
        if str(QQ) in list(itertools.chain.from_iterable([list(x) for x in Adminer])):
            try:
                shutupuserid = json.loads(msg)['UserID'][0]
                shutuptime = json.loads(msg)['Content'].split(' ')[2]
                if shutuptime == '':
                    POST.GroupMsg(msg='缺少参数', groupid=GroupID, picurl=0, picbase=0)
                    return
            except:
                POST.GroupMsg(msg='缺少参数', groupid=GroupID, picurl=0, picbase=0)
                return
            POST.SetShutUpUser(qq=shutupuserid, time=shutuptime, groupid=GroupID)
            POST.GroupMsg(msg='操作成功', groupid=GroupID, picurl=0, picbase=0)

            
            if shutuptime != '0':
                sqllist = sql.read('SELECT * FROM Violation;')
                print(sqllist)
                if str(shutupuserid) in str(sqllist):
                    edtimes = sql.read(f'SELECT WarningTimes FROM Violation WHERE QQ="{shutupuserid}";')[0][0]
                    sql.write(f'UPDATE Violation SET WarningTimes={edtimes+1} WHERE QQ="{shutupuserid}";')
                else:
                    sql.write(f'INSERT INTO Violation VALUES ("{shutupuserid}",1);')
            
            if str(GroupID) == loggroup:
                import time
                nowtime=time.strftime("%Y%m%d%H%M%S",time.localtime())
                sqlcode = f'INSERT INTO ShutUplog (time,type,shutuptime,who,QQ) VALUES ("{nowtime}","Shutup","{int(shutuptime)}","{str(QQ)}","{str(shutupuserid)}");'
                sql.write(sqlcode)
                return
                
        else:
            POST.GroupMsg(msg='非许可用户,不可使用该命令',
                          groupid=GroupID, picurl=0, picbase=0)

def LoginBilibili(msg, QQ, GroupID):
    if msg == msg.split()[0] == "yb.dl":
        POST.GroupMsg(msg='请私聊我发送“yb.dl”登录哦',
                      groupid=GroupID, picurl=0, picbase=0)

def Block(Type, GroupID, MsgSeq, MsgRandom, QQ, NickName):
    #Adminer = sql.read('SELECT * FROM Admin;')
    if str(QQ) == str(config['botqq']):
        return
    else:
        POST.CheHui(GroupID=GroupID, MsgSeq=MsgSeq, MsgRandom=MsgRandom)
        POST.GroupMsg(msg=f'@{NickName} 监测到违规信息,请注意文明聊天,类型为{Type}',
                      groupid=GroupID, picurl=0, picbase=0)
        POST.SetShutUpUser(
            qq=QQ, time=config['TextShutupTime'], groupid=GroupID)

def Weather(msg, QQ, GroupID):
    fakeflag = False
    def print_weather(fakeflag):
        if fakeflag:
            cityid = sqlr3[0][2]
        else:
            cityid = sqlr[0][2]
        rawdata = json.loads(requests.get("http://www.worldweather.cn/zh/json/%d_zh.xml"%cityid).text)
        rawndta = json.loads(requests.get("https://worldweather.wmo.int/en/json/present.xml").text)["present"]
        for x in rawndta.keys():
            if rawndta[x]['cityId'] == cityid:
                usendta = rawndta[x]
                break
        nowtemp = usendta['temp']
        nowrh = usendta['rh']
        for x in rawdata["city"]["forecast"]["forecastDay"]:
            if x["forecastDate"] == time.strftime("%Y-%m-%d"):
                bfc=x
                break
        templow = bfc["minTemp"]
        temphigh = bfc["maxTemp"]
        dsc = bfc["weather"]
        icon = str(bfc["weatherIcon"])[:-2]
        ret = ""
        if fakeflag:
            ret += "找不到这个城市, 但是有1个相似记录\n也许你想找的是这个?\n\n"
        ret +="%s的天气状况: \n"%rawdata["city"]["cityName"]
        ret += "温度: "+str(nowtemp)+"℃ ("+str(templow)+"℃ - "+str(temphigh)+"℃)\n"
        ret += "湿度: "+str(nowrh)+"%\n"
        ret += dsc+"\n"
        try:
            picf = open("./plugin/weather/"+icon+".png", "rb").read()
            pbase = base64.b64encode(picf).decode()
            rtst += "\n[PICFLAG]"
        except:
            try:
                picf = open("./plugin/weather/"+icon+"a.png", "rb").read()
                pbase = base64.b64encode(picf).decode()
                rtst += "\n[PICFLAG]"
            except:
                pbase = 0
        ret += "\n程式所使用的API 仍然处于测试阶段, 瞬时温度准确率较差, 请以当地政府部门的数据为准。"
        POST.GroupMsg(msg=ret, groupid = GroupID, picurl = 0, picbase = pbase)
    msg = zhconv.convert(msg, "zh-hans")
    if msg.split()[0] == "yb.tq" and len(msg.split()) < 3 and len(msg.split()) > 1:
        city = msg.split()[1].replace("'","").lower().replace(' ','')
        if '#' in city or '--' in city or '"' in city:
            POST.GroupMsg(msg = zhconv.convert("请不要尝试进行SQL注入。\n怀疑违规行为已经向所有风纪委员通报。", {True: "zh-hant", False: "zh-hans"}[tflag]), groupid = GroupID, picurl = 0, picbase = 0)
            POST.GroupMsg(msg = "QQ号为"+str(QQ)+"的用户怀疑正在进行SQL注入，请注意且自行判断其违规行为并予以惩罚。\n消息内容: \n"+msg, groupid = 872324801 , picurl = 0, picbase = 0)
        else:
            sqlr = sql.read("select * from weather_city_list where 2layer = '"+city+"';")
            if len(sqlr) == 0:
                sqlr2 = sql.read("select * from weather_city_list where 1layer = '"+city+"';")
                if len(sqlr2)>0:
                    POST.GroupMsg(msg = "请输入具体城市名作为参数。可选列表: \n"+", ".join([x[1] for x in sql.read('SELECT * FROM weather_city_list WHERE 1layer="'+city+'"')]), groupid=GroupID, picurl=0, picbase=0)
                    return 0
                else:
                    sqlr3 = sql.read("select * from weather_city_list where 2layer like '%"+city+"%';")
                    if len(sqlr3)==0:
                        POST.GroupMsg(msg = "无查询结果。\n请确认是否有错别字或者拼写错误。", groupid = GroupID, picurl = 0, picbase = 0)
                        return 0
                    elif len(sqlr3) == 1:
                        print_weather(True)
                    else:
                        mess = "找不到这个城市, 但是有%d个相似记录\n"%len(sqlr3)
                        mess+= "也许你要找的是: \n"
                        mess+= "\n".join([sqlr3[x][1] for x in range(0, min(10, len(sqlr3)))])
                        if len(mess)>10:
                            mess+="\n等"
                        POST.GroupMsg(msg = mess, groupid = GroupID, picurl = 0, picbase = 0)
                        return 0
            else:
                print_weather(False)

def hitokoto(msg,QQ,GroupID):
    Mainurl = 'https://v1.hitokoto.cn/'
    if msg.split(' ')[0] == "yb.my":
        Typelist = ['a','b','c','d','e','f','g','h','i','j','k','l']
        Typelist2 = ['动画','漫画','游戏','文学','原创','来自网络','其他','影视','诗词','网易云','哲学','抖机灵']

        try:
            Type = msg.split(' ')[1]
        except:
            POST.GroupMsg(msg='缺失参数',groupid=GroupID,picbase=0,picurl=0)
            return

        if Type == '类别':
            POST.GroupMsg(msg=str(Typelist2),groupid=GroupID,picbase=0,picurl=0)
            return

        try:
            CodeTypeindex = Typelist2.index(Type)
        except:
            POST.GroupMsg(msg='无此类别',groupid=GroupID,picbase=0,picurl=0)
            return


        CodeType = Typelist[CodeTypeindex]
        jsonstr = json.loads(requests.get(Mainurl+f'?c={CodeType}').text)
        if jsonstr['from_who'] == None:
            saying = jsonstr['hitokoto']+'----'+jsonstr['from']
        else:
            saying = jsonstr['hitokoto']+'----'+jsonstr['from']+' '+jsonstr['from_who']
        POST.GroupMsg(msg=saying,groupid=GroupID,picbase=0,picurl=0)

def Calc(msg, QQ, GroupID):
    msg = msg.replace("^", "**")
    if msg.split()[0] == "yb.js" and len(msg.split())>1:
        transformations = (standard_transformations + (implicit_multiplication_application,))
        #rmsg = msg[1:]
        def get_concat_v_blank(im1, im2, color=(255, 255, 255, 0)):
            dst = Image.new('RGBA', (max(im1.width, im2.width), im1.height + im2.height + 50), color)
            dst.paste(im1, (0, 0))
            dst.paste(im2, (0, im1.height+50))
            return dst
        def parse(s, e=True):
            return parse_expr(s, transformations=transformations, evaluate = e)
        expo = msg.split()[1]
        msg = msg.split()
        if expo.lower() in ['解方程','因式分解','一般计算', '画图', 'alg', 'factor', 'calc', 'plot']:
            meth = {'解方程':0,'因式分解':1,'一般计算':2, '画图':3, 'alg':0, 'factor':1, 'calc':2, 'plot':3}[expo.lower()]
            msg = msg[1:]
            exp = msg[1]
            exp2 = exp.replace("^","**").replace(" ","").split("=")
            if len(exp2) == 1:
                if meth == 0:
                    meth = 2
            else:
                if meth == 1 or meth == 2:
                    POST.GroupMsg(msg= "请检查输入!", groupid = GroupID, picurl = 0, picbase = 0)
                    return
        else:
            POST.GroupMsg(msg= "请检查输入!", groupid = GroupID, picurl = 0, picbase = 0)
            return
        try:
            u=msg[2]
        except:
            u=None
        exp = exp.replace("^","**").replace(" ","")
        exp = exp.split("=")
        if meth == 2:
            try:
                f = latex(parse(exp[0]))
                try:
                    with evaluate(False):
                        v = latex(parse(exp[0], False))
                except:
                    v = latex(parse(exp[0], False))
                u = v + "=" + f
                img = base64.b64encode(request.urlopen("http://latex2png.com"+eval(requests.post("http://latex2png.com/api/convert", json = {"auth":{"user":"guest","password":"guest"},"latex":u,"resolution":600,"color":"000000"}).text)['url']).read()).decode()
                POST.GroupMsg(msg = "结果: "+str(parse(exp[0]))+'\n[PICFLAG]', groupid = GroupID, picurl = 0, picbase = img)
            except BaseException as e:
                POST.GroupMsg(msg = "可能无解, 或者输入错误, 或者程式不支援", groupid = GroupID, picurl = 0, picbase = 0)
                raise e
        elif meth == 0:
            try:
                equat = Eq(parse(exp[0]), parse(exp[1]))
                if u != None:
                    u = parse(u)
                    if not (u in list(parse(exp[0]).free_symbols)+list(parse(exp[1]).free_symbols)):
                        u = None
                if u == None:
                    solv = solve(equat, dict=True)
                else:
                    solv = solve(equat, u, dict=True)
                if len(solv)>0:
                    rtlist = []
                    imgs = []
                    for x in solv:
                        var = list(x.keys())[0]
                        res = list(x.values())[0]
                        ltv = latex(var)
                        ltr = latex(res)
                        lt = ltv+'='+ltr
                        imgs.append(Image.open(request.urlopen("http://latex2png.com"+eval(requests.post("http://latex2png.com/api/convert", json = {"auth":{"user":"guest","password":"guest"},"latex":lt,"resolution":600,"color":"000000"}).text)['url'])))
                        rtlist.append(str(var)+"="+str(res))
                    fimg = imgs[0]
                    del imgs[0]
                    for x in imgs:
                        fimg = get_concat_v_blank(fimg, x)
                    buffer = io.BytesIO()
                    fimg.save(buffer, format='PNG')
                    b6e = base64.b64encode(buffer.getvalue()).decode()
                    POST.GroupMsg(msg = "解: \n"+" 或\n".join(rtlist)+"\n[PICFLAG]", groupid = GroupID, picurl = 0, picbase = b6e)
                else:
                    POST.GroupMsg(msg = "可能无解, 或者输入错误", groupid = GroupID, picurl = 0, picbase = 0)
            except BaseException as e:
                POST.GroupMsg(msg = "可能无解, 或者输入错误, 或者程式不支援", groupid = GroupID, picurl = 0, picbase = 0)
        elif meth == 1:
            try:
                expres = parse(exp[0])
                try:
                    with evaluate(False):
                        ov = latex(parse(exp[0]))
                except:
                    ov = latex(parse(exp[0]))
                v = factor(expres)
                b6e2 = request.urlopen("http://latex2png.com"+eval(requests.post("http://latex2png.com/api/convert", json = {"auth":{"user":"guest","password":"guest"},"latex":ov + '=' + latex(v),"resolution":600,"color":"000000"}).text)['url']).read()
                POST.GroupMsg(msg = '解: '+str(v).replace("**", '^')+"\n[PICFLAG]", groupid=GroupID, picurl = 0, picbase = base64.encodebytes(b6e2).decode())
            except BaseException as e:
                POST.GroupMsg(msg = "可能无法分解, 或者输入错误, 或者程式不支援", groupid = GroupID, picurl = 0, picbase = 0)
                raise(e)
        elif meth == 3:
            udata = msg[1:]
            xy1 = []
            xy2 = set()
            xy3 = {}
            if len(udata) < 3:
                POST.GroupMsg(msg = "请检查输入", groupid = GroupID, picurl = 0, picbase = 0)
                return
            try:
                axis = int(udata[-1])
                symb = parse(udata[-2])
            except ValueError:
                POST.GroupMsg(msg = "请检查输入", groupid = GroupID, picurl = 0, picbase = 0)
                return
            udata = udata[:-2]
            for xyc1 in udata:
                if '=' in xyc1:
                    xtc = xyc1.split('=')
                    if len(parse(xtc[0]).free_symbols) + len(parse(xtc[1]).free_symbols)> 2:
                        POST.GroupMsg(msg = "程式暂不支援", groupid = GroupID, picurl = 0, picbase = 0)
                        return
                    elif len(parse(xtc[0]).free_symbols) + len(parse(xtc[1]).free_symbols)>=1:
                        lt = list(parse(xtc[0]).free_symbols) + list(parse(xtc[1]).free_symbols)
                        for n in lt:
                            if n in xy3.keys():
                                xy3[n].append(solve(Eq(parse(xtc[0]), parse(xtc[1])), n))
                            else:
                                xy3.update({n: [solve(Eq(parse(xtc[0]), parse(xtc[1])), n)]})
                else:
                    POST.GroupMsg(msg = "程式暂不支援", groupid = GroupID, picurl = 0, picbase = 0)
                    return
            if len(xy2)>1:
                POST.GroupMsg(msg = "程式暂不支援", groupid = GroupID, picurl = 0, picbase = 0)
                return
            else:
                if len(xy3.keys())>2 or not (symb in xy3.keys()):
                    POST.GroupMsg(msg = "程式暂不支援", groupid = GroupID, picurl = 0, picbase = 0)
                    return
                try:
                    x5 = list(xy3.keys())
                    x5.remove(list(xy2)[0])
                    if len(x5)!=1:
                        POST.GroupMsg(msg = "程式暂不支援", groupid = GroupID, picurl = 0, picbase = 0)
                        return
                    for x4 in xy3[x5[0]]:
                        [xy1.append(x6) for x6 in x4]
                except:
                    pass
            fsym = list(xy3.keys())
            fsym.remove(symb)
            xy8 = list(itertools.chain.from_iterable(xy3[fsym[0]]))
            subs = [[str(x) for x in xy8], str(symb), axis, str(symb), str(fsym[0])]
            res = eval(subprocess.getoutput("python ./plugin/Calc/Plot.py "+base64.b64encode(repr(subs).encode()).decode()))
            POST.GroupMsg(msg = res[0], groupid = GroupID, picbase = res)
        else:
            POST.GroupMsg(msg = "程式不支援", groupid = GroupID, picurl = 0, picbase = 0)

def Menu(msg, QQ, Group):
    if msg.split()[0] != "御坂菜单":
        return
    cfg = json.loads(open('./plugin/settings.json', encoding='utf-8').read())['menu']
    uauser = []
    for item in cfg:
        if not item["priv"]:
            uauser.append(item)
    Adminer = sql.read('SELECT * FROM Admin;')
    if str(QQ) in list(itertools.chain.from_iterable([list(x) for x in Adminer])):
        unuser = cfg
    else:
        unuser = uauser
    menu = "御坂御坂可以帮您做这些事情哦:\n"+"\n".join(["%d. %s (%s)"%(ct+1, unuser[ct]['desc'], unuser[ct]['help']) for ct in range(len(unuser))])
    if len(msg.split())==1:
        POST.GroupMsg(msg=menu, groupid=Group, picbase=0, picurl=0)
    else:
        try:
            mm = int(msg.split()[1])
            if mm > 0 and mm < len(unuser)+1:
                mg = msg.split()[2:]
                me = unuser[mm-1]['cmd']
                mr = me + ' ' + " ".join(mg)
                unuser[mm-1]['callback'](mr, QQ, Group)
            else:
                POST.GroupMsg(msg=menu, groupid=Group, picbase=0, picurl=0)
        except:
            raise

def gmeth_test(msg, QQ, GroupID):
    if msg.split()[0] == 'yb.test':
        ret = "OK\n参数: "+','.join(msg.split()[1:])
        POST.GroupMsg(msg=ret, groupid=GroupID, picbase=0, picurl=0)

def Blockbyman(msg, QQ, GroupID):
    if "yb.ch" in msg and QQ != config['botqq']:
        Adminer = sql.read('SELECT * FROM Admin;')
        if str(QQ) in list(itertools.chain.from_iterable([list(x) for x in Adminer])):
            
            try:
                msgid = msg.split(' ')[1]
                if msgid == '':
                    POST.GroupMsg(msg='缺少参数', groupid=GroupID, picurl=0, picbase=0)
                    return

            except:
                POST.GroupMsg(msg='缺少参数', groupid=GroupID, picurl=0, picbase=0)
                return
            
            msglist = sql.read(f'SELECT msgseq,msgran FROM log WHERE id={msgid}')
            if msglist == ():
                POST.GroupMsg(msg='不存在的消息', groupid=GroupID, picurl=0, picbase=0)
                return
            else:
                chehui = sql.read(f'SELECT Chehui FROM log WHERE id={msgid}')[0][0]
                if chehui == 0 :
                    MsgSeq = msglist[0][0]
                    MsgRandom = msglist[0][1]
                    POST.CheHui(GroupID=GroupID, MsgSeq=MsgSeq, MsgRandom=MsgRandom)
                    POST.GroupMsg(msg='操作成功', groupid=GroupID, picurl=0, picbase=0)
                    sql.write(f'UPDATE log SET Chehui=1 WHERE id={msgid};')
                else:
                    POST.GroupMsg(msg='消息已被撤回', groupid=GroupID, picurl=0, picbase=0)
            
#函数区结束

#初始化

customize = json.loads(open('./plugin/settings.json', encoding='utf-8').read())['customize']

def loadphp(msg, QQ, GroupID, file):
    rt = subprocess.call(["php", file, base64.b64encode(msg), base64.b64encode(QQ), base64.b64encode(GroupID)])
    return rt

def loadpy(msg, QQ, GroupID, file):
    exec(open(file, 'r').read(), globals(), {'msg': msg, 'QQ': QQ, 'GroupID': GroupID})

_cbk = customize.copy()
for _c in _cbk.keys():
    _cbk[_c] = globals()[_cbk[_c]]
_initx = globals().copy()
for _initn in _initx.keys():
    if _initn[:6] == "gmeth_" and type(_initx[_initn]).__name__=='function':
        _cbk.update({_initn: _initx[_initn]})
_cbkl1 = _cbk.copy()
def Group(msg, QQ, GroupID):
    '''
    Old Method: 
    ShutUp(msg, QQ, GroupID)
    LoginBilibili(msg, QQ, GroupID)
    Weather(msg, QQ, GroupID)
    Calc(msg, QQ, GroupID)
    Menu(msg, QQ, GroupID)
    '''
    _cbk = _cbkl1.copy()
    _initgb = glob.glob('./plugin/pfile/*.py')
    for _initf in _initgb:
        _initp = os.path.splitext(_initf)[0].replace('\\', '/').split('/')[-1]
        globals().update({_initp:(lambda msg, QQ, GroupID: loadpy(msg, QQ, GroupID, os.path.abspath(_initf)))})
        _cbk.update({_initp: globals().copy()[_initp]})
    _initphp = glob.glob('./plugin/php/*.php')
    for _initf in _initphp:
        _initp = os.path.splitext(_initf)[0].replace('\\', '/').split('/')[-1]
        globals().update({_initp:(lambda msg, QQ, GroupID: loadphp(msg, QQ, GroupID, os.path.abspath(_initf)))})
        _cbk.update({_initp: globals().copy()[_initp]})
    for _stepx in _cbk.values():
        _stepx(msg, QQ, GroupID)
