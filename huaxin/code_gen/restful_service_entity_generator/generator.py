# -*- coding: utf-8 -*-
import os
import re
import json
import astor
from copy import deepcopy

from _common.global_config import GlobalConfig
from _common.utility import Utility
from code_gen.lib.json_handler import getCleanJsonView, getJsonData
from har_entity import HarEntity

FILE_NAME = "har_entity_template.py"
CURRENT_PATH = os.getcwd()
COMPLETE_FILE_NAME = CURRENT_PATH + os.sep + FILE_NAME
ARG_VALUE_TYPE_MAP_ATTR = {
    int: 'n',
    float: 'n',
    list: 's',
    tuple: 's',
    str: 's',
    unicode: 's',
    bool: 'id',
    dict: 's'
}


def _to_lower(matched):
    if matched.group('first'):
        return matched.group().lower()
    return '_' + matched.group().lower()


def _format_query_data(query_data):
    data = ''
    for i in query_data:
        if i == query_data[0]:
            data += str(i) + '=%s'
        else:
            data += '&' + str(i) + '=%s'
    return data


def _handle_class_doc(node_body, response_dict):
    for sub_node in node_body:
        if sub_node.__class__.__name__ == 'ClassDef':
            for i in sub_node.body:
                if i.__class__.__name__ == 'Expr':
                    i.value.s = i.value.s % json.dumps(response_dict, indent=2)


def handle_global_assignment(node_body, arg_name, arg_value):
    # dict type arg is not supported now
    if arg_value:
        for sub_node in node_body:
            if sub_node.__class__.__name__ == 'Assign':
                target = sub_node.targets[0]
                value = sub_node.value

                if target.id == arg_name:
                    attr = ARG_VALUE_TYPE_MAP_ATTR[type(arg_value)]

                    if type(arg_value) == dict:
                        arg_value = json.dumps(arg_value, indent=2)

                    setattr(value, attr, arg_value)


def handle_cls_name(node_body, old_name, new_name):
    for sub_node in node_body:
        if sub_node.__class__.__name__ == 'ClassDef':
            if sub_node.name == old_name:
                sub_node.name = new_name
                handle_super_call_in_init(sub_node.body, old_name, new_name)
                # print astor.dump(node_body)


def handle_path_parameters(node_body, init_args):
    for sub_node in node_body:
        if sub_node.__class__.__name__ == 'ClassDef':
            for i in sub_node.body:
                if i.__class__.__name__ == 'FunctionDef' and i.name == '__init__':
                    for item in init_args:
                        temp_args = deepcopy(i.args.args[-1])
                        temp_args.id = re.sub(r'(?P<first>^[A-Z])|[A-Z]',
                                              _to_lower, item)
                        temp_args.col_offset = temp_args.col_offset + len(
                            item) + 2
                        i.args.args.append(temp_args)


def handle_super_call_in_init(node_body, old_cls_name, new_cls_name):
    for i in node_body:
        if i.__class__.__name__ == 'FunctionDef' and i.name == '__init__':
            for expr in i.body:
                if hasattr(expr.value, 'func'):
                    call_as_attribute = expr.value
                    call_as_attribute_args = expr.value.args
                    call_as_attribute_keywords = expr.value.keywords
                    attribute = call_as_attribute.func
                    attr = attribute.attr
                    attr_value = attribute.value

                    if attr_value.__class__.__name__ == 'Call':
                        attr_value_args = attr_value.args
                        attr_value_keywords = attr_value.keywords
                        attr_value_func_name = attr_value.func.id

                        [setattr(i, 'id', new_cls_name)
                         for i in attr_value_args if i.id == old_cls_name]


