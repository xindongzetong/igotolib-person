import requests


class Check:
    headers = {'Host': 'wechat.v2.traceint.com', 'Connection': 'keep-alive', 'Origin': 'http://tuia.sensezeal.com',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3149 MMWEBSDK/20211001 Mobile '
                             'Safari/537.36 MMWEBID/68 MicroMessenger/8.0.16.2040(0x28001053) Process/toolsmp '
                             'WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
               'Content-Type': 'application/json', 'Accept': '*/*',
               'Referer': 'http://tuia.sensezeal.com/', 'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
    list_body = {"operationName": "getList",
                 "query": "query getList {userAuth{credit{tasks{id task_id task_name task_info task_url credit_num "
                          "contents conditions task_type status}}}}"}
    check_body = {"operationName": "done2",
                  "query": "mutation done2($user_task_id: Int!) {userAuth {credit {done2(user_task_id: "
                           "$user_task_id)}}}",
                  "variables": {"user_task_id": 96981628}}

    def __init__(self, cookie):
        self.cookie = cookie[14:]
        self.headers['Authorization'] = self.cookie

    def check_in(self):
        for i in range(5):
            r = requests.post("https://wechat.v2.traceint.com/index.php/graphql/", json=self.list_body,
                              headers=self.headers).json()
            if r["data"]["userAuth"] is not None:
                try:
                    check_id = r["data"]["userAuth"]["credit"]["tasks"][0]["id"]
                    self.check_body["variables"]["user_task_id"] = check_id
                    requests.post("https://wechat.v2.traceint.com/index.php/graphql/", json=self.check_body,
                                  headers=self.headers)
                    break
                except Exception as e:
                    print(e)
