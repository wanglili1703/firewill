import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/jointcard/getMobileCode'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = {"cardNo": "6235954021000000071", "mobile": "13501000077", "name": "\u6d4b\u8bd5\u8005", "certType": "0",
                "certNo": "542524198412100588", "timestamp": "1497939776838", "noncestr": "831g3frisv4r6507",
                "signature": "566056654A4B7EE5FD9EBC78DA970E77A21E6A99"}


class V1ServicesJointcardGetmobilecodeEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesJointcardGetmobilecodeEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                     data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                     request_content_type=CONTENT_TYPE,
                                                                     has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                     **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesJointcardGetmobilecodeEntity()
    e.send_request()
