import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/risk/saveQuestion'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
# REQUEST_HEADERS = [{u'name': u'Host', u'value': u'10.199.111.2'}, {u'name': u'Content-Length', u'value': u'87'}, {u'name': u'Pragma', u'value': u'no-cache'}, {u'name': u'Cache-Control', u'value': u'no-cache'}, {u'name': u'deviceId', u'value': u'AZU5Go-NhM3r_ckbf5bGcZ'}, {u'name': u'Origin', u'value': u'http://10.199.111.2'}, {u'name': u'User-Agent', u'value': u'Mozilla/5.0 (Linux; Android 7.0; ZUK Z2131 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36'}, {u'name': u'Content-Type', u'value': u'application/json'}, {u'name': u'Accept', u'value': u'*/*'}, {u'name': u'X-Requested-With', u'value': u'XMLHttpRequest'}, {u'name': u'token', u'value': u'90001f4a-c007-4f7d-83ec-edb0e2552c93'}, {u'name': u'clientVersion', u'value': u'a-2.2.0'}, {u'name': u'Referer', u'value': u'http://10.199.111.2/V1/pages/account/risk_review.html'}, {u'name': u'Accept-Encoding', u'value': u'gzip, deflate'}, {u'name': u'Accept-Language', u'value': u'zh-CN,en-US;q=0.8'}, {u'name': u'Cookie', u'value': u'JSESSIONID=65C5FC2CD2D05110E60C21228654EDF5; token=90001f4a-c007-4f7d-83ec-edb0e2552c93; channel=hx; deviceId=AZU5Go-NhM3r_ckbf5bGcZ; clientVersion=a-2.2.0; buildNo=1274'}]
HAS_DATA_PATTERN = True
DATA_PATTERN = {"questionNo": "000003", "answer": "b,a,a,d,c,d,d,d,e,d,c,d,e,d,d,b,b,c,c,b", "score": "83",
                "timestamp": "1498451757600", "noncestr": "pdwzgovzhdpfq5n2",
                "signature": "B044E474A0DFF84A9547BE028FF4C4DDEF43F6BE"}


class V1ServicesRiskSavequestionEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesRiskSavequestionEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                               data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                               request_content_type=CONTENT_TYPE,
                                                               has_data_pattern=HAS_DATA_PATTERN, token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesRiskSavequestionEntity()
    e.send_request()
