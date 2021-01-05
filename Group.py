# -*- coding: UTF-8 -*-

import json
import itertools
import urllib
import base64
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
from sympy import *
from PIL import Image
from urllib import request
import requests
import io
import glob
import zhconv
import os
class sql:
    def read(a):
        return [['admin']]

class POST:
    def GroupMsg(msg, groupid = 0, picurl = 0, picbase = 0):
        print(msg)
        if picbase != 0:
            a = io.BytesIO(base64.decodebytes(picbase.encode()))
            Image.open(a).show()
        

def ShutUp(msg, QQ, GroupID):
    import json
    if "/禁言" in msg and QQ != config['botqq']:
        Adminer = sql.read('SELECT * FROM Admin;')
        if str(QQ) in list(itertools.chain.from_iterable([list(x) for x in Adminer])):
            try:
                shutupuserid = json.loads(msg)['UserID'][0]
                time = json.loads(msg)['Content'].split(' ')[2]
            except:
                POST.GroupMsg(msg='缺少参数', groupid=GroupID, picurl=0, picbase=0)
                return
            POST.SetShutUpUser(qq=shutupuserid, time=time, groupid=GroupID)
            POST.GroupMsg(msg='操作成功', groupid=GroupID, picurl=0, picbase=0)
        else:
            POST.GroupMsg(msg='非许可用户,不可使用该命令',
                          groupid=GroupID, picurl=0, picbase=0)


