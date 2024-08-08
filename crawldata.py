import json
import requests
import time
import random


class Crawl:
    SERVERID = ['82967fec9605fac9a28c437e2a3ef1a4', 'b9fc7bd86d2eed91b23d7347e0ee995e',
                'e3fa93b0fb9e2e6d4f53273540d4e924', 'd3936289adfff6c3874a2579058ac651']
    headers = {'Host': 'wechat.v2.traceint.com', 'Connection': 'keep-alive', 'App-Version': '2.0.14', 'Origin': 'https://web.traceint.com',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3149 MMWEBSDK/20211001 Mobile '
                             'Safari/537.36 MMWEBID/68 MicroMessenger/8.0.16.2040(0x28001053) Process/toolsmp '
                             'WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
               'Content-Type': 'application/json', 'Accept': '*/*',
               'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
               'Referer': 'https://web.traceint.com/web/index.html', 'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
    rule_body = {"operationName": "htmlRule", "query": "query htmlRule {\n userAuth {\n rule {\n htmlRule\n }\n }\n}"}
    index_body = {"operationName": "index",
                  "query": "query index($pos: String!, $param: [hash]) {\n "
                           "userAuth {\n oftenseat {\n list {\n id\n info\n lib_id\n seat_key\n status\n }\n }\n "
                           "message {\n new(from: \"system\") {\n has\n from_user\n title\n num\n }\n indexMsg {\n "
                           "message_id\n title\n content\n isread\n isused\n from_user\n create_time\n }\n }\n "
                           "reserve {\n reserve {\n token\n status\n user_id\n user_nick\n sch_name\n lib_id\n "
                           "lib_name\n lib_floor\n seat_key\n seat_name\n date\n exp_date\n exp_date_str\n "
                           "validate_date\n hold_date\n diff\n diff_str\n mark_source\n isRecordUser\n isChooseSeat\n "
                           "isRecord\n mistakeNum\n openTime\n threshold\n daynum\n mistakeNum\n closeTime\n "
                           "timerange\n forbidQrValid\n renewTimeNext\n forbidRenewTime\n forbidWechatCancle\n }\n "
                           "getSToken\n }\n currentUser {\n user_id\n user_nick\n user_mobile\n user_sex\n "
                           "user_sch_id\n user_sch\n user_last_login\n user_avatar(size: MIDDLE)\n user_adate\n "
                           "user_student_no\n user_student_name\n area_name\n user_deny {\n deny_deadline\n }\n sch "
                           "{\n sch_id\n sch_name\n activityUrl\n isShowCommon\n isBusy\n }\n }\n }\n "
                           "ad(pos: $pos, param: $param) {\n name\n pic\n url\n }\n}", "variables": {"pos": "App-首页"}}
    cancle_body = {"operationName":"reserveCancle","query":"mutation reserveCancle($sToken: String!) {\n userAuth {\n "
                                                           "reserve {\n reserveCancle(sToken: $sToken) {\n "
                                                           "timerange\n img\n hours\n mins\n per\n }\n }\n }\n}",
                   "variables":{"sToken":""}}

    def __init__(self, cookie):
        self.cookie = cookie + '; FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1713417820,1714277047,1714304621,1714376091; ' \
                               'Hm_lpvt_7ecd21a13263a714793f376c18038a87=' + str(int(time.time() - 1)) + '; SERVERID=' + \
                      random.choice(self.SERVERID) + '|' + str(int(time.time() - 1)) + '|1714376087'
        self.headers['Cookie'] = self.cookie

    def get_info(self):
        r = requests.post("https://wechat.v2.traceint.com/index.php/graphql/", json=self.index_body,
                          headers=self.headers).json()
        if 'errors' in r:
            return False
        else:
            user = r['data']['userAuth']
            if len(user['oftenseat']['list']) != 2:
                return False
            else:
                seat_info = {'lib_id': user['oftenseat']['list'][0]['lib_id'], 'seat_key': user['oftenseat']['list'][0]['seat_key'],
                             'info': user['oftenseat']['list'][0]['info']}
                return seat_info

    def cookie_update(self):
        try:
            r = requests.post("https://wechat.v2.traceint.com/index.php/graphql/", json=self.rule_body,
                              headers=self.headers)
            r_cookie = requests.utils.dict_from_cookiejar(r.cookies)
            return r_cookie
        except Exception as e:
            print(e)

    def wechat_update(self):
        try:
            url = 'https://wechat.v2.traceint.com/index.php/reserve/index.html?f=wechat'
            headers = {'Host': 'wechat.v2.traceint.com',
                       'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; MI 5 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, '
                                     'like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile '
                                     'Safari/537.36 MicroMessenger/6.6.5.1280(0x26060536) NetType/WIFI Language/zh_CN',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;'
                                 'q=0.9,image/avif,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,image/tpg,'
                                 '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                       'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,en-US;q=0.8', 'Cookie': self.cookie}
            requests.get(url, headers=headers)
        except Exception as e:
            print(e)




