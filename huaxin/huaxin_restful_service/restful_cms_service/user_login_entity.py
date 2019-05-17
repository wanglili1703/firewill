import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.105.127:8088'
URL = u'http://%s/user/login'
BODY_DATA = '{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'form'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
REQUEST_HEADERS = [{u'name': u'Host', u'value': u'10.199.105.127:8088'}, {u'name': u'Content-Length', u'value': u'63'},
                   {u'name': u'Origin', u'value': u'http://10.199.105.127:8080'}, {u'name': u'User-Agent',
                                                                                   u'value': u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'},
                   {u'name': u'content-type', u'value': u'application/x-www-form-urlencoded'},
                   {u'name': u'Accept', u'value': u'*/*'},
                   {u'name': u'Referer', u'value': u'http://10.199.105.127:8080/login'},
                   {u'name': u'Accept-Encoding', u'value': u'gzip, deflate'},
                   {u'name': u'Accept-Language', u'value': u'zh-CN,zh;q=0.8'}, {u'name': u'Cookie',
                                                                                u'value': u'JSESSIONID=11C68BFA00F7F196B96FE52E43ED627D; cms-user="AtjaYIWYnHOITRFxHh5tLQ=="'}]
HAS_DATA_PATTERN = True
DATA_PATTERN = {"username": "wanglili",
                "password": "99b1dd150b82bdcdc0c41bf7bd05a86f"}


class UserLoginEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(UserLoginEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA,
                                              method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE,
                                              has_data_pattern=HAS_DATA_PATTERN, token=token,
                                              **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = UserLoginEntity()
    e.send_request()
