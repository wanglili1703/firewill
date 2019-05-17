import re

from code_gen.lib.basic_troop_service_entity_handler import BasicTroopServiceEntityHandler
from code_gen.lib.json_handler import getJsonData

BAISIC_URL_PATTERN = "http://%s"
PATH = '/proxy/8081/har'
URL = BAISIC_URL_PATTERN + PATH
BODY_DATA = ''
QUERY_DATA = ''
METHOD_TYPE = 'get'
CONTENT_TYPE = ''
HAS_DATA_PATTERN = False
REG_DOMAIN_PATTERN = r'(http(s)?:\/\/)[A-Za-z0-9.:-]+(\/)?'
REG_HTTP_GET_PATH_PATTERN = r'\D*\d*\D*\?'
REG_CLS_NAME_POLISHING_PATTERN = r'[.:\?/{}-]'
REG_HTTP_GET_URL_PATTERN = r'(http(s)?:\/\/)[A-Za-z0-9.:-]+(\/)?\D\d*\D*\?'


class HarEntity(BasicTroopServiceEntityHandler):
    def __init__(self, domain_name='192.168.20.211:9090', json_content=None, filter_pattern=None):
        super(HarEntity, self).__init__(
            domain_name=domain_name,
            url_string=URL,
            method_type=METHOD_TYPE,
            request_content_type=CONTENT_TYPE,
            has_data_pattern=HAS_DATA_PATTERN)

        self._domain_name = domain_name
        self._filter_pattern = filter_pattern

        if json_content:
            try:
                self._json_content = json_content['log']['entries']
            except (TypeError, KeyError):
                self._json_content = json_content

            if self._filter_pattern:
                self.filter(self._filter_pattern)

    def filter(self, patten):
        index = 0
        for i in self.request_url:
            if not re.search(patten, i):
                self._json_content.pop(index)
                index -= 1
            index += 1

        return self._json_content

    def next_entity(self):
        temp_json_content = self._json_content
        entities_attr_map = {}
        inner_attr_map = {}

        def _get_query_string():
            if self.queryString:
                def _get():
                    query_items = self.queryString
                    iter_query_items = iter(query_items)
                    out_string = ''

                    while True:
                        in_string = yield out_string

                        item = iter_query_items.next()
                        values = item.values()
                        out_string = '%s=%s' % (values[0], values[1])

                        if in_string:
                            in_string += '&'
                        out_string = in_string + out_string

                generator = _get()
                query_string = generator.next()

                while True:
                    try:
                        query_string = generator.send(query_string)
                    except StopIteration:
                        break

                return query_string

        def _get_post_data():
            if self.postData_text:
                return self.postData_text

            if self.postData_params:
                params_name = self.params_name
                params_value = self.params_value

                if len(params_name) == len(params_value):
                    return dict(zip(params_name, params_value))

        def _get_path():
            if re.match(REG_DOMAIN_PATTERN, url):
                path = re.sub(REG_DOMAIN_PATTERN, '', url)

                if method_type == 'GET' and re.search(r'\?', path):
                    path = re.search(REG_HTTP_GET_PATH_PATTERN, path).group()

                return path
            else:
                raise Exception('url path parse error, url: {url}'.format(url=url))

        def _get_cls_name():
            name = _get_path()

            if name:
                name = name.title()
            else:
                name = host.title()

            name = re.sub(REG_CLS_NAME_POLISHING_PATTERN, '', name.title()) + 'Entity'

            return name

        def _get_url_pattern():
            if host:
                if method_type == 'GET' and re.search(r'\?', url_path):
                    url_pattern = re.search(REG_HTTP_GET_URL_PATTERN, url).group()
                else:
                    url_pattern = url

                return re.sub(host, '%s', url_pattern)

        def _get_value_from_headers(headers, condition_value):
            # condition_value should be a value for key value pair of a header dict
            for i in headers:
                if condition_value in i.values():
                    return i['value']

        def _get_content_type():
            if request_headers:
                content_type = _get_value_from_headers(request_headers, 'Content-Type') \
                               or _get_value_from_headers(request_headers, 'content-type')
                if content_type:
                    content_type = re.search(r'json', content_type.lower()) and 'json' \
                                   or re.search(r'form', content_type.lower()) and 'form'

                    return content_type

        def _get_host():
            return _get_value_from_headers(request_headers, 'Host')

        while temp_json_content:
            self._json_content = temp_json_content.pop(0)
            method_type = self.method
            request_headers = self.request_headers
            url = self.url
            post_data = _get_post_data()
            query_data = _get_query_string()
            host = _get_host()
            cls_name = _get_cls_name()
            content_type = _get_content_type()
            url_path = _get_path()
            url_pattern = _get_url_pattern()
            has_data_pattern = False

            inner_attr_map = {}
            inner_attr_map.update({
                'method_type': method_type.lower(),
                'cls_name': cls_name,
                'url': url,
                'url_pattern': url_pattern,
                'path': url_path,
                'request_headers': request_headers,
                'body_data': post_data,
                'query_data': query_data,
                'content_type': content_type,
                'has_data_pattern': has_data_pattern,
                'host': host
            })
            entities_attr_map_key = cls_name
            entities_attr_map.update({entities_attr_map_key: inner_attr_map})

            yield entities_attr_map


def har_entity_filter(json_content, patten):
    entity = HarEntity('192.168.20.211:9090')
    return entity.filter(json_content, patten)


if __name__ == '__main__':
    # path = '/Users/linkinpark/Untitled.json'
    path = '/Users/linkinpark/Downloads/har.har'
    json_content = None
    with open(path) as f:
        json_content = getJsonData(f)

        print json_content['log']['entries']

    # entity = HarEntity(json_content=json_content)
    #
    # print entity.json_content

    # from code_gen_service_entity import CodeGenServiceEntity
    #
    # code_gen_entity = CodeGenServiceEntity(domain_name='10.199.101.211:8080', data=json_content)
    # code_gen_entity.send_request()
    # print code_gen_entity.data
