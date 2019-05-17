# coding: utf-8
import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/card/getMobileCodeUpgrade'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
# REQUEST_HEADERS = [{u'name': u'deviceId', u'value': u'AlRrdlQ4hH2JEdmTpYe7Ak'}, {u'name': u'token', u'value': u'295f7337-5a18-4b91-9163-4a1985030712'}, {u'name': u'channel', u'value': u'hx'}, {u'name': u'deviceName', u'value': u'ZUK Z2131'}, {u'name': u'deviceModel', u'value': u'ZUK Z2131'}, {u'name': u'clientVersion', u'value': u'a-2.1.0'}, {u'name': u'Content-Type', u'value': u'application/json; charset=utf-8'}, {u'name': u'Content-Length', u'value': u'215'}, {u'name': u'Host', u'value': u'10.199.111.2'}, {u'name': u'Connection', u'value': u'Keep-Alive'}, {u'name': u'Accept-Encoding', u'value': u'gzip'}, {u'name': u'User-Agent', u'value': u'okhttp/2.7.5'}]
HAS_DATA_PATTERN = True
# operType = 1 是升级
DATA_PATTERN = {"desBankNo": "305", "bankCardId": "0000000000100965", "operType": "1", "timestamp": "1498184864952",
                "noncestr": "p5cif0zh1tr88u18",
                "signature": "D5F3DEA35251062AEAB4EC2DCDA138D976FD9AAD"}


class V1ServicesCardGetmobilecodeupgradeEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCardGetmobilecodeupgradeEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                       data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                       request_content_type=CONTENT_TYPE,
                                                                       has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                       **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesCardGetmobilecodeupgradeEntity()
    e.send_request()
