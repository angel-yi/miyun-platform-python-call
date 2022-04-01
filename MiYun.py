# coding: utf-8
"""
@title: 米云sdk
@author: xiao mu
@date: 20220401
"""
import logging
import re
import requests
from retry import retry

from settings import *


class MiYun(object):
    def __init__(self):
        self.username = USERNAME
        self.password = PASSWORD
        self.token = TOKEN

    @retry(tries=RESTRY_TRIES, delay=RETRY_DELAY)
    def get_response(self, method, url, headers, data=None):
        '''
        此函数用来处理所有的请求
        :param method:
        :param url:
        :param headers:
        :param data:
        :return:
        '''
        logging.info(f'进入get_response函数，入参：[[method, url, headers, data]]')
        if method == 'get':
            resp = requests.get(url, headers=headers, timeout=TIMEOUT, proxies=PROXIES)
            logging.info(f'请求完成：[[resp]]')
            # logging.error(f'请求完成：', resp.text)
            if resp.status_code == 200:
                return resp
            else:
                pass
                # 自定义其他代码
        else:
            resp = requests.post(url, headers=headers, data=data, timeout=TIMEOUT, proxies=PROXIES)
            logging.info(f'请求完成：[[resp]]')
            # logging.error(f'请求完成：', resp.text)
            if resp.status_code == 200:
                return resp.json()
            else:
                pass
                # 自定义其他代码

    def login(self):
        """
        参数名	必传	缺省值	描述
        apiName	Yes	 	API账号
        password	Yes	 	用户密码

        {"token":"","message":"API账号或密码错误(账号为: MY. 开头，请在客户端查阅)"}
        {"token":"418c6c68dddf-10004","message":"ok"} token[重要参数，后面的请求都需要]
        :return:
        """
        resp = self.get_response('get', LOGIN_URL, HEADERS)
        if 'ok' in resp.text:
            with open('./settings.py', 'r', encoding='utf-8') as fp:
                data = fp.read()
                fp.close()
            self.token = resp.json()['token']
            logging.info(f'token: {self.token}')
            with open('./settings.py', 'w', encoding='utf-8') as fp:
                fp.write(re.sub("TOKEN = '(.*?)'", f"TOKEN = '{self.token}'", data))
                fp.close()
            return True

    def get_money(self):
        """
        参数名	必传	缺省值	描述
        token	Yes	 	登录返回token令牌

        {"message":"token已失效","money":""}
        {"message":"ok","money":"0.00"}
        :return:
        """
        resp = self.get_response('get', MYINFO_URL, HEADERS)
        logging.info(f'{resp.text}')
        return resp.json()['money']

    def get_mobile(self, project_id=None):
        """
        参数名	必传	缺省值	描述
        token	Yes		登录返回token
        project_id	Yes		项目id (登录网页版或者电脑客户端查询)
        operator	No		(0=默认 4=实卡 5=虚卡) 可为空,请传数字
        phone_num	No		指定取号的话,这里填要取的手机号
        scope	No		指定号段查询 (譬如:137开头的号段或者1371开头的号段),最多支持20个号段。用逗号分隔 比如150,1501,1502
        scope_black	No		排除号段最长支持4位且可以支持多个,最多支持20个号段。用逗号分隔 比如184,1841
        address	No		归属地选择 例如 湖北 甘肃 不需要带省、市字样
        api_id	No		开发者返现账号（请填写登录的用户名）

        错误：{"message":"账号或密码错误","mobile":"","minute":0}
        错误：{"message":"余额不足, 余额剩余: 0","mobile":"","minute":0}
        错误：{"message":"您设置为取专属号，但当前没有专属列表！","mobile":"","minute":59}
        错误：{"message":"没有可用号码，请休息5秒后再试","mobile":"","minute":59}
        正确: {"message":"ok","mobile":"15088888888","minute":59}
        :param project_id:
        :return:
        """
        resp = self.get_response('get', GET_MOBILE_URL.format(self.token, project_id), HEADERS)
        logging.info(f'{resp.text}')
        return resp.json()

    def get_message(self, project_id, mobile_id):
        """
        参数名	必传	缺省值	描述
        token	Yes		登录返回token
        project_id	Yes		项目id
        phone_num	Yes		取卡返回的手机号

        错误：{"message":"token已失效","code":"","modle":""}
        错误：{"message":"暂无消息..","code":"","modle":""}
        正确：{"message":"ok","code":"123411","modle":"【apple】您的验证码为123411，有效期30分钟"}

        当没有获取到短信时，需要再次调用此接口，建议每5秒调用一次，100次以后就不要再获取了。
        正确获取验证码之后，无需调用拉黑、释放接口！
        :param project_id:
        :param mobile_id:
        :return:
        """
        resp = self.get_response('get', GET_MESSAGE_URL.format(self.token, project_id, mobile_id), HEADERS)
        logging.info(f'{resp.text}')
        return resp.json()

    def add_black(self, project_id, mobile_id):
        """
        参数名	必传	缺省值	描述
        token	Yes		登录返回token
        phone_num	Yes		手机号码
        project_id	Yes		项目ID

        错误：{"message":"账号或密码错误"}
        正确：{"message":"ok"}
        :param project_id:
        :param mobile_id:
        :return:
        """
        resp = self.get_response('get', ADD_BLACK_URL.format(self.token, project_id, mobile_id), HEADERS)
        logging.info(f'{resp.text}')
        return resp.json()

    def free_mobile(self, project_id, mobile_id):
        """
        参数名	必传	缺省值	描述
        token	Yes		登录返回token
        phone_num	Yes		手机号码
        project_id	Yes		项目ID

        错误：{"message":"账号或密码错误"}
        正确：{"message":"ok"}
        :param project_id:
        :param mobile_id:
        :return:
        """
        resp = self.get_response('get', FREE_MOBILE_URL.format(self.token, project_id, mobile_id), HEADERS)
        logging.info(f'{resp.text}')
        return resp.json()
