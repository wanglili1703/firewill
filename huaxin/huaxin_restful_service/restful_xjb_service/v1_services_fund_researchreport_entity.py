import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s//V1/services//fund/researchReport'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = True
DATA_PATTERN = {"pageSize": "20", "pageNo": "1", "timestamp": "1502778774459", "noncestr": "vsvv8kp6yn942px8",
                "signature": "531C213677216B7D39D61725D4D276FBC6234CD6"}


class V1ServicesFundResearchreportEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesFundResearchreportEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                 data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                 request_content_type=CONTENT_TYPE,
                                                                 has_data_pattern=HAS_DATA_PATTERN,
                                                                 token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesFundResearchreportEntity()
    e.send_request()
