import requests


class PostMsg:
    def __init__(self,url,botqq):
        self.url=url
        self.botqq=botqq

    def UserMsg(self,msg,to,picurl,picbase):
        serverurl=self.url
        botqq=self.botqq
        url = serverurl+f'/v1/LuaApiCaller?qq={botqq}&funcname=SendMsg'

        if picbase != 0 or picurl != 0:
            payload = {"toUser":to,"sendToType":1,"sendMsgType":"PicMsg","content":msg,"picUrl":picurl,"picBase64Buf":picbase}#拼接消息包
            headers = {'Content-Type': 'application/json'}
            response = requests.request("POST", url, headers=headers,json=payload)
            return(response.text)
        else:
            payload = {"toUser":to,"sendToType":1,"sendMsgType":"TextMsg","content":msg}#拼接消息包
            headers = {'Content-Type': 'application/json'}
            response = requests.request("POST", url, headers=headers,json=payload)
            return(response.text)

    def GroupMsg(self,msg,groupid,picbase,picurl,atUser):

        serverurl=self.url
        botqq=self.botqq
        url = serverurl+f'/v1/LuaApiCaller?qq={botqq}&funcname=SendMsg'

        if picbase != 0 or picurl != 0:
            payload = {"toUser":groupid,"sendToType":2,"sendMsgType":"PicMsg","content":msg,"picUrl":picurl,"picBase64Buf":picbase,"atUser":atUser}#拼接消息包
            headers = {'Content-Type': 'application/json'}
            response = requests.request("POST", url, headers=headers,json=payload)
            return(response.text)
        else:
            payload = {"toUser":groupid,"sendToType":2,"sendMsgType":"TextMsg","content":msg}#拼接消息包
            headers = {'Content-Type': 'application/json'}
            response = requests.request("POST", url, headers=headers,json=payload)
            return(response.text)

    def SetShutUpUser(self,qq,time,groupid):
        serverurl=self.url
        botqq=self.botqq
        url = serverurl+f'/v1/LuaApiCaller?qq={botqq}&funcname=OidbSvc.0x570_8'

        payload = {"GroupID":groupid,"ShutUpUserID":qq,"ShutTime":time}#拼接消息包
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers,json=payload)
        return(response.text)


    def TemporaryMsg(self,msg,to,groupid,picbase,picurl):

        serverurl=self.url
        botqq=self.botqq
        url = serverurl+f'/v1/LuaApiCaller?qq={botqq}&funcname=SendMsg'

        if picbase != 0 or picurl != 0:
            payload = {"toUser":to,"groupid":groupid,"sendToType":3,"sendMsgType":"PicMsg","content":msg,"picUrl":picurl,"picBase64Buf":picbase}#拼接消息包
            headers = {'Content-Type': 'application/json'}
            response = requests.request("POST", url, headers=headers,json=payload)
            return(response.text)
        else:
            payload = {"toUser":to,"groupid":groupid,"sendToType":3,"sendMsgType":"TextMsg","content":msg}#拼接消息包
            headers = {'Content-Type': 'application/json'}
            response = requests.request("POST", url, headers=headers,json=payload)
            return(response.text)
    

    def Announce(self,groupid,title,text,Pinned,Usewindow,tonewuser):
        serverurl=self.url
        botqq=self.botqq
        url = serverurl+f'/v1/Group/Announce?qq={botqq}'
        if Pinned == True:
            Pinned=1
        else:
            Pinned=0

        if Usewindow == True:
            Type = 10
        elif tonewuser == True:
            Type = 20
        else:
            Type = 0

        payload = {"GroupID":groupid,"Title":title,"Text":text,"Pinned":Pinned,"Type":Type}#拼接消息包
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers,json=payload)
        return(response.text)

    def CheHui(self,GroupID,MsgSeq,MsgRandom):
        serverurl=self.url
        botqq=self.botqq
        url = serverurl+f'/v1/LuaApiCaller?qq={botqq}&funcname=PbMessageSvc.PbMsgWithDraw'
        payload = {"GroupID":GroupID, "MsgSeq":MsgSeq, "MsgRandom":MsgRandom}
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers,json=payload)
        return(response.text)


#A = PostMsg('http://127.0.0.1:8888',2502515980)
#A.UserMsg(msg='这是Wordpress',to=3526436393,picbase=0,picurl=0)

def GetUserBilibili(QQ):
    from module import sql
    QQ = str(QQ)
    tmp = sql.read(f'SELECT * FROM bilibili WHERE QQ="{QQ}"')
    return({"csrf":tmp[1],"cookie":tmp[2]})


'''
A = PostMsg(这里是服务器地址,这里是机器人QQ)
A.GroupMsg(msg=要发的信息,groupid=群号,picurl=图片url,picbase=图片base)  #发送群信息
A.SetShutUpUser(qq=被禁言的QQ,time=时间，0为解除,groupid=群号)  #群禁言
A.UserMsg(msg=信息,to=发给谁,picurl=图片url,picbase=图片的base64) #发送私聊信息
A.TemporaryMsg(msg=信息,to=发给谁,groupid=群号,picurl=图片url,picbase=图片的base64) #发送临时会话
A.Announce(groupid=群号,title=公告标题,text="公告内容",Pinned=是否置顶（传入布尔参数),Usewindow=是否弹出（布尔）,tonewuser="是否给新用户发送(布尔)")#发送群公告
'''