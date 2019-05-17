import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/trade/redeem'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = {"soldShare": "10", "fundId": "05#050026", "soldType": "0", "timestamp": "1494569585293",
                "noncestr": "8ov1nyrxg6xhcx6t", "signature": "FDC15DE629320DC023D948AC1636E23111F2FE81"}


class V1ServicesTradeRedeemEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, **kwargs):
        super(V1ServicesTradeRedeemEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA,
                                                          method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE,
                                                          has_data_pattern=HAS_DATA_PATTERN, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesTradeRedeemEntity()
    e.send_request()
