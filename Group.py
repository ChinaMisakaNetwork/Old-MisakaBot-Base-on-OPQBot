# -*- coding: UTF-8 -*-

import json
import itertools
import urllib
import base64
import api
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
from sympy import parse_expr, latex, evaluate, latex, Eq, solve, factor, plot
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
from bs4 import BeautifulSoup
import lxml
import time
import Tools

f = open('./config.json')
config = json.loads(f.read())['BotConfig']
f.close()
POST = api.PostMsg(url=config['server'], botqq=config['botqq'])
MasterGroup = config['MasterGroup']


# 函数区开始

def ShutUp(msg, QQ, GroupID):
    import json
    if "yb.jy" in msg and QQ != config['botqq']:
        Adminer = sql.read(f'SELECT * FROM {GroupID}_Admin;')
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
                sqllist = sql.read(f'SELECT * {GroupID}_FROM Violation;')
                if str(shutupuserid) in str(sqllist):
                    edtimes = sql.read(f'SELECT WarningTimes FROM {GroupID}_Violation WHERE QQ="{shutupuserid}";')[0][0]
                    sql.write(f'UPDATE {GroupID}_Violation SET WarningTimes={edtimes + 1} WHERE QQ="{shutupuserid}";')
                else:
                    sql.write(f'INSERT INTO {GroupID}_Violation VALUES ("{shutupuserid}",1);')

            if str(GroupID) == MasterGroup:
                import time
                nowtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
                sqlcode = f'INSERT INTO {GroupID}_ShutUplog (time,type,shutuptime,who,QQ) VALUES ("{nowtime}","Shutup","{int(shutuptime)}","{str(QQ)}","{str(shutupuserid)}");'
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
    # Adminer = sql.read('SELECT * FROM Admin;')
    if str(QQ) == str(config['botqq']):
        return
    else:
        POST.CheHui(GroupID=GroupID, MsgSeq=MsgSeq, MsgRandom=MsgRandom)
        POST.GroupMsg(msg=f'@{NickName} 监测到违规信息,请注意文明聊天,类型为{Type}',
                      groupid=GroupID, picurl=0, picbase=0)
        POST.SetShutUpUser(
            qq=QQ, time=config['TextShutupTime'], groupid=GroupID)


def Weather(msg, QQ, GroupID):
    if msg.split()[0] == "yb.tq":
        Content = Tools.weather(msg.split()[1])
        if Content:
            message = "{}当前{}，{}度，{}{}，空气质量指数{}".format(Content["cityname"], Content["weather"], Content["temp"],
                                                        Content["WD"], Content["WS"], Content["aqi"])
        else:
            message = "请输入正确的市级行政区"
        POST.GroupMsg(msg=message, groupid=GroupID, picbase=0, picurl=0)


def hitokoto(msg, QQ, GroupID):
    Mainurl = 'https://v1.hitokoto.cn/'
    if msg.split(' ')[0] == "yb.my":
        Typelist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
        Typelist2 = ['动画', '漫画', '游戏', '文学', '原创', '来自网络', '其他', '影视', '诗词', '网易云', '哲学', '抖机灵']

        try:
            Type = msg.split(' ')[1]
        except:
            POST.GroupMsg(msg='缺失参数', groupid=GroupID, picbase=0, picurl=0)
            return

        if Type == '类别':
            POST.GroupMsg(msg=str(Typelist2), groupid=GroupID, picbase=0, picurl=0)
            return

        try:
            CodeTypeindex = Typelist2.index(Type)
        except:
            POST.GroupMsg(msg='无此类别', groupid=GroupID, picbase=0, picurl=0)
            return

        CodeType = Typelist[CodeTypeindex]
        jsonstr = json.loads(requests.get(Mainurl + f'?c={CodeType}').text)
        if jsonstr['from_who'] == None:
            saying = jsonstr['hitokoto'] + '----' + jsonstr['from']
        else:
            saying = jsonstr['hitokoto'] + '----' + jsonstr['from'] + ' ' + jsonstr['from_who']
        POST.GroupMsg(msg=saying, groupid=GroupID, picbase=0, picurl=0)