def create_py_modules(target_swagger_domain_name='loanapp-dev.sl.com'):
    # 生成或切换目录
    temp_module_directory = re.sub('restful_service_entity_generator',
                                   'temp_modules',
                                   os.getcwd())
    if not os.path.isdir(temp_module_directory):
        os.mkdir(temp_module_directory)
        os.path.join(temp_module_directory)

    module_entity = None
    module_entity.send_request()
    node = astor.parsefile(COMPLETE_FILE_NAME)
    paths = module_entity.paths

    for i in range(len(paths)):
        module_dict = module_entity.next()

        for module_item in module_dict.values():
            _node = deepcopy(node)
            handle_cls_name(_node.body, 'Foo', module_item['cls_name'])
            # set global assignment
            handle_global_assignment(_node.body, 'PATH', module_item['path'])
            handle_global_assignment(_node.body, 'METHOD_TYPE',
                                     module_item['method_type'])

            content_type = module_item['content_type']
            if content_type:
                print content_type
                content_type = str(re.search(r'json|form', content_type).group())
                handle_global_assignment(_node.body, 'CONTENT_TYPE',
                                         content_type)

            handle_global_assignment(_node.body, 'HAS_DATA_PATTERN',
                                     module_item['has_data_pattern'])
            # set request data
            if 'parameters_in_path' in module_item:
                handle_path_parameters(_node.body, module_item['parameters_in_path'])
            if 'body_data' in module_item:
                if content_type == 'form':
                    handle_global_assignment(_node.body, 'BODY_DATA',
                                             _format_query_data(
                                                 module_item['body_data'].keys()))
                else:
                    handle_global_assignment(_node.body, 'BODY_DATA',
                                             module_item['body_data'])
            if 'query_data' in module_item:
                handle_global_assignment(_node.body, 'QUERY_DATA',
                                         '?' + _format_query_data(
                                             module_item['query_data']))
            # set response doc
            _handle_class_doc(_node.body, module_item['response'])
            # Written to the .py file
            file_name = re.sub(r'(?P<first>^[A-Z])|[A-Z]', _to_lower,
                               module_item['cls_name']) + '.py'
            # temp_lines = astor.to_source(_node)
            # lines = re.sub(r"\\n[ ]+'", '\n    """',
            #                re.sub(r"'\\n", '"""\n', temp_lines))
            # print re.sub(r"\\n([ ]*)", lambda m: '\n' + m.group(1), lines)
            # assert 0
            with open(temp_module_directory + os.sep + file_name, 'w') as py_module:
                temp_lines = astor.to_source(_node)
                lines = re.sub(r"\\n[ ]+'", '\n    """',
                               re.sub(r"'\\n", '"""\n', temp_lines))
                py_module.write(
                    re.sub(r"\\n([ ]*)", lambda m: '\n' + m.group(1), lines))


def create_har_py_modules(entity_instance, mode='file'):
    # mode: 'file'/'json'
    # 生成或切换目录
    temp_module_directory = re.sub('restful_service_entity_generator',
                                   'temp_modules',
                                   os.getcwd())
    if not os.path.isdir(temp_module_directory):
        os.mkdir(temp_module_directory)
        os.path.join(temp_module_directory)

    module_entity = entity_instance
    node = astor.parsefile(COMPLETE_FILE_NAME)
    next_entity = module_entity.next_entity()
    json_template = {}

    while True:
        try:
            module_dict = next_entity.next()

            for module_item in module_dict.values():
                _node = deepcopy(node)
                handle_cls_name(_node.body, 'Foo', module_item['cls_name'])
                # set global assignment
                # set value for PATH
                handle_global_assignment(_node.body, 'PATH', module_item['path'])
                # set value for METHOD_TYPE
                handle_global_assignment(_node.body, 'METHOD_TYPE',
                                         module_item['method_type'])

                content_type = module_item['content_type']
                if content_type:
                    content_type = str(re.search(r'json|form', content_type).group())
                    # set value for CONTENT_TYPE
                    handle_global_assignment(_node.body, 'CONTENT_TYPE',
                                             content_type)
                # set value for domain_name
                handle_global_assignment(_node.body, 'DOMAIN_NAME',
                                         module_item['host'])
                # set value for url
                handle_global_assignment(_node.body, 'URL',
                                         module_item['url_pattern'])
                # set value for request_headers
                handle_global_assignment(_node.body, 'REQUEST_HEADERS',
                                         module_item['request_headers'])
                # set value for HAS_DATA_PATTERN
                handle_global_assignment(_node.body, 'HAS_DATA_PATTERN',
                                         module_item['has_data_pattern'])
                # set request data
                # set value for BODY_DATA
                handle_global_assignment(_node.body, 'BODY_DATA',
                                         module_item['body_data'])

                # set value for QUERY_DATA
                handle_global_assignment(_node.body, 'QUERY_DATA',
                                         module_item['query_data'])
                # Written to the .py file
                file_name = re.sub(r'(?P<first>^[A-Z])|[A-Z]', _to_lower,
                                   module_item['cls_name']) + '.py'
                # prepare code lines to inject
                temp_lines = astor.to_source(_node)
                lines = re.sub(r"\\n[ ]+'", '\n    """',
                               re.sub(r"'\\n", '"""\n', temp_lines))
                lines = re.sub(r"\\n([ ]*)", lambda m: '\n' + m.group(1), lines)

                if mode == 'file':
                    with open(temp_module_directory + os.sep + file_name, 'w') as py_module:
                        py_module.write(lines)

                if mode == 'json':
                    json_template.update({module_item['cls_name']: lines})

        except StopIteration:
            if json_template:
                return json_template
            break


if __name__ == '__main__':
    # path = '/Users/wanglili/Documents/http_archive/productGetHotProductList.har'
    # path = GlobalConfig.RESOURCE_ROOT_PATH + '/code_gen/temp_modules/Untitled.har'
    path = '/Users/zhangzhenzhen/restfulpacket/purchaseValidateUnmatch.har'

    filter_pattern = ""
    json_data = None
    with open(path) as f:
        json_data = getJsonData(f)

    entity = HarEntity('10.199.101.211:8080', json_data, filter_pattern)

    r = create_har_py_modules(entity, 'file')
    print getCleanJsonView(r)
