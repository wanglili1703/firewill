import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler
DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/custinfo/updateCustBaseInfo'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = {"address":"\u4e0a\u6d77\u5e02\u5e02\u8f96\u533a\u9ec4\u6d66\u533a\u5357\u4eac\u897f\u8def399\u53f7\u660e\u5929\u5e7f\u573a","email":"13579845@qq.com","pcIds":"310000,310100,310101","area":"\u5357\u4eac\u897f\u8def399\u53f7\u660e\u5929\u5e7f\u573a","timestamp":"1505290441129","noncestr":"w8dvkbrpb2e2cf3s","signature":"C4DB4E70762A05E3A5A2F1F799BF19479E74BF9B"}


class V1ServicesCustinfoUpdatecustbaseinfoEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCustinfoUpdatecustbaseinfoEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA, method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE, has_data_pattern=HAS_DATA_PATTERN, token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN
if (__name__ == '__main__'):
    e = V1ServicesCustinfoUpdatecustbaseinfoEntity()
    e.send_request()