def Calc(msg, QQ, GroupID):
    msg = msg.replace("^", "**")
    if msg.split()[0] == "yb.js" and len(msg.split()) > 1:
        transformations = (standard_transformations + (implicit_multiplication_application,))

        # rmsg = msg[1:]
        def get_concat_v_blank(im1, im2, color=(255, 255, 255, 0)):
            dst = Image.new('RGBA', (max(im1.width, im2.width), im1.height + im2.height + 50), color)
            dst.paste(im1, (0, 0))
            dst.paste(im2, (0, im1.height + 50))
            return dst

        def parse(s, e=True):
            return parse_expr(s, transformations=transformations, evaluate=e)

        expo = msg.split()[1]
        msg = msg.split()
        if expo.lower() in ['解方程', '因式分解', '一般计算', '画图', 'alg', 'factor', 'calc', 'plot']:
            meth = {'解方程': 0, '因式分解': 1, '一般计算': 2, '画图': 3, 'alg': 0, 'factor': 1, 'calc': 2, 'plot': 3}[expo.lower()]
            msg = msg[1:]
            exp = msg[1]
            exp2 = exp.replace("^", "**").replace(" ", "").split("=")
            if len(exp2) == 1:
                if meth == 0:
                    meth = 2
            else:
                if meth == 1 or meth == 2:
                    POST.GroupMsg(msg="请检查输入!", groupid=GroupID, picurl=0, picbase=0)
                    return
        else:
            POST.GroupMsg(msg="请检查输入!", groupid=GroupID, picurl=0, picbase=0)
            return
        try:
            u = msg[2]
        except:
            u = None
        exp = exp.replace("^", "**").replace(" ", "")
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
                img = base64.b64encode(request.urlopen("http://latex2png.com" + eval(
                    requests.post("http://latex2png.com/api/convert",
                                  json={"auth": {"user": "guest", "password": "guest"}, "latex": u, "resolution": 600,
                                        "color": "000000"}).text)['url']).read()).decode()
                POST.GroupMsg(msg="结果: " + str(parse(exp[0])) + '\n[PICFLAG]', groupid=GroupID, picurl=0, picbase=img)
            except BaseException as e:
                POST.GroupMsg(msg="可能无解, 或者输入错误, 或者程式不支援", groupid=GroupID, picurl=0, picbase=0)
                raise e
        elif meth == 0:
            try:
                equat = Eq(parse(exp[0]), parse(exp[1]))
                if u != None:
                    u = parse(u)
                    if not (u in list(parse(exp[0]).free_symbols) + list(parse(exp[1]).free_symbols)):
                        u = None
                if u == None:
                    solv = solve(equat, dict=True)
                else:
                    solv = solve(equat, u, dict=True)
                if len(solv) > 0:
                    rtlist = []
                    imgs = []
                    for x in solv:
                        var = list(x.keys())[0]
                        res = list(x.values())[0]
                        ltv = latex(var)
                        ltr = latex(res)
                        lt = ltv + '=' + ltr
                        imgs.append(Image.open(request.urlopen("http://latex2png.com" + eval(
                            requests.post("http://latex2png.com/api/convert",
                                          json={"auth": {"user": "guest", "password": "guest"}, "latex": lt,
                                                "resolution": 600, "color": "000000"}).text)['url'])))
                        rtlist.append(str(var) + "=" + str(res))
                    fimg = imgs[0]
                    del imgs[0]
                    for x in imgs:
                        fimg = get_concat_v_blank(fimg, x)
                    buffer = io.BytesIO()
                    fimg.save(buffer, format='PNG')
                    b6e = base64.b64encode(buffer.getvalue()).decode()
                    POST.GroupMsg(msg="解: \n" + " 或\n".join(rtlist) + "\n[PICFLAG]", groupid=GroupID, picurl=0,
                                  picbase=b6e)
                else:
                    POST.GroupMsg(msg="可能无解, 或者输入错误", groupid=GroupID, picurl=0, picbase=0)
            except BaseException as e:
                POST.GroupMsg(msg="可能无解, 或者输入错误, 或者程式不支援", groupid=GroupID, picurl=0, picbase=0)
        elif meth == 1:
            try:
                expres = parse(exp[0])
                try:
                    with evaluate(False):
                        ov = latex(parse(exp[0]))
                except:
                    ov = latex(parse(exp[0]))
                v = factor(expres)
                b6e2 = request.urlopen("http://latex2png.com" + eval(requests.post("http://latex2png.com/api/convert",
                                                                                   json={"auth": {"user": "guest",
                                                                                                  "password": "guest"},
                                                                                         "latex": ov + '=' + latex(v),
                                                                                         "resolution": 600,
                                                                                         "color": "000000"}).text)[
                    'url']).read()
                POST.GroupMsg(msg='解: ' + str(v).replace("**", '^') + "\n[PICFLAG]", groupid=GroupID, picurl=0,
                              picbase=base64.encodebytes(b6e2).decode())
            except BaseException as e:
                POST.GroupMsg(msg="可能无法分解, 或者输入错误, 或者程式不支援", groupid=GroupID, picurl=0, picbase=0)
                raise (e)
        elif meth == 3:
            udata = msg[1:]
            xy1 = []
            xy2 = set()
            xy3 = {}
            if len(udata) < 3:
                POST.GroupMsg(msg="请检查输入", groupid=GroupID, picurl=0, picbase=0)
                return
            try:
                axis = int(udata[-1])
                symb = parse(udata[-2])
            except ValueError:
                POST.GroupMsg(msg="请检查输入", groupid=GroupID, picurl=0, picbase=0)
                return
            udata = udata[:-2]
            for xyc1 in udata:
                if '=' in xyc1:
                    xtc = xyc1.split('=')
                    if len(parse(xtc[0]).free_symbols) + len(parse(xtc[1]).free_symbols) > 2:
                        POST.GroupMsg(msg="程式暂不支援", groupid=GroupID, picurl=0, picbase=0)
                        return
                    elif len(parse(xtc[0]).free_symbols) + len(parse(xtc[1]).free_symbols) >= 1:
                        lt = list(parse(xtc[0]).free_symbols) + list(parse(xtc[1]).free_symbols)
                        for n in lt:
                            if n in xy3.keys():
                                xy3[n].append(solve(Eq(parse(xtc[0]), parse(xtc[1])), n))
                            else:
                                xy3.update({n: [solve(Eq(parse(xtc[0]), parse(xtc[1])), n)]})
                else:
                    POST.GroupMsg(msg="程式暂不支援", groupid=GroupID, picurl=0, picbase=0)
                    return
            if len(xy2) > 1:
                POST.GroupMsg(msg="程式暂不支援", groupid=GroupID, picurl=0, picbase=0)
                return
            else:
                if len(xy3.keys()) > 2 or not (symb in xy3.keys()):
                    POST.GroupMsg(msg="程式暂不支援", groupid=GroupID, picurl=0, picbase=0)
                    return
                try:
                    x5 = list(xy3.keys())
                    x5.remove(list(xy2)[0])
                    if len(x5) != 1:
                        POST.GroupMsg(msg="程式暂不支援", groupid=GroupID, picurl=0, picbase=0)
                        return
                    for x4 in xy3[x5[0]]:
                        [xy1.append(x6) for x6 in x4]
                except:
                    pass
            fsym = list(xy3.keys())
            fsym.remove(symb)
            xy8 = list(itertools.chain.from_iterable(xy3[fsym[0]]))
            subs = [[str(x) for x in xy8], str(symb), axis, str(symb), str(fsym[0])]
            res = eval(
                subprocess.getoutput("python ./plugin/Calc/Plot.py " + base64.b64encode(repr(subs).encode()).decode()))
            POST.GroupMsg(msg=res[0], groupid=GroupID, picbase=res)
        else:
            POST.GroupMsg(msg="程式不支援", groupid=GroupID, picurl=0, picbase=0)


