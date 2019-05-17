# -*- coding: utf-8 -*-
from common.basic_troop_service_entity_handler import \
    BasicTroopServiceEntityHandler

BASIC_URL_PATTERN = "http://%s"
PATH = ''
URL = BASIC_URL_PATTERN + PATH
BODY_DATA = ''
QUERY_DATA = ''
METHOD_TYPE = ''
CONTENT_TYPE = ''
HAS_DATA_PATTERN = False
TOKEN = None


class Foo(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name):
        super(Foo, self).__init__(
            domain_name=domain_name,
            url_string=URL,
            method_type=METHOD_TYPE,
            request_content_type=CONTENT_TYPE,
            has_data_pattern=HAS_DATA_PATTERN,
            token=TOKEN)

    def _set_data_pattern(self, *args, **kwargs):
        pass
