# *_*coding:utf-8 *_*
from flask import Flask, request
from hashlib import sha1
import sys
import xmltodict
import time

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'Wang'
__time__ = '2018/04/13 下午4:24'

# If this runs wrong, don't ask me, I don't know why;
# If this runs right, thank god, and I don't know why.
# Maybe the answer, my friend, is blowing in the wind.

app = Flask(__name__)

WECHAT_TOKEN = 'PYTHON26'


@app.route('/wechat8011', methods=['POST', 'GET'])
def wechat():
    singnature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')

    temp = [WECHAT_TOKEN, timestamp, nonce]
    temp.sort()

    temp = ''.join(temp)
    sig = sha1(temp).hexdigest()

    if sig != singnature:
        return ''

    if request.method == 'GET':
        return echostr
    if request.method == 'POST':
        req_data = request.data
        req_dict = xmltodict.parse(req_data)['xml']
        msg_type = req_dict.get('MsgType')
        event = req_dict.get('Event')
        if msg_type == 'text':
            res_dict = {
                'ToUserName': req_dict.get('FromUserName'),
                'FromUserName': req_dict.get('ToUserName'),
                'CreateTime': time.time(),
                'MsgType': 'text',
                'Content': req_dict.get('Content')
            }

        elif msg_type == 'voice':
            res_dict = {
                'ToUserName': req_dict.get('FromUserName', ''),
                'FromUserName': req_dict.get('ToUserName', ''),
                'CreateTime': int(time.time()),
                'MsgType': 'text',
                'Content': req_dict.get('Recognition', u'无法识别')
            }
        elif msg_type == 'event':
            if event == 'subscribe':
                res_dict = {
                    'ToUserName': req_dict.get('FromUserName', ''),
                    'FromUserName': req_dict.get('ToUserName', ''),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': '感谢关注,么么哒!!'
                }
                event_key = req_dict.get('EventKey')
                if event_key:
                    res_dict['Content'] += '场景值:%s' % event_key.replace('qrscene_', '')
            elif event == 'unsubscribe':
                print '取消订阅'
                res_dict = None
            else:
                res_dict = None

        else:
            res_dict = {
                'ToUserName': req_dict.get('FromUserName'),
                'FromUserName': req_dict.get('ToUserName'),
                'CreateTime': time.time(),
                'MsgType': 'text',
                'Content': u'嬷嬷大'
            }
        if res_dict:
            res_dict = {u'xml': res_dict}
            res_data = xmltodict.unparse(res_dict)
        else:
            res_data = ''

        return res_data


if __name__ == '__main__':
    app.run(port=8011, debug=True)
