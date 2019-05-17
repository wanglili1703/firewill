import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/product/dqbProductList?'
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = u'isHistory=0&pageNo=1&pageSize=20&timestamp=1499304343400&noncestr=ezi6c3kt13x7oy2z&signature=35330A67C2EF6920EEEBAF3563D8CB3C35C200FA'
METHOD_TYPE = u'get'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
# REQUEST_HEADERS = [{u'name': u'Content-Type', u'value': u'application/json; charset=utf-8'}, {u'name': u'deviceId', u'value': u'ATnBdV3V9Cs7SFMbC3mfxw'}, {u'name': u'token', u'value': u'18a57863-894c-40f9-a2a2-cefd5b60e224'}, {u'name': u'channel', u'value': u'hx'}, {u'name': u'deviceName', u'value': u'MI 5s'}, {u'name': u'deviceModel', u'value': u'MI 5s'}, {u'name': u'clientVersion', u'value': u'a-2.1.0'}, {u'name': u'Host', u'value': u'10.199.111.2'}, {u'name': u'Connection', u'value': u'Keep-Alive'}, {u'name': u'Accept-Encoding', u'value': u'gzip'}, {u'name': u'User-Agent', u'value': u'okhttp/2.7.5'}]
HAS_DATA_PATTERN = False


class V1ServicesProductDqbproductlistEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesProductDqbproductlistEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                    data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                    request_content_type=CONTENT_TYPE,
                                                                    has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                    **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        pass


if (__name__ == '__main__'):
    e = V1ServicesProductDqbproductlistEntity()
    e.send_request()
