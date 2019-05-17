import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/trade/getSalaryFinPlanDetail'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
# REQUEST_HEADERS = [{u'name': u'deviceId', u'value': u'AoKNERJn9HlKhnOmycdJuh'}, {u'name': u'token', u'value': u'7db04c9b-a849-4770-bb94-d4157c4719ab'}, {u'name': u'clientVersion', u'value': u'a-3.0.0'}, {u'name': u'deviceModel', u'value': u'MI 5'}, {u'name': u'Accept', u'value': u'application/json'}, {u'name': u'deviceName', u'value': u'MI 5'}, {u'name': u'channel', u'value': u'hx'}, {u'name': u'X-Tingyun-Id', u'value': u'gxV2W0HkeBk;c=2;r=1163580822;'}, {u'name': u'X-Tingyun-Lib-Type-N-ST', u'value': u'3;1501226076588'}, {u'name': u'Content-Type', u'value': u'application/json; charset=utf-8'}, {u'name': u'Content-Length', u'value': u'159'}, {u'name': u'Host', u'value': u'10.199.111.2'}, {u'name': u'Connection', u'value': u'Keep-Alive'}, {u'name': u'Accept-Encoding', u'value': u'gzip'}, {u'name': u'User-Agent', u'value': u'okhttp/2.7.5'}]
HAS_DATA_PATTERN = True
DATA_PATTERN = {"salaryFinPlanId": "0", "timestamp": "1494408566365", "noncestr": "h9x3ca7098ydlqo0",
                "signature": "E8D8B3A2E7EABC2219D76FB8449848611BC2E299"}


class V1ServicesTradeGetsalaryfinplandetailEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesTradeGetsalaryfinplandetailEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                          data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                          request_content_type=CONTENT_TYPE,
                                                                          token=token,
                                                                          has_data_pattern=HAS_DATA_PATTERN, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesTradeGetsalaryfinplandetailEntity()
    e.send_request()
