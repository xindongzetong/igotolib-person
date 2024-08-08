import requests
import random
import time


class Reserve:
    SERVERID = ['82967fec9605fac9a28c437e2a3ef1a4', 'b9fc7bd86d2eed91b23d7347e0ee995e',
                'e3fa93b0fb9e2e6d4f53273540d4e924', 'd3936289adfff6c3874a2579058ac651']
    headers = {'Host': 'wechat.v2.traceint.com', 'Connection': 'keep-alive', 'App-Version': '2.1.2.p1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) '
                             'WindowsWechat(0x6307001e)', 'Content-Type': 'application/json', 'Accept': '*/*'}
    reserve_body = {"operationName": "reserueSeat",
                    "query": "mutation reserueSeat($libId: Int!, $seatKey: String!, $captchaCode: String, $captcha: String!) {\n userAuth {\n reserve {\n reserueSeat(\n libId: $libId\n seatKey: $seatKey\n captchaCode: $captchaCode\n captcha: $captcha\n )\n }\n }\n}",
                    "variables": {"captchaCode": "", "captcha": ""}}

    def __init__(self, cookie):
        self.cookie = cookie + '; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1713417820,1714277047,1714304621,1714376091; ' \
                               'Hm_lpvt_7ecd21a13263a714793f376c18038a87=' + str(int(time.time() - 1)) + '; SERVERID=' + \
                      random.choice(self.SERVERID) + '|' + str(int(time.time() - 1)) + '|1714376087'
        self.headers['Cookie'] = self.cookie

    def choose_seat(self, floor, seat):
        try:
            self.reserve_body['variables']['libId'] = int(floor)
            self.reserve_body['variables']['seatKey'] = seat
            msg = requests.post("https://wechat.v2.traceint.com/index.php/graphql/", json=self.reserve_body,
                                headers=self.headers).json()
            if 'errors' in msg:
                return False
            else:
                return True
        except Exception as e:
            print(e)
