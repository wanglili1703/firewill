import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler
DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/fund/csiExponent?'
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = u'timestamp=1504173562897&noncestr=ax8ec8wn17f7mjh9&signature=16E1A421716C23F97AC071C4A38807A8CA628F2A'
METHOD_TYPE = u'get'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
#REQUEST_HEADERS = [{u'name': u'Content-Type', u'value': u'application/json; charset=utf-8'}, {u'name': u'deviceId', u'value': u'28dd2c7955ce926456240b2ff0100bde'}, {u'name': u'token', u'value': u'5689c20e-559c-4255-953b-0ad7b3ca94b8'}, {u'name': u'channel', u'value': u'hx'}, {u'name': u'deviceName', u'value': u'Coolpad A8-831'}, {u'name': u'deviceModel', u'value': u'Coolpad A8-831'}, {u'name': u'clientVersion', u'value': u'a-3.0.2'}, {u'name': u'X-Tingyun-Lib-Type-N-ST', u'value': u'3;1504173562897'}, {u'name': u'Host', u'value': u'10.199.111.2'}, {u'name': u'Connection', u'value': u'Keep-Alive'}, {u'name': u'Accept-Encoding', u'value': u'gzip'}, {u'name': u'User-Agent', u'value': u'okhttp/2.7.5'}]
HAS_DATA_PATTERN = False


class V1ServicesFundCsiexponentEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesFundCsiexponentEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA, method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE, has_data_pattern=HAS_DATA_PATTERN, token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        pass

if (__name__ == '__main__'):
    e = V1ServicesFundCsiexponentEntity()
    e.send_request()