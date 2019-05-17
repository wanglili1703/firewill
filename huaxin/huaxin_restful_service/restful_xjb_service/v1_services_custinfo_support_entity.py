import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/custinfo/support'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = True
DATA_PATTERN = {"fundManagerId": "1", "timestamp": "1495003936270", "noncestr": "xbi0wyd0tlzuh3ek",
                "signature": "AA8AE0A5F31D370198152D2B1C793C40FC0F7589"}


class V1ServicesCustinfoSupportEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCustinfoSupportEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                              data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                              request_content_type=CONTENT_TYPE,
                                                              has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                              **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesCustinfoSupportEntity()
    e.send_request()
