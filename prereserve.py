import asyncio
import requests
import random
import time
import websockets


class Prereserve:
    SERVERID = ['82967fec9605fac9a28c437e2a3ef1a4', 'b9fc7bd86d2eed91b23d7347e0ee995e',
                'e3fa93b0fb9e2e6d4f53273540d4e924', 'd3936289adfff6c3874a2579058ac651']
    headers = {'Host': 'wechat.v2.traceint.com', 'Connection': 'keep-alive', 'App-Version': '2.1.2.p1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) '
                             'WindowsWechat(0x6307001e)', 'Content-Type': 'application/json', 'Accept': '*/*'}
    socket_headers = {'Host': 'wechat.v2.traceint.com', 'Connection': 'Upgrade', 'Pragma': 'no-cache',
                      'Cache-Control': 'no-cache',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781'
                                    '(0x6700143B) WindowsWechat(0x63070517)',
                      'Upgrade': 'websocket', 'Origin': 'https://web.traceint.com', 'Sec-WebSocket-Version': '13',
                      'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                      'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits'}
    check_prereserve_body = {"operationName": "prereserveCheckMsg",
                             "query": "query prereserveCheckMsg {\n userAuth {\n prereserve {\n prereserveCheckMsg\n }\n }\n}"}
    prereserve_body = {"operationName": "save",
                       "query": "mutation save($key: String!, $libid: Int!, $captchaCode: String, $captcha: String) "
                                "{\n userAuth {\n prereserve {\n save(key: $key, libId: $libid, captcha: $captcha, "
                                "captchaCode: $captchaCode)\n }\n }\n}",
                       "variables": {"captchaCode": "", "captcha": ""}}

    def __init__(self, cookie):
        self.cookie = cookie + '; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1713417820,1714277047,1714304621,1714376091; ' \
                               'Hm_lpvt_7ecd21a13263a714793f376c18038a87=' + str(int(time.time() - 1)) + '; SERVERID=' + \
                      random.choice(self.SERVERID) + '|' + str(int(time.time() - 1)) + '|1714376087'
        self.headers['Cookie'] = self.cookie

    async def queue(self):
        self.socket_headers['Cookie'] = self.cookie
        async with websockets.connect("wss://wechat.v2.traceint.com/ws?ns=prereserve/queue",
                                      extra_headers=self.socket_headers) as websocket:
            while True:
                await websocket.send('{"ns":"prereserve/queue","msg":""}')
                response = await websocket.recv()
                if 'u6392' in response:
                    break

    def prereserve(self, floor, seat):
        try:
            r = requests.post("https://wechat.v2.traceint.com/index.php/graphql/", json=self.check_prereserve_body,
                              headers=self.headers).json()
            if r['data']['userAuth']['prereserve']['prereserveCheckMsg'] == '':
                asyncio.run(self.queue())
                self.prereserve_body['variables']['libid'] = int(floor)
                self.prereserve_body['variables']['key'] = seat
                msg = requests.post("https://wechat.v2.traceint.com/index.php/graphql/", json=self.prereserve_body,
                                        headers=self.headers).json()
                if 'errors' in msg:
                    return False
                else:
                    return True
            else:
                return False
        except Exception as e:
            print(e)
