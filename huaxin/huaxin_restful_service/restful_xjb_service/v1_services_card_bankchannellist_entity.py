import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler
DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/card/bankChannelList?'
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = u'certType=0&timestamp=1498119910680&noncestr=30q492vz0kkiuwdo&signature=9CE749413C9409783E0408E3A7D452F6E23479A0'
METHOD_TYPE = u'get'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
# REQUEST_HEADERS = [{u'name': u'Content-Type', u'value': u'application/json; charset=utf-8'}, {u'name': u'deviceId', u'value': u'D_ZXqg2jdHiq_EDrgvLjAb'}, {u'name': u'token', u'value': u'724222f7-608c-428b-93ad-6e2a57fc89a1'}, {u'name': u'channel', u'value': u'hx'}, {u'name': u'header_device_name', u'value': u'Redmi Note 3'}, {u'name': u'header_device_model', u'value': u'Redmi Note 3'}, {u'name': u'clientVersion', u'value': u'a-2.1.0'}, {u'name': u'Host', u'value': u'10.199.111.2'}, {u'name': u'Connection', u'value': u'Keep-Alive'}, {u'name': u'Accept-Encoding', u'value': u'gzip'}, {u'name': u'User-Agent', u'value': u'okhttp/2.7.5'}]
HAS_DATA_PATTERN = True
DATA_PATTERN = {"certType":"0","timestamp":"1498119910680","noncestr":"30q492vz0kkiuwdo","signature":"9CE749413C9409783E0408E3A7D452F6E23479A0"}


class V1ServicesCardBankchannellistEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME,token=None,**kwargs):
        super(V1ServicesCardBankchannellistEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA, method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE,has_data_pattern=HAS_DATA_PATTERN,token=token,**kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN

if (__name__ == '__main__'):
    e = V1ServicesCardBankchannellistEntity()
    e.send_request()