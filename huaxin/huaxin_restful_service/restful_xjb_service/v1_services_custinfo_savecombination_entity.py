import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/custinfo/saveCombination'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = True

DATA_PATTERN = {"objectIds": "27#000214,27#000118,31#310368,31#310328", "percents": "25,0,0,75",
                "timestamp": "1496801363782", "noncestr": "gkp5bn9tdl8d8d9l",
                "signature": "73D23FD3D674390C9412F15D2F901FFD76183563"}


class V1ServicesCustinfoSavecombinationEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCustinfoSavecombinationEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                      data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                      request_content_type=CONTENT_TYPE,
                                                                      has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                      **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN
        pass


if (__name__ == '__main__'):
    e = V1ServicesCustinfoSavecombinationEntity()
    e.send_request()