def Menu(msg, QQ, Group):
    if msg.split()[0] != "御坂菜单":
        return
    cfg = json.loads(open('./plugin/settings.json', encoding='utf-8').read())['menu']
    uauser = []
    for item in cfg:
        if not item["priv"]:
            uauser.append(item)
    Adminer = sql.read(f'SELECT * FROM {Group}_Admin;')
    if str(QQ) in list(itertools.chain.from_iterable([list(x) for x in Adminer])):
        unuser = cfg
    else:
        unuser = uauser
    menu = "御坂御坂可以帮您做这些事情哦:\n" + "\n".join(
        ["%d. %s (%s)" % (ct + 1, unuser[ct]['desc'], unuser[ct]['help']) for ct in range(len(unuser))])
    if len(msg.split()) == 1:
        POST.GroupMsg(msg=menu, groupid=Group, picbase=0, picurl=0)
        return
    else:
        try:
            mm = int(msg.split()[1])
            if mm > 0 and mm < len(unuser) + 1:
                mg = msg.split()[2:]
                me = unuser[mm - 1]['cmd']
                mr = me + ' ' + " ".join(mg)
                unuser[mm - 1]['callback'](mr, QQ, Group)
            else:
                POST.GroupMsg(msg=menu, groupid=Group, picbase=0, picurl=0)
                return
        except:
            raise


