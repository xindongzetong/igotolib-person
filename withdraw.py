import requests
import random
import time


class Withdraw:
    SERVERID = ['82967fec9605fac9a28c437e2a3ef1a4', 'b9fc7bd86d2eed91b23d7347e0ee995e',
                'e3fa93b0fb9e2e6d4f53273540d4e924', 'd3936289adfff6c3874a2579058ac651']
    headers = {'Host': 'wechat.v2.traceint.com', 'Connection': 'keep-alive', 'App-Version': '2.1.2.p1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) '
                             'WindowsWechat(0x6307001e)', 'Content-Type': 'application/json', 'Accept': '*/*'}
    index_body = {"operationName": "index",
                  "query": "query index($pos: String!, $param: [hash]) {\n userAuth {\n oftenseat {\n list {\n id\n "
                           "info\n lib_id\n seat_key\n status\n }\n }\n message {\n new(from: \"system\") {\n has\n "
                           "from_user\n title\n num\n }\n indexMsg {\n message_id\n title\n content\n isread\n "
                           "isused\n from_user\n create_time\n }\n }\n reserve {\n reserve {\n token\n status\n "
                           "user_id\n user_nick\n sch_name\n lib_id\n lib_name\n lib_floor\n seat_key\n seat_name\n "
                           "date\n exp_date\n exp_date_str\n validate_date\n hold_date\n diff\n diff_str\n "
                           "mark_source\n isRecordUser\n isChooseSeat\n isRecord\n mistakeNum\n openTime\n "
                           "threshold\n daynum\n mistakeNum\n closeTime\n timerange\n forbidQrValid\n renewTimeNext\n "
                           "forbidRenewTime\n forbidWechatCancle\n }\n getSToken\n }\n currentUser {\n user_id\n "
                           "user_nick\n user_mobile\n user_sex\n user_sch_id\n user_sch\n user_last_login\n "
                           "user_avatar(size: MIDDLE)\n user_adate\n user_student_no\n user_student_name\n "
                           "area_name\n user_deny {\n deny_deadline\n }\n sch {\n sch_id\n sch_name\n activityUrl\n "
                           "isShowCommon\n isBusy\n }\n }\n }\n ad(pos: $pos, param: $param) {\n name\n pic\n url\n "
                           "}\n}",
                  "variables": {"pos": "App-首页"}}
    withdraw_body = {"operationName": "reserveCancle",
                   "query": "mutation reserveCancle($sToken: String!) {\n userAuth {\n "
                            "reserve {\n reserveCancle(sToken: $sToken) {\n "
                            "timerange\n img\n hours\n mins\n per\n }\n }\n }\n}",
                   "variables": {"sToken": ""}}

    def __init__(self, cookie):
        self.cookie = cookie + '; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1713417820,1714277047,1714304621,1714376091; ' \
                               'Hm_lpvt_7ecd21a13263a714793f376c18038a87=' + str(int(time.time() - 1)) + '; SERVERID=' + \
                      random.choice(self.SERVERID) + '|' + str(int(time.time() - 1)) + '|1714376087'
        self.headers['Cookie'] = self.cookie

    def withdraw(self):
        try:
            r = requests.post("https://wechat.v2.traceint.com/index.php/graphql/", json=self.index_body,
                              headers=self.headers).json()
            if r["data"]["userAuth"] is not None:
                SToken = r["data"]["userAuth"]["reserve"]["getSToken"]
                self.withdraw_body['variables']['sToken'] = SToken
                requests.post("https://wechat.v2.traceint.com/index.php/graphql/", json=self.withdraw_body,
                              headers=self.headers).json()
        except Exception as e:
            print(e)
