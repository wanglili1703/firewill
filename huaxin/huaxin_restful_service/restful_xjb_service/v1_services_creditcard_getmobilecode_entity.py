import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/creditcard/getMobileCode'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = {"mobile": "13501000057", "bankNo": "X05", "bankGroupName": "\u5efa\u8bbe\u94f6\u884c",
                "cardNo": "5324584553895238", "name": "\u63a5\u53e3\u6d4b\u8bd5", "timestamp": "1495692614455",
                "noncestr": "s9z5aghz5qo0u8q9", "signature": "35652DF8B4B273AF9A6490CD8A427AA342841B6F"}


class V1ServicesCreditcardGetmobilecodeEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCreditcardGetmobilecodeEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                      data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                      request_content_type=CONTENT_TYPE,
                                                                      has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                      **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesCreditcardGetmobilecodeEntity()
    e.send_request()
