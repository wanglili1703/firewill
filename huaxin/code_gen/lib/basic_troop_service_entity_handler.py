# -*- coding:utf-8 -*-
import inspect
import urllib
import urlparse
import re
import json
import copy

from _common.global_config import GlobalConfig
from code_gen.lib.exceptions import BorrowerResponseException, LenderResponseException
from code_gen.lib.json_handler import handle_item_in_json
from code_gen.lib.service_helper import ServiceHelperSingleton


def retrieve_value_from_dict(target_key, target_dict):
    """
    retrieve value from dict whose keys may be tuple and input target_key is in the tuple.
    """
    for key in target_dict.keys():

        if isinstance(key, tuple):
            if target_key in key:
                return target_dict[key]
        elif target_key == key:
            return target_dict[target_key]


def set_request_data_from_args(func):
    def wrapper(entity, *args, **kwargs):
        if not entity._data and entity._has_data_pattern:
            function_inspect = inspect.getargspec(entity._set_data_pattern)

            if len(function_inspect.args) <= 1 and \
                            function_inspect.varargs is None and function_inspect.keywords is None:
                entity._set_data_pattern()
            else:
                args, kwargs = entity._set_data_pattern(*args, **kwargs) or (
                    args, kwargs)

            data_pattern = entity.current_data_pattern
            encode_str = lambda x: (type(x) == unicode) and \
                                   unicode(x).encode('utf-8') or str(x)
            if data_pattern:
                data = ''

                def handle_str_fake(data):
                    find_fake_phrases_pattern = r'fake(?:_en|_cn)?.\w*'
                    find_only_fake_pattern = r'^fake(?:_en|_cn)?.'
                    if re.search(find_fake_phrases_pattern, data):
                        phrases = re.findall(find_fake_phrases_pattern, data)
                        for fake_item in phrases:
                            fake_object = getattr(entity.utility,
                                                  re.search(
                                                      r"^fake(?:_en|_cn)?",
                                                      fake_item).group())

                            fake_attribute = re.sub(find_only_fake_pattern, '',
                                                    fake_item)
                            faked_value = getattr(fake_object, fake_attribute)()
                            data = re.sub(find_fake_phrases_pattern,
                                          encode_str(faked_value),
                                          encode_str(data), 1)
                    return data

                def handle_str_data_patten():
                    def prepare_url_dict(l_arg):
                        rt_dict = {}
                        keys = [t_items[0] for t_items in l_arg]
                        values = [unicode(t_items[1]).encode('utf-8') for
                                  t_items in l_arg]
                        for item in keys:
                            index_num = keys.index(item)
                            temp_count = keys.count(item)
                            if temp_count > 1:
                                temp_l = tuple(
                                    [i for i in
                                     values[index_num:index_num + temp_count]])
                                rt_dict.update({item: temp_l})
                            else:
                                rt_dict.update({item: values[index_num]})
                        return rt_dict

                    if args:
                        parsed_data_pattern = urlparse.parse_qsl(data_pattern)
                        number_of_args_difference = len(
                            parsed_data_pattern) - len(args)
                        zipped_list = zip([list(i)
                                           for i in parsed_data_pattern], args)
                        tmp_list = [list(i) for i in zipped_list]
                        new_list = []
                        for i in tmp_list:
                            i[0][1] = i[1]
                            new_list.append(i[0])
                        data = urllib.urlencode(prepare_url_dict(new_list), 1)
                        if number_of_args_difference:
                            data += '&' + \
                                    urllib.urlencode(prepare_url_dict(
                                        parsed_data_pattern[
                                        -number_of_args_difference:]), 1)
                    else:
                        data = data_pattern

                    if kwargs:
                        decode_str = lambda x: (type(
                            x) == str) and x.decode("utf8") or unicode(x)
                        keyword_sub_pattern = u"=[\u4e00-\u9fa5/%A-Za-z0-9_.-]*(?=&)?"
                        for k in kwargs:
                            if not re.search(k + keyword_sub_pattern, data):
                                raise KeyError('kwargs does not exists!')
                            data = encode_str(re.sub(k + keyword_sub_pattern,
                                                     k + '=' + decode_str(kwargs[k]),
                                                     decode_str(data)))

                    return data

                def handle_dict_data_pattern():
                    if kwargs:
                        for k in kwargs:
                            node, key = entity.get_json_value_by_node_key(k)
                            value = copy.copy((kwargs[k]))
                            if value is None:
                                handle_item_in_json(data_pattern, node,
                                                    key, mode='pop_key')
                            else:
                                handle_item_in_json(data_pattern, node,
                                                    key, values=value, mode='set')
                    if args:
                        raise Exception('*args is not supported now!')

                    data = data_pattern

                    return data

                def transform_data_pattern_to_json(temp_data_pattern):
                    try:
                        temp_data_pattern = json.loads(temp_data_pattern)
                    except ValueError:
                        return False
                    return temp_data_pattern

                if isinstance(data_pattern, (str, unicode)):
                    data_pattern = handle_str_fake(data_pattern)
                    tmp_data_pattern = transform_data_pattern_to_json(
                        data_pattern)
                    if tmp_data_pattern:
                        data_pattern = tmp_data_pattern
                        data = handle_dict_data_pattern()
                    else:
                        data = handle_str_data_patten()
                elif isinstance(data_pattern, dict):
                    data_pattern = handle_str_fake(json.dumps(data_pattern))
                    data_pattern = json.loads(data_pattern)
                    data = handle_dict_data_pattern()

                entity._data = data
            else:
                raise ValueError('_current_data_pattern is not properly set')

        return func(entity, *args, **kwargs)

    return wrapper