def gmeth_test(msg, QQ, GroupID):
    if msg.split()[0] == 'yb.test':
        ret = "OK\n参数: " + ','.join(msg.split()[1:])
        POST.GroupMsg(msg=ret, groupid=GroupID, picbase=0, picurl=0)
        return


def Blockbyman(msg, QQ, GroupID):
    try:
        json_parsing = json.loads(msg)
        if "yb.ch" in json_parsing["Content"]:
            adminlist = sql.read(f'select * from {GroupID}_Admin;')
            if str(QQ) in list(itertools.chain.from_iterable([list(x) for x in adminlist])):
                msgse = json_parsing["MsgSeq"]
                msg_dt2 = sql.read(f'select msgran, id from {GroupID}_log where msgseq=' + str(msgse) + ';')[0]
                msgran = msg_dt2[0]
                idmsg = msg_dt2[1]
                print("DT2", msg_dt2)
                print("Ran", msgran, "id", idmsg)
                if not sql.read(f'select Chehui from {GroupID}_log where id=' + str(idmsg))[0][0]:
                    POST.CheHui(GroupID=GroupID, MsgSeq=msgse, MsgRandom=msgran)
                    sql.write(f'UPDATE {GroupID}_log SET Chehui=1 WHERE id={idmsg};')
                    flag1 = True
                else:
                    flag1 = False
                print("Rollback status", flag1)
                recnum = 0
                def rec_dele(msgseqrec, totalnum=0, fg=0, recnum=0):
                    newl = sql.read(f'select id, msgseq, msgran from {GroupID}_log where Replyseq=' + str(msgseqrec))
                    totalnum += len(newl)
                    print("rec1", newl)
                    for x in newl:
                        idr = x[0]
                        msgseqr = x[1]
                        msgranr = x[2]
                        if not sql.read(f'select Chehui from {GroupID}_log where id=' + str(idr))[0][0]:
                            POST.CheHui(GroupID=GroupID, MsgSeq=msgseqr, MsgRandom=msgranr)
                            sql.write(f'UPDATE {GroupID}_log SET Chehui=1 WHERE id={idr};')
                        else:
                            fg += 1
                    for x in newl:
                        arr = rec_dele(x[1], totalnum=totalnum, fg=fg, recnum = recnum + 1)
                        print('arrrecins', arr)
                        totalnum += arr[0]
                        fg += arr[1]
                        print(recnum, totalnum, fg)
                    return [totalnum, fg]

                arr2 = rec_dele(msgse)
                totalnum = arr2[0]
                fg = arr2[1]
                tmsg = ""
                if flag1:
                    tmsg += '撤回成功'
                else:
                    tmsg += '消息已被发送者本人撤回'
                if totalnum == 0:
                    tmsg += '。'
                else:
                    if not fg:
                        tmsg += ', 另 所有回复此消息的消息已被全部撤回。'
                    else:
                        tmsg += ', 另 在回复此消息的消息中, 共有' + str(fg) + '调被消息发送者本人撤回, 其他均已成功撤回。'
                POST.GroupMsg(msg=tmsg, groupid=GroupID, picurl=0, picbase=0)
            else:
                POST.GroupMsg(msg='权限不足。 请联系风纪委员处理请求。', groupid=GroupID, picurl=0, picbase=0)
    except Exception as e:
        if "yb.ch" in msg and QQ != config['botqq']:
            Adminer = sql.read(f'SELECT * FROM {GroupID}_Admin;')
            if str(QQ) in list(itertools.chain.from_iterable([list(x) for x in Adminer])):

                try:
                    msgid = msg.split(' ')[1]
                    if msgid == '':
                        POST.GroupMsg(msg='缺少参数', groupid=GroupID, picurl=0, picbase=0)
                        return

                except:
                    POST.GroupMsg(msg='缺少参数', groupid=GroupID, picurl=0, picbase=0)
                    return

                msglist = sql.read(f'SELECT msgseq,msgran FROM {GroupID}_log WHERE id={msgid}')
                if msglist == ():
                    POST.GroupMsg(msg='不存在的消息', groupid=GroupID, picurl=0, picbase=0)
                    return
                else:
                    chehui = sql.read(f'SELECT Chehui FROM {GroupID}_log WHERE id={msgid}')[0][0]
                    if chehui == 0:
                        MsgSeq = msglist[0][0]
                        MsgRandom = msglist[0][1]
                        POST.CheHui(GroupID=GroupID, MsgSeq=MsgSeq, MsgRandom=MsgRandom)
                        flagc = True
                    else:
                        flagc = False
                    print("rollback status 2", flagc)
                    print("seq", MsgSeq, "ran", MsgRandom, "id", msgid)
                    sql.write(f'UPDATE {GroupID}_log SET Chehui=1 WHERE id={msgid};')

                    def rec_del(msgs, totalnum=0, fg=0):
                        newlist = sql.read(f'select id, msgseq, msgran from log where Replyseq={msgs}')
                        print('recur', newlist)
                        totalnum += len(newlist)
                        for x in newlist:
                            idr = x[0]
                            msgseqr = x[1]
                            msgranr = x[2]
                            if not sql.read(f'select {GroupID}_Chehui from log where id=' + str(idr))[0][0]:
                                POST.CheHui(GroupID=GroupID, MsgSeq=msgseqr, MsgRandom=msgranr)
                                sql.write(f'UPDATE {GroupID}_log SET Chehui=1 WHERE id={idr};')
                            else:
                                fg += 1
                        for x in newlist:
                            arr3 = rec_del(x[1])
                            totalnum += arr3[0]
                            fg += arr3[1]
                        return [totalnum, fg]

                    arr4 = rec_del(MsgSeq)
                    totalnum = arr4[0]
                    fg = arr4[1]
                    tmsg = ""
                    if flagc:
                        tmsg += '撤回成功'
                    else:
                        tmsg += '消息已被发送者本人撤回'
                    if totalnum == 0:
                        tmsg += '。'
                    else:
                        if not fg:
                            tmsg += ', 另 所有回复此消息的消息已被全部撤回。'
                        else:
                            tmsg += ', 另 在回复此消息的消息中, 共有' + str(fg) + '调被消息发送者本人撤回, 其他均已成功撤回。'
                    POST.GroupMsg(msg=tmsg, groupid=GroupID, picurl=0, picbase=0)


