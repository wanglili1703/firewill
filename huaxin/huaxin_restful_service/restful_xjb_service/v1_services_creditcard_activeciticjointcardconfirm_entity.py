import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/creditcard/activeCiticJointcardConfirm'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
# REQUEST_HEADERS = [{u'name': u'deviceId', u'value': u'AlRrdlQ4hH2JEdmTpYe7Ak'}, {u'name': u'token', u'value': u'ffa4de89-85b8-475a-a265-d4544f4fff92'}, {u'name': u'channel', u'value': u'hx'}, {u'name': u'deviceName', u'value': u'ZUK Z2131'}, {u'name': u'deviceModel', u'value': u'ZUK Z2131'}, {u'name': u'clientVersion', u'value': u'a-2.1.0'}, {u'name': u'Content-Type', u'value': u'application/json; charset=utf-8'}, {u'name': u'Content-Length', u'value': u'184'}, {u'name': u'Host', u'value': u'10.199.111.2'}, {u'name': u'Connection', u'value': u'Keep-Alive'}, {u'name': u'Accept-Encoding', u'value': u'gzip'}, {u'name': u'User-Agent', u'value': u'okhttp/2.7.5'}]
HAS_DATA_PATTERN = True
DATA_PATTERN = {"serialNo": "", "mobileCode": "",
                "timestamp": "1497961460830", "noncestr": "gglcm4cn1dpnmr9i",
                "signature": "FFBBBC100E858A02B31F338AB77C6AD63C6DC85F"}


class V1ServicesCreditcardActiveCiticJointcardConfirmEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCreditcardActiveCiticJointcardConfirmEntity, self).__init__(domain_name=domain_name,
                                                                                    url_string=URL,
                                                                                    data=REQUEST_DATA,
                                                                                    method_type=METHOD_TYPE,
                                                                                    request_content_type=CONTENT_TYPE,
                                                                                    has_data_pattern=HAS_DATA_PATTERN,
                                                                                    token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesCreditcardActiveCiticJointcardConfirmEntity()
    e.send_request()
