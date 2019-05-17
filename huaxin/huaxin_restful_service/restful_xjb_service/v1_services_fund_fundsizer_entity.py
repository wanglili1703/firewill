import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/fund/fundSizer'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
# if no companyId in the post data, it means all fund companies, if companyId appears in the post data, it will show the result for this fund company.
DATA_PATTERN = {"companyId": "157555", "gradeOrgId": "10668", "gradeLevel": "5", "riseMin": "0", "riseMax": "100",
                "riseSection": "4",
                "pageNo": "1", "pageSize": "20", "timestamp": "1494985030520", "noncestr": "z6mjivwd50ps7z1t",
                "signature": "80491B44CE7CC8FA21E3FABDE00F0E800650B891"}


class V1ServicesFundFundsizerEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesFundFundsizerEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA,
                                                            method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE,
                                                            has_data_pattern=HAS_DATA_PATTERN, token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesFundFundsizerEntity()
    e.send_request()
