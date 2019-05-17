# coding: utf-8
import inspect
import os
import re
import sys




def get_resource_root_path():

    string_separator = 'huaxin'
    current_module_path = inspect.getmodule(get_resource_root_path).__file__
    init_path = re.split(string_separator, current_module_path)[0]
    resource_path = os.path.normpath(os.path.join(init_path, string_separator))
    return resource_path

sys.path.append(get_resource_root_path())

from ui_ios_xjb_3_0_unit_test.xjb_3_0_unit_test import UiIosXjb30UnitTest

class MainController(
    UiIosXjb30UnitTest
):
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'