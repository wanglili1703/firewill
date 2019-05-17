import json
from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler

DOMAIN_NAME = u'10.199.111.24:8080'
URL = u'http://%s/coupon/issueCoupon'
BODY_DATA = '{}'
_BODY_DATA = ''
if BODY_DATA:
    _BODY_DATA = json.loads(BODY_DATA)
QUERY_DATA = ''
METHOD_TYPE = u'post'
CONTENT_TYPE = 'form'
REQUEST_DATA = (_BODY_DATA or QUERY_DATA)
REQUEST_HEADERS = [{u'name': u'Host', u'value': u'10.199.111.24:8080'}, {u'name': u'Content-Length', u'value': u'5'},
                   {u'name': u'Origin', u'value': u'http://10.199.111.24:9090'}, {u'name': u'User-Agent',
                                                                                  u'value': u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'},
                   {u'name': u'content-type', u'value': u'application/x-www-form-urlencoded'},
                   {u'name': u'Accept', u'value': u'*/*'},
                   {u'name': u'Referer', u'value': u'http://10.199.111.24:9090/productCatena/couponSend'},
                   {u'name': u'Accept-Encoding', u'value': u'gzip, deflate'},
                   {u'name': u'Accept-Language', u'value': u'zh-CN,zh;q=0.8,en;q=0.6'}, {u'name': u'Cookie',
                                                                                         u'value': u'JSESSIONID=D26AB74D948B7482C47338C8F9DB86A6; active-menu=220; cms-hxzq=72BE9D0EDA26F9C34B1572E287EA2E1A; cms-user="Y/6SGrFASpr6UsZKa8k7kw=="'}]
HAS_DATA_PATTERN = True
DATA_PATTERN = {"id": "4"}


class CouponIssuecouponEntity(BasicTroopServiceEntityHandler):
    """
    accessible attribute list for response data:
    %s
    ==================
    kwargs for request:
    Please refer to the constants BODY_DATA or QUERY_DATA request parameters
    """

    def __init__(self, domain_name=DOMAIN_NAME, token=None, **kwargs):
        super(CouponIssuecouponEntity, self).__init__(domain_name=domain_name, url_string=URL, data=REQUEST_DATA,
                                                      method_type=METHOD_TYPE, request_content_type=CONTENT_TYPE,
                                                      # request_headers=REQUEST_HEADERS,
                                                      has_data_pattern=HAS_DATA_PATTERN, token=token, **kwargs)

    def _set_data_pattern(self, *args, **kwargs):
        self._current_data_pattern = DATA_PATTERN


if (__name__ == '__main__'):
    e = CouponIssuecouponEntity()
    e.send_request()
