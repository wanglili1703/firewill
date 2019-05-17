import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/product/getFinProductSearchConditionGroupList'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = True
# groupId: 0=period 1=product type 2=min invest amount, multiple values can be seperated by ;
DATA_PATTERN = {"groupId": "", "timestamp": "1501222491858", "noncestr": "pwlrwraqu55infwx",
                "signature": "DAE000FCCECA965994F1024FD11E6CDEDB5A856E"}


class V1ServicesProductGetFinProductSearchConditionGroupListEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesProductGetFinProductSearchConditionGroupListEntity, self).__init__(domain_name=domain_name,
                                                                                           url_string=URL,
                                                                                           data=REQUEST_DATA,
                                                                                           method_type=METHOD_TYPE,
                                                                                           request_content_type=CONTENT_TYPE,
                                                                                           has_data_pattern=HAS_DATA_PATTERN,
                                                                                           token=token,
                                                                                           **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesProductGetFinProductSearchConditionGroupListEntity()
    e.send_request()
