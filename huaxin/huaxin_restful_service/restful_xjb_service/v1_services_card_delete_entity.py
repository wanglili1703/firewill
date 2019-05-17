import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s//V1/services/card/delete'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = True

DATA_PATTERN = '''{"serialNo":"A2KuOrQ_hM35H0vDtLXIwz","tradePassword":"8Y9E1PMywAA=","timestamp":"1494815261831","noncestr":"txl0qy80zvposhuu","signature":"0A1D296371C2C9C2541F6F7AC7E9560C252D370D"}'''


class V1ServicesCardDeleteEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCardDeleteEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA,
                                                         method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE,
                                                         has_data_pattern=HAS_DATA_PATTERN,
                                                         token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesCardDeleteEntity()
    e.send_request()
