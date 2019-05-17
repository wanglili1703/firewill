import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/product/allProductTypes?'
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = u'timestamp=1499304343400&noncestr=ezi6c3kt13x7oy2z&signature=35330A67C2EF6920EEEBAF3563D8CB3C35C200FA'
METHOD_TYPE = u'get'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = False


class V1ServicesProductAllproducttypesEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesProductAllproducttypesEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                     data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                     request_content_type=CONTENT_TYPE,
                                                                     has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                     **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        pass


if (__name__ == '__main__'):
    e = V1ServicesProductAllproducttypesEntity()
    e.send_request()
