import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s//V1/services/card/getMobileCode'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = True

DATA_PATTERN = '''{"mobile":"15222222444","serialNo":"C-hFlJ8ShIfrnq4_cuL0dQ","smsMode":"N","bankNo":"602","bankName":"\u5de5\u5546\u94f6\u884c","certType":"0","cardNo":"62220213224456223","name":"ruuririrorr","certNo":"623022198912161353","appKind":"8","accptMode":"M","timestamp":"1494905745802","noncestr":"a6dwl02kfhi6bq8u","signature":"45F9E1CFFAAD11E2FF1F45653220E7D692C5123F"}'''


class V1ServicesCardGetmobilecodeEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCardGetmobilecodeEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                request_content_type=CONTENT_TYPE,
                                                                has_data_pattern=HAS_DATA_PATTERN,
                                                                token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesCardGetmobilecodeEntity()
    e.send_request()
