import os
import time
from pywebio import *
import pywebio_battery
from crawldata import Crawl
from check import Check
from hold import Hold
from withdraw import Withdraw
import hashlib
import utils
from pymemcache.client.base import PooledClient
from prereserve import Prereserve
from reserve import Reserve
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor


def set_seat_time():
    def check_url(urlparse):
        if 'wechat.v2.traceint.com/index.php/graphql/?operationName=index&query=' not in urlparse:
            return '请仔细看教程，填写正确链接！'

    cookie = client.get('authorization').decode('utf-8')
    task = client.get('task').decode('utf-8')
    moment = client.get('time').decode('utf-8')
    delay = client.get('delay').decode('utf-8')
    seat_info = Crawl(cookie).get_info()
    while not seat_info:
        img = open('./qr.png', 'rb').read()
        output.put_image(img, width='300px')
        output.toast('请使用微信扫一扫复制链接并填写', position='center', color='#2188ff', duration=2)
        url = input.textarea(label='输入链接', type=input.TEXT, validate=check_url, required=True)
        cookie = utils.get_cookie(url, True)
        if not cookie:
            output.toast('链接过期或未设置常用座位，请设置好，重新获取！', position='center', color='#2188ff', duration=5)
        else:
            client.set('authorization', cookie)
            seat_info = Crawl(cookie).get_info()
        output.clear()
    infor = input.input_group('设置信息', [
        input.input(label='位置信息', name='seat', type=input.TEXT, value=seat_info['info'], readonly=True),
        input.radio(label='选座任务', name='task', inline=True, options=[('定时选座', '1'), ('明日预约', '2'), ('不启用选座', '0')],
                    required=True, value=task),
        input.input(label='选座时间', name='time', type=input.TIME, value=moment, required=True),
        input.slider(label="选座延迟秒数", name='delay', min_value=0, max_value=59, value=int(delay), required=True)
    ])
    h, m = int(infor['time'].split(':')[0]), int(infor['time'].split(':')[1])
    s = int(infor['delay'])
    if infor['task'] != '0':
        scheduler.add_job(id='task', func=process_task, trigger='cron', hour=h, minute=m, second=s,
                          args=[infor['task'], seat_info['lib_id'], seat_info['seat_key']], replace_existing=True)
    else:
        if scheduler.get_job(job_id='task'):
            # 如果存在相同的ID任务，删掉
            scheduler.remove_job(job_id='task')
    client.set('delay', infor['delay'])
    client.set('task', infor['task'])
    client.set('time', infor['time'])
    output.toast('设置完成', position='center', color='#2188ff', duration=1)
    time.sleep(1)
    session.go_app('index', new_window=False)


def set_sign():
    def check_url(urlparse):
        if 'wechat.v2.traceint.com/index.php/graphql/?operationName=index&query=' not in urlparse:
            return '请仔细看教程，填写正确链接！'

    sess_id = client.get('sess_id').decode('utf-8')
    major = client.get('major').decode('utf-8')
    minor = client.get('minor').decode('utf-8')
    act = input.actions('远程打卡', ['立即打卡', '更新信息'])
    if act == '立即打卡':
        msg = utils.sign_in(sess_id[14:], major, minor)
        output.toast(msg, position='center', color='#2188ff', duration=2)
        time.sleep(2)
    elif act == '更新信息':
        img = open('./qr.png', 'rb').read()
        output.put_image(img, width='300px')
        output.toast('请使用微信扫一扫复制链接并填写', position='center', color='#2188ff', duration=2)
        url = input.textarea(label='输入链接', type=input.TEXT, validate=check_url, required=True)
        wechatSESS_ID = utils.get_cookie(url, False)
        output.clear()
        infor = input.input_group('设置打卡信息', [
            input.input(label="major", name='major', type=input.TEXT, value=major, required=True),
            input.input(label="minor", name='minor', type=input.TEXT, value=minor, required=True)
        ])
        client.set('sess_id', wechatSESS_ID)
        client.set('major', infor['major'])
        client.set('minor', infor['minor'])
        client.close()
        output.toast('更新完成', position='center', color='#2188ff', duration=1)
        time.sleep(1)
    session.go_app('index', new_window=False)


