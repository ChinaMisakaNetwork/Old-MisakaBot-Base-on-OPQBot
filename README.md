# 御坂网络机器人  
## 0x01  
本机器人目前支持的功能:  
1. 自动撤回违规消息  
2. 禁言(语法 yb.jy @某人 时间)
3. bilibili登录(语法 yb.dl 私聊)  
持续增加中
## 0x02 增加新功能  
现有三种方法可以增加新功能
1. 在Group.py内撰写新函数, 并预留3个参数位置传入消息, qq号以及群号
群内功能提供三个参数(msg,QQ,GroupID)代表消息内容,发的人的QQ,群号并手动在setting.json内的customize项新增一个json值{"函数名": "变量名"}
函数可以提供的操作(直接复制并传入参数就可以,不需要发送图片就picurl=0,picbase=0,这两参数都是可选,只需要传入一个就可以的,不用的参数就=0) 
2. 在Group.py内撰写新函数并令变量名以gmeth_开头, 并预留3个参数位置传入消息, qq号以及群号
3. 在./plugin/pfile内新增一个python文件, 消息, qq号和群号将会以msg, QQ, GroupID为名的变量呈现。

基本操作如下:
1. 发送群消息
```
POST.GroupMsg(msg=要发的信息,groupid=群号,picurl=图片url,picbase=图片base64值)
```
2. 禁言操作
```
POST.SetShutUpUser(qq=被禁言的QQ,time=时间，0为解除,groupid=群号)
```
3. 发送私聊消息
```
POST.UserMsg(msg=信息,to=发给谁,picurl=图片url,picbase=图片的base64)
```
4. 发送临时会话 (机器人必须和接受者处于同一个群内)
```
POST.TemporaryMsg(msg=信息,to=发给谁,groupid=群号,picurl=图片url,picbase=图片的base64)
```
5. 发送群公告
```
POST.Announce(groupid=群号,title=公告标题,text="公告内容",Pinned=是否置顶（传入布尔参数),Usewindow=是否弹出（布尔）,tonewuser="是否给新用户发送(布尔)")
```
6. 撤回消息
```
POST.CheHui(GroupID=群号, MsgSeq=消息MsgSeq, MsgRandom=消息MsgRandom)
```
## 0x03 如果你想贡献代码  
### 为御坂御坂新添加群功能  
你只需要在Group.py修改即可,在我们规定的函数区域加一个函数,比如这样  
```
def example(msg, QQ, GroupID): #定义函数,三个参数分别代表消息正文.发消息的QQ号,哪一个群
    if msg.split()[0] == "yb.example":  #限制只有当消息是以yb.example开头才触发
        POST.GroupMsg(msg='HelloWorld',groupid=GroupID,picurl=0,picbase=0)#发送消息
```
然后,你需要把这个函数加入加载列表  
看到plugin/settings.json了吗?
我们在menu下加上这么一条:
```
{"desc": "测试", "help":"yb.example", "priv":false, "callback":"example", "cmd":"yb.site"}
```
* desc:功能名
* help:功能帮助
* priv:仅管理员能使用(如果这项为true,那么请在函数内加判断代码
* callback:写成函数名就行
* cmd:触发这个功能的命令
然后,下面有个customize对吧?
我们同样新增一项:
```
"example": "example",
```
最终是改成这样
```
{
  "menu":
  [
    ...
    {"desc": "测试", "help":"yb.example", "priv":false, "callback":"example", "cmd":"yb.site"}
    ...
  ],
  "customize":
  {
    ...
    "example": "example"
    ...
  }
}
```
特别提示:json规范,加项的时候记得给上一项最后加个 ,