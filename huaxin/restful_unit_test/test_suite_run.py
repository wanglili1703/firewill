# coding=utf-8

import inspect
import os
import re


def get_resource_root_path():
    string_separator = 'huaxin'
    current_module_path = inspect.getmodule(get_resource_root_path).__file__
    init_path = re.split(string_separator, current_module_path)[0]
    resource_path = os.path.normpath(os.path.join(init_path, string_separator))
    return resource_path


import unittest
import BSTestRunner
from _common.global_controller import GlobalController

class TestSuiteRun(object):
    def run_test(self, class_name):
        suite = unittest.TestLoader().loadTestsFromTestCase(class_name)

        filePath = get_resource_root_path() + '/pyResult.html'
        fp = file(filePath, 'wb')

        runner = BSTestRunner.BSTestRunner(stream=fp, title='Restful Service Test Report',
                                           description='service is: ' + GlobalController.RESTFUL_CONNECT)

        runner.run(suite)
