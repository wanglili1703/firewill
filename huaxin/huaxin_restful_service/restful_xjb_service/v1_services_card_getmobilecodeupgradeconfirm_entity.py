import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/card/getMobileCodeUpgradeConfirm'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
# REQUEST_HEADERS = [{u'name': u'deviceId', u'value': u'AlRrdlQ4hH2JEdmTpYe7Ak'}, {u'name': u'token', u'value': u'295f7337-5a18-4b91-9163-4a1985030712'}, {u'name': u'channel', u'value': u'hx'}, {u'name': u'deviceName', u'value': u'ZUK Z2131'}, {u'name': u'deviceModel', u'value': u'ZUK Z2131'}, {u'name': u'clientVersion', u'value': u'a-2.1.0'}, {u'name': u'Content-Type', u'value': u'application/json; charset=utf-8'}, {u'name': u'Content-Length', u'value': u'172'}, {u'name': u'Host', u'value': u'10.199.111.2'}, {u'name': u'Connection', u'value': u'Keep-Alive'}, {u'name': u'Accept-Encoding', u'value': u'gzip'}, {u'name': u'User-Agent', u'value': u'okhttp/2.7.5'}]
HAS_DATA_PATTERN = True
DATA_PATTERN = {"mobileCode": "123456", "serialNo": "AoyzPnx4VPIIBBvm6R0ZDp", "timestamp": "1498186573047",
                "noncestr": "hgcat8tsj1py2yay", "signature": "73AF74AC28186967C4C48335384FAC897C13C5A0"}


class V1ServicesCardGetmobilecodeupgradeconfirmEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCardGetmobilecodeupgradeconfirmEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                              data=REQUEST_DATA,
                                                                              method_type=METHOD_TYPE,
                                                                              request_content_type=CONTENT_TYPE,
                                                                              has_data_pattern=HAS_DATA_PATTERN,
                                                                              token=token,
                                                                              **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesCardGetmobilecodeupgradeconfirmEntity()
    e.send_request()
