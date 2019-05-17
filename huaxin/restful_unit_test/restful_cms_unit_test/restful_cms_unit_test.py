# coding=utf-8

import inspect
import os
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_resource_root_path():
    string_separator = 'huaxin'
    current_module_path = inspect.getmodule(get_resource_root_path).__file__
    init_path = re.split(string_separator, current_module_path)[0]
    resource_path = os.path.normpath(os.path.join(init_path, string_separator))
    return resource_path


sys.path.append(get_resource_root_path())

import unittest
from _tools.mysql_xjb_tools import MysqlXjbTools
from ddt import ddt, file_data, data, unpack
from _tools.restful_cms_tools import RestfulCmsTools
from restful_unit_test.test_suite_run import TestSuiteRun


@ddt
class XjbServiceTest_01(unittest.TestCase):
    def setUp(self):
        self._restful_cms = RestfulCmsTools()
        self._db = MysqlXjbTools()

    @file_data
    def test_issue_coupon(self, code, mobile, quantity):
        self._restful_cms.issue_coupon(code=str(code), mobile=str(mobile), quantity=str(quantity))

    def tearDown(self):
        return


if __name__ == '__main__':
    TestSuiteRun().run_test(XjbServiceTest_01)
    # TestSuiteRun().run_test(XjbServiceTest_02)
