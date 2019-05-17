# coding: utf-8
import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

DOMAIN_NAME = u'10.199.111.18:8080'
URL = u'http://%s/hop/front'
BODY_DATA = u'{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'json'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
HAS_DATA_PATTERN = True
DATA_PATTERN = {
    "interfaceId": "0CIF000001",
    "companyNo": "1111",
    "signType": "01",
    "signature": "EORHCwvAdK+PmOWt5CPIcGIUV1NmKqAlsS2bYR3Tx/uIkm9AKTuq1eEjJ0W/H91glbdoR2vi1h6RGE+lcm+7jFMw7zhBnIbhNW7l2j7B0D4NscsdfNUgjDz/nbCp6yN+YRTMKx/8REqBe40fNUR1RleVbyvNj7xRp3C69FfalNEr6QlgA+rTE3XVBjBWVOTEMCtmuASgDxO3kNkfV0nwP5JBTEfPUH6mXOuJT2MNIgoroPae8q3Ndj4p4R3WbndHU3OXaPrELI3SFokwH9CKKzxS1/bI4w6zPaq2ivx0MBrPkfUKshL58is+mq+EneRdS+pqystAg2kvVYejSFgOFQ==",
    "content": "{\"apDate\":\"20170317\",\"apTime\":\"103000\",\"setDate\":\"20170317\",\"operNo\":\"16\",\"outerOrderNo\":\"170077\",\"name\":\"测试者\",\"certType\":\"1\",\"certNo\":\"542524198412100588\",\"certSignOrg\":\"1000_北京市\",\"certValidDate\":\"20250925\",\"bank\":\"A46\",\"cardType\":\"41\",\"cardNo\":\"6235954021000000071\",\"mobile\":\"13501000077\",\"homeTel\":\"\",\"officeTel\":\"\",\"address\":\"上海\",\"email\":\"\",\"zipcode\":\"888888\",\"occupation\":\"1011\",\"branchCode\":\"9600\",\"branchName\":\"广州分行营业部\",\"openDate\":\"20170317\",\"openTime\":\"\",\"cardValidDate\":\"20251231\",\"operator\":\"009146\",\"reviewer\":\"000830\",\"extendInfo\":\"\"}"
}


class V1ServicesHopFrontEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(V1ServicesHopFrontEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA,
                                                       method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE,
                                                       has_data_pattern=HAS_DATA_PATTERN, token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesHopFrontEntity()
    e.send_request()
