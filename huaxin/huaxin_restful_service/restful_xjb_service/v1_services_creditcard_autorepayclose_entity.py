import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/creditcard/autoRepayClose'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = {"cardSerialNo": "6229180024000113", "timestamp": "1496724217165", "noncestr": "iqd9esw4bs1svn0i",
                "signature": "01F5FC02C80D3F711ACC0418BC21F35FB43C8294"}


class V1ServicesCreditcardAutorepaycloseEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCreditcardAutorepaycloseEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                       data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                       request_content_type=CONTENT_TYPE,
                                                                       has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                       **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesCreditcardAutorepaycloseEntity()
    e.send_request()