def LoginBilibili(msg, QQ, GroupID):
    if msg == msg.split()[0] == "/御坂登录":
        POST.GroupMsg(msg='请私聊我发送“/御坂登录”登录哦',
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
    oldmsg = msg
    msg = zhconv.convert(msg, "zh-hans")
    if msg != oldmsg:
        tflag = True
    else:
        tflag = False
    if msg.split()[0] == "/查询天气" and len(msg.split()) < 4 and len(msg.split()) > 1:
        city = msg.split()[1].replace("'", "").lower().replace(' ', '')
        if '#' in city or '--' in city or '"' in city:
            POST.GroupMsg(msg=zhconv.convert("请不要尝试进行SQL注入。\n怀疑违规行为已经向所有风纪委员通报。", {
                          True: "zh-hant", False: "zh-hans"}[tflag]), groupid=GroupID, picurl=0, picbase=0)
            POST.GroupMsg(msg="QQ号为"+str(QQ)+"的用户怀疑正在进行SQL注入，请注意且自行判断其违规行为并予以惩罚。\n消息内容: \n" +
                          msg, groupid=872324801, picurl=0, picbase=0)
        else:
            sqlr = sql.read('SELECT * FROM city WHERE cityZh = "' +
                            city+'" or cityEn = "'+city+'"')
            if len(sqlr) == 0:
                sqlr2 = sql.read(
                    'SELECT * FROM city WHERE provinceZh = "'+city+'" or provinceEn = "'+city+'"')
                if len(sqlr2) > 0:
                    POST.GroupMsg(msg=zhconv.convert("请输入具体城市名作为参数。属于"+sqlr2[0][4]+"省的城市有: \n"+", ".join([x[2] for x in sql.read(
                        'SELECT * FROM city WHERE provinceZh="'+city+'" or provinceEn="'+city+'"')])+"。", {True: "zh-hant", False: "zh-hans"}[tflag]), groupid=GroupID, picurl=0, picbase=0)
                else:
                    POST.GroupMsg(msg=zhconv.convert("无查询结果。\n请确认是否有错别字或者拼写错误。", {
                                  True: "zh-hant", False: "zh-hans"}[tflag]), groupid=GroupID, picurl=0, picbase=0)
            else:
                seindex = 0
                if len(sqlr) > 1:
                    try:
                        seindex = int(msg.split()[2]) - 1
                        if seindex < 0:
                            POST.GroupMsg(msg=zhconv.convert("请提供一个大于0的数字作为索引。", {
                                          True: "zh-hant", False: "zh-hans"}[tflag]), groupid=GroupID, picurl=0, picbase=0)
                            return
                        elif seindex > len(sqlr)-1:
                            POST.GroupMsg(msg=zhconv.convert("索引超出检索范围，请检查索引。", {
                                          True: "zh-hant", False: "zh-hans"}[tflag]), groupid=GroupID, picurl=0, picbase=0)
                            return
                    except ValueError:
                        POST.GroupMsg(msg=zhconv.convert("请提供一个大于0的数字作为索引。", {
                                      True: "zh-hant", False: "zh-hans"}[tflag]), groupid=GroupID, picurl=0, picbase=0)
                        return
                    except IndexError:
                        POST.GroupMsg(msg=zhconv.convert("搜索字眼拥有多于1个匹配结果, 请把序号填入第三个参数中区分。\n"+"\n".join([str(x+1)+": "+sqlr[x][2]+" - "+sqlr[x][8]+" - "+sqlr[x][4] for x in range(
                            len(sqlr))]), {True: "zh-hant", False: "zh-hans"}[tflag]), groupid=GroupID, picurl=0, picbase=0)
                        return
                raw = json.loads(urllib.request.urlopen(
                    "https://tianqiapi.com/api?version=v6&appid=18224395&appsecret=lgCc5VqI&cityid="+str(sqlr[seindex][0])).read())
                rtst = sqlr[0][2]
                if len(sqlr) > 1:
                    rtst += " (%s)" % sqlr[seindex][4]
                rtst += "的天气状况: \n"
                rtst += "温度: " + \
                    str(raw['tem'])+"℃ ("+str(raw['tem2']) + \
                    "℃-"+str(raw['tem1'])+"℃)\n"
                rtst += "湿度："+raw['humidity']+'\n'
                rtst += raw['wea']+'\n'
                rtst += "吹"+raw['win']+' '+raw['win_speed']
                try:
                    picf = open('./plugin/weather/' +
                                raw['wea_img']+'.png', 'rb').read()
                    pbase = base64.b64encode(picf).decode()
                    rtst += '\n[PICFLAG]'
                except:
                    pbase = 0
                POST.GroupMsg(msg=zhconv.convert(rtst, {
                              True: "zh-hant", False: "zh-hans"}[tflag]), groupid=GroupID, picurl=0, picbase=pbase)


def Calc(msg, QQ, GroupID):
    if msg.split()[0] == "/计算" and len(msg.split())>1 and len(msg.split())<4:
        transformations = (standard_transformations + (implicit_multiplication_application,))
        rmsg = msg[1:]
        def get_concat_v_blank(im1, im2, color=(255, 255, 255, 0)):
            dst = Image.new('RGBA', (max(im1.width, im2.width), im1.height + im2.height + 50), color)
            dst.paste(im1, (0, 0))
            dst.paste(im2, (0, im1.height+50))
            return dst
        def parse(s, e=True):
            return parse_expr(s, transformations=transformations, evaluate = e)
        expo = msg.split()[1]
        if expo.lower() in ['解方程','因式分解','一般计算', 'alg', 'factor', 'calc']:
            meth = {'解方程':0,'因式分解':1,'一般计算':2, 'alg':0, 'factor':1, 'calc':2}[expo.lower()]
            msg = msg[1:]
            exp = msg.split()[1]
            exp2 = exp.replace("^","**").replace(" ","").split("=")
            if len(exp2) == 1:
                if meth == 0:
                    meth = 2
            else:
                if meth == 1 or meth == 2:
                    POST.GroupMsg(msg= "请检查输入!", groupid = GroupID, picurl = 0, picbase = 0)
                    return
        else:
            exp = msg.split()[1]
            exp2 = exp.replace("^","**").replace(" ","").split("=")
            if len(exp2) == 1:
                meth = 2
            else:
                meth = 0
        try:
            u=msg.split()[2]
        except:
            u=None
        exp = exp.replace("^","**").replace(" ","")
        exp = exp.split("=")
        if meth == 2:
            try:
                f = latex(parse(exp[0]))
                with evaluate(False):
                    v = latex(parse(exp[0], False))
                u = v + "=" + f
                img = base64.b64encode(request.urlopen("http://latex2png.com"+eval(requests.post("http://latex2png.com/api/convert", json = {"auth":{"user":"guest","password":"guest"},"latex":u,"resolution":600,"color":"000000"}).text)['url']).read()).decode()
                POST.GroupMsg(msg = "结果: "+str(parse(exp[0]))+'\n[PICFLAG]', groupid = GroupID, picurl = 0, picbase = img)
            except BaseException as e:
                raise e
                POST.GroupMsg(msg = "可能无解, 或者输入错误, 或者程式不支援", groupid = GroupID, picurl = 0, picbase = 0)
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
                v = sympy.factor(expres)
                b6e2 = request.urlopen("http://latex2png.com"+eval(requests.post("http://latex2png.com/api/convert", json = {"auth":{"user":"guest","password":"guest"},"latex":latex(v),"resolution":600,"color":"000000"}).text)['url'])
                POST.GroupMsg(msg = '解: '+str(v).replace("**", '^')+"\n[PICFLAG]", groupid=GroupID, picurl = 0, picbase = base64.encodebytes(b6e2).decode())
            except BaseException as e:
                POST.GroupMsg(msg = "可能无法分解, 或者输入错误, 或者程式不支援", groupid = GroupID, picurl = 0, picbase = 0)
        else:
            return POST.GroupMsg(msg = "程式不支援", groupid = GroupID, picurl = 0, picbase = 0)

def Menu(msg, QQ, Group):
    cfg = [
        {"desc": "查询天气", "help":"/查询天气 {城市名} {索引}", "priv":False, "callback":Weather, "cmd":"/查询天气"},
        {"desc": "登录哔哩哔哩", "help":"/御坂登录", "priv":False, "callback":LoginBilibili, "cmd":"/御坂登录"},
        {"desc": "群管", "help":"/禁言 @某人 时间", "priv":True, "callback":ShutUp, "cmd":"/禁言"},
        {"desc": "测试", "help":"/测试 [参数]", "priv":True, "callback":gmeth_test, "cmd":"/测试"}
    ]
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
    if msg.split()[0] == "/御坂菜单" and len(msg.split())==1:
        POST.GroupMsg(msg=menu, groupid=Group, picbase=0, picurl=0)
    elif msg.split()[0] == "/御坂菜单":
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
    if msg.split()[0] == '/测试':
        ret = "OK\n参数: "+','.join(msg.split()[1:])
        POST.GroupMsg(msg=ret, groupid=GroupID, picbase=0, picurl=0)

#函数区结束

#初始化

customize = {"Weather": Weather,
    "ShutUp": ShutUp,
    "LoginBilibili": LoginBilibili,
    "Calc": Calc,
    "Menu": Menu}


_cbk = customize.copy()
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
    _initgb = glob.glob('./plugins/pfile/*.py')
    for _initf in _initgb:
        _initp = os.path.splitext(_initf)[0].split('/')[-1]
        globals().update({_initp:(lambda msg, QQ, GroupID: exec(open(_initf).read(), globals(), {'msg': msg, 'QQ': QQ, 'GroupID': GroupID}))})
        _cbk.update({_initp: globals().copy()[_initp]})
    for _stepx in _cbk.values():
        _stepx(msg, QQ, GroupID)
