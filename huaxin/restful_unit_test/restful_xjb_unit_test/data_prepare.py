# coding=utf-8
import datetime
import decimal
import inspect
import os
import re
import sys
import time

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
from _tools.restful_xjb_tools import RestfulXjbTools
from restful_unit_test.test_suite_run import TestSuiteRun


@ddt
class XjbServiceTest_DataPrepare(unittest.TestCase):
    def setUp(self):
        self._restful_xjb = RestfulXjbTools()
        self._db = MysqlXjbTools()

    def tearDown(self):
        return

    @file_data('test_data/dataprepare.json')
    def test_register_binding_card_recharge_buy_product(self, mobile, password, card_bin, trade_password,
                                                        recharge_amount, product_id, amt, assert_info):
        # self._restful_xjb.register_binding_card(mobile=str(mobile), login_password=str(password),
        #                                         card_bin=str(card_bin),
        #                                         trade_password=str(trade_password))
        #
        # # self._restful_xjb.login_binding_card(mobile=str(mobile), login_password=str(password),
        # #                                      card_bin=str(card_bin), trade_password=str(trade_password))
        #
        # self._restful_xjb.risk_evaluating(user_name=str(mobile), login_password=str(password))
        #
        # self._restful_xjb.recharge(user_name=str(mobile), password=str(password),
        #                            trade_password=str(trade_password),
        #                            recharge_amount=str(recharge_amount))

        self._restful_xjb.buy_product(user_name=str(mobile), login_password=str(password), product_id=str(product_id),
                                      amt=str(amt), pay_type='0', trade_password=str(trade_password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])


if __name__ == '__main__':
    TestSuiteRun().run_test(XjbServiceTest_DataPrepare)
