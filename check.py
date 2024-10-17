import requests
import random
import time


class Check:
    SERVERID = ['82967fec9605fac9a28c437e2a3ef1a4', 'b9fc7bd86d2eed91b23d7347e0ee995e',
                'e3fa93b0fb9e2e6d4f53273540d4e924', 'd3936289adfff6c3874a2579058ac651']
    headers = {'Host': 'wechat.v2.traceint.com', 'Connection': 'keep-alive', 'App-Version': '2.1.5',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) '
                             'WindowsWechat(0x6307001e)', 'Content-Type': 'application/json', 'Accept': '*/*'}
    list_body = {"operationName": "getList",
                 "query": "query getList {\n userAuth {\n credit {\n tasks {\n id\n task_id\n task_name\n task_info\n "
                          "task_url\n credit_num\n contents\n conditions\n task_type\n status\n }\n staticTasks "
                          "{\n id\n name\n task_type_name\n credit_num\n contents\n button\n }\n }\n }\n}"}
    check_body = {"operationName": "done",
                  "query":"mutation done($user_task_id: Int!) {\n userAuth {\n credit {\n done(user_task_id: "
                          "$user_task_id)\n }\n }\n}",
                  "variables": {"user_task_id": 98318215}}

    def __init__(self, cookie):
        self.cookie = cookie + '; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1713417820,1714277047,1714304621,1714376091; ' \
                               'Hm_lpvt_7ecd21a13263a714793f376c18038a87=' + str(int(time.time() - 1)) + '; SERVERID=' + \
                      random.choice(self.SERVERID) + '|' + str(int(time.time() - 1)) + '|1714376087'
        self.headers['Cookie'] = self.cookie

    def check_in(self):
        r = requests.post("https://wechat.v2.traceint.com/index.php/graphql/", json=self.list_body,
                          headers=self.headers).json()
        print(r)
        if r["data"]["userAuth"] is not None:
            try:
                check_id = r["data"]["userAuth"]["credit"]["tasks"][0]["id"]
                self.check_body["variables"]["user_task_id"] = check_id
                r = requests.post("https://wechat.v2.traceint.com/index.php/graphql/", json=self.check_body,
                              headers=self.headers)
                print(r.text)
            except Exception as e:
                print(e)
