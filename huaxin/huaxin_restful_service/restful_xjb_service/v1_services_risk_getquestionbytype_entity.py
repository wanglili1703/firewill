import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/risk/getQuestionByType?'
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = u'type=1&timestamp=1495104812275&noncestr=dxj65mq1dtb3b4m0&signature=BF35534409313C35CA05D90CDD9EBF9AD86FC311'
METHOD_TYPE = u'get'
CONTENT_TYPE = ''
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
# REQUEST_HEADERS = [{u'name': u'Host', u'value': u'10.199.111.2'}, {u'name': u'Pragma', u'value': u'no-cache'}, {u'name': u'Cache-Control', u'value': u'no-cache'}, {u'name': u'deviceId', u'value': u'AZU5Go-NhM3r_ckbf5bGcZ'}, {u'name': u'Accept', u'value': u'*/*'}, {u'name': u'X-Requested-With', u'value': u'XMLHttpRequest'}, {u'name': u'User-Agent', u'value': u'Mozilla/5.0 (Linux; Android 7.0; ZUK Z2131 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36'}, {u'name': u'token', u'value': u'90001f4a-c007-4f7d-83ec-edb0e2552c93'}, {u'name': u'clientVersion', u'value': u'a-2.2.0'}, {u'name': u'Referer', u'value': u'http://10.199.111.2/V1/pages/account/risk_review.html'}, {u'name': u'Accept-Encoding', u'value': u'gzip, deflate'}, {u'name': u'Accept-Language', u'value': u'zh-CN,en-US;q=0.8'}, {u'name': u'Cookie', u'value': u'JSESSIONID=65C5FC2CD2D05110E60C21228654EDF5; token=90001f4a-c007-4f7d-83ec-edb0e2552c93; channel=hx; deviceId=AZU5Go-NhM3r_ckbf5bGcZ; clientVersion=a-2.2.0; buildNo=1274'}]
HAS_DATA_PATTERN = False


class V1ServicesRiskGetquestionbytypeEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesRiskGetquestionbytypeEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                    data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                    request_content_type=CONTENT_TYPE,
                                                                    has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                    **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        pass


if (__name__ == '__main__'):
    e = V1ServicesRiskGetquestionbytypeEntity()
    e.send_request()
