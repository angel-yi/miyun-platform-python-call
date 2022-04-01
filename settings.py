# coding: utf-8
"""
@title: 米云sdk-设置
@author: xiao mu
@date: 20220401
"""

USERNAME = 'xxxx'
PASSWORD = 'xxxx'
TOKEN = 'xxxx'

RESTRY_TRIES = 5
RETRY_DELAY = 3

TIMEOUT = 10
PROXIES = ''

PROJECT_ID = None

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "close",
}

LOGIN_URL = f'http://api.miyun.pro/api/login?apiName={USERNAME}&password={PASSWORD}'

MYINFO_URL = f'http://api.miyun.pro/api/get_myinfo?token={TOKEN}'

GET_MOBILE_URL = 'http://api.miyun.pro/api/get_mobile?token={}&project_id={}'

GET_MESSAGE_URL = 'http://api.miyun.pro/api/get_message?token={}&project_id={}&phone_num={}'

ADD_BLACK_URL = 'http://api.miyun.pro/api/add_blacklist?token={}&project_id={}&phone_num={}'

FREE_MOBILE_URL = 'http://api.miyun.pro/api/free_mobile?token={}&project_id={}&phone_num={}'
