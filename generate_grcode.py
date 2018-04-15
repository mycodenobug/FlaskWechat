# *_*coding:utf-8 *_*
import time
import urllib2
import json
from flask import Flask, redirect
import sys

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'Wang'
__time__ = '2018/04/15 下午2:59'

# If this runs wrong, don't ask me, I don't know why;
# If this runs right, thank god, and I don't know why.
# Maybe the answer, my friend, is blowing in the wind.

# 生成公众号二维码的过程:
# 1. 获取接口调用平局
# 2. 调用生成二维码的接口
# 3. 使用体操课换取二维码

# WECHAT_APP_ID = 'wx4b6d2f1c08675ea9'  # 测试账号
# WECHAT_APP_SECRET = '6c4a4a6c6cc7510483a62a55f027a6e4'  # 测试账号
WECHAT_APP_ID = 'wx7e3ef17f08b4e814'
WECHAT_APP_SECRET = '020272df4bd8b6e2f7351784300e0685'


class AccessToken(object):
    _access_token = {
        'access_token': '',
        'update_time': time.time(),
        'expires_in': 7200
    }

    @classmethod
    def get_access_token(cls):
        acs = cls._access_token
        if not acs.get('access_token') or (time.time() - acs.get('update_time')) > acs.get('expires_in'):
            req_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
                WECHAT_APP_ID, WECHAT_APP_SECRET)
            res_data = urllib2.urlopen(req_url).read()
            res_dict = json.loads(res_data)
            if 'errcode' in res_dict:
                raise Exception(res_dict.get('errmsg'))
            acs['access_token'] = res_dict.get('access_token')
            acs['update_time'] = time.time()
            acs['expires_in'] = res_dict.get('expires_in')
        return cls._access_token['access_token']


app = Flask(__name__)


@app.route('/<int:scene_id>')
def index(scene_id):
    access_token = AccessToken.get_access_token()
    req_url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=' + access_token
    req_dict = {
        "expire_seconds": 604800,
        "action_name": "QR_SCENE",
        "action_info": {"scene": {"scene_id": scene_id}}
    }
    req_json = json.dumps(req_dict)
    res_date = urllib2.urlopen(req_url, req_json).read()
    if res_date:
        # {"ticket": "gQH47joAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xL2taZ2Z3TVRtNzJXV1Brb3ZhYmJJAAIEZ23sUwMEmm
        #  3sUw == ","expire_seconds":60,"url":"http: // weixin.qq.com / q / kZgfwMTm72WWPkovabbI
        # "}
        res_dic = json.loads(res_date)
        if 'errcode' in res_dic:
            raise Exception(res_dic.get('errmsg'))
        ticket = res_dic.get('ticket')
        # GET请求（请使用https协议）https: // mp.weixin.qq.com / cgi - bin / showqrcode?ticket = TICKET

    return '<image src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s">' % ticket


if __name__ == '__main__':
    app.run(debug=True)

    # if __name__ == "__main__":
    #     print AccessToken.get_access_token()
    #     print AccessToken.get_access_token()
