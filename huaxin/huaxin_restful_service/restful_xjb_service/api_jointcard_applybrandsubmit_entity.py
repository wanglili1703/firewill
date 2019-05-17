# coding=utf-8
import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.131:8888'
URL = u'http://%s/api/jointCard/applyBrandSubmit'
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'form'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
# REQUEST_HEADERS = [{u'name': u'Host', u'value': u'muat.shhxzq.com'}, {u'name': u'Content-Length', u'value': u'1213'}, {u'name': u'Pragma', u'value': u'no-cache'}, {u'name': u'Cache-Control', u'value': u'no-cache'}, {u'name': u'deviceId', u'value': u'f0c2e0511886b8ec44d1220663aa407f'}, {u'name': u'Origin', u'value': u'http://10.199.105.132'}, {u'name': u'User-Agent', u'value': u'Mozilla/5.0 (Linux; Android 6.0.1; MI 5s Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36'}, {u'name': u'Content-Type', u'value': u'multipart/form-data; boundary=----WebKitFormBoundaryeWDSMDFIp231ASQA'}, {u'name': u'Accept', u'value': u'application/json, text/plain, */*'}, {u'name': u'token', u'value': u'3fce516f-d6a5-4469-9edd-acd0aa07886a'}, {u'name': u'channel', u'value': u'5'}, {u'name': u'browserName', u'value': u'Android%20Chrome'}, {u'name': u'Referer', u'value': u'http://10.199.105.132/creditcard/verify?brandSource=HX_H5&brandType=ZX_JK'}, {u'name': u'Accept-Encoding', u'value': u'gzip, deflate'}, {u'name': u'Accept-Language', u'value': u'zh-CN,en-US;q=0.8'}, {u'name': u'X-Requested-With', u'value': u'com.shhxzq.xjb'}]
HAS_DATA_PATTERN = True
DATA_PATTERN = {
    "contactName": "噢你", "contactRel": "0", "contactRelNm": "父母", "contactMobile": "13589668884",
    "insContactName": "家里", "insContactRel": "0", "insContactRelNm": "父母",
    "insContactMobile": "13564654857", "serialNo": "Dcd4uL2EpHn5IzfRPr_qAX", "brandSource": "HX_H5",
    "brandType": "ZX_JK"
}


class ApiJointcardApplybrandsubmitEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(ApiJointcardApplybrandsubmitEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                 data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                 request_content_type=CONTENT_TYPE,
                                                                 has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                 **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = ApiJointcardApplybrandsubmitEntity()
    e.send_request()
