import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/trade/leftAmt?'
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = u'productIds=899#SP8998&timestamp=1497260418682&noncestr=y4k7pzb5z1t6bbq5&signature=9D9F74D227132906BC3C1627FFB24DEE10225B31'
METHOD_TYPE = u'get'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = 'productIds=899#SP8998&timestamp=1497260418682&noncestr=y4k7pzb5z1t6bbq5&signature=9D9F74D227132906BC3C1627FFB24DEE10225B31'


class V1ServicesTradeLeftamtEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesTradeLeftamtEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA,
                                                           method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE,
                                                           has_data_pattern=HAS_DATA_PATTERN, token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN

if (__name__ == '__main__'):
    e = V1ServicesTradeLeftamtEntity()
    e.send_request(productIds='1')
