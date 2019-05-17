import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/product/searchCanTransferFundList'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = True
DATA_PATTERN = {"fromFundId": "39#399011", "keyword": "0", "pageSize": "20", "pageNo": "1",
                "timestamp": "1499395692552", "noncestr": "z9v1ltxuizof8i9n",
                "signature": "8CB0BD0CDF697EF7D77633267FA7B9A551E6341B"}


class V1ServicesProductSearchcantransferfundlistEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesProductSearchcantransferfundlistEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                               data=REQUEST_DATA,
                                                                               method_type=METHOD_TYPE,
                                                                               request_content_type=CONTENT_TYPE,
                                                                               has_data_pattern=HAS_DATA_PATTERN,
                                                                               token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesProductSearchcantransferfundlistEntity()
    e.send_request()