def set_integral():
    signin = client.get('signin').decode('utf-8')
    check = client.get('check').decode('utf-8')
    hold = client.get('hold').decode('utf-8')
    start = client.get('start').decode('utf-8')
    numbers = client.get('numbers').decode('utf-8')
    withdraw = client.get('withdraw').decode('utf-8')
    infor = input.input_group('设置日常任务', [
        input.input(label='自动蓝牙打卡', name='signin', type=input.TIME, value=signin,
                    required=True, help_text="00:00则不启动自动打卡"),
        input.input(label='自动签到', name='check', type=input.TIME, value=check,
                    required=True, help_text="00:00则不启动自动签到"),
        input.radio(label='自动暂离', name='hold', inline=True, options=[('启用自动暂离', '1'), ('不启用自动暂离', '0')],
                    required=True, value=hold, help_text="从开始时间开始每隔2小时执行一次"),
        input.input(label='自动暂离开始时间', name='start', type=input.TIME, value=start,
                    required=True),
        input.select(label='自动暂离执行次数', name='numbers', options=['1', '2', '3', '4', '5'], value=numbers,
                     required=True),
        input.input(label='自动退座', name='withdraw', type=input.TIME, value=withdraw,
                    required=True, help_text="00:00则不启动自动退座")
    ])
    if infor['signin'] != '00:00':
        h, m = int(infor['signin'].split(':')[0]), int(infor['signin'].split(':')[1])
        scheduler.add_job(id='signin', func=process_signin, trigger='cron', hour=h, minute=m, second=1,
                          replace_existing=True)
    else:
        if scheduler.get_job(job_id='signin'):
            # 如果存在相同的ID任务，删掉
            scheduler.remove_job(job_id='signin')
    if infor['check'] != '00:00':
        h, m = int(infor['check'].split(':')[0]), int(infor['check'].split(':')[1])
        scheduler.add_job(id='check', func=process_check, trigger='cron', hour=h, minute=m, second=1,
                          replace_existing=True)
    else:
        if scheduler.get_job(job_id='check'):
            # 如果存在相同的ID任务，删掉
            scheduler.remove_job(job_id='check')
    if infor['hold'] == '1':
        h, m = int(infor['start'].split(':')[0]), int(infor['start'].split(':')[1])
        for i in range(int(infor['numbers'])):
            scheduler.add_job(id='hold_' + str(i), func=process_hold, trigger='cron', hour=h, minute=m, second=1,
                              replace_existing=True)
            h += 2
    else:
        for i in range(5):
            if scheduler.get_job(job_id='hold_' + str(i)):
                # 如果存在相同的ID任务，删掉
                scheduler.remove_job(job_id='hold_' + str(i))
    if infor['withdraw'] != '00:00':
        h, m = int(infor['withdraw'].split(':')[0]), int(infor['withdraw'].split(':')[1])
        scheduler.add_job(id='check', func=process_withdraw, trigger='cron', hour=h, minute=m, second=1,
                          replace_existing=True)
    else:
        if scheduler.get_job(job_id='withdraw'):
            # 如果存在相同的ID任务，删掉
            scheduler.remove_job(job_id='withdraw')
    client.set('signin', infor['signin'])
    client.set('check', infor['check'])
    client.set('hold', infor['hold'])
    client.set('start', infor['start'])
    client.set('numbers', infor['numbers'])
    client.set('withdraw', infor['withdraw'])
    output.toast('设置完成', position='center', color='#2188ff', duration=1)
    time.sleep(1)
    session.go_app('index', new_window=False)


def index():
    session_id = pywebio_battery.get_cookie('IGOSESSION')
    if session_id is not None:
        username = os.getenv('username')
        password = os.getenv('password')
        new = hashlib.md5(f'{username}{password}'.encode()).hexdigest()
        if new == session_id:
            act = input.actions('选座脚本', ['设置位置及时间', '设置打卡', '设置日常任务'])
            output.clear()
            if act == '设置位置及时间':
                set_seat_time()
            elif act == '设置打卡':
                set_sign()
            elif act == '设置日常任务':
                set_integral()
        else:
            login()
    else:
        login()


def login():
    login_info = input.input_group('登录', [
        input.input(label='用户名', name='username', type=input.TEXT, required=True),
        input.input(label='密码', name='password', type=input.PASSWORD, required=True)
    ])
    output.clear()
    p = hashlib.md5(f"{login_info['username']}{login_info['password']}".encode()).hexdigest()
    username = os.getenv('username')
    password = os.getenv('password')
    new = hashlib.md5(f'{username}{password}'.encode()).hexdigest()
    if new == p:
        pywebio_battery.set_cookie('IGOSESSION', new, days=1)
    else:
        output.toast('账号或密码错误！', position='center', color='#2188ff', duration=3)
        time.sleep(3)
    session.go_app('index', new_window=False)


def process_task(task, floor, seat):
    cookie = client.get('authorization').decode('utf-8')
    if task == '1':
        reserve = Reserve(cookie)
        for i in range(5):
            if reserve.choose_seat(floor, seat):
                break
    else:
        Prereserve(cookie).prereserve(floor, seat)


def process_signin():
    major = client.get('major').decode('utf-8')
    minor = client.get('minor').decode('utf-8')
    if major != '' and minor != '':
        sess_id = client.get('sess_id').decode('utf-8')
        utils.sign_in(sess_id[14:], major, minor)


def process_check():
    cookie = client.get('authorization').decode('utf-8')
    Check(cookie).check_in()


def process_hold():
    cookie = client.get('authorization').decode('utf-8')
    Hold(cookie).hold()


def process_withdraw():
    cookie = client.get('authorization').decode('utf-8')
    Withdraw(cookie).withdraw()


if __name__ == '__main__':
    executors = {
        'default': ThreadPoolExecutor(20)
    }
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai', executors=executors)
    scheduler.start()
    client = PooledClient(('localhost', 11211), max_pool_size=20, timeout=3)
    client.set('authorization', '-1')
    client.set('sess_id', '-1')
    client.set('task', '0')
    client.set('time', '00:00')
    client.set('delay', '0')
    client.set('major', '')
    client.set('minor', '')
    client.set('signin', '00:00')
    client.set('check', '00:00')
    client.set('hold', '0')
    client.set('start', '00:00')
    client.set('numbers', '1')
    client.set('withdraw', '00:00')
    scheduler.add_job(id='cookie_task', func=utils.cookie_task, trigger='interval', minutes=1, seconds=47)
    config(title='我去图书馆选座', theme='yeti')
    start_server(index, port=80, cdn=False)
