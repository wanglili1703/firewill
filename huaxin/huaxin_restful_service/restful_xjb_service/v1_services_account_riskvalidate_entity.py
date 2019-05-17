import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/account/riskValidate'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = {"productId": "05#001429", "timestamp": "1502692173990", "noncestr": "d4vjgefd0la2n8my",
                "signature": "D59165EE67624F6014BE184C5775865CDDEC5325"}


class V1ServicesAccountRiskvalidateEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesAccountRiskvalidateEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                  data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                  request_content_type=CONTENT_TYPE,
                                                                  has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                  **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesAccountRiskvalidateEntity()
    e.send_request()
