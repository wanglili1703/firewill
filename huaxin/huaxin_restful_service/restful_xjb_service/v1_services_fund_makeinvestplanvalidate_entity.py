import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/fund/makeInvestPlanValidate'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)

HAS_DATA_PATTERN = True
DATA_PATTERN = {"fundId": "05#000802", "payType": "0", "eachInvestAmt": "1", "payCycle": "1#W", "payDay": "W#1",
                "isConfirmBeyondRisk": "0", "timestamp": "1500359012190", "noncestr": "0m8cl8xyt6wljnek",
                "signature": "4ED0AFDB4B2E5ACF0EC98744D919B4D879E75AF0"}


class V1ServicesFundMakeinvestplanvalidateEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesFundMakeinvestplanvalidateEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                         data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                         request_content_type=CONTENT_TYPE,
                                                                         has_data_pattern=HAS_DATA_PATTERN, token=token,
                                                                         **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesFundMakeinvestplanvalidateEntity()
    e.send_request()
