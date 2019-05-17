import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.7:8888'
URL = u'http://%s/pwap/AgreeEpaySignPre.do'
BODY_DATA = '{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'form'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
REQUEST_HEADERS = [{u'name': u'Host', u'value': u'10.199.111.7:8888'}, {u'name': u'Content-Length', u'value': u'676'},
                   {u'name': u'Pragma', u'value': u'no-cache'}, {u'name': u'Cache-Control', u'value': u'no-cache'},
                   {u'name': u'Origin', u'value': u'null'}, {u'name': u'Upgrade-Insecure-Requests', u'value': u'1'},
                   {u'name': u'User-Agent',
                    u'value': u'Mozilla/5.0 (Linux; Android 7.0; ZUK Z2131 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36'},
                   {u'name': u'Content-Type', u'value': u'application/x-www-form-urlencoded'}, {u'name': u'Accept',
                                                                                                u'value': u'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'},
                   {u'name': u'Accept-Encoding', u'value': u'gzip, deflate'},
                   {u'name': u'Accept-Language', u'value': u'zh-CN,en-US;q=0.8'},
                   {u'name': u'X-Requested-With', u'value': u'com.shhxzq.xjb'}]
HAS_DATA_PATTERN = True
DATA_PATTERN = {"TransName": "OSReq", "name": "\\u6d4b\\u8bd5\\u8005",
                "url": "http://10.199.105.132/V1/pages/account/web_binding_result.html",
                "Plain": "certType=1certNo=150203199512020472name=\\u6d4b\\u8bd5\\u8005email=150203199512020472merId=370310000094cell=url=http://10.199.105.132/V1/pages/account/web_binding_result.html",
                "bankCard": "6226731800124238", "certNo": "150203199512020472", "certType": "1", "cell": "",
                "Signature": "certType=1certNo=150203199512020472name=\\u6d4b\\u8bd5\\u8005email=150203199512020472merId=370310000094cell=url=http://10.199.105.132/V1/pages/account/web_binding_result.html",
                "email": "150203199512020472", "merId": "370310000094"}


class PwapAgreeepaysignpreDoEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, **kwargs):
        super(PwapAgreeepaysignpreDoEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA,
                                                           method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE,
                                                           request_headers=REQUEST_HEADERS,
                                                           has_data_pattern=HAS_DATA_PATTERN, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = PwapAgreeepaysignpreDoEntity()
    e.send_request()
