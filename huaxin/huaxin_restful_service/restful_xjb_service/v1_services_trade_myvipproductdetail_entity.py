import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s//V1/services//trade/myVipProductDetail'
BODY_DATA = u''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = True
DATA_PATTERN = {"orderNo": "0120170706595DDB8702DA1b3559", "productId": "H9#F90029", "valueDate": "--",
                "holdingType": "2", "timestamp": "1499323314882", "noncestr": "ifrkjqpmrh88ac9h",
                "signature": "117E15BF5EF6514A4B09A331F8BA0D57514D3198"}


class V1ServicesTradeMyvipproductdetailEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesTradeMyvipproductdetailEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                      data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                      request_content_type=CONTENT_TYPE,
                                                                      has_data_pattern=HAS_DATA_PATTERN,
                                                                      token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesTradeMyvipproductdetailEntity()
    e.send_request()
