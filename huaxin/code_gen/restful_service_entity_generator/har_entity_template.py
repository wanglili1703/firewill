# -*- coding: utf-8 -*-
import json

from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = ''
URL = ''
BODY_DATA = ''
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = ''
CONTENT_TYPE = ''
REQUEST_DATA = _BODY_DATA or QUERY_DATA
REQUEST_HEADERS = ''
HAS_DATA_PATTERN = False


class Foo(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """
    def __init__(self, domain_name=DOMAIN_NAME, **kwargs):
        super(Foo, self).__init__(
            domain_name=domain_name,
            url_string=URL,
            data=REQUEST_DATA,
            method_type=METHOD_TYPE,
            request_content_type=CONTENT_TYPE,
            request_headers=REQUEST_HEADERS,
            has_data_pattern=HAS_DATA_PATTERN,
            **kwargs
        )

    def _set_data_pattern(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    e = Foo()
    e.send_request()
