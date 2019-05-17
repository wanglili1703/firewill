import json

from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.2'
URL = u'http://%s/V1/services/common/acquireDeviceId'
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
    "deviceInfo": "{\"uuid\":\"AD982D9C-1992-367A-B6E6-54086C1040B5\",\"buildNo\":\"1607\",\"idfa\":\"0CF7678B-BE2B-4DC4-9079-78D9D831F197\",\"osVersion\":\"7.0\",\"appId\":\"com.shhxzq.xjbEnt\",\"locale\":\"zh\",\"os\":\"android\",\"isJailBroken\":\"0\",\"density\":\"3.0\",\"appVersion\":\"3.0.0\",\"model\":\"ZUK Z2131\",\"carrier\":\"-\",\"resolution\":\"640x1136\"}"}


class V1ServicesCommonAcquiredeviceidEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, **kwargs):
        super(V1ServicesCommonAcquiredeviceidEntity, self).__init__(domain_name=domain_name, url_string=URL,
                                                                    data=REQUEST_DATA, method_type=METHOD_TYPE,
                                                                    request_content_type=CONTENT_TYPE,
                                                                    has_data_pattern=HAS_DATA_PATTERN,
                                                                    **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = V1ServicesCommonAcquiredeviceidEntity()
    e.send_request()
