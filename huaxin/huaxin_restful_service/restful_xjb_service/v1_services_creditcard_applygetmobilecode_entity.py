import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services//creditcard/applyGetMobileCode'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = {"mobile": "17200000313", "timestamp": "1495692352894", "noncestr": "ycqklfpjmm7o95ki",
                "signature": "99CC5F8DC3256B7E9433B59BDADB3B18EC036957"}


class V1ServicesCreditcardApplygetmobilecodeEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCreditcardApplygetmobilecodeEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                           data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                           request_content_type=CONTENT_TYPE,
                                                                           has_data_pattern=HAS_DATA_PATTERN,
                                                                           token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesCreditcardApplygetmobilecodeEntity()
    e.send_request()