class EntityMetaClass(type):
    def __new__(cls, name, bases, attrs):
        # attrs['utility'] = Utility()
        return super(EntityMetaClass, cls).__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        cls._service_helper = kwargs.has_key('service_helper') and \
                              kwargs['service_helper'] or ServiceHelperSingleton('False')

        [kwargs.pop(key) for key in ('service_helper',) if kwargs.has_key(key)]
        return super(EntityMetaClass, cls).__call__(*args, **kwargs)


class BasicTroopServiceEntityHandler(object):
    current_data_pattern = ''
    _special_node_attributes = []
    _special_key_attributes = []

    __metaclass__ = EntityMetaClass

    def __init__(self, url_string=None, data='', has_data_pattern=True,
                 files=None, method_type='get',
                 request_content_type='form', domain_name=None, cookies=None,
                 token=None, stream=False, request_headers=None):
        self._url_string = url_string
        self._data = data
        self._has_data_pattern = has_data_pattern
        self._current_data_pattern = None
        self._request_content_type = request_content_type
        self._domain_name = domain_name
        self._method_type = method_type
        self._files = files
        self._default_url_pattern = url_string
        self._default_data = data
        self._default_request_content_type = request_content_type
        self._default_method_type = method_type
        self._json_content = None
        self._response = None
        self.cookies = cookies
        self.token = token
        self.stream = False
        self._request_headers = request_headers
        # 将类变量赋给实例变量
        self.service_helper = self._service_helper

    @property
    def json_content(self):
        return self._json_content

    @property
    def response_content(self):
        if not self._response:
            self._get_json_content()

        return self._response

    @property
    def current_data_pattern(self):
        return self._current_data_pattern

    def _refresh_default_args(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def _get_json_content(self):
        if self._method_type == 'post':
            self._response = self.service_helper.call_service_with_post(
                self._url_string, self._data,
                content_type=self._request_content_type,
                domain_name=self._domain_name, cookies=self.cookies,
                token=self.token, request_headers=self._request_headers)
        elif self._method_type == 'get':
            self._response = self.service_helper.call_service_with_get(
                self._url_string, self._data,
                domain_name=self._domain_name, cookies=self.cookies,
                token=self.token, stream=self.stream, request_headers=self._request_headers)
        elif self._method_type == 'put':
            self._response = self.service_helper.call_service_with_put(
                self._url_string, self._data,
                content_type=self._request_content_type,
                domain_name=self._domain_name, cookies=self.cookies,
                token=self.token, request_headers=self._request_headers)
        elif self._method_type == 'multipart_post':
            self._response = self.service_helper.call_service_with_multipart_post(
                self._url_string, self._data,
                self._files, domain_name=self._domain_name,
                cookies=self.cookies, token=self.token, request_headers=self._request_headers)
        elif self._method_type == 'delete':
            self._response = self.service_helper.call_service_with_delete(
                self._url_string, self._data,
                domain_name=self._domain_name, cookies=self.cookies,
                token=self.token, request_headers=self._request_headers)

        try:
            self._json_content = self._response.json()
        except ValueError:
            pass

        self.verify()

        self.cookies = self._response.cookies

    def _reload(self):
        self._url_string, self._data, self._method_type = \
            self._default_url_pattern, self._default_data, self._default_method_type

        self._get_json_content()

    def _set_data_pattern(self, *args, **kwargs):
        raise NotImplementedError(
            "Please override '_set_data_pattern' to set _current_data_pattern for request data")

    def __getattr__(self, attribute):
        if not (self._response or self._json_content):
            self._get_json_content()

        values = []
        node, key = self.get_json_value_by_node_key(attribute)
        handle_item_in_json(self._json_content, node, key, values)

        if len(values) == 1:
            values = values.pop()

        return values

    def update_partial_query_data(self, partial_query_data):
        self._data = self._default_data + partial_query_data
        self._get_json_content()

        return self

    def verify(self):
        url_string = self._url_string % (
            self._domain_name or GlobalConfig.SESSION['current_domain_name'])
        if str(self.result) in ("error", "failed") or str(self.ajaxResult) in (
                "error", "failed"):
            error_message = self.apiReturn_ValidationError or self.apiReturn_ErrorMessage or self.errors \
                            or self.ErrorMessage or self.ajaxErrors
            if isinstance(error_message, list) and len(error_message) == 1:
                error_message = error_message.pop()
            content_apiReturn = hasattr(self,
                                        'content_apiReturn') and self.content_apiReturn or {}
            raise BorrowerResponseException(url_string, error_message,
                                            self.result, content_apiReturn)

        if str(self.result) == "NG":
            raise LenderResponseException(url_string, self.message, self.result)
        elif self.code and self.code not in (200, '103', '101'):
            raise LenderResponseException(url_string,
                                          self.errors or self.message,
                                          self.result)
        elif self.returnCode and self.returnCode not in ('000000',):
            raise Exception('service on error! path: %s, error_code: %s'
                            % (str(self._url_string), self.returnCode))

    @set_request_data_from_args
    def send_request(self, *args, **kwargs):
        self._get_json_content()

    def get(self):
        self._get_json_content()
        return self

    def get_json_value_by_node_key(self, attribute):
        if attribute in self._special_node_attributes:
            node, key = attribute, None
        elif attribute in self._special_key_attributes:
            raw_list = attribute.split('_')
            node, key = raw_list[0], '_' + raw_list[1]
        else:
            raw_list = attribute.split('_')
            if len(raw_list) == 1:
                node, key = attribute, None
            elif len(raw_list) == 2:
                node, key = raw_list[0], raw_list[1]
            else:
                raise Exception(
                    '''The attribute, named: %s, don't suitable for getting in this way.''' % attribute)
        return node, key
