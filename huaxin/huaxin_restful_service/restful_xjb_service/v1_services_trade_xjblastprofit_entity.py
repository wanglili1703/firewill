import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler
DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/trade/xjbLastProfit'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = {"pageNo":"1","pageSize":"20","timestamp":"1497858837239","noncestr":"2x5b5tsxf0uj5u1m","signature":"F6696D4453CBB9704226BAA8BE56E28D78A9F899"}


class V1ServicesTradeXjblastprofitEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME,token=None,**kwargs):
        super(V1ServicesTradeXjblastprofitEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA,
                                                                 method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE,
                                                                 has_data_pattern=HAS_DATA_PATTERN,token=token,**kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN

if (__name__ == '__main__'):
    e = V1ServicesTradeXjblastprofitEntity()
    e.send_request()