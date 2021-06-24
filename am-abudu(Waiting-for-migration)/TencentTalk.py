from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import requests
import time
import random
import math
import urllib
import hashlib

def genSignString(parser, appkey):
    uri_str = ''
    for key in sorted(parser.keys()):
        if parser[key] != '':
            uri_str += "%s=%s&" % (key, urllib.parse.quote(str(parser[key]), safe = ''))
    sign_str = uri_str + 'app_key=' + appkey
    hash_md5 = hashlib.md5(sign_str.encode("utf8"))
    return hash_md5.hexdigest().upper()

@on_command("talk")
async def talk(session: CommandSession):
    question = session.state.get('message')
    randn = random.randint(0,20)
    if question[0]=="#":
        question = question[1:]
    elif randn != 3 :
        return
    for _item in range(6):
        url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
        appkey = "xxx"
        app_id = 1234567890
        params = {
            'app_id': app_id,
            'session': str(random.randint(827333,102938333312)),
            'question': question,
            'time_stamp': math.floor(time.time()),
            'nonce_str': ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',16)),
            'sign': '',
        }
        params["sign"] = genSignString(params, appkey)
        response = requests.post(url, data=params).json()
        msg = response["data"]["answer"]
        if msg != ' ' and msg != '':
            break
    await session.send(msg)
        
@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(60.0, 'talk', args={'message': session.msg_text})
