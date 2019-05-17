import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/trade/modifyExpireDisposeType'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = {"expireDisposeType": "1", "expireQuitAmt": "1", "productId": "H9#H99998", "valueDate": "",
                "timestamp": "1502268191808", "noncestr": "b8mh2xcp8p1xc35x",
                "signature": "59CADCFCA5238DCE57187BA8D3A1C2FB6FF2443D"}


class V1ServicesTradeModifyexpiredisposetypeEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesTradeModifyexpiredisposetypeEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                           data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                           request_content_type=CONTENT_TYPE,
                                                                           has_data_pattern=HAS_DATA_PATTERN,
                                                                           token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesTradeModifyexpiredisposetypeEntity()
    e.send_request()
