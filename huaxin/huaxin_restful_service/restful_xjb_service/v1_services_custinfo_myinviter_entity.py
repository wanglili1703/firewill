import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/custinfo/myInviter?'
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = u'timestamp=1505099130146&noncestr=gq03ia9vbskcki7m&signature=FAEED8E6443F0407B89113E8EFFF5247E055CEC2'
METHOD_TYPE = u'get'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = False


class V1ServicesCustinfoMyinviterEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesCustinfoMyinviterEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                request_content_type=CONTENT_TYPE,
                                                                has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        pass


if (__name__ == '__main__'):
    e = V1ServicesCustinfoMyinviterEntity()
    e.send_request()
