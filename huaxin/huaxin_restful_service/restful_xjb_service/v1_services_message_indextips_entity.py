import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/message/indexTips?'
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = u'position=0&timestamp=1502779751156&noncestr=zqedaclldx189do8&signature=81310DA6B456546844BA3FE00B6976AF1A72D4AC'
METHOD_TYPE = u'get'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = True
DATA_PATTERN = {"position": "0", "timestamp": "1502779751156", "noncestr": "zqedaclldx189do8",
                "signature": "81310DA6B456546844BA3FE00B6976AF1A72D4AC"}


class V1ServicesMessageIndextipsEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesMessageIndextipsEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                               data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                               request_content_type=CONTENT_TYPE,
                                                               has_data_pattern=HAS_DATA_PATTERN,
                                                               token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesMessageIndextipsEntity()
    e.send_request()
