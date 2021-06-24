from nonebot import on_command, CommandSession
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote

@on_command('菜单', only_to_me=False)
async def menu(session: CommandSession):
    msg="\n[T]站长工具\n● Ping[域名/IP]\n● 扒站[地址]\n● 短链接[链接]\n● 二维码[内容]\n● 备案查询[域名]\n● 收录查询[域名]\n● 报毒检测[域名/IP]\n在消息前加上\"#\"还能和我聊天哟~"
    await session.send(msg, at_sender=True)

@on_command('ping', only_to_me=False)
async def ping(session: CommandSession):
    ip = session.current_arg_text.strip()
    if '.' in ip:
        url = "https://api.tx7.co/api/pingspeed/?host=" + ip
        response = requests.get(url).json()
        if response["code"] == 200:
            msg = "\n{}！\n查询域名: {}\nIP地址: {}\nIP信息: {}\n平均延迟: {}\n最低延迟: {}\n最高延迟: {}\n检测节点: {}".format(response["msg"],response["host"],response["ip"],response["location"],response["ping_time_avg"],response["ping_time_min"],response["ping_time_max"],response["node"])
        elif response["code"] == 201:
            msg = "\n{}！\n查询域名: {}\n错误信息: {}".format(response["msg"],ip,response["tips"])
        else:
            msg = response["msg"] + "！"
    else:
        msg = "\n请输入正确的域名！"
    await session.send(msg, at_sender=True)
        
@on_command('备案查询', only_to_me=False)
async def icp(session: CommandSession):
    domain = session.current_arg_text.strip()
    if '.' in domain:
        url = "https://api.muxiaoguo.cn/api/ICP?api_key=e927a0d113305f46&url=" + domain
        response = requests.get(url).json()
        if response["code"] == 200:
            data = response["data"]
            msg = "\n查询成功！\n查询域名: {}\n单位名称: {}\n备案性质: {}\n备案号: {}\n网站名称: {}\n首页域名: {}\n审核日期: {}".format(data["url"],data["organizer_name"],data["nature"],data["license"],data["website_name"],data["website_home"],data["audit_time"])
        elif response["code"] == -5:
            msg = "\n域名{}未查询到备案信息！".format(domain)
        else:
            msg = response["msg"] + "！"
    else:
        msg = "\n请输入正确的域名！"
    await session.send(msg, at_sender=True)
        
@on_command('收录查询', only_to_me=False)
async def shoulu(session: CommandSession):
    domain = session.current_arg_text.strip()
    if '.' in domain:
        url = "https://api.tx7.co/api/Included/?url=" + domain
        response = requests.get(url).json()
        if response["code"]==200:
            msg = "\n查询域名: {}\n百度收录: {}\n搜狗收录: {}\n好搜收录: {}".format(domain, str(response["baidu"]), str(response["sogou"]), str(response["haosōu"]))
        else:
            msg = "查询错误！"
    else:
        msg = "\n请输入正确的域名！"
    await session.send(msg, at_sender=True)

@on_command('二维码', only_to_me=False)
async def qrcode(session: CommandSession):
    domain = session.current_arg_text.strip()
    #await session.send("正在处理，请稍后，若在10秒内没有返回即为请求失败", at_sender=True)
    url = "https://cli.im/api/qrcode/code?text={}&mhid=vUfOWV3rmcshMHYtI9VSPqk".format(domain)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='lxml')
    qrcode_link = "https:"+ soup.find_all("img", {"class": "qrcode_plugins_img"})[0]['src']
    suo_url = "http://api.suowo.cn/api.htm"
    suo_data = {
        "url": qrcode_link,
        "key": "60b1fbcef1dda66d0d39171e@d47200b44492a4bad97b24404345a567",
        "expireDate": "2030-03-31"
    }
    suo = requests.get(suo_url, params=suo_data).text
    msg = "请求成功！\n请求内容: {}\n二维码链接: {}".format(domain, suo)
    await session.send(msg, at_sender=True)

@on_command('报毒检测', only_to_me=False)
async def baodu(session: CommandSession):
    domain = session.current_arg_text.strip()
    if '.' in domain:
        url = "https://api.tx7.co/api/urlsec/?url=" + domain
        response = requests.get(url).json()
        msg = "\n检测域名: {}\n域名状态: {}\n提示信息: {}".format(response["url"], response["type"], response["reason"])
    else:
        msg = "\n请输入正确的域名！"
    await session.send(msg, at_sender=True)

@on_command('扒站', only_to_me=False)
async def bazhan(session: CommandSession):
    domain = session.current_arg_text.strip()
    if not(("http://" in domain) or ("https://" in domain)):
        domain = "http://" + domain
    if '.' in domain:
        url = "https://xiaojieapi.com/api/v1/get/wget?url=" + domain
        response = requests.get(url).json()
        if response["code"] == 200:
            await session.send("正在处理，请稍后...", at_sender=True)
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
                    msg = "\n请求成功！\n请求地址: {}\n下载链接: {}".format(domain, suo)
                    break
            if not response.get("url"):
                msg = "请求失败，请尝试添加协议头！"
        else:
            msg = "请求失败，请检查站点信息后重试！"
    else:
        msg = "\n请输入正确的域名！"
    await session.send(msg, at_sender=True)

@on_command('短链接', only_to_me=False)
async def duan(session: CommandSession):
    uri = session.current_arg_text.strip()
    if not(("http://" in uri) or ("https://" in uri)):
        uri = "http://" + uri
    if '.' in uri:
        suo_url = "http://api.suowo.cn/api.htm"
        suo_data = {
            "url": uri,
            "key": "60b1fbcef1dda66d0d39171e@d47200b44492a4bad97b24404345a567",
            "expireDate": "2030-03-31"
        }
        suo = requests.get(suo_url, params=suo_data).text
        msg = "\n请求成功！\n原链接: {}\n短链接: {}".format(uri, suo)
    else:
        msg = "\n请输入正确的链接！"
    await session.send(msg, at_sender=True)