def SiteTools(msg, QQ, GroupID):
    if "yb.site" in msg and msg.split()[0] == "yb.site":

        # 判断是否有参数
        try:
            cansu = msg.split()[1]
        except:
            POST.GroupMsg(msg='没有参数,请用yb.site 菜单 来查询', groupid=GroupID, picbase=0, picurl=0)
            return

        if msg.split()[1] == "菜单":
            msg = "[T]站长工具\n● yb.site Ping [域名/IP]\n● yb.site 扒站 [地址]\n● yb.site 短链接 [链接]\n● yb.site 二维码 [内容]\n● yb.site 备案查询 [域名]\n● yb.site 收录查询 [域名]\n● yb.site 报毒检测 [域名/IP]"
            POST.GroupMsg(msg=msg, groupid=GroupID, picbase=0, picurl=0)

        if msg.split()[1] == "Ping" or msg.split()[1] == "ping":
            try:
                ip = msg.split()[2]
            except:
                POST.GroupMsg(msg='缺失参数', groupid=GroupID, picbase=0, picurl=0)
                return
            if '.' in ip:
                url = "https://api.tx7.co/api/pingspeed/?host=" + ip
                response = requests.get(url).json()
                if response["code"] == 200:
                    msg = "{}！\n查询域名: {}\nIP地址: {}\nIP信息: {}\n平均延迟: {}\n最低延迟: {}\n最高延迟: {}\n检测节点: {}".format(
                        response["msg"], response["host"], response["ip"], response["location"],
                        response["ping_time_avg"], response["ping_time_min"], response["ping_time_max"],
                        response["node"])
                elif response["code"] == 201:
                    msg = "{}！\n查询域名: {}\n错误信息: {}".format(response["msg"], ip, response["tips"])
                else:
                    msg = response["msg"] + "！"
            else:
                msg = "请输入正确的域名！"
            POST.GroupMsg(msg=msg, groupid=GroupID, picbase=0, picurl=0)

        if msg.split()[1] == "备案查询":
            try:
                domain = msg.split()[2]
            except:
                POST.GroupMsg(msg='缺失参数', groupid=GroupID, picbase=0, picurl=0)
                return
            if '.' in domain:
                url = "https://api.muxiaoguo.cn/api/ICP?&url=" + domain
                response = requests.get(url).json()
                if response["code"] == 200:
                    data = response["data"]
                    msg = "查询成功！\n查询域名: {}\n单位名称: {}\n备案性质: {}\n备案号: {}\n网站名称: {}\n首页域名: {}\n审核日期: {}".format(
                        data["url"], data["organizer_name"], data["nature"], data["license"], data["website_name"],
                        data["website_home"], data["audit_time"])
                elif response["code"] == -5:
                    msg = "域名{}未查询到备案信息！".format(domain)
                else:
                    msg = response["msg"] + "！"
            else:
                msg = "请输入正确的域名！"
            POST.GroupMsg(msg=msg, groupid=GroupID, picurl=0, picbase=0)

        if msg.split()[1] == '收录查询':
            try:
                domain = msg.split()[2]
            except:
                POST.GroupMsg(msg='缺失参数', groupid=GroupID, picbase=0, picurl=0)
                return
            if '.' in domain:
                url = "https://api.tx7.co/api/Included/?url=" + domain
                response = requests.get(url).json()
                if response["code"] == 200:
                    msg = "\n查询域名: {}\n百度收录: {}\n搜狗收录: {}\n好搜收录: {}".format(domain, str(response["baidu"]),
                                                                            str(response["sogou"]),
                                                                            str(response["haosōu"]))
                else:
                    msg = "查询错误！"
            else:
                msg = "\n请输入正确的域名！"
            POST.GroupMsg(msg=msg, groupid=GroupID, picurl=0, picbase=0)

        if msg.split()[1] == '二维码':
            try:
                domain = msg.split()[2]
            except:
                POST.GroupMsg(msg='缺失参数', groupid=GroupID, picbase=0, picurl=0)
                return
            url = "https://cli.im/api/qrcode/code?text={}&mhid=vUfOWV3rmcshMHYtI9VSPqk".format(domain)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, features='lxml')
            qrcode_link = "https:" + soup.find_all("img", {"class": "qrcode_plugins_img"})[0]['src']
            suo_url = "http://api.suowo.cn/api.htm"
            suo_data = {
                "url": qrcode_link,
                "key": "60b1fbcef1dda66d0d39171e@d47200b44492a4bad97b24404345a567",
                "expireDate": "2030-03-31"
            }
            suo = requests.get(suo_url, params=suo_data).text
            msg = "请求成功！\n请求内容: {}\n二维码链接: {}".format(domain, suo)
            POST.GroupMsg(msg=msg, groupid=GroupID, picurl=0, picbase=0)

        if msg.split()[1] == '报毒检测':
            try:
                domain = msg.split()[2]
            except:
                POST.GroupMsg(msg='缺失参数', groupid=GroupID, picbase=0, picurl=0)
                return
            if '.' in domain:
                url = "https://www.oplog.cn/tx.php?url=" + domain
                response = requests.get(url).json()
                if response["type"] == 1:
                    msg = "检测域名: {}\n域名状态: 正常".format(response["url"])
                elif response["type"] == 3:
                    msg = "检测域名: {}\n域名状态: 正常".format(response["url"])
                else:
                    msg = "检测域名: {}\n域名状态: 拦截\n拦截提示: {}\n拦截原因: {}".format(response["url"], response["word"],
                                                                          response["wordtit"])
            else:
                msg = "请输入正确的域名！"
            POST.GroupMsg(msg=msg, groupid=GroupID, picurl=0, picbase=0)

        if msg.split()[1] == '扒站':
            try:
                domain = msg.split()[2]
            except:
                POST.GroupMsg(msg='缺失参数', groupid=GroupID, picbase=0, picurl=0)
                return
            if not (("http://" in domain) or ("https://" in domain)):
                domain = "http://" + domain
            if '.' in domain:
                url = "https://xiaojieapi.com/api/v1/get/wget?url=" + domain
                response = requests.get(url).json()
                if response["code"] == 200:
                    POST.GroupMsg(msg='正在处理，请稍后...', groupid=GroupID, picurl=0, picbase=0)
                    for i in range(10):
                        time.sleep(4)
                        response = requests.get(url).json()
                        if response.get("url"):
                            suo_url = "http://api.suowo.cn/api.htm"
                            suo_data = {
                                "url": response["url"],
                                "key": "60b1fbcef1dda66d0d39171e@d47200b44492a4bad97b24404345a567",
                                "expireDate": "2030-03-31"
                            }
                            suo = requests.get(suo_url, params=suo_data).text
                            msg = "请求成功！\n请求地址: {}\n下载链接: {}".format(domain, suo)
                            break
                    if not response.get("url"):
                        msg = "请求失败，请尝试添加协议头！"
                else:
                    msg = "请求失败，请检查站点信息后重试！"
            else:
                msg = "请输入正确的域名！"
            POST.GroupMsg(msg=msg, groupid=GroupID, picurl=0, picbase=0)

        if msg.split()[1] == '短链接':
            try:
                uri = msg.split()[2]
            except:
                POST.GroupMsg(msg='缺失参数', groupid=GroupID, picbase=0, picurl=0)
                return
            if not (("http://" in uri) or ("https://" in uri)):
                uri = "http://" + uri
            if '.' in uri:
                suo_url = "http://api.suowo.cn/api.htm"
                suo_data = {
                    "url": uri,
                    "key": "60b1fbcef1dda66d0d39171e@d47200b44492a4bad97b24404345a567",
                    "expireDate": "2030-03-31"
                }
                suo = requests.get(suo_url, params=suo_data).text
                msg = "请求成功！\n原链接: {}\n短链接: {}".format(uri, suo)
            else:
                msg = "请输入正确的链接！"
            POST.GroupMsg(msg=msg, groupid=GroupID, picurl=0, picbase=0)


# 函数区结束

# 初始化

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
    if _initn[:6] == "gmeth_" and type(_initx[_initn]).__name__ == 'function':
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
        globals().update({_initp: (lambda msg, QQ, GroupID: loadpy(msg, QQ, GroupID, os.path.abspath(_initf)))})
        _cbk.update({_initp: globals().copy()[_initp]})
    _initphp = glob.glob('./plugin/php/*.php')
    for _initf in _initphp:
        _initp = os.path.splitext(_initf)[0].replace('\\', '/').split('/')[-1]
        globals().update({_initp: (lambda msg, QQ, GroupID: loadphp(msg, QQ, GroupID, os.path.abspath(_initf)))})
        _cbk.update({_initp: globals().copy()[_initp]})
    for _stepx in _cbk.values():
        _stepx(msg, QQ, GroupID)
