# coding=utf-8
import random

import datetime
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from _common.global_config import GlobalConfig
from _common.utility import Utility
from code_gen.lib.sendrequest import dumpCookies

requests.packages.urllib3.add_stderr_logger()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
CONTENT_TYPE_DICTIONARY = {'form': GlobalConfig.HeaderContentType.FORM,
                           'json': GlobalConfig.HeaderContentType.JSON}
CONTENT_TYPE_MAP_DATA_KWARGS = {'form': 'data',
                                'json': 'json'}


class Singleton(type):
    _instances = {}

    def __call__(cls, *args):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args)
        return cls._instances[cls]


class ServiceHelper(object):
    def __init__(self):
        self.sessions = requests.Session()

    @staticmethod
    def _build_headers(content_type=None, cookies=None, token=None, request_headers=None):
        _headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12'}
        if content_type:
            _headers.update({'Content-Type': content_type})
        if cookies:
            _headers.update({'Cookie': dumpCookies(cookies)})
        if token:
            _headers.update({'token': token})
        if request_headers:
            if isinstance(request_headers, list):
                for i in request_headers:
                    _headers.update({i['name']: i['value']})

            elif isinstance(request_headers, dict):
                _headers.update(request_headers)
            else:
                raise Exception('require list or dict!')
        return _headers

    @staticmethod
    def _build_service_url(service_url_pattern, domain_name=None):
        data = domain_name or GlobalConfig.SESSION['current_domain_name']
        if not data:
            raise Exception('domain_name should be supplied !')
        url = service_url_pattern % data
        return url

    def generate_signature(self, data, current_device_id):
        # 对dict里面的key进行ASCII升序排列
        items = data.items()
        items.sort()
        # as 对请求参数进行加密使用URL键值对的格式（即key1=value1&key2=value2…）拼接成待签名字符串
        params = ''
        for key, value in items:
            if str(key) != 'signature' and str(value) != '':
                params = params + str(key) + '=' + str(value) + '&'
        # 去掉最后一个&
        if params != '':
            params = params.rstrip('&')

        # 签名算法HmacSHA1
        signature = Utility.EncryptHandle().create_signature(request_params=str(params),
                                                             current_device_id=str(current_device_id))
        return signature

    def call_service_with_post(self, url_pattern, data, content_type='form', cookies=None, domain_name=None, token=None,
                               request_headers=None):
        url = self._build_service_url(url_pattern, domain_name)
        headers = self._build_headers(CONTENT_TYPE_DICTIONARY[content_type], cookies, token,
                                      request_headers=request_headers)
        data_kwarg = CONTENT_TYPE_MAP_DATA_KWARGS[content_type]
        if data is not '' and data.__contains__('noncestr') and data.__contains__('timestamp'):
            # 取13位时间戳
            timestamp = str(int(round(time.time() * 1000)))
            # 16位字母数字随机字符串
            noncestr = Utility.GetData().GenAlphanumeric(16)
            data.update({'timestamp': timestamp})
            data.update({'noncestr': noncestr})
            signature = self.generate_signature(data=data, current_device_id=headers['deviceId'])
            data.update({'signature': signature})
        response = self.sessions.post(url, headers=headers, verify=False, **{data_kwarg: data})
        self.verify_status_code(response, url)
        return response

    def call_service_with_get(self, url_pattern, data='', cookies=None, domain_name=None, token=None, stream=False,
                              request_headers=None):
        url = self._build_service_url(url_pattern, domain_name)
        headers = self._build_headers(cookies=cookies, token=token, request_headers=request_headers)
        if data.__contains__('noncestr') and data.__contains__('timestamp'):
            # 取13位时间戳
            timestamp = str(int(round(time.time() * 1000)))
            # 16位字母数字随机字符串
            noncestr = Utility.GetData().GenAlphanumeric(16)
            dict = {}
            tmp = data.split('&')
            for i in tmp:
                b = i.split('=')
                if len(b) == 2:
                    dict.update({b[0]: b[1]})
                elif len(b) == 1:
                    dict.update({b[0]: ''})
            dict.update({'timestamp': timestamp})
            dict.update({'noncestr': noncestr})
            signature = self.generate_signature(data=dict, current_device_id=headers['deviceId'])
            dict.update({'signature': signature})
            # 拼接成get请求的请求参数
            param = ''
            for item in dict:
                param = param + str(item) + '=' + dict[str(item)] + '&'
            # 去掉最后一个&
            param = param.rstrip('&')
            data = param
        parameters = {'url': url + data,
                      'headers': headers}
        response = self.sessions.get(verify=False, stream=stream, **parameters)
        self.verify_status_code(response, url)
        return response

    def call_service_with_delete(self, url_pattern, data='', cookies=None, domain_name=None, token=None,
                                 request_headers=None):
        url = self._build_service_url(url_pattern, domain_name)
        headers = self._build_headers(cookies=cookies, token=token, request_headers=request_headers)
        parameters = {'url': url + data,
                      'headers': headers}
        response = self.sessions.delete(verify=False, **parameters)
        self.verify_status_code(response, url)
        return response

    def call_service_with_put(self, url_pattern, data, content_type='form', cookies=None, domain_name=None, token=None,
                              request_headers=None):
        headers = self._build_headers(CONTENT_TYPE_DICTIONARY[content_type], cookies, token,
                                      request_headers=request_headers)
        url = self._build_service_url(url_pattern, domain_name)
        parameters = {'url': url,
                      'data': data,
                      'headers': headers}
        response = self.sessions.put(**parameters)
        self.verify_status_code(response, url)
        return response

    def call_service_with_multipart_post(self, url_pattern, data, files, cookies=None, domain_name=None, token=None,
                                         request_headers=None):
        url = self._build_service_url(url_pattern, domain_name)
        headers = self._build_headers(cookies=cookies, token=token, request_headers=request_headers)
        response = self.sessions.post(url, data=data, files=files, headers=headers, verify=False)
        self.verify_status_code(response, url)
        return response

    @staticmethod
    def verify_status_code(response, url):
        if response.status_code not in (200, 201):
            raise Exception('The response error is encountered(%s), url is %s and response text is %s.' % (
                response.status_code, url, response.text))


class ServiceHelperSingleton(ServiceHelper):
    def __init__(self, status):
        super(ServiceHelperSingleton, self).__init__()

    time.sleep(random.uniform(1, 5))
    __metaclass__ = Singleton
