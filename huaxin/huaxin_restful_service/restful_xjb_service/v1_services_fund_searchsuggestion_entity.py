import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/fund/searchSuggestion?'
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = u'type=0&keyword=\u535a\u65f6&pageNo=1&pageSize=20&timestamp=1495104812275&noncestr=dxj65mq1dtb3b4m0&signature=BF35534409313C35CA05D90CDD9EBF9AD86FC311'
METHOD_TYPE = u'get'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = True
DATA_PATTERN = 'type=0&keyword=%E5%8D%9A%E6%97%B6&pageNo=1&pageSize=20&timestamp=1495104812275&noncestr=dxj65mq1dtb3b4m0&signature=BF35534409313C35CA05D90CDD9EBF9AD86FC311'


class V1ServicesFundSearchsuggestionEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesFundSearchsuggestionEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                   data=REQUEST_DATA,
                                                                   method_type=METHOD_TYPE,
                                                                   request_content_type=CONTENT_TYPE,
                                                                   has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                   **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesFundSearchsuggestionEntity()
    e.send_request()
