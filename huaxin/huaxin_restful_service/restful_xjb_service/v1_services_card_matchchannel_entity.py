import json

from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/card/matchChannel?'
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = u''
METHOD_TYPE = u'get'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = 'bin=6222020057&certType=0&timestamp=1494560303118&noncestr=jl7h7fo3njqcwqjr&signature=D0EA92B9B1C0F510D6D65E2E93087C5EE7A7CF08'


class V1ServicesCardMatchchannelEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCardMatchchannelEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                               data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                               request_content_type=CONTENT_TYPE,
                                                               has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                               **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesCardMatchchannelEntity()
    e.send_request(bin='1')
