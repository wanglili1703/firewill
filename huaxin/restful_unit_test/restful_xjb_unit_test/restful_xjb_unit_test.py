# coding=utf-8
import datetime
import decimal
import inspect
import os
import re
import sys
import time
import calendar
import math
import threading

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
from _common.utility import Utility
from _common.BusinessUtility import BusinessUtility




@ddt
class XjbServiceTest_01(unittest.TestCase):
    def setUp(self):
        self._restful_xjb = RestfulXjbTools()
        self._db = MysqlXjbTools()

    def tearDown(self):
        return

    # 验证产品列表返回信息
    def verify_product_info(self, actual_product_list, expected_product_list):
        for i in range(0, len(actual_product_list)):
            self.assertEqual(actual_product_list[i]['buyButtonDesc'], '')
            self.assertEqual(str(actual_product_list[i]['productType']), str(expected_product_list[i]['product_type']))
            self.assertEqual(str(actual_product_list[i]['productId']),
                             str(expected_product_list[i]['productid']))
            self.assertEqual(str(actual_product_list[i]['recommended']),
                             str(expected_product_list[i]['recommended']))
            self.assertEqual(str(actual_product_list[i]['type']), str(expected_product_list[i]['product_type']))
            self.assertEqual(str(actual_product_list[i]['productTitle']),
                             str(expected_product_list[i]['product_short_name']))
            self.assertEqual(str(actual_product_list[i]['canRedeemAnytime']),
                             str(expected_product_list[i]['is_redem_anytime']))
            self.assertEqual(
                str(decimal.Decimal(actual_product_list[i]['minAmount']).quantize(decimal.Decimal('0.00'))),
                str(expected_product_list[i]['min_subscribe_amount']))

    # 用户登录
    @file_data('test_data/test_login.json')
    def test_login(self, user_name, password, is_successful, assert_info):
        self._restful_xjb.login(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertIn(assert_info["returnMsg"], entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if str(is_successful) == 'true':
            cust_no = entity.custNo
            trade_account = entity.tradeAccount
            expected_cust_no = self._db.get_cust_info(columns='cust_no', match='=', mobile=str(user_name))[0]['cust_no']
            expected_trade_acco = self._db.get_trade_acco_info(cust_no=str(expected_cust_no))[0]['trade_acco']

            self.assertEqual(str(cust_no), expected_cust_no)
            self.assertEqual(str(trade_account), expected_trade_acco)

    # 注册绑工商银行卡
    @data(
        (Utility.GetData().mobile(), '12qwaszx', '622202', '135790', {'returnCode': '000000', 'returnMsg': ''}),
    )
    @unpack
    def test_register_binding_card(self, mobile, login_password, card_bin, trade_password, assert_info):
        self._restful_xjb.register_binding_card(mobile=str(mobile), login_password=login_password,
                                                card_bin=card_bin, trade_password=trade_password)

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        cards = self._db.get_cust_debit_card(bank_mobile=str(mobile))
        self.assertEqual(str(cards[0]['card_no']), self._restful_xjb.entity.card_no)
        self.assertEqual(cards[0]['type'], '1')
        self.assertEqual(str(cards[0]['accept_mode']), 'M')

    # 登录绑卡
    @file_data('test_data/login_binding_card.json')
    def test_login_binding_card(self, user_name, login_password, card_bin, trade_password, assert_info):
        self._restful_xjb.login_binding_card(mobile=str(user_name), login_password=str(login_password),
                                             card_bin=str(card_bin), trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        cards = self._db.get_cust_debit_card(bank_mobile=str(user_name))
        self.assertEqual(str(cards[0]['card_no']), self._restful_xjb.entity.card_no)
        self.assertEqual(cards[0]['type'], '1')
        self.assertEqual(str(cards[0]['accept_mode']), 'M')

    # 登录-充值
    @file_data('test_data/test_recharge.json')
    def test_recharge(self, user_name, password, trade_password, recharge_amount, bank_card_id, is_successful,
                      assert_info):
        self._restful_xjb.recharge(user_name=str(user_name), password=str(password), trade_password=str(trade_password),
                                   recharge_amount=str(recharge_amount),
                                   bank_card_id=str(bank_card_id))

        entity = self._restful_xjb.entity.current_entity

        self.assertIn(assert_info["returnMsg"], entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if str(is_successful) == 'true':
            self.assertEqual(str(entity.body_returnResult), 'Y')
            self.assertEqual(entity.body_title, u'存入成功')
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            self.assertEqual(str(trade_request[0]['APKIND']), '022')
            self.assertEqual(str(trade_request[0]['SUB_APKIND']), '001100')
            self.assertEqual(str(trade_request[0]['SUB_AMT']),
                             str(decimal.Decimal(str(recharge_amount)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_request[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_request[0]['RTTA_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '0')

            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '001')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '001010')
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(recharge_amount)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['SUCC_AMT']),
                             str(decimal.Decimal(str(recharge_amount)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['TO_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['STATUS']), 'Y')

    # 现金宝收支明细
    @file_data('test_data/test_get_xjb_trade_list.json')
    def test_get_xjb_trade_list(self, user_name, password, assert_info):
        self._restful_xjb.get_xjb_trade_list(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 交易记录
    @file_data('test_data/test_get_trade_list.json')
    def test_get_trade_list(self, user_name, password, product_type, assert_info):
        self._restful_xjb.get_trade_list(user_name=str(user_name), password=str(password),
                                         product_type=str(product_type))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 注册
    @data(
        (Utility.GetData().mobile(), 'a0000000', 'true', {'returnCode': '000000', 'returnMsg': ''}),
        ('15244808911', 'a0000000', 'false', {'returnCode': '030031', 'returnMsg': u'该手机号已存在'}),
        # ('15244808911', 'a0000000', 'false', {'returnCode': '030017', 'returnMsg': u'手机号注册过'}),
        (Utility.GetData().mobile(), '', 'false', {'returnCode': '081501', 'returnMsg': u'请输入密码'}),
        ('152448089', 'a0000000', 'false', {'returnCode': '030001', 'returnMsg': u'请输入正确的手机号码'}),
        (Utility.GetData().mobile(), '12345678', 'false',
         {'returnCode': '030003', 'returnMsg': u'登录密码需包含字母、数字、符号的任意两种，请重新输入'}),
        (Utility.GetData().mobile(), 'wd34534', 'false', {'returnCode': '030077', 'returnMsg': u'密码需由8~20位字母、数字、符号组成'}),
        (Utility.GetData().mobile(), 'wd3453fg3tdw335567432', 'false',
         {'returnCode': '030077', 'returnMsg': u'密码需由8~20位字母、数字、符号组成'}),
        (Utility.GetData().mobile(), 'wd3453fg3tdw3355674323', 'false',
         {'returnCode': '030077', 'returnMsg': u'密码需由8~20位字母、数字、符号组成'}),
        (
                Utility.GetData().mobile(), '234w×÷er', 'false',
                {'returnCode': '030077', 'returnMsg': u'密码需由8~20位字母、数字、符号组成'}),
        ('152448089113', 'a0000000', 'false', {'returnCode': '030001', 'returnMsg': u'请输入正确的手机号码'}),
        ('152448089113444444', 'a0000000', 'false', {'returnCode': '030001', 'returnMsg': u'请输入正确的手机号码'}),
        ('', 'a0000000', 'false', {'returnCode': '081503', 'returnMsg': u'手机号码格式错误'}),
        ('1524480 8911', 'a0000000', 'false', {'returnCode': '030001', 'returnMsg': u'请输入正确的手机号码'}),
        ('1524480a891', 'a0000000', 'false', {'returnCode': '030001', 'returnMsg': u'请输入正确的手机号码'}),
    )
    @unpack
    def test_register(self, mobile, login_password, is_succesful, assert_info):
        self._restful_xjb.register(mobile=mobile, login_password=login_password)

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        if str(is_succesful) == 'true':
            cust_info = self._db.get_cust_info(columns='cust_no', match='=', mobile=str(mobile))
            trade_acco_info = self._db.get_trade_acco_info(cust_no=str(cust_info[0]['cust_no']))
            is_need_active_salary_card = entity.body_isNeedActiveSalaryCard
            is_need_sign_protocol = entity.body_isNeedSignProtocol
            self.assertEqual(str(entity.body_custNo), str(cust_info[0]['cust_no']))
            self.assertEqual(str(entity.body_tradeAccount), str(trade_acco_info[0]['trade_acco']))
            self.assertEqual(str(is_need_active_salary_card), '0')
            self.assertEqual(str(is_need_sign_protocol), '0')

    # 首页总资产
    @file_data('test_data/test_total_asset.json')
    def test_get_total_asset(self, user_name, password, assert_info):
        self._restful_xjb.get_total_asset(user_name=str(user_name), login_password=str(password))
        vacco_asset, dqb_asset, vip_asset, fund_asset = self._db.trade_asset_total_home_page(mobile=user_name)
        total_asset = vacco_asset + dqb_asset + vip_asset + fund_asset

        entity = self._restful_xjb.entity.current_entity
        actual_total_asset = entity.totalAsset

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(str(actual_total_asset), str(decimal.Decimal(total_asset).quantize(decimal.Decimal('0.00'))))

    # 首页资产概要
    @file_data('test_data/trade_asset_total_home_page.json')
    def test_trade_asset_total_home_page(self, user_name, password, assert_info):
        self._restful_xjb.trade_asset_total_home_page(user_name=str(user_name), password=str(password))
        vacco_asset, dqb_asset, vip_asset, fund_asset = self._db.trade_asset_total_home_page(mobile=user_name)
        fund_total_profit = self._db.get_cust_total_profit(mobile=str(user_name), prod_type='2')
        dqb_total_profit = self._db.get_cust_total_profit(mobile=str(user_name), prod_type='1')
        vip_total_profit = self._db.get_cust_total_profit(mobile=str(user_name), prod_type='3')
        total_income = fund_total_profit + dqb_total_profit + vip_total_profit
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(str(entity.body_dqbTotalAssert), str(dqb_asset))
        self.assertEqual(str(entity.body_dqbTotalProfit), str(dqb_total_profit))
        self.assertEqual(str(entity.body_fundTotalAsset),
                         str(decimal.Decimal(fund_asset).quantize(decimal.Decimal('0.00'))))
        self.assertEqual(str(entity.body_fundTotalIncome), str(fund_total_profit))
        self.assertEqual(str(entity.body_totalIncomeValue), str(total_income))
        self.assertEqual(str(entity.body_vipTotalAssert), str(vip_asset))
        self.assertEqual(str(entity.body_vipTotalProfit), str(vip_total_profit))
        self.assertEqual(str(entity.body_xjbBalance), str(vacco_asset))

    # 基金搜索提示
    @file_data('test_data/fund_search_suggestion.json')
    def test_fund_search_suggestion(self, user_name, password, type, keyword, pageNo, pageSize, assert_info):
        self._restful_xjb.fund_search_suggestion(user_name=str(user_name), password=str(password), type=str(type),
                                                 keyword=str(keyword), pageNo=str(pageNo), pageSize=str(pageSize))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 交易-查询用户各类产品资产明细列表
    @file_data('test_data/trade_asset_detail_list.json')
    def test_trade_asset_detail_list(self, user_name, password, assert_info):
        self._restful_xjb.trade_asset_detail_list(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 基金（高端）认购／申购
    @file_data('test_data/test_buy_product.json')
    def test_buy_product(self, user_name, password, product_id, pay_type, amt, product_status, trade_password,
                         assert_info):
        self._restful_xjb.buy_product(user_name=str(user_name), login_password=str(password),
                                      product_id=str(product_id),
                                      pay_type=str(pay_type), amt=str(amt),
                                      trade_password=str(trade_password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            self.assertEqual(str(entity.returnResult), 'Y')
            self.assertIn('申请已受理', str(entity.title))
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))

            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['STATUS']), 'A')
            self.assertEqual(str(trade_order[0]['VALIDATE_PHONE']), str(user_name))
            if str(product_id).__contains__('05'):
                self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '2')
                if str(product_status) == '认购':
                    # 012 认购 012020 现金宝认购
                    self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
                    self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012020')
                elif str(product_status) == '申购':
                    # 013 申购 013020 现金宝申购
                    self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '013')
                    self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '013020')
            elif str(product_id).__contains__('H9'):
                self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '3')
                if str(product_status) == '认购':
                    # 012 认购 012020 现金宝认购
                    self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
                    self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012020')
                elif str(product_status) == '申购':
                    # 013 申购 013020 现金宝申购
                    self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '013')
                    self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '013020')

            if str(product_id).__contains__('05'):
                self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
                self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
                self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
                self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['RTTA_ST']), 'N')
                self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
                self.assertEqual(str(trade_request[0]['SUB_AMT']),
                                 str(decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
                if str(trade_request[0]['PROD_ID']) == str(product_id):
                    # 012 认购
                    self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
                    self.assertEqual(str(trade_request[0]['PROD_TYPE']), '2')
                    self.assertEqual(str(trade_request[0]['TANO']), str(product_id).split('#')[0])
                    self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
                    self.assertEqual(str(trade_request[0]['REDEEM_PAYMENT_TYPE']), '0')
                    if str(product_status) == '认购':
                        # 020 认购 020010 认购基金
                        self.assertEqual(str(trade_request[0]['APKIND']), '020')
                        self.assertEqual(str(trade_request[0]['SUB_APKIND']), '020010')
                    elif str(product_status) == '申购':
                        # 022 申购 022212 申购基金
                        self.assertEqual(str(trade_request[0]['APKIND']), '022')
                        self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022212')
                elif str(trade_request[0]['PROD_ID']) == 'ZX05#000730':
                    # 022 申购
                    self.assertEqual(str(trade_request[0]['PROD_TYPE']), '0')
                    self.assertEqual(str(trade_request[0]['PROD_ID']), 'ZX05#000730')
                    self.assertEqual(str(trade_request[0]['TANO']), str(product_id).split('#')[0])
                    self.assertEqual(str(trade_request[0]['PAY_ST']), 'N')
                    self.assertEqual(str(trade_request[0]['REDEEM_PAYMENT_TYPE']), '')
                    if str(product_status) == '认购':
                        # 024 赎回 024011 赎回认购基金
                        self.assertEqual(str(trade_request[0]['APKIND']), '024')
                        self.assertEqual(str(trade_request[0]['SUB_APKIND']), '024011')
                    elif str(product_status) == '申购':
                        # 024 赎回 024011 赎回申购基金
                        self.assertEqual(str(trade_request[0]['APKIND']), '024')
                        self.assertEqual(str(trade_request[0]['SUB_APKIND']), '024012')

            # 认/申购高端产品，验证CTS_TRADE_RESERVE表
            if str(product_id).__contains__('H9'):
                self.assertEqual(str(trade_reserve[0]['SHARE_TYPE']), 'A')
                self.assertEqual(str(trade_reserve[0]['BRANCH_CODE']), '675')
                self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
                self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(product_id))
                self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '3')
                self.assertEqual(str(trade_reserve[0]['PURCHASE_PAYMENT_TYPE']), '0')
                self.assertEqual(str(trade_reserve[0]['REDEEM_PAYMENT_TYPE']), '0')
                self.assertEqual(str(trade_reserve[0]['TANO']), str(product_id).split('#')[0])
                self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
                                 str(decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
                if str(product_status) == '认购':
                    # 020 认购 002211 认购高端（来自现金宝）
                    self.assertEqual(str(trade_reserve[0]['APKIND']), '020')
                    self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '002211')
                elif str(product_status) == '申购':
                    # 申购 022 022210 申购高端（来自现金宝）
                    self.assertEqual(str(trade_reserve[0]['APKIND']), '022')
                    self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '022210')

            self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(asset_in_trasit[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
            self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                             str(decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
            if str(product_id).__contains__('H9'):
                # 020 认购 020010 认购基金
                self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '3')
                if str(product_status) == '认购':
                    # 020 认购 002211 认购高端（来自现金宝）
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '002211')
                elif str(product_status) == '申购':
                    # 申购 022 022210 申购高端（来自现金宝）
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '022')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '022210')
            elif str(product_id).__contains__('05'):
                # 022 申购 022212 申购基金
                self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '2')
                if str(product_status) == '认购':
                    # 020 认购 020010 认购基金
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '020010')
                elif str(product_status) == '申购':
                    # 申购 022 022212 申购基金
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '022')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '022212')

            self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_quty_chg[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
            self.assertEqual(str(trade_quty_chg[0]['TANO']), 'ZX05')
            self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                             str(-decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
            if str(trade_quty_chg[0]['APKIND']) == '024':
                if str(product_status) == '认购':
                    self.assertEqual(str(trade_quty_chg[0]['APKIND']), '024')
                    # 024011 现金宝赎回认购基金
                    self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '024011')
                elif str(product_status) == '申购':
                    # 024012 现金宝赎回申购基金
                    self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '024012')
            elif str(trade_quty_chg[0]['APKIND']) == '031':
                # 031 份额冻结
                self.assertEqual(str(trade_quty_chg[0]['APKIND']), '031')
                if str(product_status) == '认购':
                    # 031002 认购冻结
                    self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '031002')
                elif str(product_status) == '申购':
                    # 031003 申购冻结
                    self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '031003')

    # 基金赎回
    @file_data('test_data/test_redeem_fund.json')
    def test_redeem_fund(self, user_name, password, product_id, sold_share, trade_password, sold_type, is_success,
                         assert_info):
        self._restful_xjb.redeem_product(user_name=str(user_name), login_password=str(password),
                                         product_id=str(product_id), sold_share=str(sold_share),
                                         trade_password=str(trade_password), sold_type=str(sold_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(sold_type) == '0':
            if str(is_success) == 'true':
                trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
                return_result = entity.returnResult

                # 校验交易表
                self.assertEqual(str(return_result), 'Y')
                self.assertEqual(trade_request[0]['APKIND'], '024')
                self.assertEqual(trade_request[0]['SUB_APKIND'], '024013')
                self.assertEqual(trade_request[0]['SUB_AMT'],
                                 decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(trade_request[0]['PROD_ID'], str(product_id))
                self.assertEqual(trade_request[0]['RTTA_ST'], 'N')
                self.assertEqual(trade_request[0]['PAY_ST'], 'N')
                self.assertEqual(trade_request[0]['APPLY_ST'], 'Y')
                self.assertEqual(trade_request[0]['PROD_TYPE'], 2)
                self.assertEqual(trade_request[0]['REMARK'], '赎回基金')

                # 校验订单表
                self.assertEqual(trade_order[0]['ORDER_APKIND'], '016')
                self.assertEqual(trade_order[0]['ORDER_SUB_APKIND'], '016010')
                self.assertEqual(trade_order[0]['AP_AMT'],
                                 decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(trade_order[0]['TO_PROD'], 'ZX05#000730')
                self.assertEqual(trade_order[0]['TO_PROD_TYPE'], 0)
                self.assertEqual(trade_order[0]['STATUS'], 'A')

        if str(sold_type) == '1':
            if str(is_success) == 'true':
                trade_request, trade_order = self._db.get_trade_request_vip_product(mobile=str(user_name),
                                                                                    product_id=str(product_id))
                pdc_marketing = self._db.get_pdc_product_marketing(product_id=str(product_id))
                fund_nav, count_fund_nav = self._db.get_fund_nav(fund_id=str(product_id))
                redeem_amt_order = decimal.Decimal(sold_share) * pdc_marketing[0]['fast_redeem_cashratio'] * \
                                   fund_nav[0]['nav'] / 100 - pdc_marketing[0]['fast_redeem_rate']
                redeem_amt_request = decimal.Decimal(sold_share) * pdc_marketing[0]['fast_redeem_cashratio'] * \
                                     fund_nav[0]['nav'] / 100
                if len(str(redeem_amt_order)) > 4 and int(str(redeem_amt_order)[4:len(str(redeem_amt_order))]) > 0:
                    redeem_amt_order = float(str(redeem_amt_order)[0:4]) + 0.01

                if len(str(redeem_amt_request)) > 4 and int(
                        str(redeem_amt_request)[4:len(str(redeem_amt_request))]) > 0:
                    redeem_amt_request = float(str(redeem_amt_request)[0:4]) + 0.01

                # 校验订单表
                self.assertEqual(trade_order[0]['ORDER_APKIND'], '019')
                self.assertEqual(trade_order[0]['ORDER_SUB_APKIND'], '019010')
                self.assertEqual(trade_order[0]['AP_AMT'],
                                 decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(trade_order[0]['TO_PROD'], 'ZX05#000730')
                self.assertEqual(trade_order[0]['TO_PROD_TYPE'], 0)
                self.assertEqual(trade_order[0]['STATUS'], 'A3')
                self.assertEqual(
                    decimal.Decimal(trade_order[0]['FAST_REDEEM_SUB_AMT']).quantize(decimal.Decimal('0.00')),
                    decimal.Decimal(str(redeem_amt_order)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(
                    decimal.Decimal(str(pdc_marketing[0]['fast_redeem_rate'])).quantize(decimal.Decimal('0.00')),
                    decimal.Decimal(str(trade_order[0]['FAST_REDEEM_FEE'])).quantize(decimal.Decimal('0.00')))
                self.assertEqual(
                    decimal.Decimal(str(pdc_marketing[0]['fast_redeem_cashratio'])).quantize(
                        decimal.Decimal('0.00')),
                    decimal.Decimal(str(trade_order[0]['FAST_REDEEM_CASH_RATIO'])).quantize(
                        decimal.Decimal('0.00')))

                # 校验交易表
                self.assertEqual(trade_request[0]['APKIND'], '024')
                self.assertEqual(trade_request[0]['SUB_APKIND'], '024020')
                self.assertEqual(trade_request[0]['SUB_AMT'],
                                 decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(trade_request[0]['PROD_ID'], str(product_id))
                self.assertEqual(trade_request[0]['PROD_TYPE'], 2)
                self.assertEqual(trade_request[0]['REMARK'], '赎回基金')
                self.assertEqual(
                    decimal.Decimal(trade_request[0]['FAST_REDEEM_AMT']).quantize(decimal.Decimal('0.00')),
                    decimal.Decimal(str(redeem_amt_request)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(
                    decimal.Decimal(str(pdc_marketing[0]['fast_redeem_rate'])).quantize(decimal.Decimal('0.00')),
                    decimal.Decimal(str(trade_request[0]['FAST_REDEEM_FEE'])).quantize(decimal.Decimal('0.00')))
                self.assertEqual(
                    decimal.Decimal(str(pdc_marketing[0]['fast_redeem_cashratio'])).quantize(
                        decimal.Decimal('0.00')),
                    decimal.Decimal(str(trade_request[0]['FAST_REDEEM_CASH_RATIO'])).quantize(
                        decimal.Decimal('0.00')))

    # 高端赎回
    @file_data('test_data/test_redeem_vipproduct.json')
    def test_redeem_vipproduct(self, user_name, password, product_id, sold_share, trade_password, sold_type,
                               is_success, assert_info):
        self._restful_xjb.redeem_vipproduct(user_name=str(user_name), login_password=str(password),
                                            product_id=str(product_id), sold_share=str(sold_share),
                                            trade_password=str(trade_password), sold_type=str(sold_type))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(sold_type) == '0':
            if str(is_success) == 'true':
                trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
                trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
                return_result = entity.returnResult

                # 校验订单表
                self.assertEqual(str(return_result), 'Y')
                self.assertEqual(trade_order[0]['ORDER_APKIND'], '016')
                self.assertEqual(trade_order[0]['ORDER_SUB_APKIND'], '016010')
                self.assertEqual(trade_order[0]['AP_AMT'],
                                 decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(trade_order[0]['TO_PROD'], 'ZX05#000730')
                self.assertEqual(trade_order[0]['TO_PROD_TYPE'], 0)
                self.assertEqual(trade_order[0]['STATUS'], 'A')

                # 校验交易预约表
                self.assertEqual(str(return_result), 'Y')
                self.assertEqual(trade_reserve[0]['APKIND'], '024')
                self.assertEqual(trade_reserve[0]['SUB_APKIND'], '024014')
                self.assertEqual(trade_reserve[0]['SUB_AMT'],
                                 decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(trade_reserve[0]['PROD_ID'], str(product_id))
                self.assertEqual(trade_reserve[0]['PROD_TYPE'], 3)

        if str(sold_type) == '1':
            if str(is_success) == 'true':
                trade_request, trade_order = self._db.get_trade_request_vip_product(mobile=str(user_name),
                                                                                    product_id=str(product_id))
                pdc_marketing = self._db.get_pdc_product_marketing(product_id=str(product_id))
                redeem_amt = decimal.Decimal(sold_share) * pdc_marketing[0]['fast_redeem_cashratio'] / 100 - \
                             pdc_marketing[0][
                                 'fast_redeem_rate']

                # 校验订单表
                self.assertEqual(trade_order[0]['ORDER_APKIND'], '019')
                self.assertEqual(trade_order[0]['ORDER_SUB_APKIND'], '019020')
                self.assertEqual(trade_order[0]['AP_AMT'],
                                 decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(trade_order[0]['TO_PROD'], 'ZX05#000730')
                self.assertEqual(trade_order[0]['TO_PROD_TYPE'], 0)
                self.assertEqual(trade_order[0]['STATUS'], 'A3')
                self.assertEqual(
                    decimal.Decimal(trade_order[0]['FAST_REDEEM_SUB_AMT']).quantize(decimal.Decimal('0.00')),
                    decimal.Decimal(str(redeem_amt)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(
                    decimal.Decimal(str(pdc_marketing[0]['fast_redeem_rate'])).quantize(decimal.Decimal('0.00')),
                    decimal.Decimal(str(trade_order[0]['FAST_REDEEM_FEE'])).quantize(decimal.Decimal('0.00')))
                self.assertEqual(
                    decimal.Decimal(str(pdc_marketing[0]['fast_redeem_cashratio'])).quantize(
                        decimal.Decimal('0.00')),
                    decimal.Decimal(str(trade_order[0]['FAST_REDEEM_CASH_RATIO'])).quantize(
                        decimal.Decimal('0.00')))

                # 校验交易表
                self.assertEqual(trade_request[0]['APKIND'], '024')
                self.assertEqual(trade_request[0]['SUB_APKIND'], '024029')
                self.assertEqual(trade_request[0]['SUB_AMT'],
                                 decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(trade_request[0]['PROD_ID'], str(product_id))
                self.assertEqual(trade_request[0]['PROD_TYPE'], 3)
                self.assertEqual(trade_request[0]['REMARK'], '高端T+0极速赎回')
                self.assertEqual(
                    decimal.Decimal(trade_request[0]['FAST_REDEEM_AMT']).quantize(decimal.Decimal('0.00')),
                    decimal.Decimal(str(redeem_amt)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(
                    decimal.Decimal(str(pdc_marketing[0]['fast_redeem_rate'])).quantize(decimal.Decimal('0.00')),
                    decimal.Decimal(str(trade_request[0]['FAST_REDEEM_FEE'])).quantize(decimal.Decimal('0.00')))
                self.assertEqual(
                    decimal.Decimal(str(pdc_marketing[0]['fast_redeem_cashratio'])).quantize(
                        decimal.Decimal('0.00')),
                    decimal.Decimal(str(trade_request[0]['FAST_REDEEM_CASH_RATIO'])).quantize(
                        decimal.Decimal('0.00')))

    # 基金热门搜索
    @file_data('test_data/fund_hot_search.json')
    def test_fund_hot_search(self, user_name, password, assert_info):
        self._restful_xjb.fund_hot_search(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 基金-全部基金列表
    @file_data('test_data/test_fund_all_list.json')
    def test_fund_all_list(self, user_name, password, pageNo, pageSize, assert_info):
        self._restful_xjb.fund_all_list(user_name=str(user_name), password=str(password), pageNo=str(pageNo),
                                        pageSize=str(pageSize))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 基金八大部分
    @file_data('test_data/test_fund_eight_part.json')
    def test_fund_eight_part(self, user_name, password, assert_info):
        self._restful_xjb.fund_eight_part(user_name=str(user_name),
                                          password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 基金首页下方四大块内容
    @file_data('test_data/test_fund_index_four.json')
    def test_fund_index_four(self, user_name, password, assert_info):
        self._restful_xjb.fund_index_four(user_name=str(user_name),
                                          password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 基金筛选
    @file_data('test_data/test_fund_sizer.json')
    def test_fund_sizer(self, user_name, login_password, company_id, grade_org_id, grade_level, rise_min, rise_max,
                        rise_section, page_no, page_size, fund_type, assert_info):
        fund_ids, total_count, fund_types, nav, recommend_content = None, None, None, None, None
        if (str(fund_type) is not ''):
            fund_ids, total_count, fund_types, nav, recommend_content = self._restful_xjb.fund_sizer(
                user_name=str(user_name), login_password=str(login_password),
                company_id=str(company_id), grade_org_id=str(grade_org_id),
                grade_level=str(grade_level), rise_min=str(rise_min), rise_max=str(rise_max),
                rise_section=str(rise_section), page_no=str(page_no), page_size=str(page_size),
                fund_type=str(fund_type))

        else:
            fund_ids, total_count, nav, recommend_content = self._restful_xjb.fund_sizer(
                user_name=str(user_name), login_password=str(login_password),
                company_id=str(company_id), grade_org_id=str(grade_org_id),
                grade_level=str(grade_level), rise_min=str(rise_min), rise_max=str(rise_max),
                rise_section=str(rise_section), page_no=str(page_no), page_size=str(page_size),
                fund_type=str(fund_type))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        db_result = None
        count = None
        if entity.returnCode == '000000' and len(fund_ids) is not 0:
            count, db_result = self._db.fund_sizer_info_verify(rise_min, rise_max, grade_org_id, grade_level,
                                                               rise_section,
                                                               company_id, fund_type)

            print "the expected data is : ", count, db_result

            self.assertEqual(count, int(total_count), "verify total count retured")

            # considering the paging, if the count >= 20, only verify total count, otherwise, need to verify the data details.
            if count <= 20:
                for i in range(0, len(fund_ids)):
                    print "----verify fund ids----"
                    self.assertTrue(fund_ids, "verify fund id")
                for i in range(0, len(db_result)):
                    self.assertTrue(db_result[i]['nav'] in nav, "verify fund nav")
                if str(fund_type) is not '':
                    for i in range(0, len(db_result)):
                        self.assertTrue(db_result[i]['fund_type'] in fund_type, "verify fund type")

    # 基金星级排行：全部
    @file_data('test_data/test_fund_star_level.json')
    def test_fund_all_star_level_order(self, user_name, login_password, grade_org_id, page_no,
                                       assert_info):
        print "------start to do star level sort for all funds"
        total_count, grade_levels = self._restful_xjb.fund_all_star_level_order(
            user_name=str(user_name),
            login_password=str(login_password),
            grade_org_id=str(grade_org_id),
            page_no=str(page_no))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        print "fund star level is sorted by desc by default"
        self.assertTrue(grade_levels[0] >= grade_levels[len(grade_levels) - 1])

    # 精选基金
    @file_data('test_data/test_fund_best_choices.json')
    def test_fund_best_choices_list(self, user_name, password, page_no, assert_info):
        self._restful_xjb.fund_best_choices_fund_list(user_name=str(user_name), password=str(password),
                                                      page_no=str(page_no))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            fund_best_choices_list = self._db.get_fund_best_choices_list()
            self.assertEqual(str(entity.totalCount), str(len(fund_best_choices_list)))

    # 基金公司列表
    def test_fund_company_list(self):
        print "start to test fund company list"

        fund_company_list = self._restful_xjb.fund_company_list()
        entity = self._restful_xjb.entity.current_entity

        print "fund company list is: ", fund_company_list
        self.assertEqual(entity.returnCode, "000000")
        self.assertEqual(entity.returnMsg, '')
        # self.assertEqual(len(fund_company_list), 32)

    # 基金类型列表
    @file_data('test_data/test_fund_type_list.json')
    def test_fund_type_list(self, user_name, password, assert_info):

        fund_type_list = self._restful_xjb.fund_type_list(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        expected_fund_type = {"", "1", "0", "3", "2", "4", "8", "11"}

        self.assertEqual(len(fund_type_list), len(expected_fund_type))
        for i in range(0, len(fund_type_list) - 1):
            self.assertTrue(fund_type_list[i] in expected_fund_type)

    # 删除自选基金
    @file_data('test_data/test_fund_del_fav.json')
    def test_fund_del_fav(self, user_name, password, objectIds, favType, assert_info):
        print "start to test fund del fav"
        self._restful_xjb.fund_del_fav(user_name=str(user_name), password=str(password),
                                       objectIds=str(objectIds),
                                       favType=str(favType))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 新发基金
    @file_data("test_data/test_fund_new_fund.json")
    def test_fund_new_fund_list(self, user_name, password, page_no, page_size, assert_info):
        print "start to test new fund list"

        total_count, fund_list = self._restful_xjb.fund_new_fund_list(user_name=str(user_name),
                                                                      password=str(password),
                                                                      page_no=str(page_no),
                                                                      page_size=str(page_size))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        expected_fund_list = self._db.get_new_fund_list()

        self.assertEqual(int(total_count), len(expected_fund_list))
        if int(total_count) <= int(page_size) and int(page_no) == 1:
            for i in range(0, len(expected_fund_list)):
                self.assertTrue(expected_fund_list[i]['productid'] in fund_list)

    # 信用卡列表
    @file_data('test_data/test_get_creditcard_cust_cards.json')
    def test_get_creditcard_cust_cards(self, user_name, password, assert_info):
        card_serial_no, bank_no, card_tail_no = self._restful_xjb.creditcard_get_cust_cards(
            user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        expected_card_list = self._db.get_cust_credit_card(mobile=str(user_name), sort='asc')
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        self.assertEqual(len(card_serial_no), len(expected_card_list))
        if len(card_serial_no) > 0:
            for i in range(0, len(card_serial_no)):
                self.assertEqual(str(card_serial_no[i]), str(expected_card_list[i]['id']))
                self.assertEqual(str(bank_no[i]), str(expected_card_list[i]['bank_no']))
                self.assertEqual(str(card_tail_no[i]), str(expected_card_list[i]['card_no'])[-4:])

    # 新用户注册绑信用卡
    @data(
        (Utility.GetData().mobile(), '12qwaszx', '135790', '接口测试', {'returnCode': '000000', 'returnMsg': ''})
    )
    @unpack
    def test_register_creditcard_bind(self, mobile, password, trade_password, name, assert_info):
        serial_no, info, card_no = self._restful_xjb.register_creditcard_bind_card(mobile=str(mobile),
                                                                                   password=str(password),
                                                                                   trade_password=str(trade_password),
                                                                                   name=str(name))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

        expected_card_list = self._db.get_cust_credit_card(mobile=str(mobile), sort='desc')
        self.assertEqual(card_no, expected_card_list[0]['card_no'])

    # 老用户绑信用卡
    @file_data('test_data/test_old_user_bind_credit_card.json')
    def test_old_user_bind_credit_card(self, user_name, password, credit_card_no, assert_info):
        serial_no, info = self._restful_xjb.creditcard_bind_card_existing_user(mobile=str(user_name),
                                                                               password=str(password),
                                                                               credit_card_no=str(credit_card_no))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

        expected_card_list = self._db.get_cust_credit_card(mobile=str(user_name), sort='desc')
        self.assertEqual(credit_card_no, expected_card_list[0]['card_no'])

        if entity.returnCode == '000000':
            # 删除该用户下的信用卡
            self._db.del_cust_credit_card(mobile=str(user_name))

    # 绑信用卡失败情景
    @file_data('test_data/test_old_user_bind_credit_card_except.json')
    def test_old_user_bind_credit_card_negative(self, user_name, password, card_no, mobile_code, assert_info):
        self._restful_xjb.creditcard_bind_card_invalid_mobile_code(mobile=str(user_name), password=str(password),
                                                                   mobile_code=str(mobile_code), card_no=str(card_no))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

    # 获取信用卡匹配通道
    @file_data('test_data/test_creditcard_match_channel.json')
    def test_creditcard_match_channel_negative(self, user_name, password, card_no, assert_info):
        self._restful_xjb.creditcard_get_match_channel(user_name=str(user_name), password=str(password),
                                                       card_no=str(card_no))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 保存基金组合百分比
    @file_data('test_data/test_save_fund_combination.json')
    def test_save_fund_combination(self, user_name, password, object_ids, percents, assert_info):
        self._restful_xjb.save_fund_combination(user_name=str(user_name), password=str(password),
                                                object_ids=str(object_ids), percents=str(percents))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        object_id_list = str(object_ids).split(',')
        percents_list = str(percents).split(',')
        for i in range(0, len(object_id_list)):
            expected_fund_percent = self._db.get_fund_percent(mobile=str(user_name), object_id=object_id_list[i])
            self.assertEqual(percents_list[i], str(expected_fund_percent[0]['fund_set_percent']))

    # 信用卡卡状态
    @file_data('test_data/test_creditcard_status_info.json')
    def test_creditcard_card_status_info(self, user_name, password, card_no, is_delete, assert_info):
        delete_card_mobile, is_delete_card = self._restful_xjb.creditcard_status_info(user_name=str(user_name),
                                                                                      password=str(password),
                                                                                      card_no=str(card_no))
        entity = self._restful_xjb.entity.current_entity

        if str(is_delete) == '1':
            self.assertEqual(str(delete_card_mobile), str(user_name))
            self.assertEqual(str(is_delete_card), '1')
        else:
            self.assertEqual(str(delete_card_mobile), '')
            self.assertEqual(str(is_delete_card), '0')
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

    # 信用卡删除
    @file_data('test_data/test_creditcard_delete.json')
    def test_creditcard_delete(self, user_name, password, trade_password, is_successful, assert_info):
        card = self._db.get_cust_credit_card(mobile=str(user_name), sort='desc')

        # change the deleted creditcard to normal
        if str(is_successful) == 'true':
            self._db.update_deleted_cust_credit_card_to_normal(card_id=str(card[0]['id']))

        self._restful_xjb.creditcard_delete(user_name=str(user_name), password=str(password),
                                            trade_password=str(trade_password), card_id=str(card[0]['id']))

        entity = self._restful_xjb.entity.current_entity
        card = self._db.get_cust_credit_card(mobile=str(user_name), sort='desc')
        self.assertEqual(str(card[0]['state']), 'D')
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

    # 信用卡还款
    @file_data('test_data/test_creditcard_repay.json')
    def test_creditcard_repay(self, user_name, password, amt, trade_password, is_successful, image_id, assert_info):
        card = self._db.get_cust_credit_card(mobile=str(user_name), sort='desc')
        self._restful_xjb.creditcard_bind_card_repay(mobile=str(user_name), password=str(password),
                                                     card_id=str(card[0]['id']), amt=str(amt),
                                                     trade_password=str(trade_password), image_id=str(image_id))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertTrue(assert_info['returnMsg'] in entity.returnMsg)

        if str(is_successful) == 'true':
            time.sleep(10)
            creditcard_repay_req = self._db.get_creditcard_repay_requests(mobile=str(user_name))
            self.assertEqual(str(entity.info), '信用卡还款申请已受理！')
            self.assertEqual(str(entity.returnResult), 'I')

            self.assertEqual(creditcard_repay_req[0]['repay_type'], 'M')
            self.assertEqual(creditcard_repay_req[0]['amount'],
                             decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00')))
            self.assertEqual(creditcard_repay_req[0]['card_no'], str(card[0]['card_no']))
            self.assertEqual(creditcard_repay_req[0]['accept_mode'], 'M')
            self.assertEqual(creditcard_repay_req[0]['tran_st'], 'Y')
            self.assertEqual(creditcard_repay_req[0]['success_amount'],
                             decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00')))

    # 基金星级排行：基金类型+排序
    @file_data('test_data/test_fund_type_order_star_level.json')
    def test_fund_all_order_star_level_order(self, user_name, login_password, grade_org_id, order_type,
                                             fund_type,
                                             page_no, assert_info):
        print "------start to do star level sort for all funds with order"
        total_count, grade_levels, fund_types = self._restful_xjb.fund_type_order_star_level_order(
            user_name=str(user_name),
            login_password=str(
                login_password),
            grade_org_id=str(grade_org_id),
            order_type=str(order_type),
            fund_type=str(fund_type),
            page_no=str(page_no))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        print "fund star level sort under grade org, fund type and order type"
        # order_type = -1 默认，应该就是降序，order_type = 1, 降序， order_type=0, 升序
        if int(order_type) == -1 or int(order_type) == 1:
            self.assertTrue(grade_levels[0] >= grade_levels[len(grade_levels) - 1])
        else:
            # 需求是：没有星级排最后， grade_level=0
            if int(grade_levels[len(grade_levels) - 1]) == 0:
                self.assertTrue(int(grade_levels[0]) >= 0)
            else:
                self.assertTrue(grade_levels[0] <= grade_levels[len(grade_levels) - 1])

        print "verify fund type"

        for i in range(0, len(fund_types) - 1):
            self.assertEqual(str(fund_types[i]), str(fund_type))

    # 信用卡重复预约还款
    @file_data('test_data/test_creditcard_repay_yy_duplicate.json')
    def test_credit_card_repay_schedule_duplicate(self, user_name, password, amt, trade_password, image_id,
                                                  assert_info):
        card = self._db.get_cust_credit_card(mobile=str(user_name), sort='desc')
        self._db.update_creditcard_order_state(card_id=str(card[0]['id']), orign_state='N', update_state='C')
        self._restful_xjb.creditcard_repay_schedule(user_name=str(user_name), password=str(password),
                                                    repay_amt=str(amt), card_serial_no=str(card[0]['id']),
                                                    trade_password=str(trade_password), image_id=str(image_id))
        self._restful_xjb.creditcard_repay_schedule(user_name=str(user_name), password=str(password),
                                                    repay_amt=str(amt), card_serial_no=str(card[0]['id']),
                                                    trade_password=str(trade_password), image_id=str(image_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

    # 信用卡预约还款 设置还款日在后天
    @file_data('test_data/test_creditcard_repay_yy.json')
    def test_credit_card_repay_schedule(self, user_name, password, amt, is_successful, trade_password, image_id,
                                        assert_info):
        card = self._db.get_cust_credit_card(mobile=str(user_name), sort='desc')
        self._db.update_creditcard_order_state(card_id=str(card[0]['id']), orign_state='N', update_state='C')
        self._restful_xjb.creditcard_repay_schedule(user_name=str(user_name), password=str(password),
                                                    repay_amt=str(amt), card_serial_no=str(card[0]['id']),
                                                    trade_password=str(trade_password), image_id=str(image_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertTrue(assert_info['returnMsg'] in entity.returnMsg)
        if str(is_successful) == 'true':
            credit_card_repay_order = self._db.get_creditcard_repay_order(card_id=str(card[0]['id']))
            self.assertEqual(credit_card_repay_order[0]['amount'],
                             decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00')))
            the_day_after_tomorrow = Utility.DateUtil().getToday() + datetime.timedelta(days=2)
            the_day_after_today = the_day_after_tomorrow - datetime.timedelta(days=1)
            # 还款日 D1
            self.assertEqual(str(credit_card_repay_order[0]['repay_date']),
                             the_day_after_tomorrow.strftime('%Y%m%d'))
            # 实际还款日 = 还款日的前一天，如果还款日是非工作日，如周六，周日，则实际扣款日为周五
            while self._db.determine_if_work_day(the_day_after_today.strftime('%Y%m%d')) is False:
                the_day_after_today = the_day_after_today - datetime.timedelta(days=1)

            self.assertEqual(str(credit_card_repay_order[0]['real_repay_date']),
                             the_day_after_today.strftime('%Y%m%d'))

            # 判断是否为工作日，不是获取下个工作日
            new_work_date = self._db.judge_is_work_date(day=str(the_day_after_tomorrow).replace('-', ''))
            the_day_after_tomorrow = new_work_date[0]['WORK_DATE']
            self.assertEqual(str(credit_card_repay_order[0]['repay_work_date']), str(the_day_after_tomorrow))
            self.assertEqual(str(credit_card_repay_order[0]['state']), 'N')
            self.assertEqual(str(credit_card_repay_order[0]['check_state']), 'N')
            self.assertEqual(str(credit_card_repay_order[0]['repay_state']), 'N')

    # 取消信用卡预约
    @file_data('test_data/test_credit_card_yy_repay_order_cancel.json')
    def test_credit_card_yy_repay_order_cancel(self, user_name, password, order_serial_no, is_successful, assert_info):
        card = self._db.get_cust_credit_card(mobile=str(user_name), sort='desc')
        order = self._db.get_creditcard_repay_order(card_id=str(card[0]['id']))

        # 如果数据文件里面没有传订单流水号，就从数据库里取，否则用数据库文件里的
        if str(order_serial_no) == '':
            order_serial_no = order[0]['order_serial_no']

        # 将取消的预约单还原
        if str(is_successful) == 'true':
            self._db.update_creditcard_order_state(card_id=str(card[0]['id']), orign_state='C', update_state='N')
        self._restful_xjb.cacel_credit_card_repay_order(user_name=str(user_name), password=str(password),
                                                        order_serial_no=str(order_serial_no))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        if str(is_successful) == 'true':
            credit_card_repay_order = self._db.get_creditcard_repay_order(card_id=str(card[0]['id']))
            self.assertEqual(str(credit_card_repay_order[0]['state']), 'C')

    # 删除有预约还款的信用卡
    @file_data('test_data/test_creditcard_delete_with_repay_order.json')
    def test_creditcard_delete_with_repay_order(self, user_name, password, card_no, trade_password, is_successful,
                                                image_id, assert_info):
        card = self._db.get_cust_credit_card_by_card_no(card_no=str(card_no))
        self._db.update_deleted_cust_credit_card_to_normal(card_id=str(card[0]['id']))

        self._db.update_creditcard_order_state(card_id=str(card[0]['id']), orign_state='N', update_state='C')
        self._restful_xjb.creditcard_repay_schedule(user_name=str(user_name), password=str(password),
                                                    repay_amt='1', card_serial_no=str(card[0]['id']),
                                                    trade_password=str(trade_password), image_id=str(image_id))
        self._restful_xjb.creditcard_delete(user_name=str(user_name), password=str(password),
                                            trade_password=str(trade_password), card_id=str(card[0]['id']))

        entity = self._restful_xjb.entity.current_entity
        card = self._db.get_cust_credit_card_by_card_no(card_no=str(card_no))
        self.assertEqual(str(card[0]['state']), 'D')
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

        # change the deleted creditcard to normal
        if str(is_successful) == 'true':
            self._db.update_deleted_cust_credit_card_to_normal(card_id=str(card[0]['id']))

    # 信用卡还款记录
    @file_data('test_data/test_credit_card_record.json')
    def test_credit_card_record(self, user_name, password, card_no, card_type, is_successful, assert_info):
        card = self._db.get_cust_credit_card_by_card_no(card_no=str(card_no))
        self._restful_xjb.credit_card_repay_record_list(user_name=str(user_name), password=str(password),
                                                        bank_card_id=str(card[0]['id']), card_type=str(card_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

        if str(is_successful) == 'true':
            total_count = entity.totalCount
            trade_type = entity.tradeList_tradeType
            business_type = entity.tradeList_businessType
            trade_amt = entity.tradeList_tradeAmt

            trade_list = self._db.get_creditcard_repay_requests(mobile=str(user_name))

            self.assertEqual(str(total_count), str(len(trade_list)))
            for i in range(0, len(trade_type)):
                self.assertEqual(str(business_type[i]), '030')
                self.assertEqual(str(trade_amt[i]), str(trade_list[i]['amount']))

    # 信用卡默认还款日
    @file_data('test_data/test_credit_card_default_repay_date.json')
    def test_credit_card_default_repay_date(self, user_name, password, assert_info):
        self._restful_xjb.credit_card_default_repay_date(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

        nxt_month_last_date, start_date = self._db.get_work_day_after_the_day_after_tomorrow()
        pay_start_date = entity.body_payStartDate
        pay_end_date = entity.body_payEndDate
        self.assertEqual(str(pay_start_date), str(start_date))
        self.assertEqual(str(pay_end_date), nxt_month_last_date)

    # 信用卡真实还款日
    @file_data('test_data/test_credit_card_actual_repay_date.json')
    def test_credit_card_actual_repay_date(self, user_name, password, repay_date, is_successful, assert_info):

        if str(repay_date) == '':
            repay_date = (Utility.DateUtil().getToday() + datetime.timedelta(days=1)).strftime('%Y%m%d')

        self._restful_xjb.credit_card_actual_repay_date(user_name=str(user_name), password=str(password),
                                                        repay_date=str(repay_date))

        entity = self._restful_xjb.entity.current_entity
        actual_repay_date = entity.body_payDate
        # 实际还款日 = 还款日-2
        expected_repay_date = (datetime.datetime.strptime(repay_date, '%Y%m%d') - datetime.timedelta(days=1)).strftime(
            '%Y%m%d')
        if self._db.determine_if_work_day(date=expected_repay_date) is False:
            expected_repay_date = (
                datetime.datetime.strptime(repay_date, '%Y%m%d') - datetime.timedelta(days=2)).strftime('%Y%m%d')

        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        if str(is_successful) == 'true':
            self.assertEqual(str(actual_repay_date), expected_repay_date)

    # 我的积分
    @file_data('test_data/test_my_points.json')
    def test_my_points(self, user_name, password, assert_info):

        surplus_points = self._restful_xjb.my_points(user_name=str(user_name),
                                                     password=str(password))
        expected_ponits = self._db.my_points(self)
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(str(surplus_points), str(expected_ponits))

    # 获取基金经理
    @file_data('test_data/test_get_fund_manager.json')
    def test_get_fund_manager_info(self, user_name, password, fundId, assert_info):
        productinfo = self._restful_xjb.get_fund_manager_info(user_name=str(user_name),
                                                              password=str(password),
                                                              fundId=str(fundId))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(str(productinfo), str(fundId))

    # 基金申购费率
    @file_data('test_data/test_get_purchase_fee.json')
    def test_get_purchase_fee(self, user_name, password, fund_id, assert_info):
        self._restful_xjb.get_fund_purchase_fee(user_name=str(user_name), password=str(password),
                                                fund_id=str(fund_id))

        fund_rate, fund_rates = self._db.get_product_fee(product_id=str(fund_id))
        discount_rate_res = self._db.get_fund_discount_rate(product_id=str(fund_id))
        discount_rate = discount_rate_res[0]['discount'] / 100

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        actual_rates = entity.rate
        actual_rate_after_discount = entity.rateAfterDiscount
        fund_purchase_rate = entity.fundPurchaseRate

        for i in range(0, len(fund_purchase_rate)):
            self.assertIn(str(fund_rates[i]['start_div_stand']).split('.')[0], str(fund_purchase_rate[i]['amount']))
            if str(fund_purchase_rate[i]['rate']).find('%') != -1:
                # != -1 找不到%
                self.assertEqual(str(fund_purchase_rate[i]['rate']), '%s%%' % str(decimal.Decimal(
                    fund_rates[i]['min_charge_rate']).quantize(decimal.Decimal('0.00'))))
                self.assertEqual(str(fund_purchase_rate[i]['rateAfterDiscount']), '%s%%' % str(decimal.Decimal(
                    fund_rates[i]['min_charge_rate'] / 10).quantize(decimal.Decimal('0.00'))))
            else:
                self.assertEqual(str(fund_purchase_rate[i]['rate']), str(format(decimal.Decimal(
                    fund_rates[i]['min_charge_rate']).quantize(decimal.Decimal('0.00')), ',')) + '元')
                self.assertEqual(str(fund_purchase_rate[i]['rateAfterDiscount']), str(decimal.Decimal(
                    fund_rates[i]['min_charge_rate'] / 10).quantize(decimal.Decimal('0.00'))) + '元')

                # for i in range(0, len(fund_rates)):
                #     if str(fund_rates[i]).find('%') != -1:
                #         tmp = decimal.Decimal(str(fund_rates[i]).strip('%')).quantize(decimal.Decimal('0.00'))
                #         self.assertEqual(str(actual_rates[i]).replace(',', ''), str(tmp) + '%')
                #         expected_rate_after_discount = decimal.Decimal(discount_rate) * decimal.Decimal(str(fund_rates[i]).strip('%'))
                #         self.assertEqual(str(actual_rate_after_discount[i]),
                #                          str(expected_rate_after_discount.quantize(decimal.Decimal('0.00'))) + '%')
                #     else:
                #         tmp1 = decimal.Decimal(re.findall(r'\d+', str(fund_rates[i]))[0]) * decimal.Decimal(
                #             discount_rate)
                #         tmp1 = str(tmp1.quantize(decimal.Decimal('0.00')))
                #         tmp2 = re.findall(r'\d+.\d*', str(actual_rate_after_discount[i]))[0]
                #         # 验证费率
                #         self.assertEquals(re.findall(r'\d+.\d*', str(actual_rates[i]))[0].replace(',', ''),
                #                           str(re.findall(r'\d+', str(fund_rates[i]))[0]))
                #         # 验证折扣后费率
                #         self.assertEqual(tmp2, tmp1)

    # 基金买入费率计算
    @file_data('test_data/test_trade_calculate_fee.json')
    def test_trade_calculate_fee(self, user_name, password, purchase_amt, fund_id, is_successful, assert_info):
        self._restful_xjb.trade_caltFee(user_name=str(user_name), password=str(password),
                                        purchase_amt=str(purchase_amt), fund_id=str(fund_id))

        discount_rate_res = self._db.get_fund_discount_rate(product_id=str(fund_id))
        expected_discount_rate = discount_rate_res[0]['discount'] / 100

        # 费率
        expected_product_rate, rates = self._db.get_product_fee(product_id=str(fund_id),
                                                                purchase_amt=decimal.Decimal(purchase_amt))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if is_successful == 'true':
            # 验证估算费用 估算费用estimatedCost = 申购金额 - 申购金额/(1+折扣费率)）
            # 节省费用costSaving =（申购金额 - 申购金额/(1+申购费率)） - 估算费用
            cost_saving = entity.costSaving
            estimated_cost = entity.estimatedCost
            rate = entity.rate
            rate_after_discount = entity.rateAfterDiscount
            discount = entity.disCount
            # 计算折扣费率
            expected_rate_after_discount = (decimal.Decimal(expected_product_rate['min_charge_rate']) *
                                            decimal.Decimal(expected_discount_rate)).quantize(
                decimal.Decimal('0.00'))
            # 验证折扣费率
            self.assertEqual(str(rate_after_discount), str(expected_rate_after_discount) + '%')
            # 验证折扣率
            self.assertEqual(str(discount),
                             str(decimal.Decimal(expected_discount_rate).quantize(decimal.Decimal('0.00'))))

            # 验证估算费用
            expected_estimated_cost = (decimal.Decimal(purchase_amt) - decimal.Decimal(purchase_amt) / (
                1 + decimal.Decimal(expected_rate_after_discount) / 100)).quantize(decimal.Decimal('0.00'))
            self.assertEqual(str(estimated_cost).replace(',', ''), str(expected_estimated_cost))

            # 验证节省费用
            # 申购费用
            purchase_fee = (decimal.Decimal(purchase_amt) - decimal.Decimal(purchase_amt) / (
                1 + decimal.Decimal(str(rate).strip('%')) / 100)).quantize(decimal.Decimal('0.00'))
            expected_cost_saving = purchase_fee - expected_estimated_cost
            self.assertEqual(str(cost_saving).replace(',', ''), str(expected_cost_saving))

    # 取现额度查询
    @file_data('test_data/test_card_withdraw_limit.json')
    def test_debit_card_withdraw_limit_query(self, user_name, password, assert_info):
        bank_serial_id = self._db.get_cust_debit_card(bank_mobile=str(user_name))[0]['serial_id']
        self._restful_xjb.debit_card_withdraw_limit(user_name=str(user_name), password=str(password),
                                                    bank_serial_id=str(bank_serial_id))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 取现提示文案
    @file_data('test_data/test_with_draw_tip_info.json')
    def test_with_draw_tip_info(self, user_name, password, assert_info):
        # Must to verify this user trade time before 15:00 and after 15:00 on day
        self._restful_xjb.with_draw_tip_info(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        actual_arrived_date = entity.body_encaseInfo
        user_trade_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

        near_work_date = self._db.judge_is_work_date(day=str(user_trade_time)[0:8])[0]['WORK_DATE']
        if str(user_trade_time)[0:8] == str(near_work_date):  # 交易当天为工作日
            if str(user_trade_time)[8:14] < '150000':  # 交易当时为15：00之前
                expected_arrived_date = self._db.get_next_work_date(pre_work_date=str(user_trade_time)[0:8])[0][
                    'WORK_DATE']
            else:  # 交易当时为15：00之后
                next1_work_date = self._db.get_next_work_date(pre_work_date=str(user_trade_time)[0:8])[0]['WORK_DATE']
                expected_arrived_date = self._db.get_next_work_date(pre_work_date=str(next1_work_date))[0]['WORK_DATE']

        else:  # 交易当天为非工作日
            next1_work_date = self._db.get_next_work_date(pre_work_date=str(near_work_date))[0]['WORK_DATE']
            expected_arrived_date = self._db.get_next_work_date(pre_work_date=str(next1_work_date))[0]['WORK_DATE']

        self.assertEqual(str(actual_arrived_date),
                         '预计将于' + str(expected_arrived_date)[4:6] + '月' + str(
                             expected_arrived_date)[6:8] + '日' + '17点前到账')

    # 充值提示文案
    @file_data('test_data/test_recharge_tip_info.json')
    def test_recharge_tip_info(self, user_name, password, assert_info):
        # Must to verify this user recharge time before 15:00 and after 15:00 on day
        self._restful_xjb.recharge_tip_info(user_name=str(user_name), password=str(password))
        user_recharge_time = time.strftime('%H', time.localtime(time.time()))
        entity = self._restful_xjb.entity.current_entity
        income_date = entity.expectIncomeTipInfo
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        # self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertTrue(assert_info["returnMsg"] in entity.returnMsg)

        # 取当前任意日期时间为星期几
        today = int(time.strftime("%w"))

        # case1: 正常工作日交易
        if int(user_recharge_time) < 15 and today in range(1, 2, 3):
            # 如果用户是当日15:00前交易
            expected_calculate_profit_date = (Utility.DateUtil().getToday() + datetime.timedelta(days=1)).strftime(
                '%m{m}%d{d}').format(m='月', d='日', )
            expected_profit_get_date = (Utility.DateUtil().getToday() + datetime.timedelta(days=2)).strftime(
                '%m{m}%d{d}').format(m='月', d='日', )
            # 检查点设置
            self.assertTrue(expected_calculate_profit_date in str(income_date))
            self.assertTrue(expected_profit_get_date in str(income_date))

        elif int(user_recharge_time) > 15 and today in range(4, 5):
            # 如果用户时当天15:00之后交易
            expected_calculate_profit_date = (Utility.DateUtil().getToday() + datetime.timedelta(days=4)).strftime(
                '%m{m}%d{d}').format(m='月', d='日', )
            expected_profit_get_date = (Utility.DateUtil().getToday() + datetime.timedelta(days=5)).strftime(
                '%m{m}%d{d}').format(m='月', d='日', )
            # 检查点设置
            self.assertTrue(expected_calculate_profit_date in str(income_date))
            self.assertTrue(expected_profit_get_date in str(income_date))

        # case2: 如果取现日是非工作日（周六)
        if today == 6:
            # 如果用户时当天15:00之后交易
            expected_calculate_profit_date = (Utility.DateUtil().getToday() + datetime.timedelta(days=3)).strftime(
                '%m{m}%d{d}').format(m='月', d='日', )
            expected_profit_get_date = (Utility.DateUtil().getToday() + datetime.timedelta(days=4)).strftime(
                '%m{m}%d{d}').format(m='月', d='日', )
            # 检查点设置
            self.assertTrue(expected_calculate_profit_date in str(income_date))
            self.assertTrue(expected_profit_get_date in str(income_date))
        # 如果取现日是非工作日（周日）
        elif today == 7:
            expected_calculate_profit_date = (Utility.DateUtil().getToday() + datetime.timedelta(days=2)).strftime(
                '%m{m}%d{d}').format(m='月', d='日', )
            expected_profit_get_date = (Utility.DateUtil().getToday() + datetime.timedelta(days=3)).strftime(
                '%m{m}%d{d}').format(m='月', d='日', )
            # 检查点设置
            self.assertTrue(expected_calculate_profit_date in str(income_date))
            self.assertTrue(expected_profit_get_date in str(income_date))

    # 获取精品主题列表
    @file_data('test_data/test_get_market_index.json')
    def test_get_market_index(self, user_name, password, assert_info):
        self._restful_xjb.get_market_index(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        product_ids = entity.productId

        # 暂时的验证，目前没有找到关联的表
        self.assertEqual(len(product_ids), 4)

    # 交易密码验证
    @file_data('test_data/test_trade_password_validate.json')
    def test_trade_password_validate(self, user_name, password, trade_password, assert_info):
        self._restful_xjb.trade_password_validate(user_name=str(user_name), password=str(password),
                                                  trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertTrue(assert_info["returnMsg"] in entity.returnMsg)

    # 删除银行卡
    @file_data('test_data/test_delete_bank_card.json')
    def test_delete_bank_card(self, user_name, password, bank_card_id, card_no, trade_password, is_successful,
                              assert_info):
        cards = self._db.get_bank_card_by_card_no(mobile=str(user_name), card_no=str(card_no))
        # change deleted card to normal status
        if str(is_successful) == 'true':
            self._db.update_bank_card_delete_status(card_no=str(cards[0]['card_no']))

        self._restful_xjb.delete_bank_card(user_name=str(user_name), password=str(password),
                                           bank_card_id=str(bank_card_id),
                                           trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        cards = self._db.get_bank_card_by_card_no(mobile=str(user_name), card_no=str(card_no))
        if str(is_successful) == 'true':
            self.assertEqual(cards[0]['is_delete'], 'Y')

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 现金宝累计收益
    @file_data('test_data/test_xjb_last_profit.json')
    def test_xjb_last_profit(self, user_name, password, page_no, page_size, apkind, assert_info):
        self._restful_xjb.xjb_last_profit(user_name=str(user_name), password=str(password),
                                          page_no=str(page_no), page_size=str(page_size))
        entity = self._restful_xjb.entity.current_entity
        actual_totalProfit = entity.body_totalProfit
        expect_totalProfit = self._db.xjb_last_profit(mobile=str(user_name), apkind=str(apkind))

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(decimal.Decimal(actual_totalProfit), expect_totalProfit)

    # 联名卡激活
    @file_data('test_data/test_activate_joint_card.json')
    def test_activate_joint_card_successful(self, user_name, password, trade_password, is_successful, assert_info):
        self._restful_xjb.login_binding_card(mobile=str(user_name), login_password=str(password), card_bin='623595',
                                             trade_password=str(trade_password))
        cust_info = self._db.get_cust_info(columns='name, cert_no, cust_no', match='=', mobile=str(user_name))
        card_info = self._db.get_cust_debit_card(bank_mobile=str(user_name))[0]['card_no']
        self._db.insert_joint_card_activate_card(card_no=str(card_info), mobile=str(user_name))
        self._restful_xjb.joint_card_acitvate(card_no=str(card_info), mobile=str(user_name),
                                              name=str(cust_info[0]['name']), cert_type='0',
                                              cert_no=str(cust_info[0]['cert_no']))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if is_successful == 'true':
            joint_cards = self._db.get_joint_card(mobile=str(user_name), card_no=str(card_info))
            self.assertEqual(joint_cards[0]['cust_no'], cust_info[0]['cust_no'])
            self.assertEqual(joint_cards[0]['status'], 'N')

    # 获取是否联名卡
    @file_data('test_data/test_is_joint_card.json')
    def test_is_joint_card(self, user_name, password, card_no, assert_info):
        self._restful_xjb.is_joint_card(user_name=str(user_name), password=str(password), card_no=str(card_no))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        joint_card = self._db.get_joint_card(mobile=str(user_name), card_no=str(card_no))

        if len(joint_card) == 1:
            self.assertEqual(str(entity.result), '1')
        elif len(joint_card) == 0:
            self.assertEqual(str(entity.result), '0')

    # 设置过限额的联名卡详情
    @file_data('test_data/test_get_joint_card_detail.json')
    def test_get_joint_card_detail(self, user_name, password, card_no,
                                   assert_info):
        cards = self._db.get_cust_debit_card(bank_mobile=str(user_name))
        self._restful_xjb.get_cust_joint_card_detail(user_name=str(user_name), password=str(password),
                                                     bank_card_id=str(cards[0]['serial_id']))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        joint_card = self._db.get_joint_card(mobile=str(user_name))
        data_list = entity.custJointCard

        limit = self._db.get_nanyue_limit(card_no=str(card_no))
        pos_max_day = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'MAXPOSDAY\'')[0][
                'PM_V1']
        atm_max_day = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'MAXATMDAY\'')[0][
                'PM_V1']
        pos_max_once = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'MAXPOSQUOTA\'')[
                0][
                'PM_V1']
        atm_max_once = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'MAXATMQUOTA\'')[
                0][
                'PM_V1']
        single_amount = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'FASTWITHDRAWLIMIT\' and PM_CODE=\'SINGLEDAY\'')[0][
                'PM_V1']
        single_once_amount = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'FASTWITHDRAWLIMIT\' and PM_CODE=\'SINGLEQUOTA\'')[0][
                'PM_V1']

        self.assertEqual(data_list['bankGroupName'], u'南粤银行')
        self.assertEqual(data_list['canDelete'], u'1')
        self.assertEqual(data_list['canFastWithdraw'], u'1')
        self.assertEqual(data_list['canRecharge'], u'1')
        self.assertEqual(str(data_list['bankCardId']), str(cards[0]['serial_id']))
        self.assertEqual(data_list['isJointCard'], u'1')
        self.assertEqual(data_list['jointCardDesc'], u'南粤-华信联名卡')
        self.assertEqual(str(data_list['name']), joint_card[0]['name'])
        # 南粤银行身份证类型是1， 现金宝是0
        self.assertEqual(str(data_list['certType']), '0')
        self.assertEqual(str(data_list['cardType']), str(joint_card[0]['card_type']))
        self.assertEqual(str(data_list['certNo']), str(joint_card[0]['cert_no']))
        self.assertEqual(str(data_list['cardNo']), str(card_no))
        self.assertEqual(str(data_list['posWithdrawOnceLimitAmt']),
                         str(limit[0]['POS_ONCE_QUOTA']))
        self.assertEqual(str(data_list['posWithdrawDayLimitAmt']),
                         str(limit[0]['POS_DAY_QUOTA']))
        self.assertEqual(str(data_list['posWithdrawMaxDayLimitAmt']),
                         str(decimal.Decimal(pos_max_day).quantize(decimal.Decimal('0.00'))))
        self.assertEqual(str(data_list['posWithdrawMaxOnceLimitAmt']),
                         str(decimal.Decimal(pos_max_once).quantize(decimal.Decimal('0.00'))))
        self.assertEqual(str(data_list['atmWithdrawDayLimitAmt']),
                         str(limit[0]['ATM_ONCE_QUOTA']))
        self.assertEqual(str(data_list['atmWithdrawMaxDayLimitAmt']),
                         str(decimal.Decimal(atm_max_day).quantize(decimal.Decimal('0.00'))))
        self.assertEqual(str(data_list['atmWithdrawMaxOnceLimitAmt']),
                         str(decimal.Decimal(atm_max_once).quantize(decimal.Decimal('0.00'))))
        self.assertEqual(str(data_list['atmWithdrawOnceLimitAmt']),
                         str(limit[0]['ATM_DAY_QUOTA']))
        self.assertEqual(str(data_list['singleLimit']),
                         str(decimal.Decimal(single_once_amount).quantize(decimal.Decimal('0.00'))))
        self.assertEqual(str(data_list['dayLimit']),
                         str(decimal.Decimal(single_amount).quantize(decimal.Decimal('0.00'))))

    # 联名卡激活失败
    @file_data('test_data/test_activate_joint_card_failure.json')
    def test_activate_joint_card_failure(self, user_name, password, cert_type, mobile_code, assert_info):
        self._restful_xjb.login(user_name=str(user_name), password=str(password))
        cust_info = self._db.get_cust_info(columns='name, cert_no, cust_no', match='=', mobile=str(user_name))
        card_info = self._db.get_cust_debit_card(bank_mobile=str(user_name))[0]['card_no']
        if str(mobile_code) == '123456':
            self._restful_xjb.joint_card_acitvate(card_no=str(card_info), mobile=str(user_name),
                                                  name=str(cust_info[0]['name']), cert_type=str(cert_type),
                                                  cert_no=str(cust_info[0]['cert_no']))
        else:
            self._restful_xjb.joint_card_acitvate(card_no=str(card_info), mobile=str(user_name),
                                                  name=str(cust_info[0]['name']), cert_type=str(cert_type),
                                                  cert_no=str(cust_info[0]['cert_no']), mobile_code=str(mobile_code))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 获取用户的联名卡列表
    @file_data('test_data/test_get_joint_card_cust_cards.json')
    def test_get_joint_card_cust_cards(self, user_name, password, assert_info):
        self._restful_xjb.get_cust_joint_card_list(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        joint_card = self._db.get_joint_card(mobile=str(user_name))

        data_list = entity.dataList
        pos_day = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'POSDAY\'')[0][
                'PM_V1']
        pos_once = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'POSQUOTA\'')[0][
                'PM_V1']
        atm_day = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'ATMDAY\'')[0][
                'PM_V1']
        atm_once = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'ATMQUOTA\'')[0][
                'PM_V1']
        pos_max_day = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'MAXPOSDAY\'')[0][
                'PM_V1']
        atm_max_day = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'MAXATMDAY\'')[0][
                'PM_V1']
        pos_max_once = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'MAXPOSQUOTA\'')[
                0][
                'PM_V1']
        atm_max_once = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'NANYUEWITHDRAWLIMIT\' and PM_CODE=\'MAXATMQUOTA\'')[
                0][
                'PM_V1']
        single_amount = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'FASTWITHDRAWLIMIT\' and PM_CODE=\'SINGLEDAY\'')[0][
                'PM_V1']
        single_once_amount = \
            self._db.get_cts_parameter(query_condition='PM_KEY = \'FASTWITHDRAWLIMIT\' and PM_CODE=\'SINGLEQUOTA\'')[0][
                'PM_V1']

        self.assertEqual(len(joint_card), len(data_list))
        for i in range(0, len(data_list)):
            self.assertEqual(str(data_list[i]['canDelete']), '1')
            self.assertEqual(data_list[i]['canFastWithdraw'], u'1')
            self.assertEqual(data_list[i]['canRecharge'], u'1')
            self.assertEqual(str(data_list[i]['name']), joint_card[0]['name'])

            # 南粤银行身份证类型是1， 现金宝是0
            self.assertEqual(str(data_list[i]['certType']), '0')
            self.assertEqual(str(data_list[i]['cardType']), str(joint_card[0]['card_type']))
            self.assertEqual(str(data_list[i]['certNo']), str(joint_card[0]['cert_no']))
            self.assertEqual(str(data_list[i]['posWithdrawOnceLimitAmt']),
                             str(decimal.Decimal(pos_once).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(data_list[i]['posWithdrawDayLimitAmt']),
                             str(decimal.Decimal(pos_day).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(data_list[i]['posWithdrawMaxDayLimitAmt']),
                             str(decimal.Decimal(pos_max_day).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(data_list[i]['posWithdrawMaxOnceLimitAmt']),
                             str(decimal.Decimal(pos_max_once).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(data_list[i]['atmWithdrawDayLimitAmt']),
                             str(decimal.Decimal(atm_day).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(data_list[i]['atmWithdrawMaxDayLimitAmt']),
                             str(decimal.Decimal(atm_max_day).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(data_list[i]['atmWithdrawMaxOnceLimitAmt']),
                             str(decimal.Decimal(atm_max_once).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(data_list[i]['atmWithdrawOnceLimitAmt']),
                             str(decimal.Decimal(atm_once).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(data_list[i]['singleLimit']),
                             str(decimal.Decimal(single_once_amount).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(data_list[i]['dayLimit']),
                             str(decimal.Decimal(single_amount).quantize(decimal.Decimal('0.00'))))

    # 设置联名卡限额
    @file_data('test_data/test_set_joint_card_limit.json')
    def test_set_joint_card_limit(self, user_name, password, trade_password, limit_type, limit_amount, card_no,
                                  is_successful,
                                  assert_info):
        cards = self._db.get_cust_debit_card(bank_mobile=str(user_name))
        self._restful_xjb.set_joint_card_limit(user_name=str(user_name), password=str(password),
                                               trade_password=str(trade_password), limit_type=str(limit_type),
                                               limit_amt=str(limit_amount), bank_card_id=str(cards[0]['serial_id']))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if is_successful == 'true':
            limit = self._db.get_nanyue_limit(card_no=str(card_no))
            if str(limit_type) == '0':
                self.assertEqual(str(limit[0]['ATM_ONCE_QUOTA']),
                                 str(decimal.Decimal(limit_amount).quantize(decimal.Decimal('0.00'))))
            elif str(limit_type) == '1':
                self.assertEqual(str(limit[0]['ATM_DAY_QUOTA']),
                                 str(decimal.Decimal(limit_amount).quantize(decimal.Decimal('0.00'))))
            elif str(limit_type) == '2':
                self.assertEqual(str(limit[0]['POS_ONCE_QUOTA']),
                                 str(decimal.Decimal(limit_amount).quantize(decimal.Decimal('0.00'))))
            elif str(limit_type) == '3':
                self.assertEqual(str(limit[0]['POS_DAY_QUOTA']),
                                 str(decimal.Decimal(limit_amount).quantize(decimal.Decimal('0.00'))))

    # 升级卡
    @file_data('test_data/test_upgrade_bank_card.json')
    def test_upgrade_bank_card(self, user_name, password, mobile_code, card_no, bank_name, is_successful, assert_info):
        des_bank_no = self._db.get_highest_prio_bank_channel(bank_name=str(bank_name))
        if is_successful == 'true':
            # 升级卡，确保绑卡那里面没有最高优先级的通道存在，若有，删除
            self._db.delete_bind_card_with_highest_priority(mobile=str(user_name), bank_no=str(des_bank_no))
        cards = self._db.get_bank_card_by_card_no(mobile=str(user_name), card_no=str(card_no))
        if str(mobile_code) == 'none':
            self._restful_xjb.bank_card_upgrade(user_name=str(user_name), password=str(password),
                                                des_bank_no=str(des_bank_no), bank_card_id=str(cards[0]['serial_id']),
                                                bank_name=str(bank_name))
        else:
            self._restful_xjb.bank_card_upgrade(user_name=str(user_name), password=str(password),
                                                des_bank_no=str(des_bank_no), bank_card_id=str(cards[0]['serial_id']),
                                                bank_name=str(bank_name), mobile_code=str(mobile_code))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if is_successful == 'true':
            cards = self._db.get_binding_card_by_bank_no(mobile=str(user_name), bank_no=str(des_bank_no))
            self.assertEqual(len(cards), 1)
            self.assertEqual(str(entity.body_title), '升级成功')
            self.assertEqual(str(entity.body_authResult), 'Y')

    # 我的预约码
    @file_data('test_data/test_my_reservation_code.json')
    def test_my_reservation_code(self, user_name, password, assert_info):
        self._restful_xjb.my_reservation_code(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        excepted_reserve_code = self._db.get_reserve_code(str(user_name), '')
        if any(excepted_reserve_code):
            self.assertEqual(str(entity.body_reservationCodeInfos[0]['reservationCode']),
                             str(excepted_reserve_code[0]['RESERVE_CODE']))
            self.assertEqual(str(entity.body_reservationCodeInfos[0]['productName']),
                             str(excepted_reserve_code[0]['PROD_ABBREVIATE']))
            self.assertEqual(str(entity.body_reservationCodeInfos[0]['reservationLimit']),
                             str(excepted_reserve_code[0]['RESERVE_QUOTA']))
            self.assertEqual(str(excepted_reserve_code[0]['STATUS']), '2', '状态可使用')
        else:
            print 'The reserve code is Empty!'

    # 查询预约码
    @file_data('test_data/query_reservation_code.json')
    def test_query_reserve_code(self, user_name, password, reservation_code, assert_info):
        self._restful_xjb.query_reserve_code(user_name=str(user_name), password=str(password),
                                             reservation_code=str(reservation_code))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        excepted_result = self._db.get_reserve_code(str(user_name), str(reservation_code))
        if any(excepted_result):
            self.assertEqual(str(entity.body_reservationCodeInfo['reservationCode']),
                             str(excepted_result[0]['RESERVE_CODE']))
            self.assertEqual(str(entity.body_reservationCodeInfo['productName']),
                             str(excepted_result[0]['PROD_ABBREVIATE']))
            self.assertEqual(str(entity.body_reservationCodeInfo['reservationLimit']),
                             str(excepted_result[0]['RESERVE_QUOTA']))
            self.assertEqual(str(excepted_result[0]['STATUS']), '2', '状态可使用')
        else:
            print 'The reserve code is Empty!'

    # 绑卡-查询所有通道信息
    @file_data('test_data/test_check_all_bank_channel_list.json')
    def test_check_all_bank_channel_list(self, user_name, password, cert_type, assert_info):
        self._restful_xjb.check_all_bank_channel_list(user_name=str(user_name),
                                                      password=str(password),
                                                      cert_type=str(cert_type))
        entity = self._restful_xjb.entity.current_entity
        actual_bank_name = entity.bankGroupName
        actual_group_id = entity.bankGroupId
        expect_groups = self._db.check_all_bank_channel_list()

        self.assertEquals(len(actual_bank_name), len(expect_groups))
        self.assertEquals(len(actual_group_id), len(expect_groups))

        for i in range(0, len(actual_group_id)):
            self.assertTrue(str(expect_groups[i]['group_id']) in actual_group_id)
            self.assertTrue(str(expect_groups[i]['group_name']) in actual_bank_name)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 基金-设置自选基金
    @file_data('test_data/test_set_fav_fund.json')
    def test_set_fav_fund(self, user_name, password, object_ids, fav_type, is_successful, assert_info):
        if str(is_successful) == 'true':
            self._db.update_fav_fund(mobile=str(user_name), fund_id=str(object_ids))
        self._restful_xjb.set_fav_fund(user_name=str(user_name), password=str(password),
                                       object_ids=str(object_ids), fav_type=str(fav_type))
        entity = self._restful_xjb.entity.current_entity
        add_fav_fund, add_fav = self._db.get_fav_fund(mobile=str(user_name), object_id=str(object_ids))
        if str(is_successful) == 'true':
            self.assertEqual(add_fav_fund[0]['is_delete'], 0)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 基金12大分类
    @file_data('test_data/test_fund_twelve_part.json')
    def test_fund_twelve_part(self, user_name, password, assert_info):
        self._restful_xjb.fund_twelve_part(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        channel_name = entity.channelName
        name_list = {u'研究报告', u'机构观点', u'达人论基', u'市场指数', u'全部基金', u'评级排行', u'自选基金',
                     u'对比分析', u'最佳基金', u'专家开讲', u'新发基金', u'精选基金'}
        for n in name_list:
            self.assertTrue(str(n) in channel_name)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 设置信用卡提醒
    @file_data('test_data/test_credit_card_reminder.json')
    def test_credit_card_reminder(self, user_name, password, reminder_day, open_type, card_no, is_successful,
                                  assert_info):
        credit_cards = self._db.get_cust_credit_card_by_card_no(card_no=str(card_no))
        self._restful_xjb.credit_card_set_reminder(user_name=str(user_name), password=str(password),
                                                   card_id=str(credit_cards[0]['id']), open_type=str(open_type),
                                                   repay_reminder_date=str(reminder_day))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(is_successful) == 'true':
            credit_cards_new = self._db.get_cust_credit_card_by_card_no(card_no=str(card_no))
            if str(open_type) == '1':
                self.assertEqual(str(credit_cards_new[0]['is_warn']), str(credit_cards[0]['is_warn']))
            elif str(open_type) == '2':
                self.assertEqual(str(credit_cards_new[0]['is_warn']), '1')
            else:
                self.assertEqual(str(credit_cards_new[0]['is_warn']), '0')

            if str(open_type) == '1':
                self.assertEqual(str(credit_cards_new[0]['warn_date']), str(credit_cards[0]['warn_date']))
                self.assertEqual(str(entity.repayRemindDate), str(credit_cards[0]['warn_date']))
            elif str(open_type) == '2':
                self.assertEqual(str(credit_cards_new[0]['warn_date']), str(reminder_day))
                self.assertEqual(str(entity.repayRemindDate), str(reminder_day))

    # 用优惠券 预约认购高端
    @file_data('test_data/test_buy_vip_using_coupon.json')
    def test_buy_vip_using_coupon(self, user_name, password, product_id, pay_type, pay_amount, prod_type_scope_val,
                                  trade_password, is_successful, ecard_no, assert_info):
        coupon, can_used_coupon, can_not_used_coupon = self._db.get_coupon_count(mobile=str(user_name),
                                                                                 amount=str(pay_amount),
                                                                                 prod_type_scope_val=str(
                                                                                     prod_type_scope_val),
                                                                                 prod_id=str(product_id))

        if str(ecard_no) == '':
            coupon_ecard = can_used_coupon[0]['ECARD_NO']
            discount_amount = can_used_coupon[0]['AMOUNT']
            ecard_no = coupon_ecard
        self._restful_xjb.buy_product_using_coupon(user_name=str(user_name), login_password=str(password),
                                                   product_id=str(product_id), pay_type=str(pay_type),
                                                   pay_amount=str(pay_amount), coupon_ids=str(ecard_no),
                                                   trade_password=str(trade_password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(is_successful) == 'true':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))
            trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
            # 012 认购 012020 现金宝认购
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012020')
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '3')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['STATUS']), 'A')
            self.assertEqual(str(trade_order[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))

            # 020 认购 002211 认购高端（来自现金宝）
            self.assertEqual(str(trade_reserve[0]['APKIND']), '020')
            self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '002211')
            self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_reserve[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '3')
            self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(trade_reserve[0]['PURCHASE_PAYMENT_TYPE']), '5')
            self.assertEqual(str(trade_reserve[0]['RES_ST']), 'N')
            self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))

            # 031 份额冻结 031002 预约认购冻结
            amount_pay_by_vacco = decimal.Decimal(str(pay_amount)) - decimal.Decimal(discount_amount)
            self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
            self.assertEqual(str(trade_quty_chg[0]['APKIND']), '031')
            self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '031002')
            self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')

            # 020 认购 002211 认购高端（来自现金宝）
            self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '3')
            self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
            self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                             str(decimal.Decimal(pay_amount).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
            self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '002211')

            self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(vacco_detail[0]['APKIND']), '031')
            self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '031002')
            self.assertEqual(str(vacco_detail[0]['SUB_AMT']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))

    # 优惠券申购基金
    @file_data('test_data/test_buy_fund_using_coupon.json')
    def test_buy_fund_using_coupon(self, user_name, password, product_id, pay_type, pay_amount, prod_type_scope_val,
                                   trade_password, is_successful, ecard_no, assert_info):
        coupon, can_used_coupon, can_not_used_coupon = self._db.get_coupon_count(mobile=str(user_name),
                                                                                 amount=str(pay_amount),
                                                                                 prod_type_scope_val=str(
                                                                                     prod_type_scope_val),
                                                                                 prod_id=str(product_id))

        if str(ecard_no) == '':
            coupon_ecard = can_used_coupon[0]['ECARD_NO']
            discount_amount = can_used_coupon[0]['AMOUNT']
            ecard_no = coupon_ecard
        self._restful_xjb.buy_product_using_coupon(user_name=str(user_name), login_password=str(password),
                                                   product_id=str(product_id), pay_type=str(pay_type),
                                                   pay_amount=str(pay_amount), coupon_ids=str(ecard_no),
                                                   trade_password=str(trade_password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(is_successful) == 'true':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))
            # 013 申购 013020 现金宝申购
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '013')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '013020')
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '2')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['STATUS']), 'A')
            self.assertEqual(str(trade_order[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))

            # 022 申购 022212 申购基金
            self.assertEqual(str(trade_request[0]['APKIND']), '022')
            self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022212')
            self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '2')
            self.assertEqual(str(trade_request[0]['PURCHASE_PAYMENT_TYPE']), '5')
            self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['SUB_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_request[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount).quantize(decimal.Decimal('0.00'))))

            # 024 赎回 024012 现金宝赎回买基金
            amount_pay_by_vacco = decimal.Decimal(str(pay_amount)) - decimal.Decimal(discount_amount)
            self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
            self.assertEqual(str(trade_quty_chg[0]['APKIND']), '024')
            self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '024012')
            self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')

            # 022 申购 022212 申购基金
            self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '2')
            self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
            self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                             str(decimal.Decimal(pay_amount).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(asset_in_trasit[0]['APKIND']), '022')
            self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '022212')

            self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(vacco_detail[0]['APKIND']), '024')
            self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '024012')
            self.assertEqual(str(vacco_detail[0]['SUB_AMT']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))

            ecard = self._db.get_coupon_no(ecard_no=str(ecard_no))
            self.assertEqual(str(ecard[0]['STATUS']), 'USED')

            consume_coupon = self._db.get_cust_consume_coupon(mobile=str(user_name), ecard_no=str(ecard_no))
            self.assertEqual(str(consume_coupon[0]['ITEM_ID']), str(product_id))
            self.assertEqual(str(consume_coupon[0]['SOURCE_TYPE']), 'COUPON_DEDUCTE_PRODUCT')
            self.assertEqual(str(consume_coupon[0]['COUPON_STATUS']), 'CONSUME')

            self.assertEqual(str(entity.returnResult), 'Y')

    # 积分-优惠券列表
    @file_data('test_data/test_points_discount_coupon_list.json')
    def test_points_discount_coupon_list(self, user_name, password, purchase_amt, prod_type_scope_val, product_id,
                                         is_successful,
                                         assert_info):
        self._restful_xjb.points_discount_coupon(user_name=str(user_name), password=str(password),
                                                 purchase_amt=str(purchase_amt), product_id=str(product_id))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(is_successful) == 'true':
            coupon_count, coupon_avail, coupon_not_used = self._db.get_coupon_count(mobile=str(user_name),
                                                                                    amount=str(purchase_amt),
                                                                                    prod_type_scope_val=str(
                                                                                        prod_type_scope_val),
                                                                                    prod_id=str(product_id))
            can_not_used_count = len(coupon_not_used)
            self.assertEqual(str(entity.canUsedInfo), str('可使用优惠券(' + str(len(coupon_avail)) + '张)'))
            self.assertEqual(str(entity.cannotUsedInfo), str('不可使用优惠券(' + str(can_not_used_count) + '张)'))
            coupon_list = entity.dataList
            self.assertEqual(len(coupon_list), len(coupon_count))

            for i in range(0, len(coupon_count)):
                coupon_ecard = self._db.get_coupon_no(ecard_no=str(coupon_list[i]['couponId']))
                self.assertEqual(str(coupon_list[i]['couponType']), str(coupon_ecard[0]['COUPON_TYPE']))
                self.assertEqual(str(coupon_list[i]['usePeriod']),
                                 str(coupon_ecard[0]['START_AT']).split(' ')[0].replace('-', '.') + '-' +
                                 str(coupon_ecard[0]['END_AT']).split(' ')[0].replace('-', '.'))
                self.assertEqual(str(coupon_list[i]['couponAmt']), str(coupon_ecard[0]['AMOUNT']))
                self.assertEqual(str(coupon_list[i]['canUseAmt']), str(coupon_ecard[0]['COUPON_AMOUNT']))
                if (str(coupon_ecard[0]['ECARD_NO']) in str(coupon_avail)) is True:
                    self.assertEqual(str(coupon_list[i]['canUsed']), '1')
                else:
                    self.assertEqual(str(coupon_list[i]['canUsed']), '0')

                if str(coupon_ecard[0]['SUPPORT_COMPOSITE']) == 'Y':
                    self.assertEqual(str(coupon_list[i]['canOverload']), '1')
                    self.assertEqual(str(coupon_list[i]['canOverloadInfo']), '可叠加使用')
                else:
                    self.assertEqual(str(coupon_list[i]['canOverload']), '0')
                    self.assertEqual(str(coupon_list[i]['canOverloadInfo']), '不可叠加使用')

    # 叠加优惠券认购基金, 用两张优惠券
    @file_data('test_data/test_using_coupon_superposed.json')
    def test_buy_fund_using_coupon_superposed(self, user_name, password, product_id, pay_type, pay_amount,
                                              prod_type_scope_val, coupon_batch_id, trade_password,
                                              is_successful,
                                              ecard_no, assert_info):
        coupon, can_used_coupon, can_not_used_coupon = self._db.get_coupon_count_new(mobile=str(user_name),
                                                                                     amount=str(pay_amount),
                                                                                     prod_type_scope_val=str(
                                                                                         prod_type_scope_val),
                                                                                     coupon_batch_id=str(
                                                                                         coupon_batch_id),
                                                                                     prod_id=str(product_id))

        if str(ecard_no) == '':
            coupon_ecard1 = can_used_coupon[0]['ECARD_NO']
            coupon_ecard2 = can_used_coupon[1]['ECARD_NO']
            discount_amount1 = can_used_coupon[0]['AMOUNT']
            discount_amount2 = can_used_coupon[1]['AMOUNT']
            ecard_no = str(coupon_ecard1) + ',' + str(coupon_ecard2)
        self._restful_xjb.buy_product_using_coupon(user_name=str(user_name), login_password=str(password),
                                                   product_id=str(product_id), pay_type=str(pay_type),
                                                   pay_amount=str(pay_amount), coupon_ids=str(ecard_no),
                                                   trade_password=str(trade_password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(is_successful) == 'true':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))
            # 012 认购 012020 现金宝申购
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012020')
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '2')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['STATUS']), 'A')
            self.assertEqual(str(trade_order[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount1 + discount_amount2).quantize(
                                 decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))

            # 020 认购 020010 认购基金
            self.assertEqual(str(trade_request[0]['APKIND']), '020')
            self.assertEqual(str(trade_request[0]['SUB_APKIND']), '020010')
            self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '2')
            self.assertEqual(str(trade_request[0]['PURCHASE_PAYMENT_TYPE']), '5')
            self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['SUB_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_request[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount1 + discount_amount2).quantize(
                                 decimal.Decimal('0.00'))))

            # 024 赎回 024011 现金宝赎回认购基金
            amount_pay_by_vacco = decimal.Decimal(str(pay_amount)) - decimal.Decimal(
                discount_amount1 + discount_amount2)
            self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
            self.assertEqual(str(trade_quty_chg[0]['APKIND']), '024')
            self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '024011')
            self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')

            # 020 申购 020010 认购基金
            self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '2')
            self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
            self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                             str(decimal.Decimal(pay_amount).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
            self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '020010')

            self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(vacco_detail[0]['APKIND']), '024')
            self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '024011')
            self.assertEqual(str(vacco_detail[0]['SUB_AMT']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))
            if ',' in str(ecard_no):
                ecards = ecard_no.split(',')
                for i in range(0, len(ecards)):
                    ecard = self._db.get_coupon_no(ecard_no=str(ecards[i]))
                    self.assertEqual(str(ecard[0]['STATUS']), 'USED')
                    consume_coupon = self._db.get_cust_consume_coupon(mobile=str(user_name),
                                                                      ecard_no=str(ecards[i]))
                    self.assertEqual(str(consume_coupon[0]['ITEM_ID']), str(product_id))
                    self.assertEqual(str(consume_coupon[0]['SOURCE_TYPE']), 'COUPON_DEDUCTE_PRODUCT')
                    self.assertEqual(str(consume_coupon[0]['COUPON_STATUS']), 'CONSUME')

            self.assertEqual(str(entity.returnResult), 'Y')

    # 获取优惠券数量信息
    @file_data('test_data/test_get_coupon_info.json')
    def test_get_coupon_info(self, user_name, password, product_id, prod_type_scope_val, is_successful,
                             assert_info):
        self._restful_xjb.get_coupon_info(user_name=str(user_name), password=str(password), product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        actual_coupon_hold_qty = entity.body_couponCount
        actual_coupon_info = entity.body_info

        if str(is_successful) == 'true':
            expect_coupon_available_qty = self._db.get_coupon_info(mobile=str(user_name),
                                                                   prod_type_scope_val=str(prod_type_scope_val),
                                                                   prod_id=str(product_id))
            if len(expect_coupon_available_qty) == 0:
                self.assertTrue('无可用优惠券' in str(actual_coupon_info))
            else:
                self.assertTrue('张优惠券可用' in str(actual_coupon_info))
                self.assertTrue(str(len(expect_coupon_available_qty)) in str(actual_coupon_info))
            self.assertEqual(int(actual_coupon_hold_qty), len(expect_coupon_available_qty))

    # 计算可用积分
    @file_data('test_data/test_can_used_points_count.json')
    def test_can_used_points_count(self, user_name, password, product_id, amt, coupon_ids, is_use_points,
                                   is_successful, assert_info):
        self._restful_xjb.can_used_points_count(user_name=str(user_name), password=str(password),
                                                product_id=str(product_id), amt=str(amt),
                                                coupon_ids=str(coupon_ids), is_use_points=str(is_use_points))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        actual_use_coupon = entity.body_couponInfo
        actual_use_points = entity.body_pointsCount
        actual_pay_money = entity.body_payAmt

        if str(is_successful) == 'true':
            expected_use_coupon = self._db.get_coupon_no(ecard_no=str(coupon_ids))
            self.assertEqual(str(actual_use_coupon), str(-(expected_use_coupon[0]['AMOUNT'])))
            self.assertEqual(str(actual_use_points),
                             str(decimal.Decimal(float(amt) * 0.001).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(actual_pay_money), str(decimal.Decimal(amt) - expected_use_coupon[0]['AMOUNT']))

    # 优惠券认购定期
    @file_data('test_data/test_buy_dqb_using_coupon.json')
    def test_buy_dqb_using_coupon(self, user_name, password, product_id, pay_type, pay_amount,
                                  prod_type_scope_val, trade_password, is_successful, ecard_no, assert_info):
        coupon, can_used_coupon, can_not_used_coupon = self._db.get_coupon_count(mobile=str(user_name),
                                                                                 amount=str(pay_amount),
                                                                                 prod_type_scope_val=str(
                                                                                     prod_type_scope_val),
                                                                                 prod_id=str(product_id))

        if str(ecard_no) == '':
            coupon_ecard1 = can_used_coupon[0]['ECARD_NO']
            discount_amount1 = can_used_coupon[0]['AMOUNT']
            ecard_no = str(coupon_ecard1)
        self._restful_xjb.buy_product_using_coupon(user_name=str(user_name), login_password=str(password),
                                                   product_id=str(product_id), pay_type=str(pay_type),
                                                   pay_amount=str(pay_amount), coupon_ids=str(ecard_no),
                                                   trade_password=str(trade_password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(is_successful) == 'true':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))
            # 012 认购 012020 现金宝认购
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012020')
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '1')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['STATUS']), 'A')
            self.assertEqual(str(trade_order[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount1).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))

            # 020 认购 002210 认购定期
            self.assertEqual(str(trade_request[0]['APKIND']), '020')
            self.assertEqual(str(trade_request[0]['SUB_APKIND']), '002210')
            self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '1')
            self.assertEqual(str(trade_request[0]['PURCHASE_PAYMENT_TYPE']), '5')
            self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['SUB_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_request[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount1).quantize(decimal.Decimal('0.00'))))

            # 024 赎回 002201 现金宝赎回认购定期
            amount_pay_by_vacco = decimal.Decimal(str(pay_amount)) - decimal.Decimal(
                discount_amount1)
            self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
            self.assertEqual(str(trade_quty_chg[0]['APKIND']), '024')
            self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '002201')
            self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')

            # 020 认购 020040 认购定期
            self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '1')
            self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
            self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                             str(decimal.Decimal(pay_amount).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
            self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '002210')

            self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(vacco_detail[0]['APKIND']), '024')
            self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '002201')
            self.assertEqual(str(vacco_detail[0]['SUB_AMT']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))
            if ',' in str(ecard_no):
                ecards = ecard_no.split(',')
                for i in range(0, len(ecards)):
                    ecard = self._db.get_coupon_no(ecard_no=str(ecards[i]))
                    self.assertEqual(str(ecard[0]['STATUS']), 'USED')
                    consume_coupon = self._db.get_cust_consume_coupon(mobile=str(user_name), ecard_no=str(ecards[i]))
                    self.assertEqual(str(consume_coupon[0]['ITEM_ID']), str(product_id))
                    self.assertEqual(str(consume_coupon[0]['SOURCE_TYPE']), 'COUPON_DEDUCTE_PRODUCT')
                    self.assertEqual(str(consume_coupon[0]['COUPON_STATUS']), 'CONSUME')

            self.assertEqual(str(entity.returnResult), 'Y')

    # 优惠券预约认购定期
    # FULL_OFF_100_12_0028
    @file_data('test_data/test_subscribe_dqb_using_coupon.json')
    def test_subscribe_dqb_using_coupon(self, user_name, password, product_id, pay_type, pay_amount,
                                        prod_type_scope_val, trade_password, is_successful, ecard_no, assert_info):
        coupon, can_used_coupon, can_not_used_coupon = self._db.get_coupon_count(mobile=str(user_name),
                                                                                 amount=str(pay_amount),
                                                                                 prod_type_scope_val=str(
                                                                                     prod_type_scope_val),
                                                                                 prod_id=str(product_id))
        if str(ecard_no) == '':
            coupon_ecard1 = can_used_coupon[0]['ECARD_NO']
            discount_amount1 = can_used_coupon[0]['AMOUNT']
            ecard_no = str(coupon_ecard1)
        self._restful_xjb.buy_product_using_coupon(user_name=str(user_name), login_password=str(password),
                                                   product_id=str(product_id), pay_type=str(pay_type),
                                                   pay_amount=str(pay_amount), coupon_ids=str(ecard_no),
                                                   trade_password=str(trade_password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(is_successful) == 'true':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))
            trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
            # 012 认购 012020 现金宝认购
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012020')
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '1')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['STATUS']), 'A')
            self.assertEqual(str(trade_order[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount1).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))

            # 020 认购 020020 预约认购定期宝（来自现金宝）
            self.assertEqual(str(trade_reserve[0]['APKIND']), '020')
            self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '020020')
            self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_reserve[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '1')
            self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(trade_reserve[0]['PURCHASE_PAYMENT_TYPE']), '5')
            self.assertEqual(str(trade_reserve[0]['RES_ST']), 'N')
            self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))

            # 031 份额冻结 031002 预约认购冻结
            amount_pay_by_vacco = decimal.Decimal(str(pay_amount)) - decimal.Decimal(discount_amount1)
            self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
            self.assertEqual(str(trade_quty_chg[0]['APKIND']), '031')
            self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '031002')
            self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')

            # 020 认购 020020 预约认购定期宝（来自现金宝）
            self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '1')
            self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
            self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                             str(decimal.Decimal(pay_amount).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
            self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '020020')

            # 024 赎回 002201 现金宝赎回（用于买入定期宝）
            self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(vacco_detail[0]['APKIND']), '024')
            self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '002201')
            self.assertEqual(str(vacco_detail[0]['SUB_AMT']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))
            if ',' in str(ecard_no):
                ecards = ecard_no.split(',')
                for i in range(0, len(ecards)):
                    ecard = self._db.get_coupon_no(ecard_no=str(ecards[i]))
                    self.assertEqual(str(ecard[0]['STATUS']), 'USED')
                    consume_coupon = self._db.get_cust_consume_coupon(mobile=str(user_name), ecard_no=str(ecards[i]))
                    self.assertEqual(str(consume_coupon[0]['ITEM_ID']), str(product_id))
                    self.assertEqual(str(consume_coupon[0]['SOURCE_TYPE']), 'COUPON_DEDUCTE_PRODUCT')
                    self.assertEqual(str(consume_coupon[0]['COUPON_STATUS']), 'CONSUME')

            self.assertEqual(str(entity.returnResult), 'Y')

    # 预约码认购定期宝
    @file_data('test_data/buy_dqb_using_reserve_code.json')
    def test_buy_product_using_reserve_code(self, user_name, login_password, product_id, reservation_code,
                                            amount, trade_password, is_successful, assert_info):
        excepted_result = self._db.get_reserve_code(str(user_name), str(reservation_code))
        status = excepted_result[0]['STATUS']
        if status != '2' and str(is_successful) == 'true':
            # 修改预约码状态和预约额度
            self._db.reservation_code_status_modify(buy_quota=str(amount), buy_count=str(10000),
                                                    reserve_quota=str(10000), reserve_count=str(10000),
                                                    mobile=str(user_name), reserve_code=str(reservation_code),
                                                    product_id=str(product_id))

        self._restful_xjb.buy_product_using_reserve_code(user_name=str(user_name), login_password=str(login_password),
                                                         product_id=str(product_id),
                                                         reservation_code=str(reservation_code), amount=str(amount),
                                                         trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(is_successful) == 'true':
            excepted_result = self._db.get_reserve_code(str(user_name), str(reservation_code))
            status = excepted_result[0]['STATUS']
            self.assertEqual(str(excepted_result[0]['RESERVE_QUOTA']),
                             str(decimal.Decimal(str(amount)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(excepted_result[0]['STATUS']), '3')
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))
            trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
            # 012 认购 012020 现金宝认购
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012020')
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '1')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['STATUS']), 'A')
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(amount)).quantize(decimal.Decimal('0.00'))))
            # 031 份额冻结 031002 预约认购冻结
            self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
            self.assertEqual(str(trade_quty_chg[0]['APKIND']), '031')
            self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '031002')
            self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                             str(-decimal.Decimal(amount).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')

            # 020 认购 020020 预约认购定期宝（来自现金宝）
            self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '1')
            self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
            self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                             str(decimal.Decimal(amount).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
            self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '020020')

            # 024 赎回 002201 现金宝赎回（用于买入定期宝）
            self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(vacco_detail[0]['APKIND']), '024')
            self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '002201')
            self.assertEqual(str(vacco_detail[0]['SUB_AMT']),
                             str(-decimal.Decimal(amount).quantize(decimal.Decimal('0.00'))))

            # 020 认购 020020 预约认购定期宝（来自现金宝）
            self.assertEqual(str(trade_reserve[0]['APKIND']), '020')
            self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '020020')
            self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_reserve[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '1')
            self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(trade_reserve[0]['PURCHASE_PAYMENT_TYPE']), '0')
            self.assertEqual(str(trade_reserve[0]['RES_ST']), 'N')
            self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
                             str(decimal.Decimal(str(amount)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(entity.returnResult), 'Y')

    # 使用现金宝+多张优惠券(滿50减1）申购高端，撤单，优惠券返回
    @file_data('test_data/test_buy_vip_cancel.json')
    def test_buy_vip_cancel(self, user_name, password, product_id, amt, prod_type_scope_val, trade_password,
                            assert_info):
        coupon, can_used_coupon, can_not_used_coupon = self._db.get_coupon_count(mobile=str(user_name),
                                                                                 amount=str(amt),
                                                                                 prod_type_scope_val=str(
                                                                                     prod_type_scope_val),
                                                                                 prod_id=str(product_id))
        coupon_ecard1 = can_used_coupon[0]['ECARD_NO']
        coupon_ecard2 = can_used_coupon[1]['ECARD_NO']
        discount_amount1 = can_used_coupon[0]['AMOUNT']
        discount_amount2 = can_used_coupon[1]['AMOUNT']
        ecard_no = str(coupon_ecard1) + ',' + str(coupon_ecard2)
        self._restful_xjb.purchase_then_cancel(user_name=str(user_name), password=str(password),
                                               product_id=str(product_id), trade_password=str(trade_password),
                                               purchase_amt=str(amt), coupon_ids=ecard_no)

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
        vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
        trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
        # 013 申购 013020 现金宝申购
        self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '013')
        self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '013020')
        self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
        self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
        self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
        self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
        self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '3')
        self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
        self.assertEqual(str(trade_order[0]['STATUS']), 'C')
        self.assertEqual(str(trade_order[0]['COUPON_AMOUNT']),
                         str(decimal.Decimal(discount_amount1 + discount_amount2).quantize(decimal.Decimal('0.00'))))
        self.assertEqual(str(trade_order[0]['AP_AMT']),
                         str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))

        # 022 申购 022210 申购高端（来自现金宝）
        self.assertEqual(str(trade_reserve[0]['APKIND']), '022')
        self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '022210')
        self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
        self.assertEqual(str(trade_reserve[0]['BRANCH_CODE']), '675')
        self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '3')
        self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(product_id))
        self.assertEqual(str(trade_reserve[0]['PURCHASE_PAYMENT_TYPE']), '5')
        self.assertEqual(str(trade_reserve[0]['RES_ST']), 'C')
        self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
                         str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))

        # 032 份额解冻 032002 预约申购解冻
        amount_pay_by_vacco = decimal.Decimal(str(amt)) - decimal.Decimal(
            discount_amount1 + discount_amount2)
        self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
        self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')
        self.assertEqual(str(vacco_detail[0]['APKIND']), '032')
        self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '032002')
        self.assertEqual(str(vacco_detail[0]['SUB_AMT']),
                         str(decimal.Decimal(amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))
        if ',' in str(ecard_no):
            ecards = ecard_no.split(',')
            for i in range(0, len(ecards)):
                ecard = self._db.get_coupon_no(ecard_no=str(ecards[i]))
                self.assertEqual(str(ecard[0]['STATUS']), 'ISSUE')
                coupon_frozen = self._db.get_cust_latest_coupon_frozen_his(ecard_no=str(ecards[i]))
                self.assertEqual(str(coupon_frozen[0]['ITEM_ID']), str(product_id))
                self.assertEqual(str(coupon_frozen[0]['ACTION_STATUS']), 'UNFROZEN')

        self.assertEqual(str(entity.returnResult), 'Y')

    # 查询认购赎回交易详情
    @file_data('test_data/test_query_tradedetail.json')
    def test_query_tradedetail(self, user_name, login_password, trade_serial_no, assert_info):
        self._restful_xjb.query_trade_detail(user_name=str(user_name), login_password=str(login_password),
                                             trade_serial_no=str(trade_serial_no))
        entity = self._restful_xjb.entity.current_entity
        tradeDetail = entity.body_tradeDetail
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(tradeDetail['tradeAmt'], str(decimal.Decimal(
            str(tradeDetail['tradeAmt'])).quantize(decimal.Decimal('0.00'))))
        trade_request, trade_order, product_from_info, product_to_info = self._db.get_trade_info(
            order_no=str(trade_serial_no))
        self.assertEqual(tradeDetail['fromSourse'], product_from_info[0]['product_short_name'])
        self.assertEqual(tradeDetail['status'], str(trade_order[0]['STATUS']))
        self.assertEqual(tradeDetail['statusDescribe'], '已受理')
        self.assertEqual(tradeDetail['toSourse'], str(product_to_info[0]['product_short_name']))
        self.assertEqual(tradeDetail['tradeDay'].replace('-', ''), str(trade_order[0]['AP_DATE']))
        tradeType = '买入' if str(product_from_info[0]['productid']) == 'ZX05#000730' else '卖出'
        tradeUnits = '元' if str(product_from_info[0]['productid']) == 'ZX05#000730' else '份'
        if "今天" in tradeDetail['tradeTime']:
            today = time.strftime("%Y-%m-%d", time.localtime())
            self.assertEqual(tradeDetail['tradeTime'].replace('今天', today), str(trade_request[0]['CREATED_AT']))
        elif "昨天" in tradeDetail['tradeTime']:
            yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
            self.assertEqual(tradeDetail['tradeTime'].replace('昨天', yesterday), str(trade_request[0]['CREATED_AT']))
        else:
            self.assertEqual(tradeDetail['tradeTime'], str(trade_request[0]['CREATED_AT']))
        self.assertEqual(tradeDetail['tradeType'], tradeType)
        self.assertEqual(tradeDetail['tradeUnits'], tradeUnits)

    # 获取产品热门列表
    @file_data('test_data/test_get_hot_product_list.json')
    def test_get_hot_product_list(self, user_name, password, assert_info):
        self._restful_xjb.hot_product_list(user_name=str(user_name), password=str(password))
        dqb_list = self._db.get_hot_on_sale_product_list(product_type='1')
        vip_list = self._db.get_hot_on_sale_product_list(product_type='3')

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        actual_dqb_list = entity.dataList[0]['list']
        actual_vip_list = entity.dataList[1]['list']

        self.assertEqual(len(actual_dqb_list), len(dqb_list))
        self.assertEqual(len(actual_vip_list), len(vip_list))

        for i in range(0, len(actual_dqb_list)):
            self.assertTrue(str(actual_dqb_list[i]['productId']) in str(dqb_list))
            self.assertEqual(str(actual_dqb_list[i]['productType']), '1')
        for i in range(0, len(actual_vip_list)):
            self.assertTrue(str(actual_vip_list[0]['productId']) in str(vip_list))
            self.assertEqual(str(actual_vip_list[i]['productType']), '3')

    # 现金宝普取/快取
    @file_data('test_data/test_withdraw_validate.json')
    def test_withdraw_validate(self, user_name, password, amt, withdraw_type, trade_password, assert_info):
        self._restful_xjb.withdraw(user_name=str(user_name), password=str(password), withdraw_amount=str(amt),
                                   withdraw_type=str(withdraw_type), trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(assert_info["returnCode"]) == '000000':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))
            capital_in_transit = self._db.get_capital_in_transit(mobile=str(user_name))

            if str(withdraw_type) == '1':
                apkind = '024'
                sub_apkind = '001200'
                order_apkind = '002'
                order_sub_apkind = '002010'
                remark = '普通取现'
            else:
                apkind = '098'
                sub_apkind = '004201'
                order_apkind = '003'
                order_sub_apkind = '003010'
                remark = '快速取现'

            # 验证trade_request表
            self.assertEqual(str(trade_request[0]['APKIND']), apkind)
            self.assertEqual(str(trade_request[0]['SUB_APKIND']), sub_apkind)
            self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '0')
            self.assertEqual(str(trade_request[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_request[0]['SUB_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_request[0]['REMARK']), remark)

            # 验证trade_order表
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), order_apkind)
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), order_sub_apkind)
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))

            # 验证CTS_TRADE_QUTY_CHG表
            self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
            self.assertEqual(str(trade_quty_chg[0]['APKIND']), apkind)
            self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), sub_apkind)
            self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                             str(-decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_quty_chg[0]['BRANCH_CODE']), '675')

            # 验证CTS_CAPITAL_IN_TRANSIT
            self.assertEqual(str(capital_in_transit[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(capital_in_transit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(capital_in_transit[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(capital_in_transit[0]['PROD_TYPE']), '0')
            self.assertEqual(str(capital_in_transit[0]['APKIND']), '024')
            self.assertEqual(str(capital_in_transit[0]['BALANCE']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))

    # 使用使用优惠券购买基金撤单确认后优惠券返还
    @file_data('test_data/test_after_fund_trade_cancel_coupon_pay_back.json')
    def test_after_fund_trade_cancel_coupon_pay_back(self, user_name, password, product_id, pay_amount,
                                                     prod_type_scope_val, trade_password, ecard_no, is_successful,
                                                     assert_info):
        coupon, can_used_coupon, can_not_used_coupon = self._db.get_coupon_count(mobile=str(user_name),
                                                                                 amount=str(pay_amount),
                                                                                 prod_type_scope_val=str(
                                                                                     prod_type_scope_val),
                                                                                 prod_id=str(product_id))
        if str(ecard_no) == '':
            coupon_ecard = can_used_coupon[0]['ECARD_NO']
            discount_amount = can_used_coupon[0]['AMOUNT']
            ecard_no = coupon_ecard

        self._restful_xjb.purchase_then_cancel(user_name=str(user_name), password=str(password),
                                               product_id=str(product_id), purchase_amt=str(pay_amount),
                                               coupon_ids=str(ecard_no), trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(is_successful) == 'true':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))

            # 现金宝申购 013
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '013')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '013020')
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '2')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['STATUS']), 'C')
            self.assertEqual(str(trade_order[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))

            # 022 申购 022212 申购基金
            self.assertEqual(str(trade_request[0]['APKIND']), '022')
            self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022212')
            self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '2')
            self.assertEqual(str(trade_request[0]['PURCHASE_PAYMENT_TYPE']), '5')
            self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'C')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['SUB_AMT']),
                             str(decimal.Decimal(str(pay_amount)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_request[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount).quantize(decimal.Decimal('0.00'))))

            # 022 申购 022212 现金宝收支明细
            self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(vacco_detail[0]['APKIND']), '022')
            self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '001F01')

            # 撤单后该优惠券当前可用状态为：
            ecards = ecard_no
            ecard = self._db.get_coupon_no(ecard_no=str(ecards))
            self.assertEqual(str(ecard[0]['STATUS']), 'ISSUE')

    # 获取定期列表
    @file_data('test_data/test_get_dqb_product_list.json')
    def test_get_dqb_product_list(self, user_name, password, assert_info):
        self._restful_xjb.dqb_product_list(user_name=str(user_name), password=str(password))
        dqb_list = self._db.get_on_sale_product_list(product_type='1', accept_mode='M', is_archive='0')

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        actual_dqb_count = entity.totalCount
        actual_dqb_list = entity.dataList

        self.assertEqual(int(actual_dqb_count), len(dqb_list))

        for i in range(0, len(actual_dqb_list)):
            self.assertTrue(str(actual_dqb_list[i]['productId']) in str(dqb_list))
            self.assertEqual(str(actual_dqb_list[i]['productType']), '1')

    # 获取高端列表
    @file_data('test_data/test_get_vip_product_list.json')
    def test_get_vip_product_list(self, user_name, password, assert_info):
        self._restful_xjb.vip_product_list(user_name=str(user_name), password=str(password))
        vip_list = self._db.get_on_sale_product_list(product_type='3', accept_mode='M', is_archive='0')

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        actual_vip_count = entity.totalCount
        actual_vip_list = entity.dataList

        self.assertEqual(int(actual_vip_count), len(vip_list))

        for i in range(0, len(actual_vip_list)):
            self.assertTrue(str(actual_vip_list[i]['productId']) in str(vip_list))
            self.assertEqual(str(actual_vip_list[i]['productType']), '3')

    # 设置合格投资者
    @file_data('test_data/test_set_qualified_investor.json')
    def test_set_qualified_investor(self, user_name, password, assert_info):
        self._restful_xjb.set_qualified_investor(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 首页收益信息
    @file_data('test_data/test_get_index_income_info.json')
    def test_get_index_income_info(self, user_name, password, assert_info):
        self._restful_xjb.get_index_income_info(user_name=str(user_name), password=str(password))
        fund_total_profit = self._db.get_cust_total_profit(mobile=str(user_name), prod_type='2')
        dqb_total_profit = self._db.get_cust_total_profit(mobile=str(user_name), prod_type='1')
        vip_total_profit = self._db.get_cust_total_profit(mobile=str(user_name), prod_type='3')
        vacco_total_profit = self._db.xjb_last_profit(mobile=str(user_name), apkind='143')
        total_income = fund_total_profit + dqb_total_profit + vip_total_profit + vacco_total_profit

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        actual_total_profit = entity.sumIncome

        self.assertEqual(str(decimal.Decimal(actual_total_profit).quantize(decimal.Decimal('0.00'))),
                         str(decimal.Decimal(total_income).quantize(decimal.Decimal('0.00'))))

    # 我的定期宝产品详情
    @file_data('test_data/my_dqb_detail.json')
    def test_my_dqb_detail(self, user_name, password, product_id, holding_type, assert_info):
        # 从数据库中查出order_no，放入参数中
        trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
        self._restful_xjb.my_dqb_detail(user_name=str(user_name), password=str(password),
                                        order_no=str(str(trade_order[0]['ORDER_NO'])),
                                        product_id=str(product_id), holding_type=str(holding_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

        self.assertEqual(str(trade_order[0]['TO_PROD']), entity.body_detail['productId'])
        self.assertEqual(str(trade_order[0]['AP_AMT']), entity.body_detail['purchaseAmt'])

        product_info = self._db.get_product_info(product_id=str(product_id))
        self.assertEqual(str(product_info[0]['productid']), entity.body_detail['productId'])
        self.assertEqual(str(product_info[0]['product_short_name']), entity.body_detail['productName'])
        self.assertEqual(str(product_info[0]['float_yield']), entity.body_detail['expectedAnnualYield'])
        self.assertEqual(str(product_info[0]['min_hold_amount']), entity.body_detail['minHoldingCount'])
        self.assertEqual(str(product_info[0]['min_redeem_amount']), entity.body_detail['minRedeemAmount'])

    # 我的高端产品详情
    @file_data('test_data/my_vip_detail.json')
    def test_my_vip_detail(self, user_name, password, product_id, holding_type, assert_info):
        # 从数据库中查出order_no，放入参数中
        trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
        self._restful_xjb.my_vip_detail(user_name=str(user_name), password=str(password),
                                        order_no=str(str(trade_order[0]['ORDER_NO'])),
                                        product_id=str(product_id), holding_type=str(holding_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

        self.assertEqual(str(trade_order[0]['ORDER_NO']), entity.body_detail['orderNo'])
        self.assertEqual(str(trade_order[0]['TO_PROD']), entity.body_detail['productId'])
        self.assertEqual(str(trade_order[0]['AP_AMT']), entity.body_detail['purchaseAmt'])
        self.assertEqual(str(trade_order[0]['VALIDATE_PHONE']), str(user_name))

        product_info = self._db.get_product_info(product_id=str(product_id))
        self.assertEqual(str(product_info[0]['productid']), entity.body_detail['productId'])
        self.assertEqual(str(product_info[0]['product_short_name']), entity.body_detail['productName'])
        self.assertEqual(str(product_info[0]['min_hold_amount']), entity.body_detail['minHoldingCount'])
        self.assertEqual(str(product_info[0]['min_redeem_amount']), entity.body_detail['minRedeemAmount'])

    # 我的基金产品详情
    @file_data('test_data/my_fund_detail.json')
    def test_my_fund_detail(self, user_name, password, fund_id, holding_type, assert_info):
        # 从数据库中查出order_no，放入参数中
        trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
        self._restful_xjb.my_fund_detail(user_name=str(user_name), password=str(password),
                                         order_no=str(str(trade_order[0]['ORDER_NO'])),
                                         fund_id=str(fund_id), holding_type=str(holding_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

        self.assertEqual(str(trade_order[0]['ORDER_NO']), entity.body_detail['orderId'])
        self.assertEqual(str(trade_order[0]['TO_PROD']), entity.body_detail['fundId'])
        self.assertEqual(str(trade_order[0]['AP_AMT']), entity.body_detail['purchaseAmt'])
        self.assertEqual(str(trade_order[0]['VALIDATE_PHONE']), str(user_name))

        product_info = self._db.get_product_info(product_id=str(fund_id))
        self.assertEqual(str(product_info[0]['productid']), entity.body_detail['fundId'])
        self.assertEqual(str(product_info[0]['product_short_name']), entity.body_detail['fundName'])
        self.assertEqual(str(product_info[0]['min_hold_amount']), entity.body_detail['minHoldShare'])
        self.assertEqual(str(product_info[0]['min_redeem_amount']), entity.body_detail['minRedeemAmount'])
        self.assertEqual(str(decimal.Decimal(product_info[0]['latest_nav']).quantize(decimal.Decimal('0.0000'))),
                         entity.body_detail['dynamicColumnValue'])

    # 获取用户基本信息
    @file_data('test_data/get_cust_base_info.json')
    def test_get_cust_base_info(self, user_name, password, assert_info):
        self._restful_xjb.get_cust_base_info(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        cust_info = self._db.get_cust_info(
            columns='cust_no, cert_no, cert_type, name, mobile, type, status, source, level, risk_level',
            match='=', mobile=str(user_name))
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        self.assertEqual(str(cust_info[0]['cust_no']), str(entity.body_custNo))
        self.assertEqual(str(cust_info[0]['cert_no']), str(entity.body_certNo))
        self.assertEqual(str(cust_info[0]['cert_type']), str(entity.body_certType))
        self.assertEqual(str(cust_info[0]['name']), str(entity.body_name))
        self.assertEqual(str(cust_info[0]['mobile']), str(entity.body_mobile))
        self.assertEqual(str(cust_info[0]['type']), str(entity.body_type))
        self.assertEqual(str(cust_info[0]['status']), str(entity.body_status))
        self.assertEqual(str(cust_info[0]['source']), str(entity.body_source))
        self.assertEqual(str(cust_info[0]['level']), str(entity.body_level))
        self.assertEqual(str(cust_info[0]['risk_level']), str(entity.body_riskLevel))

    # 搜索所有产品（定期和高端）
    @file_data('test_data/search_all_fin_product.json')
    def test_search_all_fin_product(self, user_name, password, keyword, assert_info):
        self._restful_xjb.search_all_fin_product(user_name=str(user_name), password=str(password), keyword=str(keyword))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

        dqb_product_info, dqb1_product_info, vip_product_info, vip1_product_info, fund_product_info, fund1_product_info \
            = self._db.search_all_fin_product(keyword=str(keyword))
        data_list = entity.body_dataList
        for index in range(0, len(data_list)):
            db_vip_len = len(vip_product_info) or len(vip1_product_info)
            if str(data_list[index]['listTitle']) == '高端理财':
                vip_list = data_list[index]['list']
                if db_vip_len > 5:
                    db_vip_len = 5
                self.assertEqual(str(db_vip_len), str(len(vip_list)))
                if len(data_list) != 1:
                    for i in range(index, len(vip_list)):
                        self.assertEqual(str(vip_product_info[i]['productid']), vip_list[i]['productId'])
                        self.assertEqual(str(vip_product_info[i]['product_short_name']),
                                         entity.body_dataList[index]['list'][i]['productTitle'])
                        self.assertEqual(str(vip_product_info[i]['product_type']),
                                         entity.body_dataList[index]['list'][i]['productType'])
                elif len(data_list) == 1:
                    for b in range(index, len(vip_list)):
                        self.assertEqual(str(vip1_product_info[b]['productid']), vip_list[b]['productId'])
                        self.assertEqual(str(vip1_product_info[b]['product_short_name']),
                                         entity.body_dataList[index]['list'][b]['productTitle'])
                        self.assertEqual(str(vip1_product_info[b]['product_type']),
                                         entity.body_dataList[index]['list'][b]['productType'])

            db_dqb_len = len(dqb_product_info) or len(dqb1_product_info)
            if str(data_list[index]['listTitle']) == '定期宝':
                dqb_list = data_list[index]['list']
                if db_dqb_len > 5:
                    db_dqb_len = 5
                self.assertEqual(str(db_dqb_len), str(len(dqb_list)))
                if len(data_list) != 1:
                    for j in range(0, len(dqb_list)):
                        self.assertEqual(str(dqb_product_info[j]['productid']),
                                         entity.body_dataList[index]['list'][j]['productId'])
                        self.assertEqual(str(dqb_product_info[j]['product_short_name']),
                                         entity.body_dataList[index]['list'][j]['productTitle'])
                        self.assertEqual(str(dqb_product_info[j]['product_type']),
                                         entity.body_dataList[index]['list'][j]['productType'])
                elif len(data_list) == 1:
                    for a in range(0, len(dqb_list)):
                        self.assertEqual(str(dqb1_product_info[a]['productid']),
                                         entity.body_dataList[index]['list'][a]['productId'])
                        self.assertEqual(str(dqb1_product_info[a]['product_short_name']),
                                         entity.body_dataList[index]['list'][a]['productTitle'])
                        self.assertEqual(str(dqb1_product_info[a]['product_type']),
                                         entity.body_dataList[index]['list'][a]['productType'])

    # 积分+优惠券认购定期
    @file_data('test_data/test_purchase_using_points_coupon.json')
    def test_purchase_using_points_coupon(self, user_name, password, product_id, trade_password, pay_amt, points,
                                          is_use_points, prod_type_scope_val, is_successful, assert_info):

        coupon, can_used_coupon, can_not_used_coupon = self._db.get_coupon_count(mobile=str(user_name),
                                                                                 amount=str(pay_amt),
                                                                                 prod_type_scope_val=str(
                                                                                     prod_type_scope_val),
                                                                                 prod_id=str(product_id))
        coupon_ecard = can_used_coupon[0]['ECARD_NO']
        discount_amount = can_used_coupon[0]['AMOUNT']
        points = self._restful_xjb.buy_product_using_coupon_points(user_name=str(user_name),
                                                                   login_password=str(password),
                                                                   product_id=str(product_id),
                                                                   trade_password=str(trade_password),
                                                                   is_use_points=str(is_use_points),
                                                                   pay_amount=str(pay_amt),
                                                                   points=str(points),
                                                                   coupon_ids=str(coupon_ecard))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

        if str(is_successful) == 'true':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))
            # 012 认购 012020 现金宝认购
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012020')
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '1')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['STATUS']), 'A')
            self.assertEqual(str(trade_order[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount).quantize(decimal.Decimal('0.00'))))
            if str(is_use_points) == '1':
                self.assertEqual(str(trade_order[0]['POINTS_AMOUNT']),
                                 str(decimal.Decimal(points).quantize(decimal.Decimal('0.00'))))
                self.assertEqual(str(trade_order[0]['POINTS_QUANTITY']),
                                 str(decimal.Decimal(points).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(pay_amt)).quantize(decimal.Decimal('0.00'))))

            # 020 认购 002210 认购定期
            self.assertEqual(str(trade_request[0]['APKIND']), '020')
            self.assertEqual(str(trade_request[0]['SUB_APKIND']), '002210')
            self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '1')
            self.assertEqual(str(trade_request[0]['PURCHASE_PAYMENT_TYPE']), '5')
            self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['SUB_AMT']),
                             str(decimal.Decimal(str(pay_amt)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_request[0]['COUPON_AMOUNT']),
                             str(decimal.Decimal(discount_amount).quantize(decimal.Decimal('0.00'))))
            if str(is_use_points) == '1':
                self.assertEqual(str(trade_request[0]['POINTS_AMOUNT']),
                                 str(decimal.Decimal(points).quantize(decimal.Decimal('0.00'))))
                self.assertEqual(str(trade_request[0]['POINTS_QUANTITY']),
                                 str(decimal.Decimal(points).quantize(decimal.Decimal('0.00'))))

            # 024 赎回 002201 现金宝赎回认购定期
            amount_pay_by_vacco = decimal.Decimal(str(pay_amt)) - decimal.Decimal(
                discount_amount) - decimal.Decimal(str(points))
            self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
            self.assertEqual(str(trade_quty_chg[0]['APKIND']), '024')
            self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '002201')
            self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')

            # 020 认购 020040 认购定期
            self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '1')
            self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
            self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                             str(decimal.Decimal(pay_amt).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
            self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '002210')

            self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(vacco_detail[0]['APKIND']), '024')
            self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '002201')
            self.assertEqual(str(vacco_detail[0]['SUB_AMT']),
                             str(decimal.Decimal(-amount_pay_by_vacco).quantize(decimal.Decimal('0.00'))))

            # verify used coupon
            ecard = self._db.get_coupon_no(ecard_no=str(coupon_ecard))
            self.assertEqual(str(ecard[0]['STATUS']), 'USED')
            consume_coupon = self._db.get_cust_consume_coupon(mobile=str(user_name), ecard_no=str(coupon_ecard))
            self.assertEqual(str(consume_coupon[0]['ITEM_ID']), str(product_id))
            self.assertEqual(str(consume_coupon[0]['SOURCE_TYPE']), 'COUPON_DEDUCTE_PRODUCT')
            self.assertEqual(str(consume_coupon[0]['COUPON_STATUS']), 'CONSUME')

            # verify used points
            if str(is_use_points) == '1':
                points_consume = self._db.get_points_consume(mobile=str(user_name))
                self.assertEqual(str(points_consume[0]['AMOUNT']),
                                 str(decimal.Decimal(str(points)).quantize(decimal.Decimal('0.00'))))
                self.assertEqual(str(points_consume[0]['ITEM_ID']), str(product_id))
                self.assertEqual(str(points_consume[0]['SOURCE_TYPE']), 'POINT_DEDUCTE_BUY_PRODUCT')
                self.assertEqual(str(points_consume[0]['POINT_TYPE']), 'CONSUME')

            self.assertEqual(str(entity.returnResult), 'Y')

    # 使用现金宝申购高端，撤单，钱返回到现金宝
    @file_data('test_data/test_buy_product_cancel.json')
    def test_buy_product_cancel(self, user_name, password, product_id, amt, trade_password, is_successful,
                                assert_info):
        self._restful_xjb.purchase_then_cancel(user_name=str(user_name), password=str(password),
                                               product_id=str(product_id), trade_password=str(trade_password),
                                               purchase_amt=str(amt), coupon_ids='')

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(is_successful) == 'true':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
            trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))

            # 013 申购 013020 现金宝申购
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '013')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '013020')
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            if str(product_id).startswith('H9'):
                self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '3')
            else:
                self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '2')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['STATUS']), 'C')
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))

            # 022 申购 022212 申购基金
            if str(product_id).startswith('H9') is False:
                self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022212')
                self.assertEqual(str(trade_request[0]['PROD_TYPE']), '2')
                self.assertEqual(str(trade_request[0]['APKIND']), '022')
                self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
                self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
                self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
                self.assertEqual(str(trade_request[0]['PURCHASE_PAYMENT_TYPE']), '0')
                self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
                self.assertEqual(str(trade_request[0]['APPLY_ST']), 'C')
                self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['SUB_AMT']),
                                 str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
                # 024 赎回
                self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
                self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
                self.assertEqual(str(trade_quty_chg[0]['APKIND']), '024')
                # 024012 现金宝赎回买基金
                self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '024012')
                self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                                 str(decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
                self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')

                self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
                self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')

            if str(product_id).startswith('H9'):
                # 032 份额解冻 032002 预约申购解冻
                self.assertEqual(str(vacco_detail[0]['APKIND']), '032')
                self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '032002')
            else:
                # 022 申购 001F01 现金宝普通赎回撤单
                self.assertEqual(str(vacco_detail[0]['APKIND']), '022')
                self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '001F01')
            self.assertEqual(str(vacco_detail[0]['SUB_AMT']),
                             str(decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))

            if str(product_id).startswith('H9'):
                # 022 申购 022210 申购高端（来自现金宝）
                self.assertEqual(str(trade_reserve[0]['APKIND']), '022')
                self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '022210')
                self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '3')
                self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
                self.assertEqual(str(trade_reserve[0]['BRANCH_CODE']), '675')
                self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(product_id))
                self.assertEqual(str(trade_reserve[0]['PURCHASE_PAYMENT_TYPE']), '0')
                self.assertEqual(str(trade_reserve[0]['RES_ST']), 'C')
                self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
                                 str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(entity.returnResult), 'Y')

    # 积分+现金宝购买产品
    @file_data('test_data/test_purchase_product_using_points.json')
    def test_purchase_product_using_points(self, user_name, password, amt, trade_password, points, is_use_points,
                                           product_id, product_status, product_type, assert_info):
        total_points_before_buy_product = self._db.get_cust_total_points_amount(mobile=str(user_name))[0]['AMOUNT']
        points = self._restful_xjb.buy_product_using_coupon_points(user_name=str(user_name),
                                                                   login_password=str(password), pay_amount=str(amt),
                                                                   trade_password=str(trade_password),
                                                                   points=str(points), is_use_points=str(is_use_points),
                                                                   product_id=str(product_id), coupon_ids='')
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertIn(assert_info["returnMsg"], entity.returnMsg)
        if str(assert_info["returnCode"]) == '000000':
            self.assertEqual(str(entity.returnResult), 'Y')
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))
            trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
            if str(product_status) == '认购' or str(product_status) == '预约认购':
                # 012 认购 012020 现金宝认购
                self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
                self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012020')
            elif str(product_status) == '申购':
                # 013 申购 013020 现金宝申购
                self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '013')
                self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '013020')

            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), str(product_type))
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['STATUS']), 'A')
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
            if str(is_use_points) == '1':
                self.assertEqual(str(trade_order[0]['POINTS_AMOUNT']),
                                 str(decimal.Decimal(points).quantize(decimal.Decimal('0.00'))))
                self.assertEqual(str(trade_order[0]['POINTS_QUANTITY']),
                                 str(decimal.Decimal(points).quantize(decimal.Decimal('0.00'))))

            if str(product_status) == '认购' and str(product_type) == '2':
                # 020 认购 020010 认购基金
                self.assertEqual(str(trade_request[0]['APKIND']), '020')
                self.assertEqual(str(trade_request[0]['SUB_APKIND']), '020010')
            elif str(product_status) == '认购' and str(product_type) == '1':
                # 020 认购 002210 认购定期
                self.assertEqual(str(trade_request[0]['APKIND']), '020')
                self.assertEqual(str(trade_request[0]['SUB_APKIND']), '002210')
            elif str(product_status) == '申购' and str(product_type) == '2':
                # 022 申购 022212 申购基金
                self.assertEqual(str(trade_request[0]['APKIND']), '022')
                self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022212')

            if str(product_type) != '3' and str(product_status) != '预约认购':
                self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
                self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
                self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
                self.assertEqual(str(trade_request[0]['PROD_TYPE']), str(product_type))
                self.assertEqual(str(trade_request[0]['PURCHASE_PAYMENT_TYPE']), '5')
                self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
                self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['SUB_AMT']),
                                 str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
                if str(is_use_points) == '1':
                    self.assertEqual(str(trade_request[0]['POINTS_AMOUNT']),
                                     str(decimal.Decimal(points).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(str(trade_request[0]['POINTS_QUANTITY']),
                                     str(decimal.Decimal(points).quantize(decimal.Decimal('0.00'))))

            if str(product_type) == '3' or str(product_status) == '预约认购':
                if str(product_type) == '3' and str(product_status).__contains__('认购'):
                    # 020 认购 002211 认购高端（来自现金宝）
                    self.assertEqual(str(trade_reserve[0]['APKIND']), '020')
                    self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '002211')
                elif str(product_type) == '3' and str(product_status).__contains__('申购'):
                    # 022 申购 022210 申购高端（来自现金宝）
                    self.assertEqual(str(trade_reserve[0]['APKIND']), '022')
                    self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '022210')
                else:
                    # 020020 预约认购定期宝
                    self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '020020')
                self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
                self.assertEqual(str(trade_reserve[0]['BRANCH_CODE']), '675')
                self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), str(product_type))
                self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(product_id))
                self.assertEqual(str(trade_reserve[0]['PURCHASE_PAYMENT_TYPE']), '5')
                self.assertEqual(str(trade_reserve[0]['RES_ST']), 'N')
                self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
                                 str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))

                # 031 份额冻结
                self.assertEqual(str(trade_quty_chg[0]['APKIND']), '031')
                if str(product_status).__contains__('认购'):
                    # 031002 预约认购冻结
                    self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '031002')
                else:
                    # 031003 预约申购冻结
                    self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '031003')

            self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
            if str(product_type) == '1' and str(product_status) != '预约认购':
                # 024 赎回 002201 现金宝赎回认购定期
                self.assertEqual(str(trade_quty_chg[0]['APKIND']), '024')
                self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '002201')
            elif str(product_type) == '2':
                # 024 赎回
                self.assertEqual(str(trade_quty_chg[0]['APKIND']), '024')
                if str(product_status) == '认购':
                    # 024011 现金宝赎回认购基金
                    self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '024011')
                else:
                    # 024012 现金宝赎回申购基金
                    self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '024012')

            actual_amt = decimal.Decimal(str(amt)) - decimal.Decimal(str(points))
            self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                             str(decimal.Decimal(-actual_amt).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')

            self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), str(product_type))
            self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
            self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                             str(decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
            if str(product_type) == '1':
                self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
                # 020 认购
                if str(product_status) == '认购':
                    # 002210 认购定期
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '002210')
                elif str(product_status) == '预约认购':
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '020020')
            elif str(product_type) == '2':
                if str(product_status) == '认购':
                    # 020 认购 020010 认购基金
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '020010')
                else:
                    # 022 申购 022212 申购基金
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '022')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '022212')
            elif str(product_type) == '3':
                if str(product_status).__contains__('认购'):
                    # 020 认购 002211 认购高端（来自现金宝）
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '002211')
                else:
                    # 022 申购 022210 申购高端（来自现金宝）
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '022')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '022210')

            self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')
            if str(product_type) == '1':
                # 024 赎回 002201 现金宝赎回认购定期
                self.assertEqual(str(vacco_detail[0]['APKIND']), '024')
                self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '002201')
            elif str(product_type) == '2':
                # 024 赎回 024011 赎回认购基金
                self.assertEqual(str(vacco_detail[0]['APKIND']), '024')
                if str(product_status) == '认购':
                    self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '024011')
                else:
                    # 024012 现金宝赎回申购基金
                    self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '024012')
            elif str(product_type) == '3':
                self.assertEqual(str(vacco_detail[0]['APKIND']), '031')
                if str(product_status).__contains__('认购'):
                    # 031002 预约认购冻结
                    self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '031002')
                else:
                    # 031003 预约申购冻结
                    self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '031003')
            self.assertEqual(str(vacco_detail[0]['SUB_AMT']),
                             str(decimal.Decimal(-actual_amt).quantize(decimal.Decimal('0.00'))))

            # verify used points
            if str(is_use_points) == '1':
                if str(product_type) != '3' and str(product_status) != '预约认购':
                    points_consume = self._db.get_points_consume(mobile=str(user_name))
                    self.assertEqual(str(points_consume[0]['AMOUNT']),
                                     str(decimal.Decimal(str(points)).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(str(points_consume[0]['ITEM_ID']), str(product_id))
                    self.assertEqual(str(points_consume[0]['SOURCE_TYPE']), 'POINT_DEDUCTE_BUY_PRODUCT')
                    self.assertEqual(str(points_consume[0]['POINT_TYPE']), 'CONSUME')
                    left_points = total_points_before_buy_product - decimal.Decimal(points)
                    actual_points = self._db.get_cust_total_points_amount(mobile=str(user_name))[0]['AMOUNT']
                    self.assertEqual(decimal.Decimal(actual_points),
                                     decimal.Decimal(left_points).quantize(decimal.Decimal('0.00')))
                else:
                    points_frozen = self._db.get_points_frozen(mobile=str(user_name))
                    # 预约下单不会扣减积分数，只会冻结
                    actual_points = self._db.get_cust_total_points_amount(mobile=str(user_name))[0]['AMOUNT']
                    self.assertEqual(decimal.Decimal(actual_points),
                                     decimal.Decimal(total_points_before_buy_product).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(str(points_frozen[0]['AMOUNT']),
                                     str(decimal.Decimal(str(points)).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(str(points_frozen[0]['APPLY_AMOUNT']),
                                     str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(str(points_frozen[0]['ITEM_ID']), str(product_id))
                    self.assertEqual(str(points_frozen[0]['SOURCE_TYPE']), 'POINT_DEDUCTE_BUY_PRODUCT')
                    self.assertEqual(str(points_frozen[0]['POINT_TYPE']), 'FROZEN')

    # 我用户持有资产
    @file_data('test_data/test_my_hold_asset.json')  #
    def test_my_hold_asset(self, user_name, password, product_type, assert_info):
        self._restful_xjb.my_hold_asset(user_name=str(user_name), password=str(password),
                                        product_type=str(product_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        hold_shares_quty, reedeem_hold_shares_transit, hold_shares_transit = self._db.my_hold_dqb_vip_list(
            mobile=str(user_name), product_type=str(product_type))
        hold_shares = hold_shares_quty + hold_shares_transit
        data_list = entity.dataList
        self.assertEqual(len(data_list), len(hold_shares))

        if str(product_type) == '2':
            for i in range(0, len(hold_shares)):

                if i < len(hold_shares_quty):
                    fund_nav, count_fund_nav = self._db.get_fund_nav(fund_id=str(hold_shares[i]['PROD_ID']))
                    fund_hold_money = decimal.Decimal(hold_shares[i]['BALANCE'] * fund_nav[0]['nav']).quantize(
                        decimal.Decimal('0.000'))
                    fund_hold_money = str(fund_hold_money)[0:len(str(fund_hold_money)) - 1]
                    money = fund_hold_money
                else:
                    money = hold_shares[i]['BALANCE']
                print hold_shares[i]['PROD_ID']
                self.assertEqual(data_list[i]['productId'], hold_shares[i]['PROD_ID'])
                self.assertEqual(str(data_list[i]['purchaseAmt']), str(money))

        if str(product_type) == '1' or str(product_type) == '3':
            for i in range(0, len(data_list)):
                self.assertEqual(data_list[i]['productId'], hold_shares[i]['PROD_ID'])
                if str(product_type) == '1':
                    self.assertEqual(str(data_list[i]['purchaseAmt']),
                                     str(hold_shares[i]['BALANCE'] + reedeem_hold_shares_transit[i]['BALANCE']))
                else:
                    self.assertEqual(str(data_list[i]['purchaseAmt']), str(hold_shares[i]['BALANCE']))

    # 质押列表
    @file_data('test_data/test_my_loan_list.json')
    def test_my_loan_list(self, user_name, password, product_id, is_history, assert_info):
        self._restful_xjb.my_loan_list(user_name=str(user_name), password=str(password),
                                       is_history=str(is_history))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        # 静态份额
        prod_quty = self._db.get_cust_prod_quty_by_product_id(mobile=str(user_name),
                                                              product_id=str(product_id))
        # 质押表
        prod_pledge_loan = self._db.get_cust_pledge_loan(mobile=str(user_name),
                                                         product_id=str(product_id),
                                                         is_history=str(is_history))
        # 产品信息
        prod_info = self._db.get_product_info(product_id=str(product_id))
        # 产品质押
        pledge_product_info = self._db.get_product_pledge_info(product_id=str(product_id))
        can_loan_continue = entity.canLoanContinue
        data_list = entity.dataList
        repay_amt_date = entity.repayAmtDate
        total_count = entity.totalCount
        total_loan_amt = entity.totalLoanAmt
        total_amt = 0
        if len(prod_quty) == 0 or len(prod_pledge_loan) == None or len(prod_pledge_loan) == 0:
            self.assertEqual(str(can_loan_continue), '0')
            self.assertEqual(str(total_count), '0')
            self.assertEqual(str(total_loan_amt), str(total_amt))
            self.assertEqual(str(repay_amt_date), '')
        else:
            # 质押起始日
            prod_start_pledge_date = pledge_product_info[0]['start_pledge'].__getslice__(0, 8)
            # 质押结束日
            prod_end_pledge_date = pledge_product_info[0]['end_pledge'].__getslice__(0, 8)
            # 强制还款日
            prod_force_redeem_reimbursement = pledge_product_info[0][
                'forced_redeem_reimbursement'].__getslice__(0,
                                                            8)
            # 产品到期日
            share_next_carry_date = prod_info[0]['share_next_carry_date']
            before_share_next_carry_date = datetime.datetime.strptime(share_next_carry_date,
                                                                      '%Y%m%d') - datetime.timedelta(
                days=1)
            # 如果借款日期是在质押起始日之前，或是质押结束日之后，或是强制还款日之后，产品到期日前一天，不能进行借款
            today = datetime.datetime.today().strftime('%Y%m%d')
            if str(prod_start_pledge_date) > today or str(
                    prod_force_redeem_reimbursement) < today or str(
                prod_end_pledge_date) < today or before_share_next_carry_date.strftime(
                '%Y%m%d') == str(today):
                self.assertEqual(str(can_loan_continue), '0')
            else:
                self.assertEqual(str(can_loan_continue), '1')
                self.assertEqual(str(repay_amt_date).replace('-', ''),
                                 str(prod_pledge_loan[0]['START_DATE']).split(' ')[0])
                self.assertEqual(str(total_count), str(len(prod_pledge_loan)))
                for i in range(0, len(prod_pledge_loan)):
                    total_amt = total_amt + prod_pledge_loan[i]['PLEDGE_AMT']
                    # 每日利息
                    days = (
                        datetime.datetime.today() - datetime.datetime.strptime(
                            prod_pledge_loan[i]['START_DATE'],
                            '%Y%m%d')).days
                    if days == 0:
                        total_interest = round(
                            prod_pledge_loan[i]['INTEREST_RATE'] * prod_pledge_loan[i][
                                'PLEDGE_AMT'] / 365, 2)
                    else:
                        total_interest = round(
                            prod_pledge_loan[i]['INTEREST_RATE'] * prod_pledge_loan[i][
                                'PLEDGE_AMT'] / 365,
                            2) * days
                    if str(is_history) == '0':
                        self.assertEqual(str(data_list[i]['loanShare']),
                                         str(prod_pledge_loan[i]['PLEDGE_QUTY']))
                        self.assertEqual(str(data_list[i]['repayCapitalAmt']),
                                         str(prod_pledge_loan[i]['PLEDGE_AMT']))
                        self.assertEqual(str(data_list[i]['repayInterestAmt']), str(total_interest))
                        self.assertEqual(str(data_list[i]['repayAmt']),
                                         str(decimal.Decimal(prod_pledge_loan[i]['PLEDGE_AMT'] +
                                                             total_interest).quantize(
                                             decimal.Decimal('0.00'))))
                        self.assertEqual(str(data_list[i]['loanRate']),
                                         str(prod_pledge_loan[i]['INTEREST_RATE']))
                        self.assertEqual(str(data_list[i]['loanStatus']),
                                         str(prod_pledge_loan[i]['STATUS']))


                    else:
                        self.assertEqual(str(data_list[i]['loanShare']), '0.00')
                        self.assertEqual(str(data_list[i]['repayCapitalAmt']), '')
                        self.assertEqual(str(data_list[i]['repayInterestAmt']), '')
                        self.assertEqual(str(data_list[i]['repayAmt']), '')
                        self.assertEqual(str(data_list[i]['loanRate']), '')
                        self.assertEqual(str(data_list[i]['loanStatus']), '')

                if str(is_history) == '0':
                    self.assertEqual(str(total_loan_amt),
                                     str(decimal.Decimal(
                                         total_amt + decimal.Decimal(total_interest)).quantize(
                                         decimal.Decimal('0.00'))))

    # 高端赎回费率
    @file_data('test_data/test_vip_redeem_rate.json')
    def test_vip_redeem_rate(self, user_name, login_password, product_id, redeem_amt, assert_info):
        self._restful_xjb.vip_redeem_rate(user_name=str(user_name), login_password=str(login_password),
                                          product_id=str(product_id), redeem_amt=str(redeem_amt))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        expected_redeem_rate = self._db.vip_redeem_rate(product_id=str(product_id))
        actual_rate = entity.rate
        self.assertEquals(
            str("%.2f%%" % (decimal.Decimal(expected_redeem_rate[0]['max_charge_rate']).quantize(
                decimal.Decimal('0.00')))),
            str(actual_rate))

    # 质押信息
    @file_data('test_data/test_load_info.json')
    def test_load_info(self, user_name, password, product_id, assert_info):
        self._restful_xjb.trade_load_info(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        # 静态份额
        prod_quty = self._db.get_cust_prod_quty_by_product_id(mobile=str(user_name), product_id=str(product_id))
        balance = prod_quty[0]['BALANCE'] - prod_quty[0]['ABNM_FROZEN']
        # 质押表
        prod_pledge_loan = self._db.get_cust_pledge_loan(mobile=str(user_name), product_id=str(product_id),
                                                         is_history=str('0'))
        prod_pledge = self._db.get_product_pledge_info(product_id=str(product_id))
        pledge_ratio = prod_pledge[0]['pledge_ratio']

        can_borrow_amt = entity.canBorrowAmt
        if len(prod_quty) == 0 or len(prod_pledge_loan) == 0:
            self.assertEqual(str(can_borrow_amt), '0.00')
        else:
            borrow_amt = balance * pledge_ratio / 100 - prod_pledge_loan[0]['PLEDGE_AMT']
            self.assertEqual(str(can_borrow_amt), str(decimal.Decimal(borrow_amt).quantize(decimal.Decimal('0.00'))))

    # 高端申购费率
    @file_data('test_data/test_vip_purchase_rate.json')
    def test_vip_purchase_rate(self, user_name, login_password, product_id, purchase_amt, assert_info):
        self._restful_xjb.vip_purchase_rate(user_name=str(user_name), login_password=str(login_password),
                                            product_id=str(product_id), purchase_amt=str(purchase_amt))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        expected_purchase_rate = self._db.vip_purchase_rate(product_id=str(product_id))
        actual_rate = entity.rate
        self.assertEquals(
            str("%.2f%%" % (decimal.Decimal(
                expected_purchase_rate[0]['max_charge_rate']).quantize(decimal.Decimal('0.00')))),
            str(actual_rate))

    # 根据借款金额获取质押信息
    @file_data('test_data/test_get_loan_apply_info.json')
    def test_get_loan_apply_info(self, user_name, password, product_id, loan_amt, assert_info):
        self._restful_xjb.trade_get_loan_apply_info(user_name=str(user_name), password=str(password),
                                                    product_id=str(product_id), loan_amt=str(loan_amt))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if str(assert_info["returnCode"]) == '000000':
            each_day_interest = entity.eachDayInterest
            loan_share = entity.loanShare
            # 质押表
            prod_pledge = self._db.get_product_pledge_info(product_id=str(product_id))
            interest_rate = prod_pledge[0]['borrow_rate'] / 100
            daily_interest = round(decimal.Decimal(str(loan_amt)) * interest_rate / 365, 2)
            # 产品净值
            prod_nav = self._db.get_product_info(product_id=str(product_id))[0]['latest_nav']
            expected_loan_share = round(
                decimal.Decimal(str(loan_amt)) * prod_nav * 100 / prod_pledge[0]['pledge_ratio'], 2)
            self.assertEqual(str(each_day_interest), str(daily_interest))
            self.assertEqual(str(loan_share), str(expected_loan_share))
        else:
            self.assertEqual(entity.body, '')

    # 定期宝赎回-获取收益信息
    @file_data('test_data/test_dqb_redeem_get_income_info.json')
    def test_dqb_redeem_get_income_info(self, user_name, login_password, product_id, trade_amt, assert_info):
        self._restful_xjb.dqb_redeem_get_income_info(user_name=str(user_name), login_password=str(login_password),
                                                     product_id=str(product_id), trade_amt=str(trade_amt))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        prod_rate = self._db.get_product_info(product_id=str(product_id))[0]['fixed_yield']
        hold_start_date = \
            self._db.get_cust_prod_quty_by_product_id(mobile=str(user_name), product_id=str(product_id))[0]['LAST_DATE']
        amount_capital_profit, profit = BusinessUtility().calculate_dhb_redeem_amount(redeem_amt=str(trade_amt),
                                                                                      rate=str(prod_rate),
                                                                                      hold_start_date=str(
                                                                                          hold_start_date))
        actual_info = entity.info
        self.assertEqual(str(actual_info),
                         str('备注：收益' + str(decimal.Decimal(profit).quantize(decimal.Decimal('0.00'))) +
                             '元，预计到账金额' +
                             str(decimal.Decimal(amount_capital_profit).quantize(decimal.Decimal('0.00'))) +
                             '元。剩余本金将按原到账日期到账'))

    # 基金制定定投计划
    @file_data('test_data/test_fund_make_invest_plan.json')
    def test_fund_make_invest_plan(self, user_name, password, fundId, payType, eachInvestAmt, payCycle,
                                   payDay, isConfirmBeyondRisk, trade_password, assert_info):
        self._restful_xjb.fund_make_invest_plan(user_name=str(user_name), password=str(password),
                                                fundId=str(fundId), payType=str(payType),
                                                eachInvestAmt=str(eachInvestAmt),
                                                payCycle=str(payCycle), payDay=str(payDay),
                                                isConfirmBeyondRisk=str(isConfirmBeyondRisk),
                                                trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(assert_info["returnCode"]) == '000000':
            fund_invest_plan = self._db.get_fund_make_invest_plan_validate(mobile=str(user_name))
            self.assertEqual(str(fund_invest_plan[0]['PERIOD']), str(payCycle))
            self.assertEqual(str(fund_invest_plan[0]['DAY']), str(payDay))
            self.assertEqual(str(fund_invest_plan[0]['AP_AMT']),
                             str(decimal.Decimal(str(eachInvestAmt)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(fund_invest_plan[0]['PURCHASE_PAYMENT_TYPE']), str(payType))
            self.assertEqual(str(fund_invest_plan[0]['PROD_ID']), str(fundId))
            self.assertEqual(str(fund_invest_plan[0]['PROD_TYPE']), '2')
            self.assertEqual(str(fund_invest_plan[0]['STATUS']), 'N')

    # 基金赎回费用估算
    @file_data('test_data/test_fund_redeem_cost_calt_value.json')
    def test_fund_redeem_cost_calt_value(self, user_name, login_password, redeem_amt, product_id, assert_info):
        self._restful_xjb.fund_redeem_cost_calt_value(user_name=str(user_name), login_password=str(login_password),
                                                      product_id=str(product_id), redeem_amt=str(redeem_amt))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        redeem_balance, product_rate, fund_nav, product_nav_value, pay_back_money_min, pay_back_money_max, set_value = \
            self._db.fund_redeem_cost_calt_value(mobile=str(user_name), product_id=str(product_id))
        user_trade_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

        near_work_date = self._db.judge_is_work_date(day=str(user_trade_time)[0:8])[0]['WORK_DATE']
        if str(user_trade_time)[0:8] == str(near_work_date):  # 交易当天为工作日
            if str(user_trade_time)[8:14] < '150000':  # 交易当时为15：00以前
                next1_work_date = self._db.get_next_work_date(pre_work_date=str(user_trade_time)[0:8])[0][
                    'WORK_DATE']
                expected_arrived_date = self._db.get_next_work_date(pre_work_date=str(next1_work_date))[0][
                    'WORK_DATE']
            else:
                next1_work_date = self._db.get_next_work_date(pre_work_date=str(user_trade_time)[0:8])[0][
                    'WORK_DATE']
                next2_work_date = self._db.get_next_work_date(pre_work_date=str(next1_work_date))[0][
                    'WORK_DATE']
                expected_arrived_date = self._db.get_next_work_date(pre_work_date=str(next2_work_date))[0][
                    'WORK_DATE']

        else:  # 交易当天为非工作日
            next1_work_date = self._db.get_next_work_date(pre_work_date=str(near_work_date))[0]['WORK_DATE']
            expected_arrived_date = self._db.get_next_work_date(pre_work_date=str(next1_work_date))[0][
                'WORK_DATE']
        actual_info = entity.info

        self.assertEqual(str(actual_info),
                         str(str(pay_back_money_min) + '元' + '~' + str(pay_back_money_max) + '元' + ' (' + str(
                             expected_arrived_date)[4:6] + '-' + str(
                             expected_arrived_date)[6:8] + '  ' + '24:00前' + ')'))

    # 获取基金定投列表验证
    @file_data('test_data/test_fund_invest_plan_list.json')
    def test_get_fund_invest_plan_list(self, user_name, password, assert_info):
        self._restful_xjb.get_fund_invest_plan(user_name=str(user_name), login_password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        fund_plans = self._db.fund_invest_plan_list(mobile=str(user_name))
        if assert_info['returnCode'] == '000000':
            if len(fund_plans) > 0:
                self.assertEqual(str(entity.body_totalCount), str(len(fund_plans)))
                for i in range(0, len(fund_plans)):
                    self.assertEqual(str(entity.body_dataList[i]['eachInvestAmt']), str(fund_plans[i]['AP_AMT']))
                    self.assertEqual(str(entity.body_dataList[i]['fundId']), str(fund_plans[i]['PROD_ID']))
                    self.assertEqual(str(entity.body_dataList[i]['investPlanId']),
                                     str(fund_plans[i]['PROTOCOL_NO']))
                    self.assertEqual(str(entity.body_dataList[i]['status']), str(fund_plans[i]['STATUS']))

    # 基金定投计划暂停type=1, 恢复type=2, 终止type=0,不传参type
    @file_data('test_data/test_handle_fund_invest_plan_validate.json')
    def test_fund_handle_invest_plan_validate(self, user_name, password, fundId, payType, eachInvestAmt, payCycle,
                                              payDay, isConfirmBeyondRisk, trade_password, assert_info):
        self._restful_xjb.fund_make_invest_plan(user_name=str(user_name), password=str(password),
                                                fundId=str(fundId), payType=str(payType),
                                                eachInvestAmt=str(eachInvestAmt), payCycle=str(payCycle),
                                                payDay=str(payDay), isConfirmBeyondRisk=str(isConfirmBeyondRisk),
                                                trade_password=str(trade_password))
        status = ['P', 'N', 'E']
        type = ['1', '2', '0']
        for i in range(0, 3):
            protocol_no = self._db.get_fund_make_invest_plan_validate(mobile=str(user_name))[0]['PROTOCOL_NO']
            self._restful_xjb.fund_handle_invest_plan_validate(user_name=str(user_name), password=str(password),
                                                               is_confirm_beyond_risk=str(isConfirmBeyondRisk),
                                                               type=str(type[i]), protocol_no=str(protocol_no),
                                                               trade_password=str(trade_password))

            entity = self._restful_xjb.entity.current_entity
            self.assertEqual(entity.returnCode, assert_info["returnCode"])
            self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

            if str(assert_info["returnCode"]) == '000000':
                fund_invest_plan = self._db.get_fund_make_invest_plan_validate(mobile=str(user_name))
                self.assertEqual(str(fund_invest_plan[0]['STATUS']), str(status[i]))

    # 基金定投计划暂停type=1, 恢复type=2, 终止type=0,传参type
    @file_data('test_data/test_handle_fund_invest_plan_sec.json')
    def test_fund_handle_invest_plan_validate_sec(self, user_name, password, is_confirm_beyond_risk, type,
                                                  trade_password, assert_info):
        if str(type) == '1' or str(type) == '0':
            protocol_no = self._db.update_fund_invest_plan_status(mobile=str(user_name), status='N')
        else:
            protocol_no = self._db.update_fund_invest_plan_status(mobile=str(user_name), status='P')

        self._restful_xjb.fund_handle_invest_plan_validate(user_name=str(user_name), password=str(password),
                                                           protocol_no=str(protocol_no),
                                                           is_confirm_beyond_risk=str(is_confirm_beyond_risk),
                                                           type=str(type), trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if assert_info['returnCode'] == '000000':
            fund_invest_plan = self._db.get_fund_make_invest_plan_validate(mobile=str(user_name))
            if str(type) == '1':
                # 暂停
                self.assertEqual(str(fund_invest_plan[0]['STATUS']), 'P')
            if str(type) == '2':
                # 恢复
                self.assertEqual(str(fund_invest_plan[0]['STATUS']), 'N')
            if str(type) == '0':
                # 终止
                self.assertEqual(str(fund_invest_plan[0]['STATUS']), 'E')

    # 高端质押-产品详情
    @file_data('test_data/test_loan_product_details.json')
    def test_loan_product_details(self, user_name, password, product_id, is_successful, assert_info):
        self._restful_xjb.trade_loan_product_detail(user_name=str(user_name), password=str(password),
                                                    product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        can_borrow_amt = entity.canBorrowAmt
        last_pay_date = entity.lastPayDate
        last_worth = entity.latestWorth
        loan_percent = entity.loanPrecent
        loan_rate = entity.loanRate
        if str(is_successful) == 'true':
            prod_quty_balance = \
                self._db.get_cust_prod_quty_by_product_id(mobile=str(user_name),
                                                          product_id=str(product_id))[0]['BALANCE']
            pledge_prod_info = self._db.get_product_pledge_info(product_id=str(product_id))
            prod_pledge_loan = self._db.get_cust_pledge_loan(mobile=str(user_name), product_id=str(product_id),
                                                             is_history=str('0'))
            product_info = self._db.get_product_info(product_id=str(product_id))

            pledge_ratio = pledge_prod_info[0]['pledge_ratio']
            borrow_rate = decimal.Decimal(pledge_prod_info[0]['borrow_rate']).quantize(decimal.Decimal('0.00'))
            if len(prod_pledge_loan) == 0:
                borrow_amt = prod_quty_balance * pledge_ratio / 100
            else:
                borrow_amt = prod_quty_balance * pledge_ratio / 100 - prod_pledge_loan[0]['PLEDGE_AMT']
            self.assertEqual(str(can_borrow_amt), str(decimal.Decimal(borrow_amt).quantize(decimal.Decimal('0.00'))))
            # 最终还款日为产品到期日的前一天（份额到期日的前一天）
            expected_end_repay_date = datetime.datetime.strftime(
                datetime.datetime.strptime(str(product_info[0]['share_next_carry_date']), '%Y%m%d') -
                datetime.timedelta(days=1), '%Y%m%d')
            self.assertEqual(str(last_pay_date).split(' ')[0].replace('-', ''), expected_end_repay_date)
            self.assertEqual(str(last_worth).split(' ')[0].replace('-', ''), str(prod_quty_balance))
            self.assertEqual(str(loan_percent),
                             str(decimal.Decimal(pledge_ratio).quantize(decimal.Decimal('0.00'))) + '%')
            self.assertEqual(str(loan_rate), str(borrow_rate) + '%')
            self.assertEqual(str(entity.productId), str(product_id))
        else:
            self.assertEqual(str(can_borrow_amt), '')
            self.assertEqual(str(last_pay_date), '')
            self.assertEqual(str(loan_percent), '')
            self.assertEqual(str(loan_rate), '')
            self.assertEqual(str(entity.productId), '')
            self.assertEqual(str(entity.productName), '')

    # 获取银行卡列表
    @file_data('test_data/test_user_bank_list.json')
    def test_bank_list(self, user_name, password, assert_info):
        bank_acco, bank_card_id, bank_no = self._restful_xjb.get_bank_card_list(user_name=str(user_name),
                                                                                login_password=str(password))
        entity = self._restful_xjb.entity.current_entity
        expected_card_list = self._db.get_cust_all_bank_cards(bank_mobile=str(user_name))
        expected_bank_no_list = self._db.get_bank_card_with_high_priority_bank_channel(bank_mobile=str(user_name))
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        self.assertEqual(len(bank_card_id), len(expected_card_list))
        if len(bank_card_id) > 0:
            for i in range(0, len(bank_card_id)):
                self.assertEqual(str(bank_acco[i]), str(expected_bank_no_list[i][0]['card_no']))
                self.assertEqual(str(bank_card_id[i]), str(expected_bank_no_list[i][0]['serial_id']))
                self.assertEqual(str(bank_no[i]), str(expected_bank_no_list[i][0]['bank_no']))

    # 质押借款申请
    @file_data('test_data/test_loan_apply.json')
    def test_loan_apply(self, user_name, password, product_id, loan_amt, loan_purpose, trade_password, assert_info):
        self._restful_xjb.loan_apply(user_name=str(user_name), login_password=str(password), loan_amt=str(loan_amt),
                                     loan_purpose=str(loan_purpose), trade_password=str(trade_password),
                                     product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertTrue(assert_info["returnMsg"] in entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if str(assert_info['returnCode']) == '000000':
            self.assertEqual(entity.body_returnResult, '')
            self.assertEqual(entity.body_title, '借款申请已受理！')
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            prod_nav = self._db.get_product_info(str(product_id))[0]['latest_nav']
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
            asset_in_transit = self._db.get_asset_in_transit(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))
            prod_loan = self._db.get_product_pledge_info(product_id=str(product_id))
            pledge_loan = self._db.get_cust_pledge_loan(mobile=str(user_name), product_id=str(product_id),
                                                        is_history='0')
            pledge_ratio = decimal.Decimal(prod_loan[0]['pledge_ratio'] / 100).quantize(decimal.Decimal('0.00'))

            order_no = trade_order[0]['ORDER_NO']
            # 两条记录，先借款冻结份额，然后充入现金宝
            trade_requests = self._db.get_trade_request_by_order_no(order_no=order_no)
            self.assertEqual(len(trade_requests), 2)
            self.assertEqual(trade_requests[0]['CUST_TYPE'], '1')
            self.assertEqual(trade_requests[0]['BRANCH_CODE'], '675')
            self.assertEqual(trade_requests[0]['ACCPT_MODE'], 'M')
            # 031 随心借 031004 质押借款冻结
            # 022 存入 022127 现金宝充值（质押借款存入）
            self.assertEqual(trade_requests[0]['APKIND'], '031')
            self.assertEqual(trade_requests[0]['SUB_APKIND'], '031004')
            self.assertEqual(trade_requests[0]['PROD_ID'], str(product_id))
            self.assertEqual(trade_requests[0]['PROD_TYPE'], 3)
            self.assertEqual(trade_requests[0]['TANO'], 'H9')
            self.assertEqual(trade_requests[0]['SHARE_TYPE'], 'A')
            pledge_quty = BusinessUtility().calculate_pledge_quty(loan_amt=str(loan_amt), pledge_ratio=pledge_ratio,
                                                                  prod_nav=prod_nav)
            self.assertEqual(trade_requests[0]['SUB_AMT'], pledge_quty)
            self.assertEqual(trade_requests[0]['APPLY_ST'], 'Y')
            self.assertEqual(trade_requests[0]['PAY_ST'], 'N')
            self.assertEqual(trade_requests[0]['RTTA_ST'], 'N')

            self.assertEqual(trade_requests[1]['CUST_TYPE'], '1')
            self.assertEqual(trade_requests[1]['BRANCH_CODE'], '675')
            self.assertEqual(trade_requests[1]['ACCPT_MODE'], 'M')
            self.assertEqual(trade_requests[1]['APKIND'], '022')
            self.assertEqual(trade_requests[1]['SUB_APKIND'], '022127')
            self.assertEqual(trade_requests[1]['PROD_ID'], 'ZX05#000730')
            self.assertEqual(trade_requests[1]['PROD_TYPE'], 0)
            self.assertEqual(trade_requests[1]['TANO'], 'ZX05')
            self.assertEqual(trade_requests[1]['SHARE_TYPE'], 'A')
            self.assertEqual(trade_requests[1]['SUB_AMT'],
                             decimal.Decimal(str(loan_amt)).quantize(decimal.Decimal('0.00')))
            self.assertEqual(trade_requests[1]['APPLY_ST'], 'Y')
            self.assertEqual(trade_requests[1]['PAY_ST'], 'Y')
            self.assertEqual(trade_requests[1]['RTTA_ST'], 'Y')

            # 031 随心借 031010 质押借款
            self.assertEqual(trade_order[0]['ACCPT_MODE'], 'M')
            self.assertEqual(trade_order[0]['BRANCH_CODE'], '675')
            self.assertEqual(trade_order[0]['FROM_PROD'], str(product_id))
            self.assertEqual(trade_order[0]['FROM_PROD_TYPE'], 3)
            self.assertEqual(trade_order[0]['TO_PROD_TYPE'], 0)
            self.assertEqual(trade_order[0]['TO_PROD'], 'ZX05#000730')
            self.assertEqual(trade_order[0]['AP_AMT'], decimal.Decimal(str(loan_amt)).quantize(decimal.Decimal('0.00')))
            self.assertEqual(trade_order[0]['SUCC_AMT'],
                             decimal.Decimal(str(loan_amt)).quantize(decimal.Decimal('0.00')))
            self.assertEqual(trade_order[0]['STATUS'], 'Y')
            self.assertEqual(trade_order[0]['ORDER_APKIND'], '031')
            self.assertEqual(trade_order[0]['ORDER_SUB_APKIND'], '031010')

            # 验证在途
            self.assertEqual(asset_in_transit[0]['PROD_ID'], str(product_id))
            self.assertEqual(asset_in_transit[0]['PROD_TYPE'], 3)
            self.assertEqual(asset_in_transit[0]['SHARE_TYPE'], 'A')
            self.assertEqual(asset_in_transit[0]['TANO'], 'H9')
            self.assertEqual(asset_in_transit[0]['ORDER_NO'], order_no)
            self.assertEqual(asset_in_transit[0]['APKIND'], '031')
            self.assertEqual(asset_in_transit[0]['SUB_APKIND'], '031004')

            # 验证质押记录
            self.assertEqual(pledge_loan[0]['ORDER_NO'], order_no)
            self.assertEqual(pledge_loan[0]['ACCPT_MODE'], 'M')
            self.assertEqual(pledge_loan[0]['PROD_TYPE'], 3)
            self.assertEqual(pledge_loan[0]['PROD_ID'], str(product_id))
            self.assertEqual(pledge_loan[0]['ACCEPT_CHANNEL'], 'H9')
            self.assertEqual(pledge_loan[0]['PLEDGE_QUTY'], pledge_quty)
            self.assertEqual(pledge_loan[0]['PLEDGE_AMT'],
                             decimal.Decimal(str(loan_amt)).quantize(decimal.Decimal('0.00')))
            self.assertEqual(pledge_loan[0]['PLEDGE_RATE'],
                             decimal.Decimal(pledge_ratio).quantize(decimal.Decimal('0.0000')))
            self.assertEqual(pledge_loan[0]['NAV'], decimal.Decimal(str(prod_nav)).quantize(decimal.Decimal('0.0000')))
            self.assertEqual(pledge_loan[0]['INTEREST_RATE'],
                             decimal.Decimal(str(prod_loan[0]['borrow_rate'] / 100)).quantize(
                                 decimal.Decimal('0.0000')))
            self.assertEqual(pledge_loan[0]['RISK_STATUS'], 'NORMAL')

            # 验证现金宝收支明细
            self.assertEqual(vacco_detail[0]['ORDER_NO'], order_no)
            self.assertEqual(vacco_detail[0]['BRANCH_CODE'], '675')
            self.assertEqual(vacco_detail[0]['SHARE_TYPE'], 'A')
            self.assertEqual(vacco_detail[0]['ACCPT_MODE'], 'M')
            self.assertEqual(vacco_detail[0]['APKIND'], '022')
            self.assertEqual(vacco_detail[0]['SUB_APKIND'], '022127')
            self.assertEqual(vacco_detail[0]['SUB_AMT'],
                             decimal.Decimal(str(loan_amt)).quantize(decimal.Decimal('0.00')))

            # 验证现金宝动态份额
            self.assertEqual(trade_quty_chg[0]['ORDER_NO'], order_no)
            self.assertEqual(trade_quty_chg[0]['PROD_ID'], 'ZX05#000730')
            self.assertEqual(trade_quty_chg[0]['PROD_TYPE'], 0)
            self.assertEqual(trade_quty_chg[0]['APKIND'], '022')
            self.assertEqual(trade_quty_chg[0]['SUB_APKIND'], '022127')
            self.assertEqual(trade_quty_chg[0]['SHARE_TYPE'], 'A')
            self.assertEqual(trade_quty_chg[0]['BRANCH_CODE'], '675')
            self.assertEqual(trade_quty_chg[0]['CHG_QUTY'],
                             decimal.Decimal(str(loan_amt)).quantize(decimal.Decimal('0.00')))

    # 质押产品列表
    @file_data('test_data/test_loan_product_list.json')
    def test_loan_product_list(self, user_name, password, assert_info):
        self._restful_xjb.loan_product_list(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertTrue(assert_info["returnMsg"] in entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        prod_quties = self._db.get_cust_prod_quty_by_product_id(mobile=str(user_name))
        data_list = entity.body_dataList
        for prod in prod_quties:
            pledge_prod_info = self._db.get_product_pledge_info(product_id=str(prod['PROD_ID']))
            if len(pledge_prod_info) == 0:
                prod_quties.remove(prod)

        for i in range(0, len(prod_quties)):
            pledge_prod_info = self._db.get_product_pledge_info(product_id=str(prod_quties[i]['PROD_ID']))
            product_info = self._db.get_product_info(product_id=str(prod_quties[i]['PROD_ID']))
            pledge_ratio = pledge_prod_info[0]['pledge_ratio']
            borrow_rate = decimal.Decimal(pledge_prod_info[0]['borrow_rate']).quantize(decimal.Decimal('0.00'))
            prod_pledge_loan = self._db.get_cust_pledge_loan(mobile=str(user_name),
                                                             product_id=str(prod_quties[i]['PROD_ID']),
                                                             is_history=str('0'))
            force_redeem_reimburse = str(pledge_prod_info[0]['forced_redeem_reimbursement'])[0:8]
            max_borrow_days = str(pledge_prod_info[0]['max_borrow_day'])
            if len(prod_pledge_loan) == 0:
                borrow_amt = prod_quties[i]['BALANCE'] * pledge_ratio / 100
            else:
                borrow_amt = prod_quties[i]['BALANCE'] * pledge_ratio / 100 - prod_pledge_loan[0]['PLEDGE_AMT']
            share_carry_date = str(product_info[0]['share_next_carry_date'])
            expected_end_repay_date = BusinessUtility().calculate_pledge_final_repay_date(
                prod_carry_date=share_carry_date, pledge_force_repay_date=force_redeem_reimburse,
                repay_days=max_borrow_days)
            self.assertEqual(str(data_list[i]['productId']), str(prod_quties[i]['PROD_ID']))
            self.assertEqual(str(data_list[i]['lastPayDate']).split(' ')[0].replace('-', ''),
                             str(expected_end_repay_date))
            self.assertEqual(str(data_list[i]['canBorrowAmt']),
                             str(decimal.Decimal(borrow_amt).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(data_list[i]['loanPrecent']),
                             str(decimal.Decimal(pledge_ratio).quantize(decimal.Decimal('0.00'))) + '%')
            self.assertEqual(str(data_list[i]['loanRate']), str(borrow_rate) + '%')
            self.assertEqual(str(data_list[i]['productName']), str(product_info[0]['product_short_name']))

    # 获取协议
    @file_data('test_data/test_get_agreement.json')
    def test_get_agreement(self, user_name, password, type, assert_info):
        self._restful_xjb.get_agreenment(user_name=str(user_name), password=str(password), type=str(type))
        entity = self._restful_xjb.entity.current_entity
        self.assertTrue(assert_info["returnMsg"] in entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        channel_agreement = entity.channelAgreements
        if str(type) == '1':
            self.assertTrue('华信现金宝员工理财服务协议' in channel_agreement[0]['agreementTitle'])
        elif str(type) == '0':
            self.assertTrue('华信现金宝定期自动转入服务协议' in channel_agreement[0]['agreementTitle'])
        else:
            self.assertTrue('华信现金宝定期自动转入服务协议' in channel_agreement[0]['agreementTitle'])

    # 获取下一个工资理财扣款日
    @file_data('test_data/test_get_next_pay_day.json')
    def test_get_next_pay_day(self, user_name, password, pay_day, assert_info):
        expected_next_pay_day = BusinessUtility().get_next_pay_date(day=str(pay_day), date_format='%Y%m%d')
        while self._db.determine_if_work_day(expected_next_pay_day) is False:
            pay_day = int(pay_day) + 1
            expected_next_pay_day = BusinessUtility().get_next_pay_date(day=str(pay_day), date_format='%Y%m%d')

        expected_next_pay_day = BusinessUtility().get_next_pay_date(day=str(pay_day), date_format='%Y-%m-%d')
        self._restful_xjb.get_next_pay_day(user_name=str(user_name), password=str(password),
                                           pay_day='M#' + str(pay_day))
        entity = self._restful_xjb.entity.current_entity
        self.assertTrue(assert_info["returnMsg"] in entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        info = entity.info
        self.assertEqual(str(info), expected_next_pay_day)

    # 工资理财-创建工资理财计划
    @file_data('test_data/test_make_salary_fin_plan.json')
    def test_make_salary_fin_plan(self, user_name, password, trade_password, purchase_amt, purchase_day, comment,
                                  card_id, assert_info):
        self._restful_xjb.make_salary_fin_plan(user_name=str(user_name), password=str(password),
                                               salary_fin_plan_id='', trade_password=str(trade_password),
                                               purchase_amt=str(purchase_amt), purchase_date=str(purchase_day),
                                               comment=str(comment), card_id=str(card_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertTrue(assert_info["returnMsg"] in entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        info = entity.info
        return_result = entity.returnResult
        title = entity.title
        if assert_info["returnCode"] == '000000':
            card = self._db.get_bank_card_by_serial_id(serial_id=str(card_id))
            pay_day = str(purchase_day).split('#')[1]
            expected_next_pay_day = BusinessUtility().get_next_pay_date(day=str(pay_day), date_format='%Y%m%d')
            plan_expected_next_pay_day = expected_next_pay_day

            expected_next_pay_day = self._db.judge_is_work_date(day=str(expected_next_pay_day))[0]['WORK_DATE']
            next_pay_day = datetime.datetime.strftime(datetime.datetime.strptime(expected_next_pay_day, '%Y%m%d'),
                                                      '%Y-%m-%d')
            plan = self._db.get_fund_make_invest_plan_validate(mobile=str(user_name))
            self.assertEqual(str(title), '设置成功！')
            self.assertEqual(str(return_result), '')

            today = Utility.DateUtil().getToday()
            tomorrow = today + datetime.timedelta(days=1)
            if next_pay_day == str(tomorrow):
                next_pay_day = '明天'
            self.assertTrue(next_pay_day in info)
            self.assertEqual(str(plan[0]['START_TIME']), str(expected_next_pay_day))
            self.assertEqual(str(plan[0]['PERIOD']), '1#M')
            self.assertEqual(str(plan[0]['DAY']), str(purchase_day))
            self.assertEqual(str(plan[0]['PLAN_NEXT_PAYMENT_DAY']), str(plan_expected_next_pay_day))
            self.assertEqual(str(plan[0]['NEXT_PAYMENT_DAY']), str(expected_next_pay_day))
            self.assertEqual(str(plan[0]['SIGN_TIME']), str(datetime.datetime.today().strftime('%Y%m%d')))
            self.assertEqual(plan[0]['AP_AMT'],
                             decimal.Decimal(str(purchase_amt)).quantize(decimal.Decimal('0.00')))
            self.assertEqual(str(plan[0]['INVESTED_PERIODS']), '0')
            self.assertEqual(plan[0]['TOTAL_AMT'], decimal.Decimal('0.00'))
            self.assertEqual(str(plan[0]['PURCHASE_PAYMENT_TYPE']), '1')
            self.assertEqual(str(plan[0]['STATUS']), 'N')
            self.assertEqual(str(plan[0]['NEXT_INVEST_ST']), 'N')
            self.assertEqual(str(plan[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(plan[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(plan[0]['CUST_TYPE']), '1')
            self.assertEqual(str(plan[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(plan[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(plan[0]['PROD_TYPE']), '0')
            self.assertEqual(str(plan[0]['BANK_ACCO']), str(card[0]['card_no']))
            self.assertEqual(str(plan[0]['INVEST_TYPE']), '2')
            self.assertEqual(str(plan[0]['IS_DELETE']), '0')
            self.assertEqual(str(plan[0]['REMARK']), str(comment))
            self.assertEqual(plan[0]['NEXT_INVEST_AMT'],
                             decimal.Decimal(str(purchase_amt)).quantize(decimal.Decimal('0.00')))

    # 工资理财-修改工资理财计划
    @file_data('test_data/test_modify_salary_fin_plan.json')
    def test_modify_salary_fin_plan(self, user_name, password, trade_password, purchase_amt, purchase_day,
                                    comment, card_id, salary_fin_plan_id, assert_info):
        if salary_fin_plan_id == str('None'):
            salary_plan = self._db.get_fund_make_invest_plan_validate(mobile=str(user_name))
            salary_fin_plan_id = salary_plan[0]['PROTOCOL_NO']
        self._restful_xjb.make_salary_fin_plan(user_name=str(user_name), password=str(password),
                                               salary_fin_plan_id=str(salary_fin_plan_id),
                                               trade_password=str(trade_password),
                                               purchase_amt=str(purchase_amt),
                                               purchase_date=str(purchase_day), comment=str(comment),
                                               card_id=card_id)

        entity = self._restful_xjb.entity.current_entity
        self.assertTrue(assert_info["returnMsg"] in entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        info = entity.info
        return_result = entity.returnResult
        title = entity.title
        if assert_info["returnCode"] == '000000':
            card = self._db.get_bank_card_by_serial_id(serial_id=str(card_id))
            pay_day = str(purchase_day).split('#')[1]
            expected_next_pay_day = BusinessUtility().get_next_pay_date(day=str(pay_day), date_format='%Y%m%d')
            plan_expected_next_pay_day = expected_next_pay_day

            expected_next_pay_day = self._db.judge_is_work_date(day=str(expected_next_pay_day))[0]['WORK_DATE']
            today = Utility.DateUtil().getToday()
            tomorrow = today + datetime.timedelta(days=1)
            next_pay_day = datetime.datetime.strftime(
                datetime.datetime.strptime(expected_next_pay_day, '%Y%m%d'), '%Y-%m-%d')
            if next_pay_day == str(tomorrow):
                next_pay_day = '明天'

            plan = self._db.get_fund_make_invest_plan_validate(mobile=str(user_name))
            self.assertEqual(str(title), '设置成功！')
            self.assertEqual(str(return_result), '')

            self.assertTrue(next_pay_day in info)
            # self.assertEqual(str(plan[0]['START_TIME']), str(expected_next_pay_day))
            self.assertEqual(str(plan[0]['PERIOD']), '1#M')
            self.assertEqual(str(plan[0]['DAY']), str(purchase_day))
            self.assertEqual(str(plan[0]['PLAN_NEXT_PAYMENT_DAY']), str(plan_expected_next_pay_day))
            self.assertEqual(str(plan[0]['NEXT_PAYMENT_DAY']), str(expected_next_pay_day))
            self.assertEqual(plan[0]['AP_AMT'],
                             decimal.Decimal(str(purchase_amt)).quantize(decimal.Decimal('0.00')))
            # self.assertEqual(str(plan[0]['INVESTED_PERIODS']), '1') 累计已投期数会叠加
            # self.assertEqual(plan[0]['TOTAL_AMT'], decimal.Decimal('0.00'))
            self.assertEqual(str(plan[0]['PURCHASE_PAYMENT_TYPE']), '1')
            self.assertEqual(str(plan[0]['STATUS']), 'N')
            self.assertEqual(str(plan[0]['NEXT_INVEST_ST']), 'N')
            self.assertEqual(str(plan[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(plan[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(plan[0]['CUST_TYPE']), '1')
            self.assertEqual(str(plan[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(plan[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(plan[0]['PROD_TYPE']), '0')
            self.assertEqual(str(plan[0]['BANK_ACCO']), str(card[0]['card_no']))
            self.assertEqual(str(plan[0]['INVEST_TYPE']), '2')
            self.assertEqual(str(plan[0]['IS_DELETE']), '0')
            self.assertEqual(str(plan[0]['REMARK']), str(comment))
            self.assertEqual(plan[0]['NEXT_INVEST_AMT'],
                             decimal.Decimal(str(purchase_amt)).quantize(decimal.Decimal('0.00')))

    # 终止、启用、暂停工资理财计划
    # status 0-终止 1-暂停 2-启用
    @file_data('test_data/test_update_salary_plan.json')
    def test_update_salary_plan(self, user_name, password, trade_password, salary_fin_plan_id, status, assert_info):
        plan = self._db.get_fund_make_invest_plan_validate(mobile=str(user_name))
        if str(salary_fin_plan_id) == 'None':
            salary_fin_plan_id = plan[0]['PROTOCOL_NO']
        if str(status) == '0' or str(status) == '1':
            self._db.update_fund_invest_plan_status(mobile=str(user_name), status=str('N'))
        elif str(status) == '2':
            self._db.update_fund_invest_plan_status(mobile=str(user_name), status=str('P'))
        self._restful_xjb.update_salary_fin_plan(user_name=str(user_name), password=str(password),
                                                 trade_password=str(trade_password),
                                                 salary_fin_plan_id=str(salary_fin_plan_id), status=str(status))
        entity = self._restful_xjb.entity.current_entity
        self.assertTrue(assert_info["returnMsg"] in entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        info = entity.info
        return_result = entity.returnResult
        title = entity.title

        if assert_info["returnCode"] == '000000':
            self.assertEqual(str(title), '设置成功！')
            self.assertEqual(str(return_result), '')
            self.assertEqual(str(info), '')

            plan = self._db.get_fund_make_invest_plan_validate(mobile=str(user_name))
            if str(status) == '0':
                self.assertEqual(str(plan[0]['STATUS']), 'E')
            elif str(status) == '1':
                self.assertEqual(str(plan[0]['STATUS']), 'P')
            elif str(status) == '2':
                self.assertEqual(str(plan[0]['STATUS']), 'N')

    # 查询工资理财（历史）计划 is_history = 0: 非历史， =1 历史
    @file_data('test_data/test_get_salary_fin_plan.json')
    def test_get_salary_fin_plan(self, user_name, password, is_history, assert_info):
        self._restful_xjb.get_salary_fin_plan(user_name=str(user_name), password=str(password),
                                              is_history=str(is_history))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        plan = self._db.get_fund_make_invest_plan_validate(mobile=str(user_name))
        data_list = entity.body_dataList

        new_list = []
        if str(is_history) == '0':
            for p in plan:
                if p['STATUS'] != 'E':
                    new_list.append(p)
        elif str(is_history) == '1':
            for p in plan:
                if p['STATUS'] == 'E':
                    new_list.append(p)

        plan = new_list
        self.assertEqual(len(data_list), len(plan))
        # 按PROTOCOL_NO升序排列
        plan = sorted(plan, key=lambda p: p['PROTOCOL_NO'])
        data_list = sorted(data_list, key=lambda p: p['salaryFinPlanId'])
        for i in range(0, len(data_list)):
            self.assertEqual(str(data_list[i]['bankCardId']), plan[i]['BANK_SERIAL_ID'])
            self.assertEqual(str(data_list[i]['cardTailNo']), str(plan[i]['BANK_ACCO'])[-4:])
            self.assertEqual(str(data_list[i]['cardType']), '0')
            next_pay_day = datetime.datetime.strptime(str(plan[i]['NEXT_PAYMENT_DAY']), '%Y%m%d').strftime(
                '%Y-%m-%d')
            self.assertEqual(str(data_list[i]['dfInfo']), '')
            self.assertEqual(str(data_list[i]['dfStatus']), '')
            self.assertEqual(str(data_list[i]['employeeId']), '')
            self.assertEqual(str(data_list[i]['isDf']), '0')
            self.assertEqual(str(data_list[i]['isNeedActiveSalaryCard']), '')
            self.assertEqual(str(data_list[i]['isNeedSignProtocol']), '')

            self.assertEqual(str(data_list[i]['planName']), '工资理财')
            self.assertEqual(str(data_list[i]['purchaseAmtInfo']).replace(',', ''),
                             str(plan[i]['AP_AMT']) + '元')
            self.assertEqual(str(data_list[i]['salaryFinPlanId']), str(plan[i]['PROTOCOL_NO']))
            self.assertEqual(str(data_list[i]['theNewestPurchaseInfo']).replace('-', ''),
                             str(plan[i]['NEXT_PAYMENT_DAY']))
            self.assertEqual(str(data_list[i]['totalPurchaseAmt']), str(format(plan[i]['TOTAL_AMT'], ',')))
            if plan[i]['STATUS'] == 'N':
                self.assertEqual(str(data_list[i]['status']), '2')
                self.assertEqual(str(data_list[i]['detailStatusInfo']), '正常执行中')
                self.assertEqual(str(data_list[i]['nextPurchaseDate']).replace('-', ''),
                                 str(plan[i]['NEXT_PAYMENT_DAY']))
                if datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1),
                                              '%Y%m%d') != str(plan[i]['NEXT_PAYMENT_DAY']):
                    self.assertEqual(str(data_list[i]['nextPurchaseInfo']).replace('-', ''),
                                     str(plan[i]['NEXT_PAYMENT_DAY']))
                else:
                    self.assertEqual(str(data_list[i]['nextPurchaseInfo']), '明天转入')
                self.assertTrue(next_pay_day in str(data_list[i]['info']))
            elif plan[i]['STATUS'] == 'E':
                self.assertEqual(str(data_list[i]['status']), '0')
                self.assertEqual(str(data_list[i]['info']), '')
                self.assertEqual(str(data_list[i]['detailStatusInfo']), '已终止')
                self.assertEqual(str(data_list[i]['nextPurchaseDate']), '已终止')
                self.assertEqual(str(data_list[i]['nextPurchaseInfo']), '已终止')
            elif plan[i]['STATUS'] == 'P':
                self.assertEqual(str(data_list[i]['status']), '1')
                self.assertEqual(str(data_list[i]['detailStatusInfo']), '已暂停')
                self.assertEqual(str(data_list[i]['nextPurchaseDate']), '已暂停')
                self.assertEqual(str(data_list[i]['nextPurchaseInfo']), '已暂停')
                self.assertEqual(str(data_list[i]['info']), '')

    # 工资代发-确认协议
    @file_data('test_data/test_confirm_salary_fin_plan.json')
    def test_confirm_salary_fin_plan(self, user_name, password, employee_id, assert_info):
        self._restful_xjb.confirm_salary_fin_plan(user_name=str(user_name), password=str(password),
                                                  employee_id=str(employee_id))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if assert_info["returnCode"] == '000000':
            employee_info = self._db.get_employee_info(employee_id=str(employee_id))
            self.assertEqual(entity.info, "开通成功")
            self.assertEqual(int(employee_info[0]['id']), int(employee_id))
            self.assertEqual(str(employee_info[0]['protocol_status']), "1", "确认绑定")
            self.assertEqual(str(employee_info[0]['mobile']), str(user_name))

    # 会员等级—查询指定等级权益
    @file_data('test_data/test_member_level_right_list.json')
    def test_get_member_level_right_list(self, user_name, password, assert_info):
        self._restful_xjb.get_member_level_right_list(user_name=str(user_name), password=str(password)),

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if assert_info["returnCode"] == '000000':
            my_member_level = self._db.get_my_member_role(mobile=str(user_name))
            member_level = self._db.get_member_role()
            interests = self._db.get_member_level_right_list_db()
            if my_member_level == 'NOVICE':
                for i in range(0, len(member_level)):
                    self.assertEqual(str(member_level[i]['CODE']), entity.body_dataList[i]['memberLevel'])
                    if i == 0:
                        for j in range(0, len(interests[i])):
                            self.assertEqual(str(interests[i][j][0]['DETAIL_ICON_URL']),
                                             str(entity.body_dataList[i]['memberRightsList'][j]['bigLogoUrl']))
                            self.assertEqual(str(interests[i][j][0]['BRIGHT_ICON_URL']),
                                             str(entity.body_dataList[i]['memberRightsList'][j]['logoUrl']))
                            self.assertEqual(str(interests[i][j][0]['CODE']),
                                             str(entity.body_dataList[i]['memberRightsList'][j]['rightsId']))
                            self.assertEqual(str(interests[i][j][0]['NAME']),
                                             str(entity.body_dataList[i]['memberRightsList'][j]['rightsName']))
                            self.assertEqual(str(interests[i][j][0]['REMARK']),
                                             str(entity.body_dataList[i]['memberRightsList'][j]['rightsDesc']))
                    else:
                        for j in range(0, len(interests[i])):
                            self.assertEqual(str(interests[i][j][0]['DETAIL_ICON_URL']),
                                             str(entity.body_dataList[i]['memberRightsList'][j]['bigLogoUrl']))
                            self.assertEqual(str(interests[i][j][0]['DIM_ICON_URL']),
                                             str(entity.body_dataList[i]['memberRightsList'][j]['logoUrl']))
                            self.assertEqual(str(interests[i][j][0]['CODE']),
                                             str(entity.body_dataList[i]['memberRightsList'][j]['rightsId']))
                            self.assertEqual(str(interests[i][j][0]['NAME']),
                                             str(entity.body_dataList[i]['memberRightsList'][j]['rightsName']))
                            self.assertEqual(str(interests[i][j][0]['REMARK']),
                                             str(entity.body_dataList[i]['memberRightsList'][j]['rightsDesc']))

    # 会员等级-查询指定权益详情
    @file_data('test_data/test_member_level_right_detail.json')
    def test_get_member_level_right_detail(self, user_name, password, code, assert_info):
        self._restful_xjb.get_member_level_right_detail(user_name=str(user_name), password=str(password),
                                                        rights_id=str(code))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if assert_info["returnCode"] == '000000':
            member_interests = self._db.get_member_level_right_detail_db(code=str(code))
            self.assertEqual(str(member_interests[0]['DETAIL_ICON_URL']), str(entity.body['detail']['bigLogoUrl']))
            self.assertEqual(str(member_interests[0]['BRIGHT_ICON_URL']), str(entity.body['detail']['logoUrl']))
            self.assertEqual(str(member_interests[0]['REMARK']), str(entity.body['detail']['rightsDesc']))
            self.assertEqual(str(member_interests[0]['NAME']), str(entity.body['detail']['rightsName']))

    # 会员等级-查询特殊权益
    @file_data('test_data/test_get_member_level_right_category_list.json')
    def test_get_member_level_right_category_list(self, user_name, password, assert_info):
        self._restful_xjb.get_member_level_right_category_list(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if assert_info["returnCode"] == '000000':
            member_type = self._db.get_member_level_category_list_db()
            special_member_interests = self._db.get_member_level_right_category_list_db()
            for i in range(0, len(special_member_interests)):
                self.assertEqual(str(member_type[i]['CODE']), entity.body_dataList[i]['categoryId'])
                self.assertEqual(str(member_type[i]['NAME']), entity.body_dataList[i]['categoryName'])
                for j in range(0, len(special_member_interests[i])):
                    self.assertEqual(str(special_member_interests[i][j][0]['DETAIL_ICON_URL']),
                                     str(entity.body_dataList[i]['memberRightsList'][j]['bigLogoUrl']))
                    self.assertEqual(str(special_member_interests[i][j][0]['REMARK']),
                                     str(entity.body_dataList[i]['memberRightsList'][j]['rightsDesc']))
                    self.assertEqual(str(special_member_interests[i][j][0]['CODE']),
                                     str(entity.body_dataList[i]['memberRightsList'][j]['rightsId']))
                    self.assertEqual(str(special_member_interests[i][j][0]['NAME']),
                                     str(entity.body_dataList[i]['memberRightsList'][j]['rightsName']))

    # 用户-保存会员等级banner浏览结果
    @file_data('test_data/test_view_member_level_banner.json')
    def test_view_member_level_banner(self, user_name, password, assert_info):
        self._restful_xjb.get_view_member_level_banner(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 用户-行为记录（提醒我）
    @file_data('test_data/test_save_behavior.json')
    def test_save_behavior(self, user_name, password, product_type, sub_product_type, assert_info):
        self._restful_xjb.get_save_behavior(user_name=str(user_name), password=str(password),
                                            product_type=str(product_type), sub_product_type=str(sub_product_type))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if assert_info["returnCode"] == '000000':
            cust_behavior = self._db.get_sava_behavior_db(mobile=str(user_name))
            self.assertEqual(str(cust_behavior[0]['product_type']), str(product_type))
            self.assertEqual(str(cust_behavior[0]['sub_product_type']), str(sub_product_type))

    # 工资代发-终止协议
    @file_data('test_data/test_stop_salary_fin_plan.json')
    def test_stop_salary_fin_plan(self, user_name, password, employee_id, trade_password, assert_info):
        self._restful_xjb.stop_salary_fin_plan(user_name=str(user_name), password=str(password),
                                               employee_id=str(employee_id), trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertIn(assert_info["returnMsg"], entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if assert_info["returnCode"] == '000000':
            employee_info = self._db.get_employee_info(employee_id=str(employee_id))
            self.assertEqual(entity.info, "开通成功")
            self.assertEqual(int(employee_info[0]['id']), int(employee_id))
            self.assertEqual(str(employee_info[0]['protocol_status']), "3", "终止协议")
            self.assertEqual(str(employee_info[0]['mobile']), str(user_name))
            self._db.update_employee_protocol_status(protocol_status='1', employee_id=str(employee_id))
            print 'update protocol_status 1'

    # banner
    @file_data('test_data/test_marketing_banner.json')
    def test_marketing_banner(self, user_name, password, position, assert_info):
        self._restful_xjb.marketing_banner(user_name=str(user_name), password=str(password), position=str(position))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # main page alert
    @file_data('test_data/test_main_page_alert.json')
    def test_main_page_alert(self, user_name, password, visit_type, assert_info):
        self._restful_xjb.marketing_main_page_alert(user_name=str(user_name), password=str(password),
                                                    visit_type=str(visit_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 热门产品列表(v3.0.0)
    @file_data('test_data/test_get_hot_product_list.json')
    def test_hot_product_list(self, user_name, password, assert_info):
        self._restful_xjb.get_hot_product_list(user_name=str(user_name), password=str(password))
        dqb_list = self._db.get_hot_on_sale_product_list(product_type='1')
        vip_list = self._db.get_hot_on_sale_product_list(product_type='3')

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        actual_dqb_list = entity.dataList[0]['productList']
        actual_vip_list = entity.dataList[1]['productList']

        self.assertEqual(len(actual_dqb_list), len(dqb_list))
        self.assertEqual(len(actual_vip_list), len(vip_list))

        for i in range(0, len(actual_dqb_list)):
            self.assertTrue(str(actual_dqb_list[i]['productId']) in str(dqb_list))
            self.assertEqual(str(actual_dqb_list[i]['productType']), '1')
        for i in range(0, len(actual_vip_list)):
            self.assertTrue(str(actual_vip_list[0]['productId']) in str(vip_list))
            self.assertEqual(str(actual_vip_list[i]['productType']), '3')

    # 工资代发-获取工资卡信息
    @file_data('test_data/test_get_salary_card_info.json')
    def test_get_salary_card_info(self, user_name, password, employee_id, assert_info):
        self._restful_xjb.get_salary_card_info(user_name=str(user_name), password=str(password),
                                               employee_id=str(employee_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        cust_joint_card_list = entity.body_custJointCard
        if assert_info["returnCode"] == '000000':
            employee_info = self._db.get_employee_info(employee_id=str(employee_id))
            self.assertEqual(str(cust_joint_card_list['employeeId']), str(employee_info[0]['id']))
            self.assertEqual(str(cust_joint_card_list['bankAcco']), str(employee_info[0]['card_no']))
            self.assertEqual(str(cust_joint_card_list['bankGroupName']), str(employee_info[0]['bank_name']))
            self.assertEqual(str(cust_joint_card_list['canDelete']), '1')
            self.assertEqual(str(cust_joint_card_list['canFastWithdraw']), '0')
            self.assertEqual(str(cust_joint_card_list['canRecharge']), '0')
            self.assertEqual(str(cust_joint_card_list['canWithdraw']), '0')
            self.assertEqual(str(cust_joint_card_list['cardStatus']), '2')
            self.assertEqual(str(cust_joint_card_list['certType']), str(employee_info[0]['cert_type']))
            self.assertEqual(str(cust_joint_card_list['isJointCard']), '0')
            self.assertEqual(str(cust_joint_card_list['isNeedActiveSalaryCard']), '1')
            self.assertEqual(str(cust_joint_card_list['name']), str(employee_info[0]['name']))

    # 功能
    @file_data('test_data/test_get_function_list.json')
    def test_get_function_list(self, user_name, password, function_type, assert_info):
        self._restful_xjb.get_function_list(user_name=str(user_name), password=str(password),
                                            function_type=str(function_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        data_list = sorted(entity.body_dataList, key=lambda p: p['functionId'])
        function_list = sorted(self._db.get_function_list(function_type=str(function_type)), key=lambda p: p['id'])
        if assert_info["returnCode"] == '000000':
            for i in range(0, len(data_list)):
                self.assertEqual(str(data_list[i]['functionDesc']), str(function_list[i]['desc']))
                self.assertEqual(str(data_list[i]['functionId']), str(function_list[i]['id']))
                self.assertEqual(str(data_list[i]['functionLink']), str(function_list[i]['link']))
                self.assertEqual(str(data_list[i]['functionName']), str(function_list[i]['name']))
                self.assertEqual(str(data_list[i]['functionType']), str(function_list[i]['function_type']))
                self.assertEqual(str(data_list[i]['logoUrl']), str(function_list[i]['logo_url']))

    # 首页-产品营销信息
    @file_data('test_data/test_get_product_marketing_info.json')
    def test_get_product_marketing_info(self, user_name, password, assert_info):
        self._restful_xjb.get_product_marketing_info(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 首页-资讯
    @file_data('test_data/test_get_doc_list.json')
    def test_get_doc_list(self, user_name, password, doc_type, position, page_no, page_size, assert_info):
        self._restful_xjb.get_doc_list(user_name=str(user_name), password=str(password), doc_type=str(doc_type),
                                       position=str(position), page_no=str(page_no), page_size=str(page_size))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 搜索所有产品（定期/高端/基金）
    @file_data('test_data/test_search_all_product.json')
    def test_search_all_product(self, user_name, password, keyword, assert_info):
        self._restful_xjb.search_all_product(user_name=str(user_name), password=str(password),
                                             keyword=str(keyword))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])

        dqb_product_info, dqb1_product_info, vip_product_info, vip1_product_info, fund_product_info, fund1_product_info \
            = self._db.search_all_fin_product(keyword=str(keyword))

        data_list = entity.body_dataList
        for index in range(0, len(data_list)):
            db_vip_len = len(vip_product_info) or len(vip1_product_info)
            if str(data_list[index]['listTitle']) == '高端理财':
                vip_list = data_list[index]['list']
                if db_vip_len > 5:
                    db_vip_len = 5
                self.assertEqual(str(db_vip_len), str(len(vip_list)))
                if len(data_list) != 1:
                    for i in range(index, len(vip_list)):
                        self.assertEqual(str(vip_product_info[i]['productid']), vip_list[i]['productId'])
                        self.assertEqual(str(vip_product_info[i]['product_short_name']),
                                         entity.body_dataList[index]['list'][i]['productTitle'])
                        self.assertEqual(str(vip_product_info[i]['product_type']),
                                         entity.body_dataList[index]['list'][i]['productType'])
                elif len(data_list) == 1:
                    for b in range(index, len(vip_list)):
                        self.assertEqual(str(vip1_product_info[b]['productid']), vip_list[b]['productId'])
                        self.assertEqual(str(vip1_product_info[b]['product_short_name']),
                                         entity.body_dataList[index]['list'][b]['productTitle'])
                        self.assertEqual(str(vip1_product_info[b]['product_type']),
                                         entity.body_dataList[index]['list'][b]['productType'])

            db_dqb_len = len(dqb_product_info) or len(dqb1_product_info)
            if str(data_list[index]['listTitle']) == '定活宝':
                dqb_list = data_list[index]['list']
                if db_dqb_len > 5:
                    db_dqb_len = 5
                self.assertEqual(str(db_dqb_len), str(len(dqb_list)))
                if len(data_list) != 1:
                    for j in range(0, len(dqb_list)):
                        self.assertEqual(str(dqb_product_info[j]['productid']),
                                         entity.body_dataList[index]['list'][j]['productId'])
                        self.assertEqual(str(dqb_product_info[j]['product_short_name']),
                                         entity.body_dataList[index]['list'][j]['productTitle'])
                        self.assertEqual(str(dqb_product_info[j]['product_type']),
                                         entity.body_dataList[index]['list'][j]['productType'])
                elif len(data_list) == 1:
                    for a in range(0, len(dqb_list)):
                        self.assertEqual(str(dqb1_product_info[a]['productid']),
                                         entity.body_dataList[index]['list'][a]['productId'])
                        self.assertEqual(str(dqb1_product_info[a]['product_short_name']),
                                         entity.body_dataList[index]['list'][a]['productTitle'])
                        self.assertEqual(str(dqb1_product_info[a]['product_type']),
                                         entity.body_dataList[index]['list'][a]['productType'])

            db_fund_len = len(fund_product_info) or len(fund1_product_info)
            if str(data_list[index]['listTitle']) == '基金':
                fund_list = data_list[index]['list']
                if db_fund_len > 5:
                    db_fund_len = 5
                self.assertEqual(str(db_fund_len), str(len(fund_list)))
                if len(data_list) != 1:
                    for m in range(0, len(fund_list)):
                        self.assertEqual(str(fund_product_info[m]['productid']),
                                         str(data_list[index]['list'][m]['productId']))
                        self.assertEqual(str(fund_product_info[m]['product_short_name']) +
                                         str(fund_product_info[m]['productid']).split('#')[1],
                                         str(data_list[index]['list'][m]['productTitle']))
                        self.assertEqual(str(fund_product_info[m]['product_type']),
                                         str(data_list[index]['list'][m]['productType']))
                elif len(data_list) == 1:
                    for c in range(0, len(fund_list)):
                        self.assertEqual(str(fund1_product_info[c]['productid']),
                                         str(data_list[index]['list'][c]['productId']))
                        self.assertEqual(str(fund1_product_info[c]['product_short_name']) +
                                         str(fund_product_info[c]['productid']).split('#')[1],
                                         str(data_list[index]['list'][c]['productTitle']))
                        self.assertEqual(str(fund1_product_info[c]['product_type']),
                                         str(data_list[index]['list'][c]['productType']))

    # 基金-基金定投计划详情
    @file_data('test_data/test_fund_invest_plan_detail.json')
    def test_fund_invest_plan_detail(self, user_name, password, invest_plan_id, assert_info):
        self._restful_xjb.get_fund_invest_plan_detail(user_name=str(user_name), password=str(password),
                                                      invest_plan_id=str(invest_plan_id))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if entity.returnCode == '000000':
            invest_plan_detail = self._db.get_fund_invest_plan_detail_db(invest_plan_id=str(invest_plan_id))
            fund_proinfo = self._db.get_fund_detail_db(invest_plan_id=str(invest_plan_id))
            self.assertEqual(str(invest_plan_detail[0]['AP_AMT']), str(entity.body_detail['eachInvestAmt']))
            self.assertEqual(str(invest_plan_detail[0]['PROD_ID']), str(entity.body_detail['fundId']))
            self.assertEqual(str(str(invest_plan_detail[0]['INVESTED_PERIODS']) + '期'),
                             str(entity.body_detail['investCountInfo']))
            self.assertEqual(str(invest_plan_detail[0]['PROTOCOL_NO']), str(entity.body_detail['investPlanId']))
            self.assertEqual(str(invest_plan_detail[0]['PERIOD']), str(entity.body_detail['payCycle']))
            self.assertEqual(str(invest_plan_detail[0]['DAY']), str(entity.body_detail['payDay']))
            self.assertEqual(str(invest_plan_detail[0]['PURCHASE_PAYMENT_TYPE']),
                             str(entity.body_detail['payType']))
            self.assertEqual(str(invest_plan_detail[0]['STATUS']), str(entity.body_detail['status']))
            self.assertEqual(str(invest_plan_detail[0]['TOTAL_AMT']), str(entity.body_detail['totalInvestAmt']))
            self.assertEqual(str(fund_proinfo[0]['product_no']), str(entity.body_detail['fundCode']))
            self.assertEqual(str(fund_proinfo[0]['fund_type']), str(entity.body_detail['fundType']))

    # 账户-查询电子签名约定书信息
    @file_data('test_data/test_get_signature_agreement_info.json')
    def test_get_signature_agreement_info(self, user_name, password, assert_info):
        self._restful_xjb.get_signature_agreement_info(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if entity.returnCode == '000000':
            signature = self._db.get_signature_agreement_info_db(mobile=str(user_name))
            if entity.body['agreementName'] == '电子签名约定书':
                self.assertEqual(str(entity.body['agreementUrl']),
                                 'http://10.199.111.2/V1/pages/agreement/elec_signature.html')
                self.assertEqual(str(entity.body['signDateInfo'])[13:23], str(signature[0]['esignature_date'])[:10])
            else:
                self.assertEqual(str(entity.body['agreementUrl']), '')
                self.assertEqual(str(entity.body['signDateInfo']), '')

    # 工资理财详情
    @file_data("test_data/test_get_salary_fin_plan_detail.json")
    def test_get_salary_fin_plan_detail(self, user_name, password, assert_info):
        invest_plan_list = self._db.fund_invest_plan_list(mobile=str(user_name))
        self._restful_xjb.get_salary_plan_detail(user_name=str(user_name), password=str(password),
                                                 salary_fin_plan_id=str(invest_plan_list[0]['PROTOCOL_NO']))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        self.assertEqual(entity.returnCode, assert_info['returnCode'])

        detail = entity.body_detail
        des_bank_no = self._db.get_highest_prio_bank_channel(bank_name=str('工商银行'))
        card = self._db.get_binding_card_by_bank_no(mobile=str(user_name), bank_no=str(des_bank_no))
        self.assertEqual(str(detail['bankCardId']), str(card[0]['serial_id']))
        self.assertEqual(str(detail['cardTailNo']), str(card[0]['card_no'][-4:]))
        self.assertEqual(str(detail['cardType']), '0')
        self.assertEqual(str(detail['detailStatusInfo']), '正常执行中')
        self.assertEqual(str(detail['dfAgreements']), '')
        self.assertEqual(str(detail['dfInfo']), '')
        self.assertEqual(str(detail['dfStatus']), '')
        self.assertEqual(str(detail['employeeId']), '')
        self.assertEqual(str(detail['isDf']), '0')
        self.assertEqual(str(detail['isNeedActiveSalaryCard']), '')
        self.assertEqual(str(detail['isNeedSignProtocol']), '')
        self.assertIn('已转', str(detail['listStatusInfo']))
        next_pay_day = datetime.datetime.strptime(str(invest_plan_list[0]['NEXT_PAYMENT_DAY']), '%Y%m%d').strftime(
            '%Y-%m-%d')
        self.assertEqual(str(detail['nextPurchaseDate']), next_pay_day)
        self.assertEqual(str(detail['planName']), '工资理财')
        self.assertEqual(str(detail['purchaseAmtInfo']), str(invest_plan_list[0]['AP_AMT']) + '元')
        if str(invest_plan_list[0]['STATUS']) == 'N':
            self.assertEqual(str(detail['status']), '2')

    # 工资代发-匹配工资卡信息
    @file_data('test_data/test_match_salary_card.json')
    def test_match_salary_card(self, user_name, password, cert_no, employee_id, assert_info):
        self._restful_xjb.match_salary_card(user_name=str(user_name), password=str(password), cert_no=str(cert_no),
                                            employee_id=str(employee_id))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if assert_info["returnCode"] == '000000':
            employee_count = self._db.get_match_salary_card(employee_id=str(employee_id), cert_no=str(cert_no))
            self.assertEqual(str(employee_count[0]['count']), str(entity.result))

    # 交易-高端极速赎回提示信息（V2.0）
    @file_data('test_data/test_vip_product_fast_redeem_tip.json')
    def test_get_vip_product_fast_redeem_tip(self, user_name, password, product_id, sold_share, assert_info):
        self._restful_xjb.get_vip_product_fast_redeem_tip(user_name=str(user_name), password=str(password),
                                                          product_id=str(product_id), sold_share=str(sold_share))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            new_nav, count_fund_nav = self._db.get_fund_nav(fund_id=str(product_id))
            amt = decimal.Decimal(str(sold_share)) * decimal.Decimal(str(new_nav[0]['nav']))
            if decimal.Decimal(sold_share) >= 1.00:
                self.assertEqual(entity.body['info'],
                                 '预计到账：' + str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))) + '元')
            else:
                self.assertEqual(entity.body['info'],
                                 '预计到账：' + str(decimal.Decimal(str(amt)).quantize(
                                     decimal.Decimal('0.00'))) + '元' + '（卖出份额不足，最低卖出1.00份）')

    # 交易-高端极速赎回限额信息(V2.0)
    @file_data('test_data/test_vip_product_fast_redeem_limit_info.json')
    def test_get_vip_product_fast_redeem_limit_info(self, user_name, password, product_id, assert_info):
        self._restful_xjb.get_vip_product_fast_redeem_limit_info(user_name=str(user_name), password=str(password),
                                                                 product_id=str(product_id))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            quota_limit = self._db.get_cust_quota_limit(mobile=str(user_name))
            if len(quota_limit) == 0:
                self.assertEqual(entity.body['fastRedeemStatus'], '1')
            else:
                self.assertEqual(entity.body['fastRedeemStatus'], '2')
                charge_type = self._db.get_product_marketing(product_id=str(product_id))[0]['charge_type']
                once_limit = quota_limit[0]['ONCE_LIMIT']
                day_limit = quota_limit[0]['DAY_LIMIT']
                month_limit = quota_limit[0]['MONTH_LIMIT']
                once_limit_w = decimal.Decimal(once_limit / 10000).quantize(decimal.Decimal('0.00'))
                day_limit_w = decimal.Decimal(day_limit / 10000).quantize(decimal.Decimal('0.00'))
                month_limit_w = decimal.Decimal(month_limit / 10000).quantize(decimal.Decimal('0.00'))
                self.assertEqual(entity.body['chargeType'], str(charge_type))
                self.assertTrue('本次最多可卖出' + str(
                    decimal.Decimal(str(once_limit)).quantize(decimal.Decimal('0.00'))) + '份' in str(entity.body[
                                                                                                         'fastRedeemTip']).replace(
                    ',', ''))
                self.assertEqual(str(entity.body['limitInfo']).replace(',', ''),
                                 '单次限额:' + str(once_limit_w) + '万\n单日限额:' + str(day_limit_w) + '万\n单月限额:' +
                                 str(month_limit_w) + '万')
                self.assertEqual(entity.body['maxFastRedeemCount'],
                                 str(decimal.Decimal(str(once_limit)).quantize(decimal.Decimal('0.00'))))

    # 理财产品列表（自3.0.0接口）
    @file_data('test_data/test_get_product_list.json')
    def test_get_product_list(self, user_name, password, product_type, high_series_type, is_history, assert_info):
        self._restful_xjb.get_product_list(user_name=str(user_name), password=str(password),
                                           high_series_type=str(high_series_type), is_history=str(is_history),
                                           product_type=str(product_type))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        self.assertEqual(entity.returnCode, assert_info['returnCode'])

        if str(product_type) == '1':
            if str(is_history) == '0':
                expected_list = self._db.get_on_sale_product_list(product_type=str(product_type),
                                                                  accept_mode='M', is_archive='0')
                expected_recomm_list = \
                    self._db.get_recomment_product_list(product_type=str(product_type), accept_mode='M')[0]
                for prod in expected_list:
                    if str(prod['productid']) == str(expected_recomm_list['productid']):
                        expected_list.remove(prod)
                        break
                recomm_product_list = entity.productList[0]
                self.assertEqual(recomm_product_list[0]['type'], str(product_type))
                self.assertEqual(recomm_product_list[0]['productId'], str(expected_recomm_list['productid']))
                self.assertEqual(recomm_product_list[0]['recommended'], str(expected_recomm_list['recommended']))
                self.assertEqual(recomm_product_list[0]['productType'], str(product_type))
                self.assertTrue(str("立即购买") in str(recomm_product_list[0]['buyButtonDesc']))
                dhb_list = entity.productList[1]

            elif str(is_history) == '1':
                expected_list = self._db.get_on_sale_product_list(product_type=str(product_type),
                                                                  accept_mode='M', is_archive='1')
                dhb_list = entity.productList
            if len(expected_list) <= 20 or str(is_history) == '0':
                self.assertEqual(len(dhb_list), len(expected_list))
                dhb_list = sorted(dhb_list, key=lambda p: p['productId'])
                expected_list = sorted(expected_list, key=lambda p: p['productid'])
                self.verify_product_info(dhb_list, expected_list)
            else:
                self.assertTrue(len(dhb_list) < len(expected_list))
                for i in range(0, len(dhb_list)):
                    self.assertTrue(str(dhb_list[i]['productId']) in str(expected_list))
        else:
            data_list = entity.dataList
            # 1008精选系列 1010现金管理系列 1030固定收益系列
            expected_1008_prod_list = self._db.get_vip_product_list(product_type=str(product_type),
                                                                    accept_mode='M', series_type='1008',
                                                                    is_archive='0')
            expected_1010_prod_list = self._db.get_vip_product_list(product_type=str(product_type),
                                                                    accept_mode='M', series_type='1010',
                                                                    is_archive='0')
            expected_1030_prod_list = self._db.get_vip_product_list(product_type=str(product_type),
                                                                    accept_mode='M', series_type='1030',
                                                                    is_archive='0')
            if str(high_series_type) == '':
                list_1008 = data_list[0]
                list_1010 = data_list[1]
                list_1030 = data_list[2]
                self.assertEqual(str(list_1008['highSeriesType']), '3')
                self.assertEqual(str(list_1008['moduleName']), str('精选系列'))
                self.assertEqual(str(list_1010['moduleName']), str('现金管理系列'))
                self.assertEqual(str(list_1030['moduleName']), str('固定收益系列'))
                self.assertEqual(str(list_1010['highSeriesType']), '2')
                self.assertEqual(str(list_1030['highSeriesType']), '1')
                actual_1008_list = list_1008['productList']
                actual_1010_list = list_1010['productList']
                actual_1030_list = list_1030['productList']
                actual_1008_list = sorted(actual_1008_list, key=lambda p: p['productId'])
                actual_1010_list = sorted(actual_1010_list, key=lambda p: p['productId'])
                actual_1030_list = sorted(actual_1030_list, key=lambda p: p['productId'])
                expected_1008_prod_list = sorted(expected_1008_prod_list, key=lambda p: p['productid'])
                expected_1010_prod_list = sorted(expected_1010_prod_list, key=lambda p: p['productid'])
                expected_1030_prod_list = sorted(expected_1030_prod_list, key=lambda p: p['productid'])
                self.assertEqual(len(actual_1008_list), len(expected_1008_prod_list))
                self.assertEqual(len(actual_1010_list), len(expected_1010_prod_list))
                self.assertEqual(len(actual_1030_list), len(expected_1030_prod_list))
                self.verify_product_info(actual_1008_list, expected_1008_prod_list)
                self.verify_product_info(actual_1010_list, expected_1010_prod_list)
                self.verify_product_info(actual_1030_list, expected_1030_prod_list)
            elif str(high_series_type) == '3':
                list_1008 = data_list[0]
                total_count = entity.body_totalCount
                actual_1008_list = list_1008['productList']
                actual_1008_list = sorted(actual_1008_list, key=lambda p: p['productId'])
                expected_1008_prod_list = sorted(expected_1008_prod_list, key=lambda p: p['productid'])
                self.assertEqual(str(total_count), str(len(expected_1008_prod_list)))
                self.assertEqual(len(actual_1008_list), len(expected_1008_prod_list))
                self.assertEqual(str(list_1008['highSeriesType']), str(high_series_type))
                self.assertEqual(str(list_1008['moduleName']), str('精选系列'))
                self.verify_product_info(actual_1008_list, expected_1008_prod_list)
            elif str(high_series_type) == '1':
                list_1030 = data_list[0]
                total_count = entity.body_totalCount
                actual_1030_list = list_1030['productList']
                actual_1030_list = sorted(actual_1030_list, key=lambda p: p['productId'])
                expected_1030_prod_list = sorted(expected_1030_prod_list, key=lambda p: p['productid'])
                self.assertEqual(str(total_count), str(len(expected_1030_prod_list)))
                self.assertEqual(len(actual_1030_list), len(expected_1030_prod_list))
                self.assertEqual(str(list_1030['moduleName']), str('固定收益系列'))
                self.assertEqual(str(list_1030['highSeriesType']), str(high_series_type))
                self.verify_product_info(actual_1030_list, expected_1030_prod_list)
            elif str(high_series_type) == '2':
                list_1010 = data_list[0]
                total_count = entity.body_totalCount
                actual_1010_list = list_1010['productList']
                actual_1010_list = sorted(actual_1010_list, key=lambda p: p['productId'])
                expected_1010_prod_list = sorted(expected_1010_prod_list, key=lambda p: p['productid'])
                self.assertEqual(str(total_count), str(len(expected_1010_prod_list)))
                self.assertEqual(len(actual_1010_list), len(expected_1010_prod_list))
                self.assertEqual(str(list_1010['moduleName']), str('现金管理系列'))
                self.assertEqual(str(list_1010['highSeriesType']), str(high_series_type))
                self.verify_product_info(actual_1010_list, expected_1010_prod_list)

    # 修改分红方式
    @file_data('test_data/test_set_melon_type.json')
    def test_set_melon_type(self, user_name, password, fund_id, share_type, cust_no, assert_info):
        self._restful_xjb.set_melon_type(user_name=str(user_name), password=str(password), fund_id=str(fund_id),
                                         share_type=str(share_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        if assert_info["returnCode"] == '000000':
            cts_trade_request, cts_prod_quty = self._db.get_melon_type_info(cust_no=str(cust_no), prod_id=str(fund_id))
            self.assertEqual(cts_trade_request[0]['MELON_MODE'], share_type)
            self.assertEqual(cts_prod_quty[0]['MELON_MODE'], share_type)

    # 获取赎回费率
    @file_data('test_data/test_get_fund_redeem_rate.json')
    def test_get_fund_redeem_rate(self, user_name, password, fund_id, assert_info):
        self._restful_xjb.get_fund_redeem_rate(user_name=str(user_name), password=str(password), fund_id=str(fund_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        if assert_info["returnCode"] == '000000':
            pdc_product_marketing = self._db.get_pdc_product_marketing(product_id=str(fund_id))
            product_discount_rate = self._db.get_fund_discount_rate(product_id=str(fund_id))
            self.assertEqual(float(pdc_product_marketing[0]['fast_redeem_rate']), float(entity.rate.strip("%")))
            rate_discount = float(pdc_product_marketing[0]['fast_redeem_rate']) * float(
                product_discount_rate[0]['discount']) * 0.01
            self.assertEqual(rate_discount, float(entity.rateAfterDiscount.strip("%")))

    # 获取下一个扣款日期
    @file_data('test_data/test_get_fund_next_pay_day.json')
    def test_get_fund_next_pay_day(self, user_name, password, fund_id, pay_cycle, pay_day, assert_info):
        self._restful_xjb.get_fund_next_pay_day(user_name=str(user_name), password=str(password),
                                                fund_id=str(fund_id), pay_cycle=pay_cycle, pay_day=pay_day)
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertEqual(entity.returnMsg, assert_info['returnMsg'])
        if assert_info["returnCode"] == '000000':
            payday = pay_day.split('#')
            paycycle = pay_cycle.split('#')

            if (paycycle[1] == 'W'):
                nextpayday = datetime.date.today()
                oneday = datetime.timedelta(days=1)
                paydaydict = {"1": calendar.MONDAY, "2": calendar.TUESDAY, "3": calendar.WEDNESDAY,
                              "4": calendar.THURSDAY, "5": calendar.FRIDAY}
                # 定义每周日期字典
                nextpayday += oneday  # 往后顺延一天
                while nextpayday.weekday() != paydaydict[payday[1]]:
                    nextpayday += oneday
            elif (paycycle[1] == 'M'):
                day_now = time.localtime()
                if int(day_now.tm_mday) <= int(payday[1]):
                    pay_date = time.strftime("%Y-%m-%d %H:%M:%S", day_now)
                    nextpayday = str(pay_date)[0:8] + str(payday[1])
                else:
                    wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)
                    # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
                    day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
                    date_end = datetime.datetime.strptime(day_end, "%Y-%m-%d").date()
                    nextpayday = (date_end + datetime.timedelta(days=int(payday[1]))).strftime('%Y-%m-%d')
            elif (paycycle[1] == 'D'):
                nextpayday = (datetime.date.today() + datetime.timedelta(days=int(payday[1]))).strftime(
                    '%Y-%m-%d')
                # 实际还款日
                nextpayday1 = str(nextpayday).replace('-', '')
                nextpayda = self._db.judge_is_work_date(day=str(nextpayday1))[0]['WORK_DATE']
                nextpaydate = str(nextpayda)[0:4] + '-' + str(nextpayda)[4:6] + '-' + str(nextpayda)[6:8]
                self.assertEqual(entity.info, '下一次扣款日期：' + str(nextpaydate))

    # 基金-设置基金自选/删除基金自选
    @file_data('test_data/test_add_fav.json')
    def test_add_fav(self, user_name, password, fund_id, assert_info):
        add_fav_fund, add_fav = self._db.get_fav_fund(mobile=str(user_name), object_id=str(fund_id))

        # 删除基金自选
        if add_fav[0]['is_delete'] == 0:
            self._restful_xjb.del_fav(user_name=str(user_name), password=str(password), fund_id=str(fund_id))
            entity = self._restful_xjb.entity.current_entity
            self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
            self.assertEqual(entity.returnCode, assert_info["returnCode"])
        elif add_fav[0]['is_delete'] == 1:
            # 设置基金自选
            self._restful_xjb.add_fav(user_name=str(user_name), password=str(password), fund_id=str(fund_id))
            entity = self._restful_xjb.entity.current_entity
            self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
            self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 基金-研究报告,数据存放在mongoDB中
    @file_data('test_data/test_research_report.json')
    def test_research_report(self, user_name, password, assert_info):
        self._restful_xjb.research_report(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertIsNotNone(entity.totalCount)
        self.assertIsNotNone(entity.dataList)

    # 基金-机构观点
    @file_data('test_data/test_org_view_point.json')
    def test_org_view_point(self, user_name, password, assert_info):
        self._restful_xjb.org_view_point(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertIsNotNone(entity.totalCount)
        self.assertIsNotNone(entity.dataList)

    # 基金-达人论基
    @file_data('test_data/test_intelligent_say.json')
    def test_intelligent_say(self, user_name, password, assert_info):
        self._restful_xjb.intelligent_say(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertIsNotNone(entity.totalCount)
        self.assertIsNotNone(entity.dataList)

    # 基金-专家开讲
    @file_data('test_data/test_expert_say.json')
    def test_expert_say(self, user_name, password, assert_info):
        self._restful_xjb.expert_say(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertIsNotNone(entity.totalCount)
        self.assertIsNotNone(entity.dataList)

    # 账户-产品风险验证
    @file_data('test_data/test_risk_validate.json')
    def test_get_risk_validate(self, user_name, password, product_id, assert_info):
        self._restful_xjb.get_risk_validate(user_name=str(user_name), password=str(password),
                                            product_id=str(product_id))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '081600':
            self.assertEqual(entity.showType, '2')
        if entity.returnCode == '000000':
            self.assertEqual(entity.returnMsg, '')
            self.assertEqual(entity.showType, '')

    # 账户-风险测评发送短信
    @file_data('test_data/test_risk_get_mobile_code.json')
    def test_get_risk_get_mobile_code(self, user_name, password, product_id, assert_info):
        self._restful_xjb.get_risk_get_mobile_code(user_name=str(user_name), password=str(password),
                                                   product_id=str(product_id))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 账户-获取登录历史
    @file_data('test_data/test_get_login_history.json')
    def test_get_login_history(self, user_name, password, page_no, page_size, assert_info):
        self._restful_xjb.get_login_history(user_name=str(user_name), password=str(password), page_no=str(page_no),
                                            page_size=str(page_size))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            log_his = self._db.get_login_history(mobile=str(user_name))
            num = len(log_his) if len(log_his) < int(page_size) else int(page_size)
            for i in range(1, num):
                self.assertEqual(str(entity.body_dataList[i]['deviceInfo']), str(log_his[i]['deviceName']))
                self.assertEqual(str(entity.body_dataList[i]['hasException']), str(log_his[i]['abnormal']))
                self.assertEqual(str(entity.body_dataList[i]['loginSite']), str(log_his[i]['location']))
                self.assertEqual(str(entity.body_dataList[i]['loginTime']), str(log_his[i]['time'])[0:16])
            self.assertEqual(str(entity.body['totalCount']), str(len(log_his)))

    # 积分-我的优惠列表(V2.3)
    @file_data('test_data/test_get_my_coupon_list.json')
    def test_get_my_coupon_list(self, user_name, password, is_history, page_no, page_size, status,
                                assert_info):
        self._restful_xjb.get_my_coupon_list(user_name=str(user_name), password=str(password),
                                             is_history=str(is_history), page_no=str(page_no),
                                             page_size=str(page_size))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if entity.returnCode == '000000':
            my_coupon_list = self._db.get_my_coupon_list(mobile=str(user_name), status=str(status))
            data_list = entity.body_dataList
            if str(is_history) == '0':
                if int(str(page_size)) >= len(my_coupon_list):
                    my_coupon_list = sorted(my_coupon_list, key=lambda p: p['ECARD_NO'], reverse=True)
                    data_list = sorted(data_list, key=lambda p: p['couponId'], reverse=True)
                    if int(str(page_no)) == 1:
                        self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))
                        for i in range(0, len(my_coupon_list)):
                            self.assertEqual(str(data_list[i]['canOverload']),
                                             (str(1) if str(
                                                 my_coupon_list[i]['SUPPORT_COMPOSITE']) == 'Y' else str(0)))
                            self.assertEqual(str(data_list[i]['canOverloadInfo']),
                                             ('可叠加使用' if str(data_list[i]['canOverload']) == '1'
                                              else '不可叠加使用'))
                            self.assertEqual(str(data_list[i]['canUseAmt']),
                                             str(decimal.Decimal(
                                                 str(my_coupon_list[i]['COUPON_AMOUNT'])).quantize(
                                                 decimal.Decimal('0.00'))))
                            self.assertEqual(str(data_list[i]['canUseInfo']),
                                             str('满' + str(my_coupon_list[i]['COUPON_AMOUNT'])[
                                                       0:len(str(my_coupon_list[i]['COUPON_AMOUNT'])) - 3] + '可用'))
                            self.assertEqual(str(data_list[i]['canUsed']),
                                             '1' if str(my_coupon_list[i]['STATUS']) == 'ISSUE' else '0')
                            self.assertEqual(str(data_list[i]['couponAmt']),
                                             str(decimal.Decimal(str(my_coupon_list[i]['AMOUNT'])).quantize(
                                                 decimal.Decimal('0.00'))))
                            self.assertEqual(str(data_list[i]['couponDesc']),
                                             str('满' + str(my_coupon_list[i]['COUPON_AMOUNT'])[0:len(
                                                 str(my_coupon_list[i]['COUPON_AMOUNT'])) - 3] + '元' + '减' +
                                                 str(my_coupon_list[i]['AMOUNT'])[0:len(
                                                     str(my_coupon_list[i]['AMOUNT'])) - 3]) + '元')
                            self.assertEqual(str(data_list[i]['couponId']),
                                             str(my_coupon_list[i]['ECARD_NO']))
                            self.assertEqual(str(data_list[i]['couponType']),
                                             str(my_coupon_list[i]['COUPON_TYPE']))
                            self.assertEqual(str(data_list[i]['usePeriod']),
                                             str(str(my_coupon_list[i]['START_AT'])[0:10]).replace("-", ".") + '-' +
                                             str(str(my_coupon_list[i]['END_AT'])[0:10]).replace("-", "."))
                    if int(str(page_no)) > 1:
                        self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))

                if 0 < int(str(page_size)) < len(my_coupon_list):
                    if int(str(page_no)) < int(
                            math.ceil(len(my_coupon_list) / decimal.Decimal(str(page_size)))):
                        self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))
                        for i in range(0, int(str(page_size))):
                            j = int(str(page_size)) * (int(str(page_no)) - 1) + i
                            self.assertEqual(str(data_list[i]['canOverload']),
                                             (str(1) if str(
                                                 my_coupon_list[j]['SUPPORT_COMPOSITE']) == 'Y' else str(0)))
                            self.assertEqual(str(data_list[i]['canOverloadInfo']),
                                             ('可叠加使用' if str(entity.body_dataList[i]['canOverload']) == '1'
                                              else '不可叠加使用'))
                            self.assertEqual(str(data_list[i]['canUseAmt']),
                                             str(decimal.Decimal(
                                                 str(my_coupon_list[j]['COUPON_AMOUNT'])).quantize(
                                                 decimal.Decimal('0.00'))))
                            self.assertEqual(str(data_list[i]['canUseInfo']),
                                             str('满' + str(my_coupon_list[j]['COUPON_AMOUNT'])[0:len(
                                                 str(my_coupon_list[j]['COUPON_AMOUNT'])) - 3] + '可用'))
                            self.assertEqual(str(data_list[i]['canUsed']),
                                             '1' if str(my_coupon_list[j]['STATUS']) == 'ISSUE' else '0')
                            self.assertEqual(str(data_list[i]['couponAmt']),
                                             str(decimal.Decimal(str(my_coupon_list[j]['AMOUNT'])).quantize(
                                                 decimal.Decimal('0.00'))))
                            self.assertEqual(str(data_list[i]['couponDesc']),
                                             str('满' + str(my_coupon_list[j]['COUPON_AMOUNT'])[0:len(
                                                 str(my_coupon_list[j]['COUPON_AMOUNT'])) - 3] + '元' + '减' +
                                                 str(my_coupon_list[j]['AMOUNT'])[0:len(
                                                     str(my_coupon_list[j]['AMOUNT'])) - 3]) + '元')
                            self.assertEqual(str(data_list[i]['couponId']),
                                             str(my_coupon_list[j]['ECARD_NO']))
                            self.assertEqual(str(data_list[i]['couponType']),
                                             str(my_coupon_list[j]['COUPON_TYPE']))
                            self.assertEqual(str(data_list[i]['usePeriod']),
                                             str(str(my_coupon_list[j]['START_AT'])[0:10]).replace("-", ".") + '-' +
                                             str(str(my_coupon_list[j]['END_AT'])[0:10]).replace("-", "."))
                    if int(str(page_no)) == int(math.ceil(len(my_coupon_list) / decimal.Decimal(str(page_size)))):
                        h = (int(math.ceil(len(my_coupon_list) / decimal.Decimal(str(page_size)))) - 1) * int(
                            str(page_size))
                        self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))
                        for i in range(0, len(my_coupon_list) - h):
                            j = h + i
                            self.assertEqual(str(data_list[i]['canOverload']),
                                             (str(1) if str(my_coupon_list[j]['SUPPORT_COMPOSITE']) == 'Y' else str(0)))
                            self.assertEqual(str(data_list[i]['canOverloadInfo']),
                                             ('可叠加使用' if str(entity.body_dataList[i]['canOverload']) == '1'
                                              else '不可叠加使用'))
                            self.assertEqual(str(data_list[i]['canUseAmt']),
                                             str(decimal.Decimal(str(my_coupon_list[j]['COUPON_AMOUNT'])).quantize(
                                                 decimal.Decimal('0.00'))))
                            self.assertEqual(str(data_list[i]['canUseInfo']),
                                             str('满' + str(my_coupon_list[j]['COUPON_AMOUNT'])[0:len(
                                                 str(my_coupon_list[j]['COUPON_AMOUNT'])) - 3] + '可用'))
                            self.assertEqual(str(entity.body_dataList[i]['canUsed']),
                                             '1' if str(my_coupon_list[j]['STATUS']) == 'ISSUE' else '0')
                            self.assertEqual(str(data_list[i]['couponAmt']),
                                             str(decimal.Decimal(str(my_coupon_list[j]['AMOUNT'])).quantize(
                                                 decimal.Decimal('0.00'))))
                            self.assertEqual(str(data_list[i]['couponDesc']),
                                             str('满' + str(my_coupon_list[j]['COUPON_AMOUNT'])[0:len(
                                                 str(my_coupon_list[j]['COUPON_AMOUNT'])) - 3] + '元' + '减' +
                                                 str(my_coupon_list[j]['AMOUNT'])[0:len(
                                                     str(my_coupon_list[j]['AMOUNT'])) - 3]) + '元')
                            self.assertEqual(str(data_list[i]['couponId']),
                                             str(my_coupon_list[j]['ECARD_NO']))
                            self.assertEqual(str(data_list[i]['couponType']),
                                             str(my_coupon_list[j]['COUPON_TYPE']))
                            self.assertEqual(str(data_list[i]['usePeriod']),
                                             str(str(my_coupon_list[j]['START_AT'])[0:10]).replace("-", ".") + '-' +
                                             str(str(my_coupon_list[j]['END_AT'])[0:10]).replace("-", "."))
                    if int(str(page_no)) > int(
                            math.ceil(len(my_coupon_list) / decimal.Decimal(str(page_size)))):
                        self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))

                if int(str(page_size)) == 0:
                    self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))

            if str(is_history) == '1':
                if str(status) == str('USED') or str(status) == str('FROZEN'):
                    if int(str(page_size)) >= len(my_coupon_list):
                        my_coupon_list = sorted(my_coupon_list, key=lambda p: p['ECARD_NO'], reverse=True)
                        data_list = sorted(data_list, key=lambda p: p['couponId'], reverse=True)
                        if int(str(page_no)) == 1:
                            self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))
                            for i in range(0, len(my_coupon_list)):
                                self.assertEqual(str(data_list[i]['couponStatus']), 'USED')
                                self.assertTrue('V1/images/trade/status/used.png' in
                                                str(data_list[i]['statusImageUrl']))
                        if int(str(page_no)) > 1:
                            self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))

                    if 0 < int(str(page_size)) < len(my_coupon_list):
                        if int(str(page_no)) < int(
                                math.ceil(len(my_coupon_list) / decimal.Decimal(str(page_size)))):
                            self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))
                            for i in range(0, int(str(page_size))):
                                self.assertEqual(str(data_list[i]['couponStatus']), 'USED')
                                self.assertTrue('V1/images/trade/status/used.png' in
                                                str(data_list[i]['statusImageUrl']))
                        if int(str(page_no)) == int(math.ceil(len(my_coupon_list) / decimal.Decimal(str(page_size)))):
                            h = (int(math.ceil(len(my_coupon_list) / decimal.Decimal(str(page_size)))) - 1) * int(
                                str(page_size))
                            self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))
                            for i in range(0, len(my_coupon_list) - h):
                                self.assertEqual(str(data_list[i]['couponStatus']), 'USED')
                                self.assertTrue(
                                    'V1/images/trade/status/used.png' in str(data_list[i]['statusImageUrl']))

                    if int(str(page_size)) == 0:
                        self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))

                if str(status) == 'OVERDUE':
                    if int(str(page_size)) >= len(my_coupon_list):
                        if int(str(page_no)) == 1:
                            self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))
                            for i in range(0, len(my_coupon_list)):
                                self.assertTrue('V1/images/trade/status/overDue.png' in
                                                str(data_list[i]['statusImageUrl']))
                        if int(str(page_no)) > 1:
                            self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))

                    if 0 < int(str(page_size)) < len(my_coupon_list):
                        if int(str(page_no)) < int(
                                math.ceil(len(my_coupon_list) / decimal.Decimal(str(page_size)))):
                            self.assertEqual(str(entity.body['totalCount']), str(page_size))
                            for i in range(0, int(str(page_size))):
                                self.assertTrue('V1/images/trade/status/overDue.png' in
                                                str(data_list[i]['statusImageUrl']))
                        if int(str(page_no)) == int(math.ceil(len(my_coupon_list) / decimal.Decimal(str(page_size)))):
                            h = (int(math.ceil(len(my_coupon_list) / decimal.Decimal(str(page_size)))) - 1) * int(
                                str(page_size))
                            self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list) - h))
                            for i in range(0, len(my_coupon_list) - h):
                                self.assertTrue('V1/images/trade/status/overDue.png' in
                                                str(data_list[i]['statusImageUrl']))

                    if int(str(page_size)) == 0:
                        self.assertEqual(str(entity.body['totalCount']), str(len(my_coupon_list)))

    # 消息中心-查询消息分类(V3.1)
    @file_data('test_data/test_get_message_category_list.json')
    def test_test_get_message_category_list(self, user_name, password, assert_info):
        self._restful_xjb.get_message_category_list(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            msg_category_list, msg_list = self._db.get_message_category_list()
            for i in range(0, len(msg_category_list)):
                self.assertEqual(str(entity.body_dataList[i]['canNotification']), '1')
                self.assertEqual(str(entity.body_dataList[i]['categoryLogo']),
                                 str(msg_category_list[i]['category_logo']))
                self.assertEqual(str(entity.body_dataList[i]['categoryName']),
                                 str(msg_category_list[i]['category_name']))
                self.assertEqual(str(entity.body_dataList[i]['categoryNo']), str(msg_category_list[i]['category_no']))
                if entity.body_dataList[i]['messageCount'] > 0:
                    ids = ''
                    msg_ids = ''
                    for j in range(0, len(msg_list[i])):
                        self.assertEqual(str(entity.body_dataList[i]['firstMessageTime']),
                                         str(msg_list[i][0]['msg_date']))
                        self.assertEqual(str(entity.body_dataList[i]['firstMessageTitle']),
                                         str(msg_list[i][0]['msg_title']))
                        self.assertEqual(str(entity.body_dataList[i]['messageCount']), str(len(msg_list[i])))
                        ids += str(msg_list[i][j]['id'])
                        msg_ids += str(str(entity.body_dataList[i]['messageIds'][j]))
                    self.assertEqual(str(msg_ids), str(ids))
                else:
                    self.assertEqual(str(entity.body_dataList[i]['firstMessageTime']), '')
                    self.assertEqual(str(entity.body_dataList[i]['firstMessageTitle']), '')
                    self.assertEqual(str(entity.body_dataList[i]['messageCount']), str(len(msg_list[i])))
                    self.assertEqual(str(entity.body_dataList[i]['messageIds']), '[]')

    # 现金宝在途资产
    @file_data('test_data/test_xjb_transit_asset.json')
    def test_xjb_transit_asset(self, user_name, password, assert_info):
        self._restful_xjb.xjb_transit_asset(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        data_list = entity.dataList
        if entity.returnCode == '000000':
            for i in range(0, len(data_list)):
                capital_in_transit = self._db.get_capital_in_transit(mobile=str(user_name))
                self.assertEqual(str(data_list[i]['fromSourse']), '现金宝')
                self.assertEqual(str(data_list[i]['tradeDesc']), '在途金额' + str(capital_in_transit[i]['BALANCE']) + '元')
                self.assertEqual(str(entity.body['totalCount']), str(len(data_list)))

    # 信用卡-中信联名卡申请
    @file_data('test_data/test_joint_card_apply_brand_validate.json')
    def test_joint_card_apply_brand(self, user_name, password, mobile, id_no, english_name, contact_name,
                                    contact_rel, contact_rel_nm, contact_mobile, ins_contact_mobile,
                                    ins_contact_name, ins_contact_rel, ins_contact_rel_nm, home_pc_ids,
                                    home_pc_names, home_area, corp_name, email, company_pc_ids, company_pc_names,
                                    company_area, corp_zone, brand_source, brand_type, corp_tel, assert_info):
        self._restful_xjb.jointcard_apply_brand_sendsms(user_name=str(user_name), password=str(password),
                                                        mobile=str(mobile), id_no=str(id_no),
                                                        english_name=str(english_name), brand_source=str(brand_source),
                                                        brand_type=str(brand_type))
        serial_no = self._restful_xjb.entity.current_entity.serialNo

        mobile_code = self._db.get_sms_verify_code(mobile=mobile, template_id='credit_apply_brand_citicb')
        self._restful_xjb.joint_card_apply_brand_validate(user_name=str(user_name), mobile=str(mobile),
                                                          id_no=str(id_no), english_name=str(english_name),
                                                          auth_code=str(mobile_code), serial_no=str(serial_no),
                                                          brand_source=str(brand_source), brand_type=str(brand_type))

        brand_request = self._db.get_credit_brand_request(mobile=str(mobile), brand_type=str(brand_type),
                                                          check_state='Y')
        brand_serial_id = brand_request[0]['serial_no']

        entity = self._restful_xjb.entity.current_entity
        serial_no = entity.resultData_serialNo
        is_new_card_apply = entity.resultData_isNewCardApply
        self.assertEqual(entity.resultMsg, assert_info["resultMsg"])
        self.assertEqual(entity.resultCode, assert_info["resultCode"])

        if str(brand_request[0]['new_card']) == 'Y':
            self.assertEqual(str(is_new_card_apply), '1')
        else:
            self.assertEqual(str(is_new_card_apply), '0')
        self.assertEqual(str(brand_request[0]['apply_state']), 'N')

        self._restful_xjb.joint_card_apply_brand_pre_submit(home_pc_ids=str(home_pc_ids),
                                                            home_pc_names=str(home_pc_names),
                                                            home_area=str(home_area), corp_name=str(corp_name),
                                                            email=str(email), company_pc_ids=str(company_pc_ids),
                                                            company_pc_names=str(company_pc_names),
                                                            company_area=str(company_area), corp_zone=str(corp_zone),
                                                            brand_source=str(brand_source), brand_type=str(brand_type),
                                                            serial_no=str(serial_no), corp_tel=str(corp_tel))
        serial_no = entity.resultData_serialNo
        self.assertEqual(entity.resultMsg, assert_info["resultMsg"])
        self.assertEqual(entity.resultCode, assert_info["resultCode"])

        if str(assert_info['resultCode']) == '000000':
            brand_detail = self._db.get_credit_brand_detail()
            self.assertEqual(brand_detail[0]['email'], str(email))
            self.assertEqual(brand_detail[0]['house_province_id'], str(home_pc_ids).split(',')[0])
            self.assertEqual(brand_detail[0]['house_city_id'], str(home_pc_ids).split(',')[1])
            self.assertEqual(brand_detail[0]['house_area_id'], str(home_pc_ids).split(',')[2])
            self.assertEqual(brand_detail[0]['house_addr'], str(home_area))
            self.assertEqual(brand_detail[0]['corp_name'], str(corp_name))
            self.assertEqual(brand_detail[0]['corp_province_id'], str(company_pc_ids).split(',')[0])
            self.assertEqual(brand_detail[0]['corp_city_id'], str(company_pc_ids).split(',')[1])
            self.assertEqual(brand_detail[0]['corp_area_id'], str(company_pc_ids).split(',')[2])
            self.assertEqual(brand_detail[0]['corp_addr'], str(company_area))

        self._restful_xjb.joint_card_apply_brand_submit(contact_name=str(contact_name), contact_rel=str(contact_rel),
                                                        contact_rel_nm=str(contact_rel_nm),
                                                        contact_mobile=str(contact_mobile),
                                                        ins_contact_mobile=str(ins_contact_mobile),
                                                        ins_contact_rel=str(ins_contact_rel),
                                                        ins_contact_name=str(ins_contact_name),
                                                        ins_contact_rel_nm=str(ins_contact_rel_nm),
                                                        serial_no=str(serial_no))

        self.assertEqual(entity.resultMsg, assert_info["resultMsg"])
        self.assertEqual(entity.resultCode, assert_info["resultCode"])
        if str(assert_info['resultCode']) == '000000':
            self.assertEqual(entity.success, True)
            brand_request = self._db.get_credit_brand_request(mobile=str(mobile), brand_serial_id=str(brand_serial_id))
            self.assertEqual(str(brand_request[0]['id_no']), str(id_no))
            self.assertEqual(str(brand_request[0]['mobile']), str(mobile))
            self.assertEqual(str(brand_request[0]['source']), str(brand_source))
            self.assertEqual(str(brand_request[0]['brand_type']), str(brand_type))
            self.assertEqual(str(brand_request[0]['accept_mode']), '5')
            self.assertEqual(str(brand_request[0]['apply_state']), 'Y')
            self.assertEqual(str(brand_request[0]['is_delete']), '0')
            if str(brand_request[0]['new_card']) == 'Y':
                self.assertEqual(str(brand_request[0]['check_code']), '1001')
                self.assertEqual(str(brand_request[0]['check_msg']), '新卡客户')
                self.assertEqual(str(brand_request[0]['apply_code']), '3001')
                self.assertEqual(str(brand_request[0]['apply_msg']), '提交成功')
        else:
            self.assertEqual(entity.success, False)

    # 消息中心-查询消息列表(V3.1)
    @file_data('test_data/test_get_category_message_list.json')
    def test_get_category_message_list(self, user_name, password, category_no, page_no, page_size, assert_info):
        self._restful_xjb.get_category_message_list(user_name=str(user_name), password=str(password),
                                                    category_no=str(category_no), page_no=str(page_no),
                                                    page_size=str(page_size))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            message_list = self._db.get_category_message_list_db(category_no=str(category_no))
            if entity.body['totalCount'] > 0:
                self.assertEqual(str(entity.body['totalCount']), str(len(message_list)))
                for i in range(0, len(message_list)):
                    self.assertEqual(str(entity.body_dataList[i]['categoryNo']), str(message_list[i]['category_no']))
                    self.assertEqual(str(entity.body_dataList[i]['content']), str(message_list[i]['msg_content']))
                    self.assertEqual(str(entity.body_dataList[i]['detailUrl']), str(message_list[i]['msg_url']))
                    self.assertEqual(str(entity.body_dataList[i]['messageId']), str(message_list[i]['id']))
                    self.assertEqual(str(entity.body_dataList[i]['publishTime']), str(message_list[i]['msg_date']))
                    self.assertEqual(str(entity.body_dataList[i]['summary']), str(message_list[i]['msg_abstract']))
                    self.assertEqual(str(entity.body_dataList[i]['title']), str(message_list[i]['msg_title']))
            else:
                self.assertEqual(str(entity.body['totalCount']), '0')

    # 信用卡-中信联名卡申请异常处理
    @file_data('test_data/test_joint_card_apply_brand_negative.json')
    def test_joint_card_apply_brand_negative(self, user_name, password, mobile, id_no, english_name, contact_name,
                                             contact_rel, contact_rel_nm, contact_mobile, ins_contact_mobile,
                                             ins_contact_name, ins_contact_rel, ins_contact_rel_nm, home_pc_ids,
                                             home_pc_names, home_area, corp_name, email, company_pc_ids,
                                             company_pc_names, company_area, corp_zone, brand_source, brand_type,
                                             corp_tel, assert_info):
        self._restful_xjb.jointcard_apply_brand_sendsms(user_name=str(user_name), password=str(password),
                                                        mobile=str(mobile), id_no=str(id_no),
                                                        english_name=str(english_name), brand_source=str(brand_source),
                                                        brand_type=str(brand_type))
        entity = self._restful_xjb.entity.current_entity
        serial_no = entity.serialNo

        if len(serial_no) == 0:
            self.assertEqual(entity.resultMsg, assert_info["resultMsg"])
            self.assertEqual(entity.resultCode, assert_info["resultCode"])
            self.assertEqual(entity.success, False)
        else:
            mobile_code = self._db.get_sms_verify_code(mobile=mobile, template_id='credit_apply_brand_citicb')
            self._restful_xjb.joint_card_apply_brand_validate(user_name=str(user_name),
                                                              mobile=str(mobile), id_no=str(id_no),
                                                              english_name=str(english_name),
                                                              auth_code=str(mobile_code), serial_no=str(serial_no),
                                                              brand_source=str(brand_source),
                                                              brand_type=str(brand_type))

            brand_request = self._db.get_credit_brand_request(mobile=str(mobile), brand_type=str(brand_type),
                                                              check_state='Y')
            brand_serial_id = brand_request[0]['serial_no']

            entity = self._restful_xjb.entity.current_entity
            serial_no = entity.resultData_serialNo
            is_new_card_apply = entity.resultData_isNewCardApply

            if str(brand_request[0]['new_card']) == 'Y':
                self.assertEqual(str(is_new_card_apply), '1')
            else:
                self.assertEqual(str(is_new_card_apply), '0')
            self.assertEqual(str(brand_request[0]['apply_state']), 'N')

            self._restful_xjb.joint_card_apply_brand_pre_submit(home_pc_ids=str(home_pc_ids),
                                                                home_pc_names=str(home_pc_names),
                                                                home_area=str(home_area), corp_name=str(corp_name),
                                                                email=str(email), company_pc_ids=str(company_pc_ids),
                                                                company_pc_names=str(company_pc_names),
                                                                company_area=str(company_area),
                                                                corp_zone=str(corp_zone),
                                                                brand_source=str(brand_source),
                                                                brand_type=str(brand_type), serial_no=str(serial_no),
                                                                corp_tel=str(corp_tel))
            serial_no = entity.resultData_serialNo

            if str(assert_info['resultCode']) == '000000':
                brand_detail = self._db.get_credit_brand_detail()
                self.assertEqual(brand_detail[0]['email'], str(email))
                self.assertEqual(brand_detail[0]['house_province_id'], str(home_pc_ids).split(',')[0])
                self.assertEqual(brand_detail[0]['house_city_id'], str(home_pc_ids).split(',')[1])
                self.assertEqual(brand_detail[0]['house_area_id'], str(home_pc_ids).split(',')[2])
                self.assertEqual(brand_detail[0]['house_addr'], str(home_area))
                self.assertEqual(brand_detail[0]['corp_name'], str(corp_name))
                self.assertEqual(brand_detail[0]['corp_province_id'], str(company_pc_ids).split(',')[0])
                self.assertEqual(brand_detail[0]['corp_city_id'], str(company_pc_ids).split(',')[1])
                self.assertEqual(brand_detail[0]['corp_area_id'], str(company_pc_ids).split(',')[2])
                self.assertEqual(brand_detail[0]['corp_addr'], str(company_area))

            self._restful_xjb.joint_card_apply_brand_submit(contact_name=str(contact_name),
                                                            contact_rel=str(contact_rel),
                                                            contact_rel_nm=str(contact_rel_nm),
                                                            contact_mobile=str(contact_mobile),
                                                            ins_contact_mobile=str(ins_contact_mobile),
                                                            ins_contact_rel=str(ins_contact_rel),
                                                            ins_contact_name=str(ins_contact_name),
                                                            ins_contact_rel_nm=str(ins_contact_rel_nm),
                                                            serial_no=str(serial_no))
            entity = self._restful_xjb.entity.current_entity
            self.assertEqual(entity.resultMsg, assert_info["resultMsg"])
            self.assertEqual(entity.resultCode, assert_info["resultCode"])
            if str(assert_info['resultCode']) == '000000':
                self.assertEqual(entity.success, True)
                brand_request = self._db.get_credit_brand_request(mobile=str(mobile),
                                                                  brand_serial_id=str(brand_serial_id))
                self.assertEqual(str(brand_request[0]['id_no']), str(id_no))
                self.assertEqual(str(brand_request[0]['mobile']), str(mobile))
                self.assertEqual(str(brand_request[0]['source']), str(brand_source))
                self.assertEqual(str(brand_request[0]['brand_type']), str(brand_type))
                self.assertEqual(str(brand_request[0]['accept_mode']), '5')
                self.assertEqual(str(brand_request[0]['apply_state']), 'Y')
                self.assertEqual(str(brand_request[0]['is_delete']), '0')
                if str(brand_request[0]['new_card']) == 'Y':
                    self.assertEqual(str(brand_request[0]['check_code']), '1001')
                    self.assertEqual(str(brand_request[0]['check_msg']), '新卡客户')
                    self.assertEqual(str(brand_request[0]['apply_code']), '3001')
                    self.assertEqual(str(brand_request[0]['apply_msg']), '提交成功')
            else:
                self.assertEqual(entity.success, False)

    # 消息中心-关闭消息推送(V3.1)
    @file_data('test_data/test_close_push.json')
    def test_close_push(self, user_name, password, category_no, status, assert_info):
        self._restful_xjb.close_push(user_name=str(user_name), password=str(password), category_no=str(category_no),
                                     status=str(status))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertIn(entity.returnCode, assert_info["returnCode"])

    # 还贷-查询还贷计划列表(V3.1)
    @file_data('test_data/test_get_plan_list.json')
    def test_get_repay_plan_list(self, user_name, password, assert_info):
        self._restful_xjb.get_plan_list(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if assert_info["returnCode"] == '000000':
            repay_plan_info = self._db.get_make_plan(mobile=str(user_name))
            self.assertEqual(user_name, str(repay_plan_info[0]['mobile']))
            self.assertEqual(str(entity.dataList[0]['bankGroupName']), '交通银行')
            self.assertEqual(str(entity.dataList[0]['cardId']), '0000000000102513')
            self.assertEqual(str(entity.dataList[0]['cardType']), '0')
            self.assertEqual(str(entity.dataList[0]['alreadyRepayCount']), str(repay_plan_info[0]['run_times']))
            self.assertEqual(str(entity.dataList[0]['repayAmt']), str(repay_plan_info[0]['amount']))
            self.assertEqual(str(entity.dataList[0]['nextRepayDate']).replace('-', ''),
                             str(repay_plan_info[0]['next_repay_date']))
            self.assertEqual(str(entity.dataList[0]['repayDateInfo']),
                             '每月' + str(repay_plan_info[0]['repay_date']) + '号')
            self.assertEqual(str(entity.dataList[0]['repayCount']), str(repay_plan_info[0]['total_repay_times']))
            self.assertEqual(str(entity.dataList[0]['repayType']), str(repay_plan_info[0]['repay_type']))
            self.assertEqual(str(entity.dataList[0]['repayPlanId']), str(repay_plan_info[0]['id']))
            self.assertEqual(str(entity.dataList[0]['status']), str(repay_plan_info[0]['status']))
            self.assertEqual(str(entity.dataList[0]['statusInfo']), '正常执行中')

    # 通用-保存附件信息（V3.1）
    @file_data('test_data/test_save_attachment.json')
    def test_save_attachment(self, user_name, password, send_type, mobile, type, assert_info):
        self._restful_xjb.save_attachment(user_name=str(user_name), password=str(password), send_type=str(send_type),
                                          mobile=str(mobile), type=str(type))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 还贷-创建/修改还贷计划(V3.1)
    @file_data('test_data/test_make_plan.json')
    def test_make_repay_plan(self, user_name, password, repay_plan_id, repay_type, card_id, repay_amt, repay_date,
                             repay_count, trade_password, assert_info):
        self._restful_xjb.make_plan(user_name=str(user_name), password=str(password), repay_plan_id=str(repay_plan_id),
                                    repay_type=str(repay_type), card_id=str(card_id), repay_amt=str(repay_amt),
                                    repay_date=str(repay_date), repay_count=str(repay_count),
                                    trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity

        self.assertIn(assert_info["returnMsg"], entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if assert_info["returnCode"] == '000000':
            self.assertEqual(entity.title, '设置成功')
            if repay_plan_id == '':
                repay_plan_info = self._db.get_make_plan(mobile=str(user_name))
                self.assertEqual(user_name, str(repay_plan_info[0]['mobile']))
                self.assertEqual(str(datetime.datetime.today().strftime('%Y%m%d')), str(repay_plan_info[0]['sys_date']))
                self.assertEqual('M', str(repay_plan_info[0]['accept_mode']))
                self.assertEqual(repay_amt, str(repay_plan_info[0]['amount']))
                self.assertEqual(repay_date, str(repay_plan_info[0]['repay_date']))
                self.assertEqual(repay_count, str(repay_plan_info[0]['total_repay_times']))
                self.assertEqual(repay_type, str(repay_plan_info[0]['repay_type']))
                self.assertEqual(str(repay_plan_info[0]['status']), 'N')
                self.assertEqual(str(repay_plan_info[0]['freeze_status']), 'U')
                self.assertEqual(str(repay_plan_info[0]['has_validated']), '0')
            else:
                repay_plan_info = self._db.get_make_plan(mobile=str(user_name), repay_plan_id=str(repay_plan_id))
                self.assertEqual(user_name, str(repay_plan_info[0]['mobile']))
                self.assertEqual('20170823', str(repay_plan_info[0]['sys_date']))
                self.assertEqual('M', str(repay_plan_info[0]['accept_mode']))
                self.assertEqual(repay_amt, str(repay_plan_info[0]['amount']))
                self.assertEqual(repay_date, str(repay_plan_info[0]['repay_date']))
                self.assertEqual(repay_count, str(repay_plan_info[0]['total_repay_times']))
                self.assertEqual(repay_type, str(repay_plan_info[0]['repay_type']))
                self.assertEqual(repay_plan_id, str(repay_plan_info[0]['id']))
                self.assertEqual(str(repay_plan_info[0]['status']), 'N')
                self.assertEqual(str(repay_plan_info[0]['freeze_status']), 'U')
                self.assertEqual(str(repay_plan_info[0]['has_validated']), '0')

    # 还贷-启用/暂停/删除还贷计划(V3.1)
    @file_data('test_data/test_update_plan.json')
    def test_update_repay_plan(self, user_name, password, repay_plan_id, status, trade_password,
                               assert_info):
        self._restful_xjb.update_plan(user_name=str(user_name), password=str(password),
                                      repay_plan_id=str(repay_plan_id), status=str(status),
                                      trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertIn(assert_info["returnMsg"], entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if assert_info["returnCode"] == '000000':
            repay_plan_info = self._db.get_make_plan(mobile=str(user_name), repay_plan_id=str(repay_plan_id))
            self.assertEqual(user_name, str(repay_plan_info[0]['mobile']))
            self.assertEqual(repay_plan_id, str(repay_plan_info[0]['id']))
            self.assertEqual(str(repay_plan_info[0]['status']), status)
            self.assertEqual(str(repay_plan_info[0]['freeze_status']), 'U')
            self.assertEqual(str(repay_plan_info[0]['has_validated']), '0')
            # 修改已删除的计划状态为初始值
            if status == 'D':
                self._db.update_plan_status(repay_plan_id=str(repay_plan_id))

    # 还贷-还贷准入（V3.1)
    @file_data('test_data/test_repay_check.json')
    def test_repay_check(self, user_name, password, assert_info):
        self._restful_xjb.repay_check(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.validateType, '3')
        self.assertIsNotNone(entity.serialNo)

    # 还贷-查询还贷计划详情(V3.1)
    @file_data('test_data/test_get_plan_detail.json')
    def test_get_repay_plan_detail(self, user_name, password, repay_plan_id, assert_info):
        self._restful_xjb.get_plan_detail(user_name=str(user_name), password=str(password),
                                          repay_plan_id=str(repay_plan_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if assert_info["returnCode"] == '000000':
            repay_plan_info = self._db.get_make_plan(mobile=str(user_name), repay_plan_id=str(repay_plan_id))
            self.assertEqual(user_name, str(repay_plan_info[0]['mobile']))
            self.assertEqual(str(entity.detail['bankGroupName']), '交通银行')
            self.assertEqual(str(entity.detail['cardId']), '0000000000102480')
            self.assertEqual(str(entity.detail['cardType']), '0')
            self.assertEqual(str(entity.detail['alreadyRepayCount']), str(repay_plan_info[0]['run_times']))
            self.assertEqual(str(entity.detail['repayAmt']), str(format(repay_plan_info[0]['amount'], ',')))
            self.assertEqual(str(entity.detail['nextRepayDate']).replace('-', ''),
                             str(repay_plan_info[0]['next_repay_date']))
            self.assertEqual(str(entity.detail['repayDateInfo']),
                             '每月' + str(repay_plan_info[0]['repay_date']) + '号')
            self.assertEqual(str(entity.detail['repayCount']), str(repay_plan_info[0]['total_repay_times']))
            self.assertEqual(str(entity.detail['repayType']), str(repay_plan_info[0]['repay_type']))
            self.assertEqual(str(entity.detail['repayPlanId']), str(repay_plan_info[0]['id']))
            self.assertEqual(str(entity.detail['repayTitle']), '还房贷')
            self.assertEqual(str(entity.detail['status']), str(repay_plan_info[0]['status']))
            self.assertEqual(str(entity.detail['statusInfo']), '正常执行中')

    # 还贷-查询还款提示（V3.1）
    @file_data('test_data/test_get_repay_tip.json')
    def test_get_repay_tip(self, user_name, password, repay_date, assert_info):
        self._restful_xjb.get_repay_tip(user_name=str(user_name), password=str(password), repay_date=str(repay_date))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if assert_info["returnCode"] == '000000':
            day = str(datetime.datetime.now())[0:10].replace('-', '')
            year = datetime.datetime.now().year
            if len(str(datetime.datetime.now().month)) == 1:
                now_month = '0' + str(datetime.datetime.now().month)
            else:
                now_month = datetime.datetime.now().month
            # 计算实际还款日(上一个工作日)
            repay_date_re = self._db.get_pre_work_date(
                work_day=str(year) + str(now_month) + str(repay_date))[0]['WORK_DATE']
            if str(repay_date_re) <= day:
                next_month = datetime.datetime.now().month + 1
                if int(next_month) > 12:
                    next_month = str(int(next_month) - 12)
                    year = int(year) + 1
                if len(str(next_month)) == 2:
                    next_month = next_month
                elif len(str(next_month)) == 1:
                    next_month = '0' + str(next_month)
            else:
                next_month = datetime.datetime.now().month
                if len(str(next_month)) == 1:
                    next_month = '0' + str(next_month)
                if int(next_month) > 12:
                    next_month = str(int(next_month) - 12)
                    year = int(year) + 1
                    if len(str(next_month)) == 2:
                        next_month = next_month
                    elif len(str(next_month)) == 1:
                        next_month = '0' + str(next_month)

            before_day = self._db.get_pre_work_date(work_day=str(year) + str(next_month) +
                                                             str(repay_date))[0]['WORK_DATE']
            before_day = str(before_day)[0:4] + '-' + str(before_day)[4:6] + '-' + str(before_day)[6:8]
            self.assertEqual(entity.info, '温馨提示：华信现金宝每月将提前一个工作日为您发起还款下次还款：' +
                             str(before_day) + '，预计12:00前到账')

    # 积分-优惠券有效性校验(V3.1)
    @file_data('test_data/test_my_coupon_validate.json')
    def test_my_coupon_validate(self, user_name, password, coupon_id, accept_mode, assert_info):
        self._restful_xjb.my_coupon_validate(user_name=str(user_name), password=str(password),
                                             coupon_id=str(coupon_id), accept_mode=str(accept_mode))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 账户-资产证明申请(V1.6)
    @file_data('test_data/test_assert_cert_apply.json')
    def test_assert_cert_apply(self, user_name, password, send_type, mobile, assert_info):
        self._restful_xjb.assert_cert_apply(user_name=str(user_name), password=str(password), send_type=str(send_type),
                                            mobile=str(mobile))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    #  产品-全部理财产品检索条件（V3.1)
    @file_data('test_data/test_get_fin_product_search_condition_group_list.json')
    def test_get_fin_product_search_condition_group_list(self, user_name, password, group_id, assert_info):
        self._restful_xjb.get_fin_product_search_condition_group_list(user_name=str(user_name),
                                                                      password=str(password),
                                                                      group_id=str(group_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if assert_info["returnCode"] == '000000':
            get_max_yield = self._db.get_max_yield_by_period()
            data_list = entity.dataList
            for i in range(0, len(data_list)):
                condition_list = data_list[i]['conditionList']
                if data_list[i]['groupId'] == '0':
                    self.assertEqual(str(data_list[i]['groupId']), str(group_id[0]))
                    self.assertEqual(str(data_list[i]['groupName']), '投资期限')
                    for a in range(0, len(condition_list)):
                        if condition_list[a]['conditionId'] == '-1':
                            # self.assertEqual(str(condition_list[a]['conditionDesc']),
                            #                  '%s%%' % str(decimal.Decimal(
                            #                      str(get_max_yield[0]['max_yield']).replace('%', '')).quantize(
                            #                      decimal.Decimal('0.00'))))
                            self.assertEqual(str(condition_list[a]['conditionId']), '-1')
                            self.assertEqual(str(condition_list[a]['conditionName']), '全部')
                        elif condition_list[a]['conditionId'] == '0':
                            # self.assertEqual(str(condition_list[a]['conditionDesc']),
                            #                  '%s%%' % str(decimal.Decimal(
                            #                      str(get_max_yield[0]['max_yield']).replace('%', '')).quantize(
                            #                      decimal.Decimal('0.00'))))
                            self.assertEqual(str(condition_list[a]['conditionId']), '0')
                            self.assertEqual(str(condition_list[a]['conditionName']), '0-3个月')
                        elif condition_list[a]['conditionId'] == '1':
                            # self.assertEqual(str(condition_list[a]['conditionDesc']), '8.80%')
                            self.assertEqual(str(condition_list[a]['conditionId']), '1')
                            self.assertEqual(str(condition_list[a]['conditionName']), '3-6个月')
                        elif condition_list[a]['conditionId'] == '2':
                            # self.assertEqual(str(condition_list[a]['conditionDesc']), '10.00%')
                            self.assertEqual(str(condition_list[a]['conditionId']), '2')
                            self.assertEqual(str(condition_list[a]['conditionName']), '6个月以上')
                elif data_list[i]['groupId'] == '1':
                    self.assertEqual(str(data_list[i]['groupId']), str(group_id).replace(',', '')[1])
                    self.assertEqual(str(data_list[i]['groupName']), '产品类型')
                    for b in range(0, len(condition_list)):
                        if condition_list[b]['conditionId'] == '-1':
                            self.assertEqual(str(condition_list[b]['conditionDesc']), '')
                            self.assertEqual(str(condition_list[b]['conditionId']), '-1')
                            self.assertEqual(str(condition_list[b]['conditionName']), '全部')
                        elif condition_list[b]['conditionId'] == '0':
                            self.assertEqual(str(condition_list[b]['conditionDesc']), '')
                            self.assertEqual(str(condition_list[b]['conditionId']), '0')
                            self.assertEqual(str(condition_list[b]['conditionName']), '定活宝')
                        elif condition_list[b]['conditionId'] == '1':
                            self.assertEqual(str(condition_list[b]['conditionDesc']), '')
                            self.assertEqual(str(condition_list[b]['conditionId']), '1')
                            self.assertEqual(str(condition_list[b]['conditionName']), '高端现金管理')
                        elif condition_list[b]['conditionId'] == '2':
                            self.assertEqual(str(condition_list[b]['conditionDesc']), '')
                            self.assertEqual(str(condition_list[b]['conditionId']), '2')
                            self.assertEqual(str(condition_list[b]['conditionName']), '高端固定收益')
                        elif condition_list[b]['conditionId'] == '3':
                            self.assertEqual(str(condition_list[b]['conditionDesc']), '')
                            self.assertEqual(str(condition_list[b]['conditionId']), '3')
                            self.assertEqual(str(condition_list[b]['conditionName']), '高端精选权益')
                elif data_list[i]['groupId'] == '2':
                    self.assertEqual(str(data_list[i]['groupId']), str(group_id).replace(',', '')[2])
                    self.assertEqual(str(data_list[i]['groupName']), '起投金额')
                    for c in range(0, len(condition_list)):
                        if condition_list[c]['conditionId'] == '-1':
                            self.assertEqual(str(condition_list[c]['conditionDesc']), '')
                            self.assertEqual(str(condition_list[c]['conditionId']), '-1')
                            self.assertEqual(str(condition_list[c]['conditionName']), '全部')
                        elif condition_list[c]['conditionId'] == '0':
                            self.assertEqual(str(condition_list[c]['conditionDesc']), '')
                            self.assertEqual(str(condition_list[c]['conditionId']), '0')
                            self.assertEqual(str(condition_list[c]['conditionName']), '1分-5万')
                        elif condition_list[c]['conditionId'] == '1':
                            self.assertEqual(str(condition_list[c]['conditionDesc']), '')
                            self.assertEqual(str(condition_list[c]['conditionId']), '1')
                            self.assertEqual(str(condition_list[c]['conditionName']), '5-100万')
                        elif condition_list[c]['conditionId'] == '2':
                            self.assertEqual(str(condition_list[c]['conditionDesc']), '')
                            self.assertEqual(str(condition_list[c]['conditionId']), '2')
                            self.assertEqual(str(condition_list[c]['conditionName']), '100万以上')

    # 交易-获取现金管理支付列表（V3.1)
    @file_data('test_data/test_get_payment_list.json')
    def test_get_payment_list(self, user_name, password, product_id, assert_info):
        self._restful_xjb.get_payment_list(user_name=str(user_name), password=str(password), product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if assert_info["returnCode"] == '000000':
            vacco_asset = self._db.trade_asset_total_home_page(mobile=user_name)
            payment_list = self._db.get_payment_list(mobile=str(user_name))
            data_list = entity.dataList
            for i in range(0, len(data_list)):
                if data_list[i]['productId'] == 'ZX05#000730':
                    self.assertEqual(str(data_list[i]['balance']), str(vacco_asset[0]))
                    self.assertEqual(str(data_list[i]['balanceInfo']),
                                     '余额：' + str(format(vacco_asset[0], ',')) + '元')
                    self.assertEqual(str(data_list[i]['paymentType']), '0')
                    self.assertEqual(str(data_list[i]['productId']), 'ZX05#000730')
                    self.assertIn('现金宝', str(data_list[i]['productName']))
                else:
                    # 根据产品id查出产品名称
                    product_info = self._db.get_product_info(str(payment_list[0]['PROD_ID']))
                    self.assertEqual(str(data_list[i]['balance']),
                                     str(payment_list[0]['BALANCE']))
                    self.assertEqual(str(data_list[i]['balanceInfo']),
                                     '余额：' + str(format(payment_list[0]['BALANCE'], ',')) + '元')
                    self.assertEqual(str(data_list[i]['paymentType']), '7')
                    self.assertEqual(str(data_list[i]['productId']),
                                     str(payment_list[0]['PROD_ID']))
                    self.assertEqual(str(data_list[i]['productName']),
                                     str(product_info[0]['product_short_name']))

    # 产品-全部理财产品列表(V3.1)
    @file_data('test_data/test_get_all_fin_product_list.json')
    def test_get_all_fin_product_list(self, user_name, password, period_id, product_type_id, min_invest_amt_id,
                                      assert_info):
        self._restful_xjb.get_all_fin_product_list(user_name=str(user_name), password=str(password),
                                                   period_id=str(period_id), product_type_id=str(product_type_id),
                                                   min_invest_amt_id=str(min_invest_amt_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        # if entity.returnCode == '000000':
        #     pdc_list = self._db.get_all_fin_product_list(period_id=str(period_id),
        #                                                  product_type_id=str(product_type_id),
        #                                                  min_invest_amt_id=str(min_invest_amt_id))
        #     left_amt = self._db.get_left_quota(period_id=str(period_id), product_type_id=str(product_type_id),
        #                                        min_invest_amt_id=str(min_invest_amt_id))
        #     pdc_list = sorted(pdc_list, key=lambda p: p['float_yield'], reverse=True)
        #     data_list = entity.body_dataList
        #     data_list = sorted(data_list, key=lambda p: p['incomeIntro'], reverse=True)
        #     self.assertEqual(str(entity.body['totalCount']), str(len(pdc_list)))
        # for i in range(0, 5):
        #     j = 5 * (int(str(page_no))-1)+i
        #     self.assertEqual(str(data_list[i]['canRedeemAnytime']), str(pdc_list[j]['is_redem_anytime']))
        #     self.assertEqual(str(data_list[i]['clientType']), str(pdc_list[j]['client_type']))
        #     self.assertEqual(str(data_list[i]['incomeIntro']),
        #                      '--%' if str(pdc_list[j]['float_yield']) == 'null%' else str(decimal.Decimal(pdc_list[j]['float_yield'][:-1]).quantize(decimal.Decimal('0.00')))+'%')
        #     self.assertEqual(str(data_list[i]['leftAmt']).replace(',', ''), str(left_amt['LEFT_QUOTA']))
        #     self.assertEqual(str(data_list[i]['productId']), str(pdc_list[j]['productid']))
        #     self.assertEqual(str(data_list[i]['productIntro']), str(pdc_list[j]['brief_desc']))
        #     self.assertEqual(str(data_list[i]['productTitle']), str(pdc_list[j]['product_short_name']))
        #     self.assertEqual(str(data_list[i]['productType']), str(pdc_list[j]['product_type']))
        #     self.assertEqual(str(data_list[i]['recommended']), str(pdc_list[j]['recommended']))

    # 产品-理财产品介绍(v3.0.0)
    @file_data('test_data/test_get_product_intro.json')
    def test_get_product_intro(self, user_name, password, common_info_type, categary_code, assert_info):
        self._restful_xjb.get_product_intro(user_name=str(user_name), password=str(password),
                                            common_info_type=str(common_info_type))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            pro_intro = self._db.get_pro_intro(user_name=str(user_name), categary_code=str(categary_code))
            self.assertEqual(str(entity.body_detail['desc']), str(pro_intro[2]['value']))
            self.assertEqual(str(entity.body_detail['logoUrl']), str(pro_intro[0]['value']))
            self.assertEqual(str(entity.body_detail['moreInfo']), str(pro_intro[4]['value']))
            self.assertEqual(str(entity.body_detail['moreLink']), str(pro_intro[3]['value']))
            self.assertEqual(str(entity.body_detail['title']), str(pro_intro[1]['value']))

    # 基金-评级机构列表
    @file_data('test_data/test_get_grade_orglist.json')
    def test_get_grade_orglist(self, user_name, password, assert_info):
        self._restful_xjb.get_grade_orglist(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            self.assertEqual(str(entity.body_dataList[0]['gradeOrgId']), '10668')
            self.assertEqual(str(entity.body_dataList[0]['gradeOrgName']), '晨星评级')
            self.assertEqual(str(entity.body_dataList[1]['gradeOrgId']), '41126')
            self.assertEqual(str(entity.body_dataList[1]['gradeOrgName']), '银河证券')
            self.assertEqual(str(entity.body_dataList[2]['gradeOrgId']), '2921')
            self.assertEqual(str(entity.body_dataList[2]['gradeOrgName']), '招商证券')
            self.assertEqual(str(entity.body_dataList[3]['gradeOrgId']), '1770')
            self.assertEqual(str(entity.body_dataList[3]['gradeOrgName']), '海通证券')
            self.assertEqual(str(entity.body_dataList[4]['gradeOrgId']), '18968')
            self.assertEqual(str(entity.body_dataList[4]['gradeOrgName']), '济安金信')
            self.assertEqual(str(entity.body_dataList[5]['gradeOrgId']), '41644')
            self.assertEqual(str(entity.body_dataList[5]['gradeOrgName']), '上海证券')

    # 基金-Shibor
    @file_data('test_data/test_fund_shior_exponent.json')
    def test_get_shibor_exponent(self, user_name, password, assert_info):
        self._restful_xjb.get_shibor_exponent(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            self.assertEqual(str(entity.body_dataList[0]['exponentCode']), '')
            self.assertEqual(str(entity.body_dataList[0]['exponentName']), '隔夜利率')
            self.assertEqual(str(entity.body_dataList[0]['exponentPoint']), '')
            self.assertEqual(str(entity.body_dataList[0]['marketType']), '')
            # self.assertEqual(str(entity.body_dataList[0]['risePercent']), '2.8310%')
            # self.assertEqual(str(entity.body_dataList[0]['risePoint']), '-9.27BP')
            self.assertEqual(str(entity.body_dataList[1]['exponentCode']), '')
            self.assertEqual(str(entity.body_dataList[1]['exponentName']), '1周利率')
            self.assertEqual(str(entity.body_dataList[1]['exponentPoint']), '')
            self.assertEqual(str(entity.body_dataList[1]['marketType']), '')
            # self.assertEqual(str(entity.body_dataList[1]['risePercent']), '2.8879%')
            # self.assertEqual(str(entity.body_dataList[1]['risePoint']), '-3.87BP')
            self.assertEqual(str(entity.body_dataList[2]['exponentCode']), '')
            self.assertEqual(str(entity.body_dataList[2]['exponentName']), '2周利率')
            self.assertEqual(str(entity.body_dataList[2]['exponentPoint']), '')
            self.assertEqual(str(entity.body_dataList[2]['marketType']), '')
            # self.assertEqual(str(entity.body_dataList[2]['risePercent']), '3.7336%')
            # self.assertEqual(str(entity.body_dataList[2]['risePoint']), '-1.64BP')
            self.assertEqual(str(entity.body_dataList[3]['exponentCode']), '')
            self.assertEqual(str(entity.body_dataList[3]['exponentName']), '1个月利率')
            self.assertEqual(str(entity.body_dataList[3]['exponentPoint']), '')
            self.assertEqual(str(entity.body_dataList[3]['marketType']), '')
            # self.assertEqual(str(entity.body_dataList[3]['risePercent']), '3.8920%')
            # self.assertEqual(str(entity.body_dataList[3]['risePoint']), '-1.35BP')
            self.assertEqual(str(entity.body_dataList[4]['exponentCode']), '')
            self.assertEqual(str(entity.body_dataList[4]['exponentName']), '3个月利率')
            self.assertEqual(str(entity.body_dataList[4]['exponentPoint']), '')
            self.assertEqual(str(entity.body_dataList[4]['marketType']), '')
            # self.assertEqual(str(entity.body_dataList[4]['risePercent']), '4.3728%')
            # self.assertEqual(str(entity.body_dataList[4]['risePoint']), '-1.39BP')
            self.assertEqual(str(entity.body_dataList[5]['exponentCode']), '')
            self.assertEqual(str(entity.body_dataList[5]['exponentName']), '6个月利率')
            self.assertEqual(str(entity.body_dataList[5]['exponentPoint']), '')
            self.assertEqual(str(entity.body_dataList[5]['marketType']), '')
            # self.assertEqual(str(entity.body_dataList[5]['risePercent']), '4.3884%')
            # self.assertEqual(str(entity.body_dataList[5]['risePoint']), '-0.84BP')
            self.assertEqual(str(entity.body_dataList[6]['exponentCode']), '')
            self.assertEqual(str(entity.body_dataList[6]['exponentName']), '9个月利率')
            self.assertEqual(str(entity.body_dataList[6]['exponentPoint']), '')
            self.assertEqual(str(entity.body_dataList[6]['marketType']), '')
            # self.assertEqual(str(entity.body_dataList[6]['risePercent']), '4.3945%')
            # self.assertEqual(str(entity.body_dataList[6]['risePoint']), '-0.73BP')
            self.assertEqual(str(entity.body_dataList[7]['exponentCode']), '')
            self.assertEqual(str(entity.body_dataList[7]['exponentName']), '1年利率')
            self.assertEqual(str(entity.body_dataList[7]['exponentPoint']), '')
            self.assertEqual(str(entity.body_dataList[7]['marketType']), '')
            # self.assertEqual(str(entity.body_dataList[7]['risePercent']), '4.4038%')
            # self.assertEqual(str(entity.body_dataList[7]['risePoint']), '-0.95BP')

    # 账户-资产证明预览
    @file_data('test_data/test_get_asset_cert_preview.json')
    def test_get_asset_cert_preview(self, user_name, password, assert_info):
        self._restful_xjb.get_asset_cert_preview(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            self.assertTrue('cust/assetCertPreview?token=' in str(entity.body['pdfUrl']))

    # 基金-首页沪深指数
    @file_data('test_data/test_repay_check.json')
    def test_csi_exponent(self, user_name, password, assert_info):
        self._restful_xjb.csi_exponent(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.dataList[0]['exponentCode'], '000001')
        self.assertEqual(entity.dataList[0]['exponentName'], '上证指数')
        self.assertEqual(entity.dataList[0]['marketType'], '1')
        self.assertEqual(entity.dataList[1]['exponentCode'], '399001')
        self.assertEqual(entity.dataList[1]['exponentName'], '深证成指')
        self.assertEqual(entity.dataList[1]['marketType'], '0')

    # 基金-市场指数
    @file_data('test_data/test_repay_check.json')
    def test_maket_exponent(self, user_name, password, assert_info):
        self._restful_xjb.maket_exponent(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        for i in range(0, len(entity.dataList)):
            if entity.dataList[i]['type'] == '1':
                self.assertEqual(entity.dataList[i]['type'], '1')
                self.assertEqual(entity.dataList[i]['name'], '综合指数')
                data_list1 = entity.dataList[i]['dataList']
                self.assertEqual(data_list1[0]['exponentCode'], '000001')
                self.assertEqual(data_list1[0]['exponentName'], '上证指数')
                self.assertEqual(data_list1[0]['marketType'], '1')
                self.assertEqual(data_list1[1]['exponentCode'], '399001')
                self.assertEqual(data_list1[1]['exponentName'], '深证成指')
                self.assertEqual(data_list1[1]['marketType'], '0')
                self.assertEqual(data_list1[2]['exponentCode'], '399006')
                self.assertEqual(data_list1[2]['exponentName'], '创业板指')
                self.assertEqual(data_list1[2]['marketType'], '0')
                self.assertEqual(data_list1[3]['exponentCode'], '399005')
                self.assertEqual(data_list1[3]['exponentName'], '中小板指')
                self.assertEqual(data_list1[3]['marketType'], '0')
                self.assertEqual(data_list1[4]['exponentCode'], '000002')
                self.assertEqual(data_list1[4]['exponentName'], 'A股指数')
                self.assertEqual(data_list1[4]['marketType'], '1')
                self.assertEqual(data_list1[5]['exponentCode'], '000300')
                self.assertEqual(data_list1[5]['exponentName'], '沪深300')
                self.assertEqual(data_list1[5]['marketType'], '1')
            elif entity.dataList[i]['type'] == '2':
                self.assertEqual(entity.dataList[i]['type'], '2')
                self.assertEqual(entity.dataList[i]['name'], '上证指数')
                data_list2 = entity.dataList[i]['dataList']
                self.assertEqual(data_list2[0]['exponentCode'], '000016')
                self.assertEqual(data_list2[0]['exponentName'], '上证50')
                self.assertEqual(data_list2[0]['marketType'], '1')
                self.assertEqual(data_list2[1]['exponentCode'], '000010')
                self.assertEqual(data_list2[1]['exponentName'], '上证180')
                self.assertEqual(data_list2[1]['marketType'], '1')
                self.assertEqual(data_list2[2]['exponentCode'], '000009')
                self.assertEqual(data_list2[2]['exponentName'], '上证380')
                self.assertEqual(data_list2[2]['marketType'], '1')
            elif entity.dataList[i]['type'] == '3':
                self.assertEqual(entity.dataList[i]['type'], '3')
                self.assertEqual(entity.dataList[i]['name'], '中证指数')
                data_list3 = entity.dataList[i]['dataList']
                self.assertEqual(data_list3[0]['exponentCode'], '000903')
                self.assertEqual(data_list3[0]['exponentName'], '中证100')
                self.assertEqual(data_list3[0]['marketType'], '1')
                self.assertEqual(data_list3[1]['exponentCode'], '000905')
                self.assertEqual(data_list3[1]['exponentName'], '中证500')
                self.assertEqual(data_list3[1]['marketType'], '1')
                self.assertEqual(data_list3[2]['exponentCode'], '000906')
                self.assertEqual(data_list3[2]['exponentName'], '中证380')
                self.assertEqual(data_list3[2]['marketType'], '1')
            elif entity.dataList[i]['type'] == '4':
                self.assertEqual(entity.dataList[i]['type'], '4')
                self.assertEqual(entity.dataList[i]['name'], '深证指数')
                data_list4 = entity.dataList[i]['dataList']
                self.assertEqual(data_list4[0]['exponentCode'], '399106')
                self.assertEqual(data_list4[0]['exponentName'], '深证综指')
                self.assertEqual(data_list4[0]['marketType'], '0')
                self.assertEqual(data_list4[1]['exponentCode'], '399009')
                self.assertEqual(data_list4[1]['exponentName'], '深证200')
                self.assertEqual(data_list4[1]['marketType'], '0')
                self.assertEqual(data_list4[2]['exponentCode'], '399004')
                self.assertEqual(data_list4[2]['exponentName'], '深证100R')
                self.assertEqual(data_list4[2]['marketType'], '0')

    # 账户-登录是否显示图片验证码
    @file_data('test_data/test_is_display_captcha_code.json')
    def test_is_display_captcha_code(self, user_name, password, assert_info):
        self._restful_xjb.is_display_captcha_code(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.isDisplayCaptchaCode, '0')

    # 账户-查询交易密码审核状态信息
    @file_data('test_data/test_is_display_captcha_code.json')
    def test_trade_password_check_info(self, user_name, password, assert_info):
        self._restful_xjb.trade_password_check_info(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.status, '')

    # 账户-二维码保存到本地
    @file_data('test_data/test_save_to_local.json')
    def test_save_to_local(self, user_name, password, assert_info):
        self._restful_xjb.save_to_local(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertTrue('Background.png' in str(entity.body['imageUrl']))

    # 交易-高端报价式年化业绩比较基准
    @file_data('test_data/test_vip_rate_history.json')
    def test_vip_rate_history(self, user_name, password, product_id, assert_info):
        self._restful_xjb.vip_rate_history(user_name=str(user_name), password=str(password), product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if entity.returnCode == '000000':
            pdc_yield_cfg = self._db.get_vip_rate(product_id=str(product_id))
            # 6% 转换成 6.00%
            year_yield_show = '%s%%' % str(decimal.Decimal(str(pdc_yield_cfg[0]['year_yield_show']).replace('%', ''))
                                           .quantize(decimal.Decimal('0.00')))
            self.assertEqual(entity.rate, year_yield_show)
            self.assertIn(pdc_yield_cfg[0]['share_carry_date'] + '-' + pdc_yield_cfg[0]['share_next_carry_date'],
                          str(entity.timeSection).replace('/', ''))

    # 交易-高端报价式产品修改到期处理方式提示信息
    @file_data('test_data/test_modify_expire_dispose_type_tip.json')
    def test_modify_expire_dispose_type_tip(self, user_name, password, expire_dispose_type, product_id, value_date,
                                            expire_date, assert_info):
        self._restful_xjb.modify_expire_dispose_type_tip(user_name=str(user_name), password=str(password),
                                                         expire_dispose_type=str(expire_dispose_type),
                                                         product_id=str(product_id), value_date=str(value_date),
                                                         expire_date=str(expire_date))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertIn('温馨提示：\n有0期产品在' + expire_date + '到期，请先赎回起息日较早产品（CI高端报价式产品，起息日-），'
                                                      '全部赎回起息日较早的产品后方可赎回该产品。', entity.info)

    # 修改手机号码-发送原手机短信
    @file_data('test_data/test_modify_mobile_get_old_mobile_code.json')
    def test_modify_mobile(self, mobile_old, login_password, trade_password, mobile_new, assert_info):
        self._restful_xjb.modify_mobile(mobile_old=str(mobile_old), login_password=str(login_password),
                                        trade_password=str(trade_password), mobile_new=str(mobile_new))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if entity.returnCode == '000000':
            self.assertEqual(str(entity.body['result']),
                             '您手机尾号' + '[' + str(mobile_new)[7:] + ']' + '的手机绑定成功！')
            time.sleep(60)
            self._restful_xjb.modify_mobile(mobile_old=str(mobile_new), login_password=str(login_password),
                                            trade_password=str(trade_password), mobile_new=str(mobile_old))
        if entity.returnCode == '081002':
            self.assertEqual(str(entity.returnMsg), '该手机号已注册')
            self.assertEqual(str(entity.showType), '0')
        if entity.returnCode == '030049':
            self.assertEqual(str(entity.returnMsg), '短信发送已达上限')
            self.assertEqual(str(entity.showType), '0')
        if entity.returnCode == '030016':
            self.assertEqual(str(entity.returnMsg), '短信发送过于频繁，请稍后再试')
            self.assertEqual(str(entity.showType), '0')

    # 账户-查询修改手机号码审核状态信息
    @file_data('test_data/test_modify_mobile_check_info.json')
    def test_modify_mobile_check_info(self, user_name, password, assert_info):
        self._restful_xjb.get_modify_mobile_check_info(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            mobile_audit_list = self._db.get_modify_mobile_check_info(user_name=str(user_name))
            if str(mobile_audit_list[0]['status']) == 'S':
                self.assertEqual(str(entity.body['status']), '')
            else:
                self.assertEqual(str(entity.body['status']), str(mobile_audit_list[0]['status']))
                if str(mobile_audit_list[0]['status']) == 'F':
                    self.assertTrue(str(entity.body['info']), '审核不通过，原因：。如有疑问，请联系客服，联系电话：' in str(entity.body['info']))
                if str(mobile_audit_list[0]['status']) == 'I':
                    self.assertTrue(str(entity.body['info']),
                                    '正在审核中，请耐心等待！如有疑问，请联系客服，联系电话：' in str(entity.body['info']))
                if str(mobile_audit_list[0]['status']) == 'S':
                    self.assertEqual(str(entity.body['info']), '')
                if str(mobile_audit_list[0]['status']) == 'R':
                    self.assertTrue(str(entity.body['info']), '待审核' in str(entity.body['info']))

    # 交易-高端报价式产品修改到期处理方式
    @file_data('test_data/test_modify_expire_dispose_type.json')
    def test_modify_expire_dispose_type(self, user_name, password, expire_dispose_type, expire_quit_amt, product_id,
                                        value_date, trade_password, assert_info):
        self._restful_xjb.modify_expire_dispose_type(user_name=str(user_name), password=str(password),
                                                     expire_dispose_type=str(expire_dispose_type),
                                                     expire_quit_amt=str(expire_quit_amt), product_id=str(product_id),
                                                     value_date=str(value_date), trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            prod_quty_detail, prod_renew = self._db.test_modify_expire_dispose_type_db(user_name=str(user_name),
                                                                                       product_id=str(product_id),
                                                                                       value_date=str(value_date))
            self.assertEqual(str(entity.body['returnResult']), 'Y')
            self.assertEqual(str(entity.body['title']), '修改已成功')

            self.assertEqual(str(prod_quty_detail[0]['prod_id']), str(product_id))
            self.assertEqual(str(prod_quty_detail[0]['value_date']), str(value_date))

            self.assertEqual(str(prod_renew[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(prod_renew[0]['VALUE_DATE']), str(value_date))
            if str(expire_dispose_type) == '0':
                self.assertEqual(str(prod_renew[0]['DUE_PROCESS_TYPE']), 'AO')
                self.assertEqual(str(prod_renew[0]['RED_AMT']), '0.00')
            if str(expire_dispose_type) == '1':
                self.assertEqual(str(prod_quty_detail[0]['prod_id']), str(product_id))
                self.assertEqual(str(prod_quty_detail[0]['value_date']), str(value_date))
                self.assertEqual(str(prod_renew[0]['DUE_PROCESS_TYPE']), 'AR')
                self.assertEqual(str(prod_renew[0]['RED_AMT']),
                                 str(decimal.Decimal(expire_quit_amt).quantize(decimal.Decimal('0.00'))))

    # 现金管理作为支付手段(交易-购买 V3.1)
    @file_data('test_data/test_purchase_product_by_cash_managment_product.json')
    def test_purchase_product_by_cash_managment_product(self, user_name, password, product_id, pay_type,
                                                        amt,
                                                        pay_product_id, trade_password, assert_info):
        self._restful_xjb.buy_product_using_cash_management(user_name=str(user_name),
                                                            login_password=str(password),
                                                            product_id=str(product_id),
                                                            pay_type=str(pay_type),
                                                            amt=str(amt),
                                                            pay_product_id=str(pay_product_id),
                                                            trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if str(assert_info["returnCode"]) == '000000':
            self._db.insert_prod_quty(user_name=str(user_name), product_id=str(product_id), amt=str(amt))
            self.assertIn('确认份额', str(entity.info))
            self.assertEqual(str(entity.returnResult), 'Y')
            self.assertEqual(str(entity.title), '申请已受理')
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))

            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), str(pay_product_id))
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '3')
            self.assertEqual(str(trade_order[0]['STATUS']), 'A')
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
            if str(product_id).__contains__('H9'):
                # 012-买入，012031-类货基认购
                self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
                self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012031')
                self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
                self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '3')
            elif str(product_id).__contains__('05'):
                self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '013')
                self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '013031')
                self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
                self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '2')
            else:  # 定活宝认购
                self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
                self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012031')
                self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
                self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '1')

            # 申购基金产品，验证CTS_TRADE_REQUEST表，申购基金、高端赎回
            if str(product_id).__contains__('05'):
                self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
                self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
                self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
                self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['RTTA_ST']), 'N')
                self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
                if str(trade_request[0]['PROD_ID']) == str(product_id):
                    # 022 申购
                    self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
                    self.assertEqual(str(trade_request[0]['PROD_TYPE']), '2')
                    self.assertEqual(str(trade_request[0]['PURCHASE_PAYMENT_TYPE']), '7')
                    self.assertEqual(str(trade_request[0]['REDEEM_PAYMENT_TYPE']), '0')
                    self.assertEqual(str(trade_request[0]['APKIND']), '022')
                    self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022221')
                    self.assertEqual(str(trade_request[0]['TANO']), str(product_id).split('#')[0])
                    self.assertEqual(str(trade_request[0]['SUB_AMT']),
                                     str(decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
                elif str(trade_request[0]['PROD_ID']) == str(pay_product_id):
                    # 024 赎回
                    self.assertEqual(str(trade_request[0]['PROD_TYPE']), '3')
                    self.assertEqual(str(trade_request[0]['PROD_ID']), str(pay_product_id))
                    self.assertEqual(str(trade_request[0]['TANO']), str(product_id).split('#')[0])
                    self.assertEqual(str(trade_request[0]['BALANCE']),
                                     str(decimal.Decimal(-amt).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(str(trade_request[0]['APKIND']), '024')
                    self.assertEqual(str(trade_request[0]['SUB_APKIND']), '024028')
                    self.assertEqual(str(trade_request[0]['PAY_ST']), 'N')

            # 认购高端产品，验证CTS_TRADE_RESERVE表
            if str(product_id).__contains__('H9'):
                self.assertEqual(str(trade_reserve[0]['SHARE_TYPE']), 'A')
                self.assertEqual(str(trade_reserve[0]['BRANCH_CODE']), '675')
                self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
                if str(trade_reserve[0]['PROD_ID']) == str(product_id):
                    # 020 认购
                    self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(product_id))
                    self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '3')
                    self.assertEqual(str(trade_reserve[0]['PURCHASE_PAYMENT_TYPE']), '0')
                    self.assertEqual(str(trade_reserve[0]['REDEEM_PAYMENT_TYPE']), '0')
                    self.assertEqual(str(trade_reserve[0]['APKIND']), '020')
                    self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '020051')
                    self.assertEqual(str(trade_reserve[0]['TANO']), str(product_id).split('#')[0])
                    self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
                                     str(decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
                elif str(trade_reserve[0]['PROD_ID']) == str(pay_product_id):
                    # 024 赎回
                    self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '3')
                    self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(pay_product_id))
                    self.assertEqual(str(trade_reserve[0]['TANO']), str(product_id).split('#')[0])
                    self.assertEqual(str(trade_reserve[0]['BALANCE']),
                                     str(decimal.Decimal(-amt).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(str(trade_reserve[0]['APKIND']), '024')
                    self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '024025')

            # 认购定活宝产品，验证CTS_TRADE_REQUEST表，认购定活宝、高端赎回
            if str(product_id).__contains__('899'):
                self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
                self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
                self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
                self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['RTTA_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
                if str(trade_request[0]['PROD_ID']) == str(product_id):
                    # 020 认购
                    self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
                    self.assertEqual(str(trade_request[0]['PROD_TYPE']), '1')
                    self.assertEqual(str(trade_request[0]['PURCHASE_PAYMENT_TYPE']), '7')
                    self.assertEqual(str(trade_request[0]['REDEEM_PAYMENT_TYPE']), '0')
                    self.assertEqual(str(trade_request[0]['APKIND']), '020')
                    self.assertEqual(str(trade_request[0]['SUB_APKIND']), '020100')
                    self.assertEqual(str(trade_request[0]['TANO']), str(product_id).split('#')[0])
                    self.assertEqual(str(trade_request[0]['SUB_AMT']),
                                     str(decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
                elif str(trade_request[0]['PROD_ID']) == str(pay_product_id):
                    # 024 赎回
                    self.assertEqual(str(trade_request[0]['PROD_TYPE']), '3')
                    self.assertEqual(str(trade_request[0]['PROD_ID']), str(pay_product_id))
                    self.assertEqual(str(trade_request[0]['TANO']), str(product_id).split('#')[0])
                    self.assertEqual(str(trade_request[0]['BALANCE']),
                                     str(decimal.Decimal(-amt).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(str(trade_request[0]['APKIND']), '024')
                    self.assertEqual(str(trade_request[0]['SUB_APKIND']), '024054')
                    self.assertEqual(str(trade_request[0]['PAY_ST']), 'N')
            self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(asset_in_trasit[0]['BRANCH_CODE']), '675')

            if str(asset_in_trasit[0]['PROD_ID']) == str(product_id):
                self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(product_id))
                self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
                self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                                 str(decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
                if str(product_id).__contains__('H9'):
                    self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '3')
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '020051')
                elif str(product_id).__contains__('05'):
                    self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '2')
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '022')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '022221')
                else:
                    self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '1')
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '020100')

            elif str(asset_in_trasit[0]['PROD_ID']) == str(pay_product_id):
                # 024 赎回
                self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '3')
                self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(pay_product_id))
                self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
                self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                                 str(decimal.Decimal(-amt).quantize(decimal.Decimal('0.00'))))
                if str(product_id).__contains__('H9'):
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '024')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '024025')
                elif str(product_id).__contains__('05'):
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '024')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '024028')
                else:
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '024')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '024054')

    # 账户-资产证明申请记录
    @file_data('test_data/test_assert_cert_apply_record.json')
    def test_get_asset_cert_apply_record(self, user_name, password, page_size, assert_info):
        self._restful_xjb.get_assert_cert_apply_record(user_name=str(user_name), password=str(password),
                                                       page_size=str(page_size))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            asset_cert = self._db.get_asset_cert_apply_record(user_name=str(user_name))
            if len(asset_cert) > 0:
                total_count = (len(asset_cert) / int(page_size)) if len(asset_cert) % int(page_size) == 0 else (
                    len(asset_cert) / int(page_size) + 1)
                self.assertEqual(str(entity.body['totalCount']), str(total_count))
                for i in range(0, int(page_size)):
                    self.assertEqual(str(entity.body_dataList[i]['address']),
                                     '' if str(asset_cert[i]['address']) == 'None' else str(asset_cert[i]['address']))
                    self.assertEqual(str(entity.body_dataList[i]['applyTime']), str(asset_cert[i]['created_at'])[5:19])
                    self.assertEqual(str(entity.body_dataList[i]['email']), str(asset_cert[i]['email']))
                    self.assertEqual(str(entity.body_dataList[i]['groupTime']), str(asset_cert[i]['created_at'])[0:10])
                    self.assertEqual(str(entity.body_dataList[i]['mobile']), str(asset_cert[i]['mobile']))
                    self.assertEqual(str(entity.body_dataList[i]['recordId']), str(asset_cert[i]['id']))
                    self.assertEqual(str(entity.body_dataList[i]['sendType']),
                                     '0' if str(asset_cert[i]['deliver_type']) == 'E' else '1')
                    self.assertEqual(str(entity.body_dataList[i]['sendTypeInfo']),
                                     '邮箱发送' if str(entity.body_dataList[i]['sendType']) == '0' else '线下寄送')
                    self.assertEqual(str(entity.body_dataList[i]['status']), str(asset_cert[i]['status']))
                    status_info = ''
                    if str(asset_cert[i]['status']) == 'I':
                        status_info = '待处理'
                    elif str(asset_cert[i]['status']) == 'R':
                        status_info = '待审核'
                    elif str(asset_cert[i]['status']) == 'S':
                        status_info = '审核通过'
                    else:
                        status_info = '审核拒绝'
                    self.assertEqual(str(entity.body_dataList[i]['statusInfo']), status_info)
            else:
                self.assertEqual(str(entity.body['totalCount']), '0')

    # 账户-资产证明发送方式tip
    @file_data('test_data/test_asset_send_type_info.json')
    def test_get_asset_send_type_info(self, user_name, password, assert_info):
        self._restful_xjb.get_asset_send_type_info(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        self.assertEqual(str(entity.body['emailInfo']), '3个工作日内发送')
        self.assertEqual(str(entity.body['offlineInfo']), '3个工作日内使用顺丰快递寄出')

    # 账户-查询我的邀请人
    @file_data('test_data/test_query_my_inviter.json')
    def test_query_my_inviter(self, user_name, password, assert_info):
        self._restful_xjb.query_my_inviter(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if entity.returnCode == '000000':
            inviter_info = self._db.query_my_inviter(user_name=str(user_name))
            if len(inviter_info) == 0:
                self.assertEqual(entity.mobile, '')
            else:
                self.assertEqual(entity.mobile, inviter_info[0]['inviter_mobile'])

    # 账户-设置我的邀请人
    @file_data('test_data/test_set_my_inviter.json')
    def test_set_my_inviter(self, user_name, password, mobile, assert_info):
        self._restful_xjb.set_my_inviter(user_name=str(user_name), password=str(password), mobile=str(mobile))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if entity.returnCode == '000000':
            inviter_info = self._db.query_my_inviter(user_name=str(user_name))
            self.assertEqual(mobile, str(inviter_info[0]['inviter_mobile']))

    # 账户-获取省市
    @file_data('test_data/test_get_province_and_city.json')
    def test_get_province_and_city(self, user_name, password, assert_info):
        self._restful_xjb.get_province_and_city(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertIsNotNone(entity.version)

    # 账户-查询个人账户信息
    @file_data('test_data/test_account_info.json')
    def test_get_account_info(self, user_name, password, assert_info):
        self._restful_xjb.get_account_info(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            card_improve, points_amount = self._db.get_account_info(user_name=str(user_name))
            activate_count = self._db.get_activate_card_count(user_name=str(user_name))
            pldge_amount = self._db.get_pldge_amount(user_name=str(user_name))

            if len(points_amount) == 0 or str(points_amount[0]['AMOUNT']) == '0.00':
                self.assertTrue('去赚积分' in str(entity.body['pointsInfo']))
            else:
                self.assertTrue(str(decimal.Decimal(points_amount[0]['AMOUNT'])) in str(entity.body['pointsInfo']))
            if card_improve != 0 and activate_count == 0:
                self.assertEqual(str(entity.body['bankCardInfo']), '您有' + str(card_improve) + '张银行卡可升级')
            if card_improve == 0 and activate_count != 0:
                self.assertEqual(str(entity.body['bankCardInfo']), '您有' + str(activate_count) + '张银行卡可激活')
            if card_improve != 0 and activate_count != 0:
                self.assertEqual(str(entity.body['bankCardInfo']),
                                 '您有' + str(card_improve + activate_count) + '张银行卡可操作')
            if card_improve == 0 and activate_count == 0:
                self.assertEqual(str(entity.body['bankCardInfo']), '')
            self.assertEqual(str(entity.body['repayAmt']), str('' if pldge_amount == 0 else pldge_amount))

    # 账户-修改账户基本信息
    @file_data('test_data/test_update_cust_base_info.json')
    def test_update_cust_base_info(self, user_name, password, email, address, pcIds, area, assert_info):
        self._restful_xjb.update_cust_base_info(user_name=str(user_name), password=str(password), email=str(email),
                                                address=str(address), pcIds=str(pcIds), area=str(area))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            cust_detail, cust_address = self._db.update_cust_base_info(user_name=str(user_name))
            self.assertEqual(str(cust_detail[0]['email']), str(email))
            self.assertEqual(str(cust_address[0]['address_code']), str(pcIds))
            self.assertEqual(str(cust_address[0]['address']), str(address))
            self.assertEqual(str(cust_address[0]['address_detail']), str(area))

        if entity.returnCode == '030126':
            self.assertEqual(str(entity.returnMsg), '邮箱格式不正确')
            self.assertEqual(str(entity.showType), '0')

    # 交易-质押还款明细
    @file_data('test_data/test_load_repay_detail_list.json')
    def test_loan_repay_detail_list(self, user_name, password, my_loan_id, assert_info):
        self._restful_xjb.loan_repay_detail_list(user_name=str(user_name), password=str(password),
                                                 my_loan_id=str(my_loan_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            if str(entity.body['totalCount']) > '0':
                pledge_repay_record = self._db.get_loan_repay_detail_list(user_name=str(user_name),
                                                                          my_loan_id=str(my_loan_id))
                self.assertEqual(str(pledge_repay_record[0]['REPAY_AMT']),
                                 str(entity.body_dataList[0]['alreadyRepayAmt']))
                self.assertEqual(str(pledge_repay_record[0]['PLEDGE_AMT']),
                                 str(entity.body_dataList[0]['alreadyRepayCapitalAmt']))
                self.assertEqual(str(pledge_repay_record[0]['INTEREST'] + pledge_repay_record[0]['PENALTY']),
                                 str(entity.body_dataList[0]['alreadyRepayInterestAmt']))
                self.assertEqual(str(entity.body_dataList[0]['repayDate']),
                                 str(pledge_repay_record[0]['WORK_DATE'])[0:4] + '-' +
                                 str(pledge_repay_record[0]['WORK_DATE'])[4:6] + '-' +
                                 str(pledge_repay_record[0]['WORK_DATE'])[6:8])
                self.assertEqual(str(entity.body_dataList[0]['repayType']), str(pledge_repay_record[0]['REPAY_TYPE']))
                self.assertEqual(str(entity.body['totalCount']), str(len(pledge_repay_record)))
            else:
                self.assertEqual(str(entity.body['dataList']), '[]')
                self.assertEqual(str(entity.body['totalCount']), '0')
        if entity.returnCode == '081578':
            self.assertEqual(str(entity.returnMsg), '质押id为空')

    # 激活中信联名卡
    @file_data('test_data/test_citic_activate_card.json')
    def test_citic_activate_card(self, user_name, password, card_no, brand_type, bank_no, assert_info):
        # 绑卡前判断卡信息是否被删除
        credit_cards = self._db.get_cust_credit_card_by_card_no(card_no=str(6229180024840002))
        if len(credit_cards) != 0:
            # 修改激活联名卡的状态为未激活
            self._db.update_ecitic_active_status(user_name=str(user_name))
            # 删除该用户下的信用卡
            self._db.del_cust_credit_card(mobile=str(user_name))

        self._restful_xjb.activate_citic_card(user_name=str(user_name), password=str(password),
                                              card_no=str(card_no), brand_type=str(brand_type), bank_no=str(bank_no))
        entity = self._restful_xjb.entity.current_entity
        self.assertIn(assert_info["returnMsg"], entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            credit_cards = self._db.get_cust_credit_card_by_card_no(card_no=str(card_no))
            credit_ecitic_brand_card = self._db.get_credit_ecitic_brand_card(user_name=str(user_name))
            self.assertEqual(str(credit_cards[0]['bank_name']), '中信银行')
            self.assertEqual(str(credit_cards[0]['mobile']), str(user_name))
            self.assertEqual(str(credit_cards[0]['card_no']), str(card_no))
            self.assertEqual(str(credit_cards[0]['bind_date']),
                             str(Utility.DateUtil().getToday()).replace('-', ''))
            self.assertEqual(str(credit_cards[0]['state']), 'N')
            self.assertEqual(str(credit_cards[0]['brand_type']), 'ZX_JK')
            self.assertEqual(str(credit_cards[0]['accept_mode']), 'M')

            self.assertEqual(str(credit_ecitic_brand_card[0]['brand_type']), str(credit_cards[0]['brand_type']))
            time.sleep(1)
            self.assertEqual(str(credit_ecitic_brand_card[0]['is_active']), '1')

            # 修改激活联名卡的状态为未激活
            self._db.update_ecitic_active_status(user_name=str(user_name))
            # 删除该用户下的信用卡
            self._db.del_cust_credit_card(mobile=str(user_name))

    # 交易-质押还款
    @file_data('test_data/test_loan_repay_apply.json')
    def test_loan_repay_apply(self, user_name, password, product_id, my_loan_id, repay_capital_amt, repay_amt,
                              trade_password, assert_info):
        pledge_loan, loan_repay_amt, remain_loan_amt = self._db.get_loan_repay_amt(user_name=str(user_name))
        pledge_replay_plan = self._db.get_pledge_replay_plan(user_name=str(user_name))
        # 借款天数 = 今天 - 借款时间
        borrow_days = (datetime.datetime.now() -
                       datetime.datetime.strptime(str(pledge_loan['START_DATE']), '%Y%m%d')).days
        # 每日利息
        interest = BusinessUtility().cal_interest(str(pledge_loan['PLEDGE_AMT']),
                                                  str(pledge_loan['INTEREST_RATE']),
                                                  str(1))
        # 目前已还总利息
        sum_interest = BusinessUtility().cal_interest(str(pledge_loan['PLEDGE_AMT']),
                                                      str(pledge_loan['INTEREST_RATE']),
                                                      str(borrow_days))
        # 还款利率
        repay_interest = BusinessUtility().cal_repay_interest(repay_amt=str(repay_amt),
                                                              borrow_amt=str(pledge_replay_plan[0]['PLEDGE_AMT']),
                                                              interest=str(pledge_replay_plan[0]['INTEREST']))
        # 还款本息
        repay_amt = round(decimal.Decimal(repay_amt) + decimal.Decimal(repay_interest), 2)

        self._restful_xjb.loan_repay_apply(user_name=str(user_name), password=str(password),
                                           product_id=str(product_id), my_loan_id=str(my_loan_id),
                                           repay_capital_amt=str(repay_capital_amt), repay_amt=str(repay_amt),
                                           trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertIn(assert_info["returnMsg"], entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            pledge_replay_plan = self._db.get_pledge_replay_plan(user_name=str(user_name))
            pledge_repay_record = self._db.pledge_repay_record(user_name=str(user_name))

            # 解压份额 = 原本质押份额 - 仍然需要质押的份额
            total_pledge_quty = pledge_replay_plan[0]['PLEDGE_QUTY']
            total_repay_amt = pledge_replay_plan[0]['AMOUNT']
            pledge_rate = pledge_replay_plan[0]['PLEDGE_RATE']
            repay_amt_before = 0.00
            pledge_quty_before = 0.00
            if len(pledge_repay_record) == 1:
                pledge_quty = BusinessUtility().cal_pledge_quty(total_pledge_quty=str(total_pledge_quty),
                                                                total_repay_amt=str(total_repay_amt),
                                                                repay_amt=str(repay_amt),
                                                                pledge_rate=str(pledge_rate),
                                                                repay_amt_before=None, pledge_quty_before=None)
                pledge_quty = decimal.Decimal(round(pledge_quty + 0.004), 2).quantize(decimal.Decimal('0.00'))
            else:
                for i in range(1, len(pledge_repay_record)):
                    repay_amt_before += float(pledge_repay_record[i]['REPAY_AMT'])
                    pledge_quty_before += float(pledge_repay_record[i]['PLEDGE_QUTY'])
                # 有多笔还款记录
                pledge_quty = BusinessUtility().cal_pledge_quty(total_pledge_quty=str(total_pledge_quty),
                                                                total_repay_amt=str(total_repay_amt),
                                                                repay_amt=str(repay_amt),
                                                                pledge_rate=str(pledge_rate),
                                                                repay_amt_before=str(repay_amt_before),
                                                                pledge_quty_before=str(pledge_quty_before))
                if pledge_quty > 0:
                    pledge_quty = decimal.Decimal(round(pledge_quty + decimal.Decimal(0.004), 2)).quantize(
                        decimal.Decimal('0.00'))
                elif pledge_quty <= 0.0:
                    pledge_quty = '0.00'

            self.assertEqual(entity.title, '现金宝还款申请成功！')

            # 032 份额解冻
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['STATUS']), 'Y')
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(repay_amt)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '032')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '032010')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '3')
            # self.assertEqual(str(trade_order[0]['PLEDGE_ORDER_NO']), str(my_loan_id))

            # 有两条记录，一条质押份额解冻，一条现金宝赎回
            self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            if str(trade_request[0]['PROD_ID']) == str(product_id):
                self.assertEqual(str(trade_request[0]['RTTA_ST']), 'N')
                self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
                self.assertEqual(str(trade_request[0]['TANO']), str(product_id).split('#')[0])
                self.assertEqual(str(trade_request[0]['PROD_TYPE']), '3')
                self.assertEqual(str(trade_request[0]['APKIND']), '032')
                self.assertEqual(str(trade_request[0]['SUB_APKIND']), '032003')
                # 金额为解冻的份额
                self.assertEqual(str(trade_request[0]['SUB_AMT']), str(pledge_quty))
            elif str(trade_request[0]['PROD_ID']) == 'ZX05#000730':
                self.assertEqual(str(trade_request[0]['RTTA_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['PROD_ID']), 'ZX05#000730')
                self.assertEqual(str(trade_request[0]['TANO']), 'ZX05')
                self.assertEqual(str(trade_request[0]['PROD_TYPE']), '0')
                self.assertEqual(str(trade_request[0]['APKIND']), '098')
                self.assertEqual(str(trade_request[0]['SUB_APKIND']), '098003')
                self.assertEqual(str(trade_request[0]['SUB_AMT']),
                                 str(decimal.Decimal(repay_amt).quantize(decimal.Decimal('0.00'))))

            # 验证质押还款计划表，自动还款跑job更新该表
            # 本金 = D-1日凌晨应还本金 - D-1日当日还款本金即在00：05更新的时候，将昨日的PLEDGE_AMT减去所有record中还款成功的本金
            # 未还的本金+利息+罚息
            # self.assertEqual(str(pledge_replay_plan[0]['AMOUNT']), str(decimal.Decimal(remain_loan_amt) +
            #                                                            decimal.Decimal(sum_interest).quantize(
            #                                                                decimal.Decimal(0.00))))
            # 质押的金额
            # self.assertEqual(str(pledge_replay_plan[0]['PLEDGE_QUTY']), str(pledge_quty))
            # 待还款本金
            # self.assertEqual(str(pledge_replay_plan[0]['PLEDGE_AMT']), str(remain_loan_amt))
            self.assertEqual(str(pledge_replay_plan[0]['PLEDGE_RATE']), '0.8000')
            self.assertEqual(str(pledge_replay_plan[0]['INTEREST_RATE']), str(pledge_loan['INTEREST_RATE']))
            self.assertEqual(str(pledge_replay_plan[0]['PENALTY_RATE']), '0.066000')
            # 待还本金 * 利率
            # self.assertEqual(str(pledge_replay_plan[0]['INTEREST']), str(sum_interest))
            self.assertEqual(str(pledge_replay_plan[0]['PENALTY']), '0.00')
            # 已还质押份额
            # self.assertEqual(str(pledge_replay_plan[0]['PAID_PLEDGE_QUTY']), '0.00')
            # 已还质押金额 = 已还本金
            # self.assertEqual(str(pledge_replay_plan[0]['PAID_PLEDGE_AMT']), str(loan_repay_amt))
            # self.assertEqual(str(pledge_replay_plan[0]['PAID_INTEREST']), '0.00')
            # self.assertEqual(str(pledge_replay_plan[0]['PAID_PENALTY']), '0.00')
            self.assertEqual(str(pledge_replay_plan[0]['START_DATE']), '20170918')
            self.assertEqual(str(pledge_replay_plan[0]['SCHEDULE_END_DATE']), '20181227')
            self.assertEqual(str(pledge_replay_plan[0]['STATUS']), 'UNPAID')

            # 验证质押还款记录表（每个自然日24：00会清除到历史表中）
            self.assertEqual(str(pledge_repay_record[0]['LOAN_ID']), str(pledge_replay_plan[0]['ID']))
            self.assertEqual(str(pledge_repay_record[0]['REPAY_PLAN_ID']), str(pledge_replay_plan[0]['ID']))
            self.assertEqual(str(pledge_repay_record[0]['REPAY_AMT']),
                             str(decimal.Decimal(repay_amt).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(pledge_repay_record[0]['PLEDGE_AMT']),
                             str(decimal.Decimal(repay_capital_amt).quantize(decimal.Decimal('0.00'))))
            # 质押份额
            self.assertEqual(str(pledge_repay_record[0]['PLEDGE_QUTY']), str(pledge_quty))
            # 还的利息
            self.assertEqual(str(pledge_repay_record[0]['INTEREST']),
                             '%.2f' % float(round(decimal.Decimal(repay_interest), 2)))
            # 还的罚息
            self.assertEqual(str(pledge_repay_record[0]['PENALTY']), '0.00')
            self.assertEqual(str(pledge_repay_record[0]['REPAY_TYPE']), '1')
            self.assertEqual(str(pledge_repay_record[0]['STATUS']), 'SUCCESS')

    # 通用-全局版本号
    @file_data('test_data/test_get_version.json')
    def test_get_version(self, user_name, password, type, assert_info):
        self._restful_xjb.get_version(user_name=str(user_name), password=str(password), type=str(type))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if str(type) == '2':
            self.assertIsNotNone(str(entity.body['version']))
        else:
            self.assertEqual(str(entity.body['version']), '')

    # 基金-极速赎回说明
    @file_data('test_data/test_fast_redeem_info.json')
    def test_fast_redeem_info(self, user_name, password, sold_share, fund_id, assert_info):
        self._restful_xjb.fast_redeem_info(user_name=str(user_name), password=str(password),
                                           sold_share=str(sold_share), fund_id=str(fund_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            pdc_latest_nav, pdc_marketing = self._db.get_fast_redeem_info(fund_id=str(fund_id))
            redeem_amt = decimal.Decimal(sold_share) * pdc_latest_nav[0]['latest_nav'] * \
                         pdc_marketing[0]['fast_redeem_cashratio'] / 100 - pdc_marketing[0]['fast_redeem_rate']
            self.assertTrue('预计到账：' + str(decimal.Decimal(str(redeem_amt)).quantize(decimal.Decimal('0.00'))) in
                            str(entity.body['redeemAmt']))
        else:
            self.assertEqual(str(entity.body), '')
            self.assertEqual(str(entity.showType), '0')

    # 交易-获取质押利息和总金额
    @file_data('test_data/test_get_loan_repay_info.json')
    def test_get_loan_repay_info(self, user_name, password, my_loan_id, repay_capital_amt, assert_info):
        self._restful_xjb.get_loan_repay_info(user_name=str(user_name), password=str(password),
                                              my_loan_id=str(my_loan_id), repay_capital_amt=str(repay_capital_amt))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            pledge_loan, loan_repay_amt, remain_loan_amt = self._db.get_loan_repay_amt(user_name=str(user_name))

            # 借款天数
            borrow_days = (datetime.datetime.now() -
                           datetime.datetime.strptime(str(pledge_loan['START_DATE']), '%Y%m%d')).days

            # 还款总利息
            sum_interest = BusinessUtility().cal_interest(str(pledge_loan['PLEDGE_AMT']),
                                                          str(pledge_loan['INTEREST_RATE']),
                                                          str(borrow_days))
            # 还款利率
            repay_interest = BusinessUtility().cal_repay_interest(repay_amt=str(repay_capital_amt),
                                                                  borrow_amt=str(remain_loan_amt),
                                                                  interest=str(sum_interest))

            repay_capital_amt = round(decimal.Decimal(repay_capital_amt) + decimal.Decimal(repay_interest), 2)

            self.assertEqual(str(entity.interestAmt),
                             str(decimal.Decimal(str(repay_interest)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(entity.punishInterestAmt, '')
            self.assertEqual(str(entity.repayAmt),
                             str(decimal.Decimal(str(repay_capital_amt)).quantize(decimal.Decimal('0.00'))))

    # 基金-Tip
    @file_data('test_data/test_fund_tip.json')
    def test_fund_tip(self, user_name, password, tip_type, fund_id, assert_info):
        self._restful_xjb.fund_tip(user_name=str(user_name), password=str(password), tip_type=str(tip_type),
                                   fund_id=str(fund_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            now_time = datetime.datetime.now()
            now_day = str(now_time)[0:10]

            next_work_date1 = self._db.get_next_work_date(pre_work_date=str(now_day).replace('-', ''))
            month1 = str(next_work_date1[0]['WORK_DATE'])[4:6]
            day1 = str(next_work_date1[0]['WORK_DATE'])[6:8]
            next_work_date2 = self._db.get_next_work_date(pre_work_date=str(next_work_date1[0]['WORK_DATE']))
            month2 = str(next_work_date2[0]['WORK_DATE'])[4:6]
            day2 = str(next_work_date2[0]['WORK_DATE'])[6:8]

            if str(tip_type) == '1':
                self.assertEqual(str(entity.body['info']),
                                 '说明\n15:00前卖出，预计' + str(month1) + '月' + str(day1) + '日确认份额\n15:00后卖出，预计'
                                 + str(month2) + '月' + str(day2) + '日确认份额')
                # T日15:00之后卖出
                if str(datetime.datetime.now())[0:19] > str(now_day) + ' 15:00:00':
                    self.assertEqual(str(entity.body['timeInfo']),
                                     '预计将于' + str(month2) + '月' + str(day2) + '日 24:00 前到账')

                # T日15:00之前卖出
                if str(datetime.datetime.now())[0:19] < str(now_day) + ' 15:00:00':
                    self.assertEqual(str(entity.body['timeInfo']),
                                     '预计将于' + str(month1) + '月' + str(day1) + '日 24:00 前到账')

            if str(tip_type) == '0':
                self.assertEqual(str(entity.body['info']),
                                 '说明\n15:00前买入，预计' + str(month1) + '月' + str(day1) + '日确认份额\n15:00后买入，预计'
                                 + str(month2) + '月' + str(day2) + '日确认份额')

    # 通用-上传地理位置
    @file_data('test_data/test_upload_geographic_location.json')
    def test_upload_geographic_location(self, user_name, password, assert_info):
        self._restful_xjb.upload_geographic_location(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 高端赎回-获取提示信息
    @file_data('test_data/test_vip_financial_redeeem_tip.json')
    def test_vip_financial_redeem_tip(self, user_name, password, product_id, assert_info):
        self._restful_xjb.get_vip_financial_redeem_tip(user_name=str(user_name), password=str(password),
                                                       product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            now_time = datetime.datetime.now()
            now_day = str(now_time)[0:10]

            # 判断当前日(T日)是否是工作日，如果不是工作日获取最近的工作日
            next_work_date1 = self._db.judge_is_work_date(day=str(now_day).replace('-', ''))
            month1 = str(next_work_date1[0]['WORK_DATE'])[4:6]
            day1 = str(next_work_date1[0]['WORK_DATE'])[6:8]
            now_work_date1 = str(next_work_date1[0]['WORK_DATE'])[0:4] + '-' + month1 + '-' + day1

            pdc_info = self._db.get_product_info(product_id=str(product_id), product_name=None)
            ack_redeem_day = pdc_info[0]['ack_redeem_day']
            delivery_day = pdc_info[0]['delivery_day']

            # T日15:00之前赎回
            if datetime.datetime.now().strftime('%H:%M:%S') < '15:00:00':
                timeArray = time.strptime(now_work_date1, "%Y-%m-%d")
                timeStamp = int(time.mktime(timeArray)) + ack_redeem_day * 24 * 3600
                ack_day = time.strftime("%Y-%m-%d", time.localtime(timeStamp))
                ack_date = self._db.judge_is_work_date(day=str(ack_day).replace('-', ''))
                ack_date_strp = str(ack_date[0]['WORK_DATE'])[0:4] + '-' + str(ack_date[0]['WORK_DATE'])[4:6] + '-' + \
                                str(ack_date[0]['WORK_DATE'])[6:8]
                timeArray = time.strptime(ack_date_strp, "%Y-%m-%d")
                timeStamp = int(time.mktime(timeArray)) + max(delivery_day - 1, 0) * 24 * 3600
                delivery_day1 = time.strftime("%Y-%m-%d", time.localtime(timeStamp))
                delivery_date = self._db.judge_is_work_date(day=str(delivery_day1).replace('-', ''))
                self.assertEqual(str(entity.body['info']), '备注：预计将于' + str(ack_date[0]['WORK_DATE'])[4:6] + '月' +
                                 str(ack_date[0]['WORK_DATE'])[6:8] + '日确认金额，' + str(
                    delivery_date[0]['WORK_DATE'])[4:6] + '月' + str(delivery_date[0]['WORK_DATE'])[6:8] + '日到账')

            # T日15:00之后赎回
            if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') > str(now_day) + ' 15:00:00':
                timeArray = time.strptime(now_work_date1, "%Y-%m-%d")
                timeStamp = int(time.mktime(timeArray)) + ack_redeem_day * 24 * 3600
                ack_day = time.strftime("%Y-%m-%d", time.localtime(timeStamp))
                ack_date = self._db.judge_is_work_date(day=str(ack_day).replace('-', ''))
                ack_date = int(ack_date[0]['WORK_DATE']) + 1
                ack_date = self._db.judge_is_work_date(day=str(ack_date))[0]['WORK_DATE']
                ack_date_strp = str(ack_date)[0:4] + '-' + str(ack_date)[4:6] + '-' + str(ack_date)[6:8]
                timeArray = time.strptime(ack_date_strp, "%Y-%m-%d")
                timeStamp = int(time.mktime(timeArray)) + max(delivery_day - 1, 0) * 24 * 3600
                delivery_day1 = time.strftime("%Y-%m-%d", time.localtime(timeStamp))
                delivery_date = self._db.judge_is_work_date(day=str(delivery_day1).replace('-', ''))
                delivery_date = int(delivery_date[0]['WORK_DATE'])
                self.assertEqual(str(entity.body['info']),
                                 '备注：预计将于' + str(ack_date)[4:6] + '月' + str(ack_date)[6:8] +
                                 '日确认金额，' + str(delivery_date)[4:6] + '月' + str(delivery_date)[6:8] + '日到账')

    # 基金-货币类月、季，年收益曲线
    @file_data('test_data/test_mf_chart_info.json')
    def test_mf_chart_info(self, user_name, password, fund_id, type, assert_info):
        self._restful_xjb.mf_chart_info(user_name=str(user_name), password=str(password), fund_id=str(fund_id),
                                        type=str(type))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 基金-持有列表数据
    @file_data('test_data/test_my_fund_list.json')
    def test_my_fund_list(self, user_name, password, fund_type, assert_info):
        self._restful_xjb.my_fund_list(user_name=str(user_name), password=str(password), fund_type=str(fund_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        data_list = entity.dataList
        asset_in_transit = self._db.get_asset_in_transit(mobile=str(user_name))
        for a in range(0, len(data_list)):
            if str(asset_in_transit[a]['PROD_TYPE']) == '2':
                product_info = self._db.get_product_info(product_id=str(asset_in_transit[a]['PROD_ID']))
                product_marketing = self._db.get_product_marketing(product_id=str(asset_in_transit[a]['PROD_ID']))
                day_before = (Utility.DateUtil().getToday() - datetime.timedelta(days=1)).strftime('%Y%m%d')
                while self._db.determine_if_work_day(date=str(day_before)) is False:
                    day_before = self._db.get_pre_work_date(work_day=str(day_before))[0]['WORK_DATE']
                day_before = datetime.datetime.strftime(datetime.datetime.strptime(str(day_before), '%Y%m%d'),
                                                        '%m-%d')

                self.assertEqual(str(data_list[a]['canModifyShareType']), '1')
                self.assertEqual(str(data_list[a]['canPurchase']), str(product_marketing[0]['onsale_status']))
                self.assertEqual(str(data_list[a]['canRedeem']), str(product_marketing[0]['support_fast_redeem']))
                self.assertEqual(str(data_list[a]['canModifyShareType']), '1')
                channel_argeement = data_list[a]['channelAgreement']
                for b in range(0, len(channel_argeement)):
                    self.assertIn('华信证券基金极速卖出协议', str(channel_argeement[b]['agreementTitle']))
                    self.assertEqual(str(channel_argeement[b]['agreementUrl']), 'agreement/fast_redeem_agreement.html')
                    self.assertEqual(str(channel_argeement[b]['id']), '')
                self.assertEqual(str(data_list[a]['custFundStatus']), '0')
                self.assertEqual(str(data_list[a]['custFundStatusIntro']), '购买确认中')
                self.assertEqual(str(data_list[a]['custFundStatusSummary']), '预计将于09月21日确认份额')
                # self.assertEqual(str(data_list[a]['dynamicColumnName']), '单位净值(' + str(day_before) + ')')
                # self.assertIn(str('%.4f' % product_info[0]['latest_nav']), str(data_list[a]['dynamicColumnValue']))
                self.assertEqual(str(data_list[a]['fastRedeemStatus']),
                                 str(product_marketing[0]['suspend_fast_redeem']))
                self.assertEqual(str(data_list[a]['fundCode']), str(asset_in_transit[a]['PROD_ID']).split('#')[1])
                self.assertEqual(str(data_list[a]['fundId']), str(asset_in_transit[a]['PROD_ID']))
                self.assertEqual(str(data_list[a]['fundName']), str(product_info[0]['product_short_name']))
                self.assertEqual(str(data_list[a]['fundType']), str(asset_in_transit[a]['PROD_TYPE']))
                self.assertEqual(str(data_list[a]['holdAmt']), '')
                self.assertEqual(str(data_list[a]['holdShare']), '')
                self.assertEqual(str(data_list[a]['howManyDaysCanRedeem']), '1')
                self.assertEqual(str(data_list[a]['isDisplayEstimatedCost']), '1')
                self.assertEqual(str(data_list[a]['minFastRedeemShareInfo']), str(asset_in_transit[a]['BALANCE']))
                self.assertEqual(str(data_list[a]['minHoldShare']), str(asset_in_transit[a]['BALANCE']))
                self.assertEqual(str(data_list[a]['minRedeemAmount']), str(asset_in_transit[a]['BALANCE']))
                self.assertEqual(str(data_list[a]['minRedeemShareInfo']), str(asset_in_transit[a]['BALANCE']))
                # self.assertEqual(str(data_list[a]['netValue']), str('%.4f' % product_info[0]['latest_nav']))
                self.assertEqual(str(data_list[a]['newestIncome']), '0')
                self.assertEqual(str(data_list[a]['orderId']), str(asset_in_transit[a]['ORDER_NO']))
                self.assertEqual(str(data_list[a]['purchaseAmt']), str(asset_in_transit[a]['BALANCE']))

    # 信用卡-银行通道列表
    @file_data('test_data/test_bank_channel_list.json')
    def test_bank_channel_list(self, user_name, password, assert_info):
        self._restful_xjb.bank_channel_list(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        data_list = entity.dataList
        for i in range(0, len(data_list)):
            credit_bank_channel, be_channel_conf, group_name = \
                self._db.get_credit_bank_channel(group_id=str(data_list[i]['bankGroupId']))
            if len(data_list) == len(credit_bank_channel):
                self.assertEqual(str(data_list[i]['bankGroupId']), str(be_channel_conf[i]['bank_group_id']))
                self.assertEqual(str(data_list[i]['bankGroupName']), str(group_name[0]['group_name']))
                # self.assertEqual(str(data_list[i]['bankLogoUrl']),
                #                  'http://10.199.111.2/V1/images/cust/bank/icon/' +
                #                  str(be_channel_conf[i]['bank_no']) + '.png')
                self.assertEqual(str(data_list[i]['bankNo']), str(be_channel_conf[i]['bank_no']))
                self.assertEqual(str(data_list[i]['cardType']), '')
                self.assertEqual(str(data_list[i]['isAvailable']), '1')
                self.assertEqual(str(be_channel_conf[i]['is_credit']), 'Y')

    # 交易-获取搜索条件树(V3.2)
    @file_data('test_data/test_get_search_condition_tree.json')
    def test_get_search_condition_tree(self, user_name, password, type, assert_info):
        self._restful_xjb.get_search_condition_tree(user_name=str(user_name), password=str(password), type=str(type))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        data_list = entity.body_dataList
        self.assertEqual(str(data_list[0]['coditionId']), '0001')
        self.assertEqual(str(data_list[0]['conditionCode']), '-1')
        self.assertEqual(str(data_list[0]['conditionName']), '全部')

        self.assertEqual(str(data_list[1]['coditionId']), '0002')
        self.assertEqual(str(data_list[1]['conditionCode']), '01')
        self.assertEqual(str(data_list[1]['conditionName']), '存入')

        self.assertEqual(str(data_list[2]['coditionId']), '0003')
        self.assertEqual(str(data_list[2]['conditionCode']), '02')
        self.assertEqual(str(data_list[2]['conditionName']), '取出')

        self.assertEqual(str(data_list[3]['coditionId']), '0004')
        self.assertEqual(str(data_list[3]['conditionCode']), '03')
        self.assertEqual(str(data_list[3]['conditionName']), '收益')
        for i in range(0, 4):
            self.assertEqual(str(data_list[i]['level']), '1')
            self.assertEqual(str(data_list[i]['parentId']), '')

        self.assertEqual(str(data_list[4]['coditionId']), '00025')
        self.assertEqual(str(data_list[4]['conditionCode']), '-1')
        self.assertEqual(str(data_list[4]['conditionName']), '全部存入')

        self.assertEqual(str(data_list[5]['coditionId']), '00021')
        self.assertEqual(str(data_list[5]['conditionCode']), '011')
        self.assertEqual(str(data_list[5]['conditionName']), '银行卡存入')

        self.assertEqual(str(data_list[6]['coditionId']), '00022')
        self.assertEqual(str(data_list[6]['conditionCode']), '012')
        self.assertEqual(str(data_list[6]['conditionName']), '工资理财存入')

        self.assertEqual(str(data_list[7]['coditionId']), '00023')
        self.assertEqual(str(data_list[7]['conditionCode']), '013')
        self.assertEqual(str(data_list[7]['conditionName']), '汇款存入')

        self.assertEqual(str(data_list[8]['coditionId']), '00024')
        self.assertEqual(str(data_list[8]['conditionCode']), '014')
        self.assertEqual(str(data_list[8]['conditionName']), '其他存入')
        for i in range(4, 9):
            self.assertEqual(str(data_list[i]['level']), '2')
            self.assertEqual(str(data_list[i]['parentId']), '0002')

        self.assertEqual(str(data_list[9]['coditionId']), '00036')
        self.assertEqual(str(data_list[9]['conditionCode']), '-1')
        self.assertEqual(str(data_list[9]['conditionName']), '全部取出')

        self.assertEqual(str(data_list[10]['coditionId']), '00031')
        self.assertEqual(str(data_list[10]['conditionCode']), '021')
        self.assertEqual(str(data_list[10]['conditionName']), '快速取出')

        self.assertEqual(str(data_list[11]['coditionId']), '00032')
        self.assertEqual(str(data_list[11]['conditionCode']), '022')
        self.assertEqual(str(data_list[11]['conditionName']), '普通取出')

        self.assertEqual(str(data_list[12]['coditionId']), '00033')
        self.assertEqual(str(data_list[12]['conditionCode']), '023')
        self.assertEqual(str(data_list[12]['conditionName']), '信用卡还款')

        self.assertEqual(str(data_list[13]['coditionId']), '00034')
        self.assertEqual(str(data_list[13]['conditionCode']), '024')
        self.assertEqual(str(data_list[13]['conditionName']), '还贷款')

        self.assertEqual(str(data_list[14]['coditionId']), '00035')
        self.assertEqual(str(data_list[14]['conditionCode']), '025')
        self.assertEqual(str(data_list[14]['conditionName']), '其他取出')
        for i in range(9, 15):
            self.assertEqual(str(data_list[i]['level']), '2')
            self.assertEqual(str(data_list[i]['parentId']), '0003')

    # 基金-详情页历史回报等
    @file_data('test_data/test_fund_rise_info.json')
    def test_fund_rise_info(self, user_name, password, fund_id, fund_type, assert_info):
        self._restful_xjb.fund_rise_info(user_name=str(user_name), password=str(password), fund_id=str(fund_id))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            data_list = entity.body_dataList
            length = len(data_list)
            self.assertEqual(str(data_list[length - 1]['type']), '5')
            self.assertEqual(str(data_list[length - 1]['name']), '风险收益特征')
            self.assertEqual(str(data_list[length - 1]['riskIncomeFeatureTitle']), '风险收益特征')
            if str(fund_type) == '5':
                self.assertEqual(str(data_list[length - 1]['riskIncomeFeatureValue']),
                                 '    本基金属于证券市场中的低风险品种，预期收益和风险高于货币市场基金，低于股票型基金。')

            if str(fund_type) == '0':
                self.assertEqual(str(data_list[length - 1]['riskIncomeFeatureValue']),
                                 '本基金属于股票型指数基金，在证券投资基金中属于较高风险、较高收益的品种，本基金主要采用指数复制法跟踪标的指数的表现，具有与标的指数相似的风险收益特征。')

            if str(fund_type) == '3':
                self.assertEqual(str(data_list[length - 1]['riskIncomeFeatureValue']),
                                 '本基金为混合型基金，其预期收益及预期风险水平高于债券型基金和货币市场基金，但低于股票型基金，属于中等风险水平的投资品种。')

            if str(fund_type) == '2':
                self.assertEqual(str(data_list[length - 1]['riskIncomeFeatureValue']),
                                 '本基金属于证券市场中的中低风险品种，预期收益和风险高于货币市场基金、普通债券型基金，低于股票型基金。')

            if str(fund_type) == '1':
                self.assertEqual(str(data_list[length - 1]['riskIncomeFeatureValue']),
                                 '　　本基金面临的风险与其他开放式基金相同(如市场风险、流动性风险、管理风险、技术风险等)，但由于本基金主要投资短期流动性金融工具，上述风险在本基金中存在一定的特殊性，投资本金损失的可能性很小。')

            if str(fund_type) == '11':
                self.assertEqual(str(data_list[length - 1]['riskIncomeFeatureValue']),
                                 '本基金为主动管理的全球配置型股票基金，主要投资方向为能源和材料等资源相关行业，属于具有较高风险和较高收益预期的证券投资基金品种，本基金力争在严格控制风险的前提下为投资人谋求资本的长期增值。')

            if str(fund_type) == '8':
                self.assertEqual(str(data_list[length - 1]['riskIncomeFeatureValue']),
                                 '本基金属于短期理财债券型证券投资基金，长期风险收益水平低于股票型基金、混合型基金及普通债券型证券投资基金。')

    # 基金-统计热门搜索基金
    @file_data('test_data/test_statistic_product_search.json')
    def test_statistic_product_search(self, user_name, password, fund_id, assert_info):
        self._restful_xjb.statistic_product_search(user_name=str(user_name), password=str(password),
                                                   fund_id=str(fund_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 积分-赚积分
    @file_data('test_data/test_earn_points.json')
    def test_earn_points(self, user_name, password, assert_info):
        self._restful_xjb.earn_points(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        points_issue_event_rule = self._db.get_points_issue_event_rule()
        data_list = entity.dataList
        for i in range(0, len(data_list)):
            self.assertEqual(str(entity.totalCount), str(len(points_issue_event_rule)))
            self.assertEqual(str(data_list[0]['buttonInfo']), '去推荐')
            self.assertEqual(str(data_list[1]['buttonInfo']), '去购买')
            self.assertEqual(str(data_list[i]['buttonLink']), str(points_issue_event_rule[i]['URL']))
            self.assertEqual(str(data_list[i]['status']), '1')
            self.assertEqual(str(data_list[i]['statusInfo']), '积分正在发放中，请耐心等待...')
            self.assertEqual(str(data_list[i]['statusUrl']), '')
            self.assertEqual(str(data_list[i]['taskName']), str(points_issue_event_rule[i]['EVENT_DESC']))
            self.assertEqual(str(data_list[0]['taskPoints']), str(points_issue_event_rule[0]['ISSUE_AMOUNT']) + '积分')
            self.assertEqual(str(data_list[1]['taskPoints']), str(points_issue_event_rule[1]['ISSUE_AMOUNT']) + '-' +
                             str(points_issue_event_rule[1]['MAX_AMOUNT']) + '积分')

    # 积分-积分明细
    @file_data('test_data/test_points_detail.json')
    def test_points_detail(self, user_name, password, type, assert_info):
        self._restful_xjb.points_detail(user_name=str(user_name), password=str(password), type=str(type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        points_account, issue_points_account_his, consume_points_account_his = \
            self._db.get_points_detail(user_name=str(user_name))
        today = Utility.DateUtil().getToday()
        created_date = str(consume_points_account_his[0]['CREATED_AT']).split(' ')[0].replace('2017-', '')
        if str(today) == created_date:
            created_date = '今天'
        elif str(today - datetime.timedelta(days=1)) == created_date:
            created_date = '昨天'
        if type == '0':
            self.assertEqual(str(entity.totalCount), str(len(issue_points_account_his)))
            self.assertEqual(str(entity.dataList[0]['pointsCount']), '+' +
                             str(issue_points_account_his[0]['AMOUNT_AFTER']))
            self.assertEqual(str(entity.dataList[0]['serialDate']),
                             str(issue_points_account_his[0]['CREATED_AT']).split(' ')[0])
            self.assertEqual(str(entity.dataList[0]['serialTime']),
                             created_date + ' ' + str(issue_points_account_his[0]['CREATED_AT']).split(' ')[1])
            self.assertEqual(str(entity.dataList[0]['title']), str(issue_points_account_his[0]['REMARK']))
        if type == '1':
            self.assertEqual(str(entity.totalCount), str(len(consume_points_account_his)))
            self.assertEqual(str(entity.dataList[0]['pointsCount']),
                             '-' + str(consume_points_account_his[0]['FROZEN_AMOUNT_BEFORE']))
            self.assertEqual(str(entity.dataList[0]['serialDate']),
                             str(consume_points_account_his[0]['CREATED_AT']).split(' ')[0])
            self.assertEqual(str(entity.dataList[0]['serialTime']), created_date + ' ' + '14:23:09')
            self.assertEqual(str(entity.dataList[0]['title']), str(consume_points_account_his[0]['REMARK']))
        if type == '-1':
            self.assertEqual(str(entity.totalCount),
                             str(decimal.Decimal(len(issue_points_account_his)) +
                                 decimal.Decimal(len(consume_points_account_his))))

    # 积分-花积分
    @file_data('test_data/test_spend_points.json')
    def test_spend_points(self, user_name, password, assert_info):
        self._restful_xjb.spend_points(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        points_deducte_rule = self._db.get_points_deducte_rule()
        points_account, issue_points_account_his, consume_points_account_his = \
            self._db.get_points_detail(user_name=str(user_name))
        data_list = entity.dataList
        for i in range(0, len(data_list)):
            self.assertEqual(str(data_list[i]['buttonInfo']), '去购买')
            self.assertEqual(str(data_list[i]['buttonLink']), str(points_deducte_rule[i]['URL']))
            self.assertEqual(str(data_list[i]['name']), str(points_deducte_rule[i]['PRODUCT_TYPE_NAME']))
            self.assertEqual(str(data_list[i]['ruleInfo']),
                             '<font color=\'#666666\'>单笔抵扣上限</font>&nbsp;&nbsp;<font color=\'#ff821f\'>500元</font>')
        self.assertEqual(str(entity.info), '在购买产品时1个积分抵扣1元，最高可抵扣购买金额的0.10%')
        self.assertEqual(str(entity.totalPoints), str(points_account[0]['AMOUNT']))

    # 积分-推荐任务
    @file_data('test_data/test_recommends.json')
    def test_recommends(self, user_name, password, assert_info):
        self._restful_xjb.point_recommends(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            recommend_list = self._db.get_points_issue_event_rule()
            data_list = entity.body_dataList
            self.assertEqual(str(entity.body['totalCount']), str(len(recommend_list)))
            for i in range(0, len(recommend_list)):
                if str(recommend_list[i]['EVENT_KEY']) == 'PAY_PROPRIETARY_FUND_AGENCY_FEE':
                    task_point = str(recommend_list[i]['ISSUE_AMOUNT']) + '-' + \
                                 str(recommend_list[i]['MAX_AMOUNT']) + '积分'
                else:
                    task_point = str(recommend_list[i]['ISSUE_AMOUNT']) + '积分'

                if str(recommend_list[i]['EVENT_KEY']) == 'RCMD_NEW_USER_REGISTER_BINDCARD':
                    button_info = '去推荐'
                elif str(recommend_list[i]['EVENT_KEY']) == 'FIRST_PAY_DQB' or \
                                str(recommend_list[i]['EVENT_KEY']) == 'FIRST_PAY_GD' or \
                                str(recommend_list[i]['EVENT_KEY']) == 'FIRST_PAY_PROPRIETARY_FUND_GT' or \
                                str(recommend_list[i]['EVENT_KEY']) == 'PAY_PROPRIETARY_FUND_AGENCY_FEE':
                    button_info = '去购买'
                elif str(recommend_list[i]['EVENT_KEY']) == 'REGISTER_BINDCARD':
                    button_info = '去绑卡'
                elif str(recommend_list[i]['EVENT_KEY']) == 'FOLLOW_BIND_WEIXIN':
                    button_info = '未绑定'
                elif str(recommend_list[i]['EVENT_KEY']) == 'FIRST_PAY_XJB_GT':
                    button_info = '去存入'
                elif str(recommend_list[i]['EVENT_KEY']) == 'STOCK_ACCOUNT_REGISTER_OPEN':
                    button_info = '去下载'
                else:
                    button_info = '去申请'
                self.assertEqual(str(data_list[i]['buttonInfo']), str(button_info))
                self.assertEqual(str(data_list[i]['status']), '1')
                self.assertEqual(str(data_list[i]['statusInfo']), '积分正在发放中，请耐心等待...')
                self.assertEqual(str(data_list[i]['taskName']), str(recommend_list[i]['EVENT_DESC']))
                self.assertEqual(str(data_list[i]['taskPoints']), str(task_point))
                self.assertEqual(str(data_list[i]['buttonLink']), str(recommend_list[i]['URL']))

    # 基金-权益类月、季，年收益曲线
    @file_data('test_data/test_sf_chart_info.json')
    def test_sf_chart_info(self, user_name, password, fund_id, type, assert_info):
        self._restful_xjb.sf_chart_info(user_name=str(user_name), password=str(password), fund_id=str(fund_id),
                                        type=str(type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 基金-对比、组合收益曲线
    @file_data('test_data/test_fund_compare.json')
    def test_fund_compare(self, user_name, password, fund_ids, type, chart_type, assert_info):
        self._restful_xjb.fund_compare(user_name=str(user_name), password=str(password), fund_ids=str(fund_ids),
                                       type=str(type), chart_type=str(chart_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 交易-申请预约交易码(V3.2)
    @file_data('test_data/test_apply_reservation_code.json')
    def test_apply_reservation_code(self, user_name, password, product_id, yy_amt, money_can_use_start_date,
                                    money_can_use_end_date, mobile, assert_info):
        self._restful_xjb.apply_reservation_code(user_name=str(user_name), password=str(password),
                                                 product_id=str(product_id), yy_amt=str(yy_amt),
                                                 money_can_use_start_date=str(money_can_use_start_date),
                                                 money_can_use_end_date=str(money_can_use_end_date),
                                                 mobile=str(mobile))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if str(product_id) == '899#SP13147':
            if entity.returnCode == '000000':
                apply_list = self._db.get_apply_reservation_code(user_name=str(user_name), product_id=str(product_id))[
                    0]
                product_presale = self._db.get_product_presale(product_id=str(product_id))[0]
                data_list = entity.body_detail
                self.assertEqual(str(data_list['applyId']), str(apply_list['ID']))
                self.assertEqual(str(data_list['mobile']), str(apply_list['MOBILE_NO']))
                self.assertEqual(str(data_list['moneyCanUseEndDate']), str(apply_list['TO_CAPITAL_AVAILABLE'])[0:10])
                self.assertEqual(str(data_list['moneyCanUseStartDate']),
                                 str(apply_list['FROM_CAPITAL_AVAILABLE'])[0:10])
                self.assertEqual(str(data_list['period']), str(product_presale['invest_period_desc']))
                self.assertEqual(str(data_list['probablyRate']), str(product_presale['yield']))
                self.assertEqual(str(data_list['productId']), str(product_id))
                self.assertEqual(str(data_list['productName']), str(product_presale['product_name']))
                self.assertEqual(str(data_list['remark']), str(apply_list['REMARK']))
                self.assertEqual(str(data_list['reservationCode']),
                                 '' if str(apply_list['RESERVE_CODE']) == 'None' else str(apply_list['RESERVE_CODE']))
                self.assertEqual(str(data_list['status']), str(apply_list['STATUS']))
                self.assertEqual(str(data_list['statusInfo']), '已收到您的购买意向')
                self.assertEqual(str(data_list['statusSummary']), '我们将会在产品开售时提醒您进行线上抢购')
                self.assertEqual(str(data_list['tip']), '抢先填写您的购买意向，您将有机会获得高端产品的优先购买权')
                self.assertEqual(str(data_list['yyAmt']), str(apply_list['AP_AMT']))
                self._db.delete_apply_reservation_code(user_name=str(user_name), product_id=str(product_id))

            else:
                self.assertEqual(str(entity.returnMsg), '申请金额不能小于起投金额')
                self.assertEqual(str(entity.showType), '0')

        else:
            self.assertEqual(str(entity.returnMsg), '该客户信息对应的预约码申请已存在')
            self.assertEqual(str(entity.showType), '0')

    # 交易-查看预约码审核进度(V3.2)
    @file_data('test_data/test_query_reservation_code_audit_status.json')
    def test_query_reservation_code_audit_status(self, user_name, password, product_id, assert_info):
        self._restful_xjb.query_reservation_code_audit_status(user_name=str(user_name), password=str(password),
                                                              product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            apply_list = self._db.get_apply_reservation_code(user_name=str(user_name), product_id=str(product_id))
            product_presale = self._db.get_product_presale(product_id=str(product_id))[0]
            data_detail = entity.body_detail
            if len(apply_list) > 0:
                apply_list = apply_list[0]
                self.assertEqual(str(data_detail['applyId']), str(apply_list['ID']))
                self.assertEqual(str(data_detail['mobile']), str(apply_list['MOBILE_NO']))
                self.assertEqual(str(data_detail['moneyCanUseEndDate']), str(apply_list['TO_CAPITAL_AVAILABLE'])[0:10])
                self.assertEqual(str(data_detail['moneyCanUseStartDate']),
                                 str(apply_list['FROM_CAPITAL_AVAILABLE'])[0:10])
                self.assertEqual(str(data_detail['period']), str(product_presale['invest_period_desc']))
                self.assertEqual(str(data_detail['probablyRate']), str(product_presale['yield']))
                self.assertEqual(str(data_detail['productId']), str(product_id))
                self.assertEqual(str(data_detail['productName']), str(product_presale['product_name']))
                self.assertEqual(str(data_detail['remark']), str(apply_list['REMARK']))
                self.assertEqual(str(data_detail['reservationCode']),
                                 '' if str(apply_list['RESERVE_CODE']) == 'None' else str(apply_list['RESERVE_CODE']))
                self.assertEqual(str(data_detail['status']), str(apply_list['STATUS']))
                self.assertEqual(str(data_detail['statusInfo']), '已收到您的购买意向')
                self.assertEqual(str(data_detail['statusSummary']), '我们将会在产品开售时提醒您进行线上抢购')
                self.assertEqual(str(data_detail['tip']), '抢先填写您的购买意向，您将有机会获得高端产品的优先购买权')
                self.assertEqual(str(data_detail['yyAmt']), str(apply_list['AP_AMT']))
                self.assertEqual(str(entity.body['hasApply']), '1')
            else:
                if len(product_presale) > 0:
                    self.assertEqual(str(data_detail['probablyRate']), str(product_presale['yield']))
                    self.assertEqual(str(data_detail['productId']), str(product_id))
                    self.assertEqual(str(data_detail['productName']), str(product_presale['product_name']))
                    self.assertEqual(str(data_detail['tip']), '抢先填写您的购买意向，您将有机会获得高端产品的优先购买权')

    # 产品-在售产品列表(热门排除售罄)
    @file_data('test_data/test_sell_product_list.json')
    def test_sell_product_list(self, user_name, password, assert_info):
        self._restful_xjb.sell_product_list(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        dqb_hot_list = self._db.get_hot_on_saling_product_list(product_type='1')
        vip_hot_list = self._db.get_hot_on_saling_product_list(product_type='3')
        data_list = entity.dataList
        self.assertEqual(str(len(data_list)), str(len(dqb_hot_list) + len(vip_hot_list)))
        for i in range(0, len(data_list)):
            if str(data_list[i]['productType']) == '1':
                self.assertEqual(str(data_list[i]['canRedeemAnytime']), str(dqb_hot_list[i]['any_redem_time']))
                self.assertEqual(str(data_list[i]['clientType']), '0')
                # self.assertEqual(str(data_list[i]['leftAmt']), '')
                self.assertEqual(str(data_list[i]['minAmount']),
                                 str(dqb_hot_list[i]['min_buy_amount']).replace('.00', ''))
                self.assertEqual(str(data_list[i]['onsaleStatus']), '4')
                self.assertEqual(str(data_list[i]['productDetailUrl']), 'hxxjb://product?commonType=1&productId=' +
                                 str(dqb_hot_list[i]['productid']).replace('#', '%23'))
                self.assertEqual(str(data_list[i]['productId']), str(dqb_hot_list[i]['productid']))
                self.assertEqual(str(data_list[i]['productStatus']), '4')
                self.assertEqual(str(data_list[i]['productTitle']), str(dqb_hot_list[i]['product_short_name']))
                self.assertEqual(str(data_list[i]['productType']), '1')
                self.assertEqual(str(data_list[i]['recommended']), '1')
                self.assertEqual(str(data_list[i]['type']), '1')
            elif str(data_list[i]['productType']) == '3':
                self.assertEqual(str(data_list[i]['canRedeemAnytime']), str(vip_hot_list[i]['any_redem_time']))
                self.assertEqual(str(data_list[i]['clientType']), '0')
                self.assertEqual(str(data_list[i]['onsaleStatus']), '4')
                self.assertEqual(str(data_list[i]['productStatus']), '4')
                self.assertEqual(str(data_list[i]['productType']), '3')
                self.assertEqual(str(data_list[i]['type']), '3')

    # 积分-兑换
    @file_data('test_data/test_points_exchange.json')
    def test_points_exchange(self, user_name, password, id, assert_info):
        self._restful_xjb.points_exchange(user_name=str(user_name), password=str(password), id=str(id))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 产品-产品库版本号
    @file_data('test_data/test_product_version.json')
    def test_product_version(self, user_name, password, assert_info):
        self._restful_xjb.product_version(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        self.assertIsNotNone(entity.version)

    # 交易-所有交易状态
    @file_data('test_data/test_all_trade_status.json')
    def test_all_trade_status(self, user_name, password, assert_info):
        self._restful_xjb.all_trade_status(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        jyzt = self._db.get_pro_intro(user_name=str(user_name), categary_code='JYZT')
        status_list = entity.body_list
        for i in range(0, len(status_list)):
            self.assertEqual(str(status_list[i]['statusId']), str(jyzt[i]['code']))
            self.assertEqual(str(status_list[i]['statusName']), str(jyzt[i]['value']))

    # 基金-公告列表
    @file_data('test_data/test_fund_notice_list.json')
    def test_fund_notice_list(self, user_name, password, fund_id, notice_type, assert_info):
        self._restful_xjb.fund_notice_list(user_name=str(user_name), password=str(password),
                                           fund_id=str(fund_id), notice_type=str(notice_type))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            notice_list = self._db.get_fund_notice_list(fund_id=str(fund_id)[3:], notice_type=str(notice_type))
            num = len(notice_list)
            self.assertEqual(str(entity.body_totalCount), str(num))
            if num > 20:
                notice_list = notice_list[0:20]
                num = 20
            notice_list = sorted(notice_list, key=lambda p: p['id'], reverse=True)
            data_list = entity.body_dataList
            data_list = sorted(data_list, key=lambda p: p['noticeId'], reverse=True)
            for i in range(0, num):
                self.assertEqual(str(data_list[i]['noticeContent']), '')
                self.assertEqual(str(data_list[i]['noticeDate']), str(notice_list[i]['bulletin_date'])[0:10])
                self.assertTrue('fund/noticeDetail.html?noticeId=' + str(notice_list[i]['id']) in
                                str(data_list[i]['noticeDetailLink']))
                self.assertEqual(str(data_list[i]['noticeId']), str(notice_list[i]['id']))
                self.assertEqual(str(data_list[i]['noticeTitle']), str(notice_list[i]['info_title']))
                self.assertEqual(str(data_list[i]['noticeType']), str(notice_list[i]['bulletin_type']))
                self.assertEqual(str(data_list[i]['noticeType']), str(notice_list[i]['bulletin_type']))

    # 产品-搜索定期或高端
    @file_data('test_data/test_search_fin_product.json')
    def test_search_fin_product(self, user_name, password, keyword, product_type, assert_info):
        self._restful_xjb.search_fin_product(user_name=str(user_name), password=str(password), keyword=str(keyword),
                                             product_type=str(product_type))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            product_list = self._db.get_search_fin_product(keyword=str(keyword))
            data_list = entity.body_dataList

            self.assertEqual(str(entity.body_totalCount), str(len(product_list)))
            num = len(product_list) if len(product_list) < 100 else 100
            for i in range(num, 0):
                self.assertEqual(
                    '--' if str(product_list[i]['product_yield']) == 'None' else str(product_list[i]['product_yield']),
                    str(data_list[i]['incomeIntro']))
                self.assertEqual(str(product_list[i]['product_yield_des']), str(data_list[i]['incomeType']))
                self.assertEqual(str(product_list[i]['productid']), str(data_list[i]['productId']))
                self.assertEqual(
                    '--' if str(product_list[i]['product_pinyin']) == '' else str(product_list[i]['product_pinyin']),
                    str(data_list[i]['productPinyin']))
                self.assertEqual(str(product_list[i]['product_short_name']), str(data_list[i]['productTitle']))
                self.assertEqual(str(product_list[i]['product_type']), str(data_list[i]['productType']))

    # 产品-发售预告列表
    @file_data('test_data/test_sell_notice.json')
    def test_sell_notice(self, user_name, password, assert_info):
        self._restful_xjb.sell_notice(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 产品-高端产品详情
    @file_data('test_data/test_vip_product_detail.json')
    def test_vip_product_detail(self, user_name, password, product_id, assert_info):
        self._restful_xjb.vip_product_detail(user_name=str(user_name), password=str(password),
                                             product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        product_info = self._db.get_product_info(product_id=str(product_id))
        product_marketing = self._db.get_product_marketing(product_id=str(product_id))
        product_left_quota = self._db.get_prod_left_quota(product_id=str(product_id))
        self.assertEqual(str(entity.detail['ackRedeemDay']), str(product_info[0]['ack_redeem_day']))
        self.assertEqual(str(entity.detail['amtLow']), str(product_info[0]['min_buy_amount']))
        self.assertEqual(str(entity.detail['amtUp']), str(product_info[0]['max_buy_amount']))
        self.assertEqual(str(entity.detail['canRedeem']), str(product_marketing[0]['support_fast_redeem']))
        self.assertEqual(str(entity.detail['canRedeemAnytime']), str(product_marketing[0]['is_redem_anytime']))
        self.assertEqual(str(entity.detail['canUsePoints']), str(product_marketing[0]['is_support_points']))
        self.assertEqual(str(entity.detail['confirmQualifiedInvestor']),
                         str(product_info[0]['confirm_qualified_investor']))
        self.assertEqual(str(entity.detail['deliveryDay']), str(product_info[0]['delivery_day']))
        self.assertEqual(str(entity.detail['hasPerformanceRate']), '0')
        self.assertEqual(str(entity.detail['incomeAllotIntro']), '暂无相关内容')
        self.assertEqual(str(entity.detail['incomeType']), '0')
        self.assertEqual(str(entity.detail['increaseRange']), str(product_info[0]['min_add_subscribe']))
        self.assertIn(str(int(product_info[0]['min_add_subscribe'])), str(entity.detail['info']))
        self.assertEqual(str(entity.detail['investTarget']), '暂无相关内容')
        self.assertEqual(str(entity.detail['isArchive']), str(product_marketing[0]['is_archive']))
        self.assertEqual(str(entity.detail['leftAmt']), str(product_left_quota[0]['LEFT_QUOTA']))
        self.assertEqual(str(entity.detail['minAmount']), str(int(product_info[0]['min_buy_amount'])) + '元')
        self.assertEqual(str(entity.detail['maxAmount']), str(int(product_info[0]['max_buy_amount']) / 10000) + '万')
        self.assertEqual(str(entity.detail['navDate']), datetime.datetime.strftime(datetime.datetime.strptime(
            str(product_info[0]['latest_nav_date']), '%Y%m%d'), '%Y.%m.%d'))
        self.assertEqual(str(entity.detail['onsaleFlag']), str(product_marketing[0]['onsale_flag']))
        self.assertEqual(str(entity.detail['onsaleStatus']), str(product_marketing[0]['onsale_status']))
        self.assertEqual(str(entity.detail['payType']), str(product_marketing[0]['support_pay_type']))
        self.assertEqual(str(entity.detail['productId']), str(product_id))
        self.assertEqual(str(entity.detail['productName']), str(product_info[0]['product_short_name']))
        self.assertEqual(str(entity.detail['productRiskLevelValue']), str(product_info[0]['product_risklevel']))
        self.assertEqual(str(entity.detail['productStage']), '4')
        self.assertEqual(str(entity.detail['productType']), str(product_info[0]['product_type']))
        self.assertEqual(str(entity.detail['productTypeName']), '高端')
        self.assertEqual(str(entity.detail['purchasedCount']), str(product_left_quota[0]['BUY_COUNT']))
        self.assertEqual(str(entity.detail['riseType']), '万份收益')
        self.assertEqual(str(entity.detail['riseValue']), '%.4f' % float(product_info[0]['fund_income_unit']))
        self.assertIn(str(format(product_left_quota[0]['LEFT_QUOTA'], ',')), str(entity.detail['saleStatusInfo']))
        self.assertEqual(str(entity.detail['startSellTime']), '0')
        self.assertEqual(str(entity.detail['supportFastRedeem']), str(product_marketing[0]['support_fast_redeem']))
        self.assertEqual(str(entity.detail['surplusStartSellTime']), '0')
        self.assertEqual(str(entity.detail['transferDays']), str(product_info[0]['transfer_days']))
        self.assertEqual(str(entity.detail['unitShareWorth']), '1元')
        self.assertEqual(str(entity.detail['updateDate']), str(product_info[0]['update_at']).split(' ')[0])
        self.assertEqual(str(entity.detail['vipProductType']), str(product_info[0]['high_wealth_type']))
        self.assertEqual(str(entity.detail['vipProductTypeDesc']), '资管计划')
        self.assertEqual(str(entity.detail['yieldInfo']), '6.000%')
        self.assertEqual(str(entity.detail['yieldType']), '七日年化收益率')
        self.assertEqual(str(entity.detail['yieldTypeCode']), '0')

    # 基金-热搜关键词
    @file_data('test_data/test_fund_trending.json')
    def test_fund_trending(self, user_name, password, assert_info):
        self._restful_xjb.fund_trending(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        fund_hot_keys = self._db.get_fund_hot_keys()
        for i in range(0, len(fund_hot_keys)):
            self.assertIn(str(fund_hot_keys[i]['keyword']), str(entity.keywords))

    # 产品-高端权益类月、季，年收益曲线
    @file_data('test_data/test_mf_chart_info.json')
    def test_mf_chart_info(self, user_name, password, product_id, type, assert_info):
        self._restful_xjb.vip_product_sfchart_info(user_name=str(user_name), password=str(password),
                                                   product_id=str(product_id), type=str(type))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 产品-所有产品类别
    def test_all_product_types(self):
        self._restful_xjb.all_product_types()
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, '')
        self.assertEqual(entity.returnCode, '000000')

        self.assertEqual(entity.list[0]['typeId'], '0')
        self.assertEqual(entity.list[0]['typeName'], '活期')
        self.assertEqual(entity.list[1]['typeId'], '1')
        self.assertEqual(entity.list[1]['typeName'], '定期')

    # 基金-基金是否已添加自选
    @file_data('test_data/test_fund_is_fav.json')
    def test_fund_is_fav(self, user_name, password, fund_id, assert_info):
        self._restful_xjb.fund_is_fav(user_name=str(user_name), password=str(password), fund_id=str(fund_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        self.assertIn(str(entity.result), '1, 0')

    # 认购/预约认购 定活宝
    @file_data('test_data/test_buy_dhb_product.json')
    def test_buy_dhb_product(self, user_name, login_password, pay_type, product_id, amt, trade_password,
                             assert_info):
        self._restful_xjb.buy_product(user_name=str(user_name), login_password=str(login_password),
                                      pay_type=str(pay_type), product_id=str(product_id), amt=str(amt),
                                      trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            vacco_detail = self._db.get_vacco_payment_details(mobile=str(user_name))
            trade_quty_chg = self._db.get_trade_quty_chg(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))
            # 012 认购 012020 现金宝认购
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '012')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '012020')
            self.assertEqual(str(trade_order[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_order[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '1')
            self.assertEqual(str(trade_order[0]['TO_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['STATUS']), 'A')
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))

            self.assertEqual(str(trade_request[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_request[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(trade_request[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['RTTA_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(trade_request[0]['TANO']), str(product_id).split('#')[0])
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '1')
            # 020 认购 002210 认购定期
            self.assertEqual(str(trade_request[0]['APKIND']), '020')
            self.assertEqual(str(trade_request[0]['SUB_APKIND']), '002210')
            self.assertEqual(str(trade_request[0]['SUB_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))

            self.assertEqual(str(trade_quty_chg[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_quty_chg[0]['PROD_TYPE']), '0')
            # 024 赎回 002201 现金宝赎回认购定期
            self.assertEqual(str(trade_quty_chg[0]['APKIND']), '024')
            self.assertEqual(str(trade_quty_chg[0]['SUB_APKIND']), '002201')
            self.assertEqual(str(trade_quty_chg[0]['CHG_QUTY']),
                             str(-decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_quty_chg[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(trade_quty_chg[0]['BRANCH_CODE']), '675')

            # 020 认购 020020 预约认购定期宝（来自现金宝）
            self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '1')
            self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(product_id))
            self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(asset_in_trasit[0]['BRANCH_CODE']), '675')
            self.assertEqual(str(asset_in_trasit[0]['TANO']), str(product_id).split('#')[0])
            self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                             str(decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))
            # 020 认购 002210 认购定期
            self.assertEqual(str(asset_in_trasit[0]['APKIND']), '020')
            self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '002210')

            # 024 赎回 002201 现金宝赎回（用于买入定期宝）
            self.assertEqual(str(vacco_detail[0]['SHARE_TYPE']), 'A')
            self.assertEqual(str(vacco_detail[0]['ACCPT_MODE']), 'M')
            self.assertEqual(str(vacco_detail[0]['APKIND']), '024')
            self.assertEqual(str(vacco_detail[0]['SUB_APKIND']), '002201')
            self.assertEqual(str(vacco_detail[0]['SUB_AMT']),
                             str(-decimal.Decimal(amt).quantize(decimal.Decimal('0.00'))))

    # 产品-高端货币类月、季，年收益曲线
    @file_data('test_data/test_vip_product_mf_chart_info.json')
    def test_mf_chart_info(self, user_name, password, product_id, type, assert_info):
        self._restful_xjb.vip_product_mfchart_info(user_name=str(user_name), password=str(password),
                                                   product_id=str(product_id), type=str(type))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 基金-看好他(基金经理)
    @file_data('test_data/test_custinfo_support.json')
    def test_custinfo_support(self, user_name, password, fund_manager_id, assert_info):
        self._restful_xjb.custinfo_support(user_name=str(user_name), password=str(password),
                                           fund_manager_id=str(fund_manager_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        add_fav_fund, add_fav = self._db.get_fav_fund(mobile=str(user_name), object_id=str(fund_manager_id))
        self.assertEqual(str(fund_manager_id), str(add_fav[0]['object_id']))
        self.assertEqual(add_fav_fund[0]['is_delete'], 0)

        # 更新is_delete字段
        self._db.update_fav_fund(mobile=str(user_name), fund_id=str(fund_manager_id))

    # 基金-基金经理看好情况
    @file_data('test_data/test_custinfo_support_detail.json')
    def test_custinfo_support_detail(self, user_name, password, fund_manager_id, assert_info):
        self._restful_xjb.custinfo_support_detail(user_name=str(user_name), password=str(password),
                                                  fund_manager_id=str(fund_manager_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            cust_fav = self._db.get_support_detail(user_name=str(user_name), fund_manager_id=str(fund_manager_id))
            self.assertEqual(str(entity.body['favCount']), '0' if cust_fav is None else str(len(cust_fav)))
            self.assertEqual(str(entity.body['result']), '0' if cust_fav is None else str(len(cust_fav)))

    # 基金-分红和拆分
    @file_data('test_data/test_get_share_and_split.json')
    def test_test_get_share_and_split(self, user_name, password, fund_id, assert_info):
        self._restful_xjb.get_share_and_split(user_name=str(user_name), password=str(password), fund_id=str(fund_id))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            div_split_list = self._db.get_share_and_split(fund_id=str(fund_id))
            data_list = entity.body_dataList
            if div_split_list is not None:
                for i in range(0, len(div_split_list)):
                    self.assertEqual(decimal.Decimal(str(data_list[i]['bonus'])).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(str(div_split_list[i]['dividend_ratio_before_tax'])).quantize(
                                         decimal.Decimal('0.00')))
                    self.assertEqual(str(data_list[i]['date']), str(div_split_list[i]['register_date'])[0:10])
                    self.assertEqual(str(data_list[i]['type']), str(div_split_list[i]['dividend_or_split']))

    # 基金-基金历史净值
    @file_data('test_data/test_fund_nav_history.json')
    def test_fund_nav_history(self, user_name, password, start_date, fund_id, assert_info):
        self._restful_xjb.fund_nav_history(user_name=str(user_name), password=str(password),
                                           start_date=str(start_date), fund_id=str(fund_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if entity.returnCode == '000000':
            fund_nav, count_fund_nav = self._db.get_fund_nav(fund_id=str(fund_id))
            fund_rise_amplitude = self._db.get_fund_rise_amplitude(fund_id=str(fund_id))
            data_list = entity.dataList
            for i in range(0, len(data_list)-2):
                self.assertEqual(str(data_list[i]['dayRise']), str(decimal.Decimal(
                    fund_rise_amplitude[i]['change_pct']).quantize(decimal.Decimal('0.00'))))
                self.assertEqual(str(data_list[i]['nav']), '%.4f' % float(fund_nav[i]['nav']))
                self.assertEqual(str(data_list[i]['navDate']),
                                 datetime.datetime.strftime(datetime.datetime.strptime(
                                     str(fund_nav[i]['nav_date']), '%Y%m%d'), '%Y-%m-%d'))
                self.assertEqual(str(data_list[i]['totalNav']), '%.4f' % float(fund_nav[i]['total_nav']))
            self.assertEqual(str(entity.totalCount), str(count_fund_nav[0]['nav_count']))

    # 基金-货币基金历史净值
    @file_data('test_data/test_fund_profit_history.json')
    def test_fund_profit_history(self, user_name, password, start_date, fund_id, assert_info):
        self._restful_xjb.fund_profit_history(user_name=str(user_name), password=str(password),
                                              start_date=str(start_date), fund_id=str(fund_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if entity.returnCode == '000000':
            fund_nav, count_fund_nav = self._db.get_fund_nav(fund_id=str(fund_id))
            data_list = entity.dataList
            for i in range(0, len(data_list)):
                self.assertEqual(str(data_list[i]['fundIncomeUnit']), '%.4f' % float(fund_nav[i]['fund_income_unit']))
                self.assertEqual(str(data_list[i]['date']),
                                 datetime.datetime.strftime(datetime.datetime.strptime(
                                     str(fund_nav[i]['nav_date']), '%Y%m%d'), '%Y-%m-%d'))
                self.assertEqual(str(data_list[i]['sevenAnnualizedYield']), '%.3f' % float(fund_nav[i]['yield']))
            self.assertEqual(str(entity.totalCount), str(count_fund_nav[0]['nav_count']))

    # 定活宝极速赎回
    @file_data('test_data/test_redeem_dhb.json')
    def test_redeem_dhb(self, user_name, password, product_id, amt, trade_password, assert_info):
        self._restful_xjb.redeem_dhb(user_name=str(user_name), login_password=str(password), amt=str(amt),
                                     product_id=str(product_id), trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
            pro_info = self._db.get_product_info(product_id=str(product_id))

            # 计算定活宝赎回本金+收益
            day1 = datetime.datetime(2017, 10, 13)
            day2 = datetime.datetime(int(trade_order[0]['AP_DATE'][0:4]), int(trade_order[0]['AP_DATE'][4:6]),
                                     int(trade_order[0]['AP_DATE'][6:8]))
            fix_yield = pro_info[0]['fixed_yield']
            redeem_yield = decimal.Decimal(str(amt)) * decimal.Decimal(str(fix_yield)) / decimal.Decimal(
                100.00) * decimal.Decimal(str(day2 - day1).split(' ')[0]) * decimal.Decimal(1 / 365.00)
            redeem_amt = round(decimal.Decimal(str(amt)) + redeem_yield, 2)

            self.assertIn('资金已到达您的现金宝帐户，您可立即快速取出到银行卡或购买更多理财产品。', str(entity.info))
            self.assertEqual(str(entity.returnResult), 'Y')
            self.assertEqual(str(entity.title), '成功')
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '018')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '018010')
            self.assertEqual(trade_order[0]['AP_AMT'], decimal.Decimal(str(redeem_amt)))
            self.assertEqual(trade_order[0]['SUCC_AMT'], decimal.Decimal(str(redeem_amt)))
            self.assertEqual(str(trade_order[0]['TO_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '1')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['STATUS']), 'Y')

            user_trade_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            near_work_date = self._db.judge_is_work_date(day=str(user_trade_time)[0:8])[0]['WORK_DATE']
            self.assertEqual(str(trade_request[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '0')
            self.assertEqual(trade_request[0]['SUB_AMT'], decimal.Decimal(str(redeem_amt)))
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['RTTA_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
            if str(user_trade_time)[0:8] == str(near_work_date):  # 交易当天为工作日
                if '090000' < str(user_trade_time)[8:14] < '150000':  # 交易为9:00-15：00之间
                    self.assertEqual(str(trade_request[0]['APKIND']), '022')
                    self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022115')
                    self.assertEqual(str(trade_request[0]['REMARK']), 'T+0赎回，实时申购现金宝')
                else:
                    self.assertEqual(str(trade_request[0]['APKIND']), '022')
                    self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022118')
                    self.assertEqual(str(trade_request[0]['REMARK']), '定期宝预约赎回，实时申购现金宝')
            else:
                self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
                self.assertEqual(str(trade_reserve[0]['APKIND']), '024')
                self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '024016')
                self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(product_id))
                self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '1')
                self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
                                 decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(str(trade_reserve[0]['REMARK']), '产品预约信息')
                self.assertEqual(str(trade_reserve[0]['RES_ST']), 'Y')

    # 通用-获取配置项(V3.3)
    @file_data('test_data/test_common_config.json')
    def test_common_config(self, user_name, password, key, assert_info):
        self._restful_xjb.common_config(user_name=str(user_name), password=str(password), key=str(key))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            if str(key) != '':
                common_config_list = self._db.get_common_config_by_code(key=str(key))
                if str(key) == 'isDisplayPoints':
                    self.assertEqual(str(entity.body['isDisplayPoints']), str(common_config_list[0]['value']))
                if str(key) == 'isDisplayLoan':
                    self.assertEqual(str(entity.body['isDisplayLoan']), str(common_config_list[0]['value']))
                if str(key) == 'investPlanUsePointsIntro':
                    self.assertEqual(str(entity.body['investPlanUsePointsIntro']), str(common_config_list[0]['value']))
                if str(key) == 'xjbName':
                    self.assertEqual(str(entity.body['xjbName']), str(common_config_list[0]['value']))
                if str(key) == 'xjbDetail':
                    self.assertEqual(str(entity.body['xjbDetail']), str(common_config_list[0]['value']))
            else:
                common_config_email = self._db.get_common_config_by_code(key='emailInfo')
                common_config_points_intro = self._db.get_common_config_by_code(key='investPlanUsePointsIntro')
                common_config_loan = self._db.get_common_config_by_code(key='isDisplayLoan')
                common_config_points = self._db.get_common_config_by_code(key='isDisplayPoints')
                common_config_offline_info = self._db.get_common_config_by_code(key='offlineInfo')
                common_config_xjb_detail = self._db.get_common_config_by_code(key='xjbDetail')
                common_config_xjb_id = self._db.get_common_config_by_code(key='xjbId')
                common_config_xjb_name = self._db.get_common_config_by_code(key='xjbName')

                self.assertEqual(str(entity.body['emailInfo']), str(common_config_email[0]['value']))
                self.assertEqual(str(entity.body['investPlanUsePointsIntro']),
                                 str(common_config_points_intro[0]['value']))
                self.assertEqual(str(entity.body['isDisplayLoan']), str(common_config_loan[0]['value']))
                self.assertEqual(str(entity.body['isDisplayPoints']), str(common_config_points[0]['value']))
                self.assertEqual(str(entity.body['offlineInfo']), str(common_config_offline_info[0]['value']))
                self.assertEqual(str(entity.body['xjbDetail']), str(common_config_xjb_detail[0]['value']))
                self.assertEqual(str(entity.body['xjbId']), str(common_config_xjb_id[0]['value']))
                self.assertEqual(str(entity.body['xjbName']), str(common_config_xjb_name[0]['value']))

    # 账户-用户修改姓名拼音(V3.3)
    @file_data('test_data/test_update_cust_name_spell.json')
    def test_update_cust_name_spell(self, user_name, password, name_spell, assert_info):
        self._restful_xjb.update_cust_name_spell(user_name=str(user_name), password=str(password),
                                                 name_spell=str(name_spell))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            cust_base = self._db.get_cust_base(user_name=str(user_name))
            self.assertEqual(str(name_spell).upper(), str(cust_base[0]['name_pinyin']))

    # 产品-收益计算器(V3.3)
    @file_data('test_data/test_income_calculator.json')
    def test_income_calculator(self, user_name, password, product_id, purchase_amt, assert_info):
        self._restful_xjb.income_calculator(user_name=str(user_name), password=str(password),
                                            product_id=str(product_id), purchase_amt=str(purchase_amt))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            pdc_info = self._db.get_product_info(product_id=str(product_id))
            pdc_detail = self._db.get_product_detail(productid=str(product_id))
            if str(pdc_detail[0]['invest_period_unit']) == '0':
                unit = '天'
                estimate_income = decimal.Decimal(purchase_amt) * decimal.Decimal(
                    str(pdc_info[0]['float_yield'])[0:len(str(pdc_info[0]['float_yield'])) - 1]) / 100 * \
                                  decimal.Decimal(str(pdc_detail[0]['invest_period'])) / 365
            elif str(pdc_detail[0]['invest_period_unit']) == '1':
                unit = '个月'
                estimate_income = decimal.Decimal(purchase_amt) * decimal.Decimal(
                    str(pdc_info[0]['float_yield'])[0:len(str(pdc_info[0]['float_yield'])) - 1]) / 100 * \
                                  decimal.Decimal(str(pdc_detail[0]['invest_period'])) / 12
            else:
                unit = '年'
                estimate_income = decimal.Decimal(purchase_amt) * decimal.Decimal(
                    str(pdc_info[0]['float_yield'])[0:len(str(pdc_info[0]['float_yield'])) - 1]) / 100 * \
                                  decimal.Decimal(str(pdc_detail[0]['invest_period']))

            if int(str(decimal.Decimal(str(estimate_income)).quantize(decimal.Decimal('0.0000')))[4:5]) >= 5:
                estimate_income += 0.01

            self.assertEqual(str(decimal.Decimal(str(entity.body['estimateIncome'])).quantize(decimal.Decimal('0.00'))),
                             str(estimate_income.quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(entity.body['investPeriod']), str(pdc_detail[0]['invest_period']) + unit)
            self.assertTrue(str(entity.body['investPeriod']) in str(entity.body['tips']))

    # 信用卡 - 卡详情
    @file_data('test_data/test_credit_card_detail.json')
    def test_credit_card_detail(self, user_name, password, card_serial_no, assert_info):
        self._restful_xjb.credit_card_detail(user_name=str(user_name), password=str(password),
                                             card_serial_no=str(card_serial_no))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            cust_credit_card = self._db.get_cust_credit_card(mobile=str(user_name), sort='asc')
            creditcard_repay = self._db.get_creditcard_repay_requests(mobile=str(user_name))
            # self.assertEqual(str(entity.bankLogoUrl), 'http://10.199.111.2/V1/images/cust/bank/icon/' +
            #                  str(cust_credit_card[0]['bank_no']) + '.png')
            self.assertEqual(str(entity.bankName), str(cust_credit_card[0]['bank_name']))
            self.assertEqual(str(entity.bankNameDesc), str(cust_credit_card[0]['bank_name']))
            self.assertEqual(str(entity.bankNo), str(cust_credit_card[0]['bank_no']))
            self.assertEqual(str(entity.cardSerialNo), str(card_serial_no))
            self.assertEqual(str(entity.cardStatus), str(cust_credit_card[0]['state']))
            self.assertEqual(str(entity.cardTailNo), str(cust_credit_card[0]['card_no'])[12:16])
            self.assertEqual(str(entity.cardType), 'C')
            self.assertEqual(str(entity.cardTypeDesc), '信用卡')
            self.assertEqual(str(entity.hasRepayRemind), str(cust_credit_card[0]['is_warn']))
            self.assertEqual(str(entity.hasYyRepay), '0')
            self.assertEqual(str(entity.isRepayPause), '1')
            self.assertEqual(str(entity.totalRepayAmt), '10000.0')
            current_month = datetime.date.today().month
            repay_date = str(creditcard_repay[0]['updated_at'])[5:7]
            if str(current_month) == repay_date:
                self.assertEqual(str(entity.usedRepayAmt), str(creditcard_repay[0]['amount']))
            else:
                self.assertEqual(str(entity.usedRepayAmt), '0.0')

    # 通知中心-个人事项设置
    @file_data('test_data/test_get_personal_setting_list.json')
    def test_get_personal_setting_list(self, user_name, password, sub_type, assert_info):
        self._restful_xjb.get_personal_setting_list(user_name=str(user_name), password=str(password),
                                                    sub_type=str(sub_type))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if entity.returnCode == '000000':
            self.assertEqual(str(entity.body['moduleName']), '个人事项设置')

    # 资讯 - 资讯分类
    @file_data('test_data/test_get_category_list.json')
    def test_get_category_list(self, user_name, password, assert_info):
        self._restful_xjb.get_category_list(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        self.assertEqual(str(entity.categoryTitle[0]), '主页')
        self.assertEqual(str(entity.categoryLink[0]),
                         'http://10.199.111.2/V1/pages/fundIntegration/fund_index.html')
        self.assertEqual(str(entity.categoryTitle[1]), '要闻')
        self.assertEqual(str(entity.categoryLink[1]),
                         'http://10.199.111.2/V1/pages/fundIntegration/information_ask.html?columnId=030008')
        self.assertEqual(str(entity.categoryTitle[2]), '专题')
        self.assertEqual(str(entity.categoryLink[2]), 'http://10.199.111.2/V1/pages/fundIntegration/topic.html')
        self.assertEqual(str(entity.categoryTitle[3]), '理财')
        self.assertEqual(str(entity.categoryLink[3]),
                         'http://10.199.111.2/V1/pages/fundIntegration/information_ask.html?columnId=040007')
        self.assertEqual(str(entity.categoryTitle[4]), '快讯')
        self.assertEqual(str(entity.categoryLink[4]),
                         'http://10.199.111.2/V1/pages/fundIntegration/news_ietter.html')

    # 通用-获取枚举值
    @file_data('test_data/test_get_enum_list.json')
    def test_get_enum_list(self, user_name, password, type, assert_info):
        self._restful_xjb.get_enum_list(user_name=str(user_name), password=str(password), type=str(type))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            enum_list = entity.body_dataList
            for i in range(0, 5):
                self.assertEqual(str(enum_list[i]['enumKey']), str(i + 1))
                if i == 0:
                    self.assertEqual(str(enum_list[i]['enumValue']), '近6月')
                elif i == 4:
                    self.assertEqual(str(enum_list[i]['enumValue']), '近5年')
                else:
                    self.assertEqual(str(enum_list[i]['enumValue']), '近' + str(i) + '年')

    # 基金-定投排行
    @file_data('test_data/test_find_invest_yield_product.json')
    def test_find_invest_yield_product(self, user_name, password, fund_type, period_type, sort_type,
                                       order_desc,
                                       assert_info):
        self._restful_xjb.find_invest_yield_product(user_name=str(user_name), password=str(password),
                                                    fund_type=str(fund_type), period_type=str(period_type),
                                                    sort_type=str(sort_type), order_desc=str(order_desc))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            # to_day = str(Utility.DateUtil().getToday()).replace('-', '')
            find_invest_yield_product_list = self._db.get_find_invest_yield_product(
                fund_type=str(fund_type),
                period_type=str(period_type),
                sort_type=str(sort_type),
                order_desc=str(order_desc))

            data_list = entity.body_dataList
            if find_invest_yield_product_list is not None:
                self.assertEqual(str(entity.body['totalCount']), str(len(find_invest_yield_product_list)))
                num = len(find_invest_yield_product_list) if len(
                    find_invest_yield_product_list) < 100 else 100
                for i in range(0, num):
                    db_daily_return = find_invest_yield_product_list[i]['daily_return']
                    if None == db_daily_return:
                        db_daily_return = ''
                    else:
                        db_daily_return = str(decimal.Decimal(str(round(decimal.Decimal(
                            str(db_daily_return)), 2))).quantize(decimal.Decimal('0.00')))
                        if db_daily_return == '-0.00':
                            db_daily_return = '0.00'
                    self.assertEqual(str(data_list[i]['dailyReturn']), db_daily_return)
                    self.assertEqual(str(data_list[i]['floatYield']),
                                     str(find_invest_yield_product_list[i]['float_yield']))
                    self.assertEqual(str(data_list[i]['fundIncomeUnit']),
                                     '' if str(find_invest_yield_product_list[i][
                                                   'fund_income_unit']) == 'None' else
                                     str(decimal.Decimal(str(round(decimal.Decimal(
                                         str(find_invest_yield_product_list[i]['fund_income_unit'])),
                                         3))).quantize(
                                         decimal.Decimal('0.000'))))
                    self.assertEqual(str(data_list[i]['fundType']),
                                     str(find_invest_yield_product_list[i]['fund_type']))
                    self.assertEqual(str(data_list[i]['isNewIssue']),
                                     str(find_invest_yield_product_list[i]['is_new_issue']))
                    self.assertEqual(str(data_list[i]['latestNav']),
                                     '--' if str(
                                         find_invest_yield_product_list[i]['latest_nav']) == 'None' else
                                     str(decimal.Decimal(str(round(decimal.Decimal(
                                         str(find_invest_yield_product_list[i]['latest_nav'])),
                                         4))).quantize(
                                         decimal.Decimal('0.0000'))))
                    self.assertEqual(str(data_list[i]['latestNavDate']),
                                     str(find_invest_yield_product_list[i]['latest_nav_date'])[4:6] + '-' +
                                     str(find_invest_yield_product_list[i]['latest_nav_date'])[6:8])
                    self.assertEqual(str(data_list[i]['monthInvestCount']),
                                     '共定投' + str(
                                         find_invest_yield_product_list[i]['month_invest_count']) + '次')
                    self.assertEqual(str(data_list[i]['monthInvestYield']),
                                     str(decimal.Decimal(str(round(decimal.Decimal(
                                         str(find_invest_yield_product_list[i]['month_invest_yield'])),
                                         2))).quantize(
                                         decimal.Decimal('0.00'))))
                    self.assertEqual(str(data_list[i]['productFullName']),
                                     str(find_invest_yield_product_list[i]['product_full_name']))
                    self.assertEqual(str(data_list[i]['productId']),
                                     str(find_invest_yield_product_list[i]['productid']))
                    self.assertEqual(str(data_list[i]['productNo']),
                                     str(find_invest_yield_product_list[i]['product_no']))
                    self.assertEqual(str(data_list[i]['productShortName']),
                                     str(find_invest_yield_product_list[i]['product_short_name']))
                    self.assertEqual(str(data_list[i]['weekInvestCount']),
                                     '共定投' + str(
                                         find_invest_yield_product_list[i]['week_invest_count']) + '次')
                    self.assertEqual(str(data_list[i]['weekInvestYield']),
                                     str(decimal.Decimal(str(round(decimal.Decimal(
                                         str(find_invest_yield_product_list[i]['week_invest_yield'])),
                                         2))).quantize(decimal.Decimal('0.00'))))

    # 账户 - 光大提额获取formbean
    @file_data('test_data/test_ceb_bank_quota_form_bean.json')
    def test_ceb_bank_quota_form_bean(self, user_name, password, bank_card_id, assert_info):
        self._restful_xjb.ceb_bank_quota_form_bean(user_name=str(user_name), password=str(password),
                                                   bank_card_id=str(bank_card_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 账户-短信验证登录(V3.3)
    @file_data('test_data/test_sms_login.json')
    def test_sms_login(self, user_name, captcha_code, mobile_code, assert_info):
        self._restful_xjb.sms_login_get_mobile_code(user_name=str(user_name), captcha_code=str(captcha_code),
                                                    mobile_code=str(mobile_code))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            cust_no = entity.custNo
            trade_account = entity.tradeAccount
            expected_cust_no = self._db.get_cust_info(columns='cust_no', match='=',
                                                      mobile=str(user_name))[0]['cust_no']
            expected_trade_acco = self._db.get_trade_acco_info(cust_no=str(expected_cust_no))[0]['trade_acco']

            self.assertEqual(str(cust_no), expected_cust_no)
            self.assertEqual(str(trade_account), expected_trade_acco)

    # 使用优惠券充值现金宝
    @file_data('test_data/test_recharge_using_coupons.json')
    def test_recharge_using_coupons(self, user_name, password, trade_password, recharge_amount, bank_card_id,
                                    bank_no, assert_info):
        self._restful_xjb.recharge_using_coupons(user_name=str(user_name), password=str(password),
                                                 recharge_amount=str(recharge_amount),
                                                 bank_card_id=str(bank_card_id),
                                                 bank_no=str(bank_no), trade_password=str(trade_password))

        entity = self._restful_xjb.entity.current_entity

        self.assertIn(assert_info["returnMsg"], entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            self.assertEqual(str(entity.body_returnResult), 'Y')
            self.assertEqual(str(entity.body_title), '存入成功')
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '001')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '001010')
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(recharge_amount)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['TO_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['STATUS']), 'Y')

            self.assertEqual(str(trade_request[0]['APKIND']), '022')
            self.assertEqual(str(trade_request[0]['SUB_APKIND']), '001100')
            self.assertEqual(str(trade_request[0]['SUB_AMT']),
                             str(decimal.Decimal(str(recharge_amount)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_request[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_request[0]['RTTA_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '0')

    # 现金管理作为支付手段赎回/极速赎回
    @file_data('test_data/test_redeem_product_purchase_by_cash_managment.json')
    def test_redeem_product_purchase_by_cash_managment(self, user_name, password, product_id, product_type,
                                                       sold_share, trade_password, sold_type, is_success,
                                                       assert_info):

        if str(product_type) == '3':
            self._restful_xjb.redeem_vipproduct(user_name=str(user_name), login_password=str(password),
                                                product_id=str(product_id), sold_share=str(sold_share),
                                                trade_password=str(trade_password), sold_type=str(sold_type))
        elif str(product_type) == '2':
            self._restful_xjb.redeem_product(user_name=str(user_name), login_password=str(password),
                                             product_id=str(product_id), sold_share=str(sold_share),
                                             trade_password=str(trade_password), sold_type=str(sold_type))
        else:
            self._restful_xjb.redeem_dhb(user_name=str(user_name), login_password=str(password),
                                         product_id=str(product_id), amt=str(sold_share),
                                         trade_password=str(trade_password))

        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        # 产品普通赎回
        if str(sold_type) == '0':
            if str(is_success) == 'true':
                trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
                trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
                asset_in_transit = self._db.get_asset_in_transit(mobile=str(user_name))
                return_result = entity.returnResult

                # 高端产品普赎
                if str(product_type) == '3':
                    # 校验订单表
                    self.assertEqual(str(return_result), 'Y')
                    self.assertEqual(trade_order[0]['ORDER_APKIND'], '016')
                    self.assertEqual(trade_order[0]['ORDER_SUB_APKIND'], '016010')
                    self.assertEqual(trade_order[0]['AP_AMT'],
                                     decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(trade_order[0]['FROM_PROD'], str(product_id))
                    self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), str(product_type))
                    self.assertEqual(trade_order[0]['TO_PROD'], 'ZX05#000730')
                    self.assertEqual(trade_order[0]['TO_PROD_TYPE'], 0)
                    self.assertEqual(trade_order[0]['STATUS'], 'A')

                    # 检验交易预约表
                    self.assertEqual(trade_reserve[0]['APKIND'], '024')
                    self.assertEqual(trade_reserve[0]['SUB_APKIND'], '024014')
                    self.assertEqual(trade_reserve[0]['SUB_AMT'],
                                     decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(trade_reserve[0]['PROD_ID'], str(product_id))
                    self.assertEqual(trade_reserve[0]['PROD_TYPE'], 3)
                    self.assertTrue('预约' in trade_reserve[0]['REMARK'])

                    # 检验在途表
                    self.assertEqual(asset_in_transit[0]['PROD_ID'], str(product_id))
                    self.assertEqual(str(asset_in_transit[0]['PROD_TYPE']), str(product_type))
                    self.assertEqual(str(asset_in_transit[0]['BALANCE']),
                                     '-' + str(
                                         decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00'))))
                    # self.assertEqual(asset_in_transit[0]['APKIND'], '031')
                    # self.assertEqual(asset_in_transit[0]['SUB_APKIND'], '031100')

                    self.assertTrue(asset_in_transit[0]['APKIND'] in ('024', '031'))
                    self.assertTrue(asset_in_transit[0]['SUB_APKIND'] in ('024014', '031100'))

                # 基金产品普赎
                else:
                    # 校验订单表
                    self.assertEqual(trade_order[0]['ORDER_APKIND'], '016')
                    self.assertEqual(trade_order[0]['ORDER_SUB_APKIND'], '016010')
                    self.assertEqual(trade_order[0]['AP_AMT'],
                                     decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(trade_order[0]['TO_PROD'], 'ZX05#000730')
                    self.assertEqual(trade_order[0]['TO_PROD_TYPE'], 0)
                    self.assertEqual(trade_order[0]['STATUS'], 'A')

                    # 校验交易表
                    self.assertEqual(str(return_result), 'Y')
                    self.assertEqual(trade_request[0]['APKIND'], '024')
                    self.assertEqual(trade_request[0]['SUB_APKIND'], '024013')
                    self.assertEqual(trade_request[0]['SUB_AMT'],
                                     decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(trade_request[0]['PROD_ID'], str(product_id))
                    self.assertEqual(trade_request[0]['RTTA_ST'], 'N')
                    self.assertEqual(trade_request[0]['PAY_ST'], 'N')
                    self.assertEqual(trade_request[0]['APPLY_ST'], 'Y')
                    self.assertEqual(trade_request[0]['PROD_TYPE'], 2)
                    self.assertEqual(trade_request[0]['REMARK'], '赎回基金')

                    # 检验在途表
                    self.assertEqual(asset_in_transit[0]['PROD_ID'], str(product_id))
                    self.assertEqual(str(asset_in_transit[0]['PROD_TYPE']), str(product_type))
                    self.assertEqual(str(asset_in_transit[0]['BALANCE']),
                                     '-' + str(
                                         decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(asset_in_transit[0]['APKIND'], '024')
                    self.assertEqual(asset_in_transit[0]['SUB_APKIND'], '024013')

        # 产品极速赎回
        if str(sold_type) == '1':
            if str(is_success) == 'true':
                trade_request, trade_order = self._db.get_trade_request_vip_product(mobile=str(user_name),
                                                                                    product_id=str(product_id))
                asset_in_transit = self._db.get_asset_in_transit(mobile=str(user_name))
                pdc_marketing = self._db.get_pdc_product_marketing(product_id=str(product_id))

                # 高端产品极速赎回
                if str(product_type) == '3':
                    redeem_amt = decimal.Decimal(sold_share) * pdc_marketing[0]['fast_redeem_cashratio'] / 100 - \
                                 pdc_marketing[0]['fast_redeem_rate']

                    # 校验订单表
                    self.assertEqual(trade_order[0]['ORDER_APKIND'], '019')
                    self.assertEqual(trade_order[0]['ORDER_SUB_APKIND'], '019020')
                    self.assertEqual(trade_order[0]['AP_AMT'],
                                     decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(trade_order[0]['TO_PROD'], 'ZX05#000730')
                    self.assertEqual(trade_order[0]['TO_PROD_TYPE'], 0)
                    self.assertEqual(trade_order[0]['STATUS'], 'A3')
                    self.assertEqual(
                        decimal.Decimal(trade_order[0]['FAST_REDEEM_SUB_AMT']).quantize(
                            decimal.Decimal('0.00')),
                        decimal.Decimal(str(redeem_amt)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(
                        decimal.Decimal(str(pdc_marketing[0]['fast_redeem_rate'])).quantize(
                            decimal.Decimal('0.00')),
                        decimal.Decimal(str(trade_order[0]['FAST_REDEEM_FEE'])).quantize(
                            decimal.Decimal('0.00')))
                    self.assertEqual(
                        decimal.Decimal(str(pdc_marketing[0]['fast_redeem_cashratio'])).quantize(
                            decimal.Decimal('0.00')),
                        decimal.Decimal(str(trade_order[0]['FAST_REDEEM_CASH_RATIO'])).quantize(
                            decimal.Decimal('0.00')))

                    # 校验交易表
                    self.assertEqual(trade_request[0]['APKIND'], '024')
                    self.assertEqual(trade_request[0]['SUB_APKIND'], '024029')
                    self.assertEqual(trade_request[0]['SUB_AMT'],
                                     decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(trade_request[0]['PROD_ID'], str(product_id))
                    self.assertEqual(trade_request[0]['PROD_TYPE'], 3)
                    self.assertEqual(trade_request[0]['REMARK'], '高端T+0极速赎回')
                    self.assertEqual(
                        decimal.Decimal(trade_request[0]['FAST_REDEEM_AMT']).quantize(decimal.Decimal('0.00')),
                        decimal.Decimal(str(redeem_amt)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(
                        decimal.Decimal(str(pdc_marketing[0]['fast_redeem_rate'])).quantize(
                            decimal.Decimal('0.00')),
                        decimal.Decimal(str(trade_request[0]['FAST_REDEEM_FEE'])).quantize(
                            decimal.Decimal('0.00')))
                    self.assertEqual(
                        decimal.Decimal(str(pdc_marketing[0]['fast_redeem_cashratio'])).quantize(
                            decimal.Decimal('0.00')),
                        decimal.Decimal(str(trade_request[0]['FAST_REDEEM_CASH_RATIO'])).quantize(
                            decimal.Decimal('0.00')))

                    # 校验在途表
                    self.assertEqual(asset_in_transit[0]['PROD_ID'], str(product_id))
                    self.assertEqual(str(asset_in_transit[0]['PROD_TYPE']), str(product_type))
                    self.assertEqual(str(asset_in_transit[0]['BALANCE']),
                                     '-' + str(
                                         decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(asset_in_transit[0]['FAST_REDEEM_CASH_RATIO'],
                                     pdc_marketing[0]['fast_redeem_cashratio'])
                    self.assertEqual(asset_in_transit[0]['APKIND'], '024')
                    self.assertEqual(asset_in_transit[0]['SUB_APKIND'], '024029')

                # 基金产品极速赎回
                else:
                    fund_nav, count_fund_nav = self._db.get_fund_nav(fund_id=str(product_id))
                    redeem_amt_order = decimal.Decimal(sold_share) * pdc_marketing[0]['fast_redeem_cashratio'] * \
                                       fund_nav[0]['nav'] / 100 - pdc_marketing[0]['fast_redeem_rate']
                    redeem_amt_request = decimal.Decimal(sold_share) * pdc_marketing[0][
                        'fast_redeem_cashratio'] * \
                                         fund_nav[0]['nav'] / 100
                    if len(str(redeem_amt_order)) > 4 and str(redeem_amt_order)[
                                                          4:len(str(redeem_amt_order))] > 0:
                        redeem_amt_order = float(str(redeem_amt_order)[0:4]) + 0.01

                    if len(str(redeem_amt_request)) > 4 and str(redeem_amt_request)[
                                                            4:len(str(redeem_amt_request))] > 0:
                        redeem_amt_request = float(str(redeem_amt_request)[0:4]) + 0.01

                    # 校验订单表
                    self.assertEqual(trade_order[0]['ORDER_APKIND'], '019')
                    self.assertEqual(trade_order[0]['ORDER_SUB_APKIND'], '019010')
                    self.assertEqual(trade_order[0]['AP_AMT'],
                                     decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(trade_order[0]['TO_PROD'], 'ZX05#000730')
                    self.assertEqual(trade_order[0]['TO_PROD_TYPE'], 0)
                    self.assertEqual(trade_order[0]['SUCC_AMT'],
                                     decimal.Decimal(str(redeem_amt_order)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(trade_order[0]['STATUS'], 'A3')
                    self.assertEqual(
                        decimal.Decimal(trade_order[0]['FAST_REDEEM_SUB_AMT']).quantize(
                            decimal.Decimal('0.00')),
                        decimal.Decimal(str(redeem_amt_order)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(
                        decimal.Decimal(str(pdc_marketing[0]['fast_redeem_rate'])).quantize(
                            decimal.Decimal('0.00')),
                        decimal.Decimal(str(trade_order[0]['FAST_REDEEM_FEE'])).quantize(
                            decimal.Decimal('0.00')))
                    self.assertEqual(
                        decimal.Decimal(str(pdc_marketing[0]['fast_redeem_cashratio'])).quantize(
                            decimal.Decimal('0.00')),
                        decimal.Decimal(str(trade_order[0]['FAST_REDEEM_CASH_RATIO'])).quantize(
                            decimal.Decimal('0.00')))

                    # 校验交易表
                    self.assertEqual(trade_request[0]['APKIND'], '024')
                    self.assertEqual(trade_request[0]['SUB_APKIND'], '024020')
                    self.assertEqual(trade_request[0]['SUB_AMT'],
                                     decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(trade_request[0]['PROD_ID'], str(product_id))
                    self.assertEqual(str(trade_request[0]['PROD_TYPE']), str(product_type))
                    self.assertEqual(trade_request[0]['REMARK'], '赎回基金')
                    self.assertEqual(
                        decimal.Decimal(trade_request[0]['FAST_REDEEM_AMT']).quantize(decimal.Decimal('0.00')),
                        decimal.Decimal(str(redeem_amt_request)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(
                        decimal.Decimal(str(pdc_marketing[0]['fast_redeem_rate'])).quantize(
                            decimal.Decimal('0.00')),
                        decimal.Decimal(str(trade_request[0]['FAST_REDEEM_FEE'])).quantize(
                            decimal.Decimal('0.00')))
                    self.assertEqual(
                        decimal.Decimal(str(pdc_marketing[0]['fast_redeem_cashratio'])).quantize(
                            decimal.Decimal('0.00')),
                        decimal.Decimal(str(trade_request[0]['FAST_REDEEM_CASH_RATIO'])).quantize(
                            decimal.Decimal('0.00')))

                    # 校验在途表
                    self.assertEqual(asset_in_transit[0]['PROD_ID'], str(product_id))
                    self.assertEqual(str(asset_in_transit[0]['PROD_TYPE']), str(product_type))
                    self.assertEqual(str(asset_in_transit[0]['BALANCE']),
                                     '-' + str(
                                         decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(asset_in_transit[0]['FAST_REDEEM_CASH_RATIO'],
                                     pdc_marketing[0]['fast_redeem_cashratio'])
                    self.assertEqual(asset_in_transit[0]['APKIND'], '024')
                    self.assertEqual(asset_in_transit[0]['SUB_APKIND'], '024020')

        # 定活宝产品随心取
        if str(sold_type) == '':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
            pro_info = self._db.get_product_info(product_id=str(product_id))

            # 计算定活宝赎回本金+收益
            day1 = datetime.datetime(2017, 10, 13)
            day2 = datetime.datetime(int(trade_order[0]['AP_DATE'][0:4]), int(trade_order[0]['AP_DATE'][4:6]),
                                     int(trade_order[0]['AP_DATE'][6:8]))
            fix_yield = pro_info[0]['fixed_yield']
            redeem_yield = decimal.Decimal(str(sold_share)) * decimal.Decimal(str(fix_yield)) / decimal.Decimal(
                100.00) * decimal.Decimal(str(day2 - day1).split(' ')[0]) * decimal.Decimal(1 / 365.00)
            redeem_amt = round(decimal.Decimal(str(sold_share)) + redeem_yield, 2)

            self.assertIn('资金已到达您的现金宝帐户，您可立即快速取出到银行卡或购买更多理财产品。', str(entity.info))
            self.assertEqual(str(entity.returnResult), 'Y')
            self.assertEqual(str(entity.title), '成功')
            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '018')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '018010')
            self.assertEqual(trade_order[0]['AP_AMT'], decimal.Decimal(str(redeem_amt)))
            self.assertEqual(trade_order[0]['SUCC_AMT'], decimal.Decimal(str(redeem_amt)))
            self.assertEqual(str(trade_order[0]['TO_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD']), str(product_id))
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '1')
            self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['STATUS']), 'Y')

            user_trade_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            near_work_date = self._db.judge_is_work_date(day=str(user_trade_time)[0:8])[0]['WORK_DATE']
            self.assertEqual(str(trade_request[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '0')
            self.assertEqual(trade_request[0]['SUB_AMT'], decimal.Decimal(str(redeem_amt)))
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['RTTA_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
            if str(user_trade_time)[0:8] == str(near_work_date):  # 交易当天为工作日
                if '090000' < str(user_trade_time)[8:14] < '150000':  # 交易为9:00-15：00之间
                    self.assertEqual(str(trade_request[0]['APKIND']), '022')
                    self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022115')
                    self.assertEqual(str(trade_request[0]['REMARK']), 'T+0赎回，实时申购现金宝')
                else:
                    self.assertEqual(str(trade_request[0]['APKIND']), '022')
                    self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022118')
                    self.assertEqual(str(trade_request[0]['REMARK']), '定期宝预约赎回，实时申购现金宝')
            else:
                self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
                self.assertEqual(str(trade_reserve[0]['APKIND']), '024')
                self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '024016')
                self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(product_id))
                self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '1')
                self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
                                 decimal.Decimal(str(sold_share)).quantize(decimal.Decimal('0.00')))
                self.assertEqual(str(trade_reserve[0]['REMARK']), '产品预约信息')
                self.assertEqual(str(trade_reserve[0]['RES_ST']), 'Y')

    # 通知中心-首页理财日历(V3.3)
    @file_data('test_data/test_index_fin_calendar.json')
    def test_index_fin_calendar(self, user_name, password, assert_info):
        self._restful_xjb.index_fin_calendar(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            modlue_list = self._db.get_modlue_list()
            noc_builder, noc_template = self._db.get_noc(user_name=str(user_name))

            # 计算每个周一的日期
            begin = datetime.date(2017, 11, 13)
            now = time.strftime('%Y%m%d', time.localtime(time.time()))
            calendar_list = {}
            j = 0
            for i in range(0, 100):
                if begin + datetime.timedelta(7 * i) >= datetime.date(int(now[0:4]), int(now[4:6]),
                                                                      int(now[6:8])):
                    calendar_list[j] = begin + datetime.timedelta(7 * i)
                    cal = calendar_list[j]
                    calendar_list[j] = self._db.judge_is_work_date(day=str(cal.strftime('%Y%m%d')))
                    j += 1
            has_product_sale_notice = '1' if noc_builder[0]['NOTICE_TYPE'] == 100000 else '0'

            data_list = entity.body_dataList
            for i in range(0, len(data_list)):
                self.assertTrue(noc_builder[0]['OUTER_KEY'] in data_list[i]['calendarLink'])
                self.assertEqual(str(calendar_list[i][0]['WORK_DATE'])[6:8], data_list[i]['dateInfo'])
                self.assertEqual(str(data_list[i]['hasProductSaleNotice']), has_product_sale_notice)
                self.assertEqual(str(calendar_list[i][0]['WORK_DATE'])[4:6], data_list[i]['monthInfo'])
                self.assertTrue(str(calendar_list[i][0]['WORK_DATE']), data_list[i]['time'])
                self.assertEqual(str(noc_template[0]['TEMPLATE_NAME']), data_list[i]['title'])
                self.assertEqual(str(noc_template[0]['MARKET_FLAG']), data_list[i]['titleIntro'])
                self.assertEqual(str(noc_builder[0]['NOTICE_TYPE']), data_list[i]['type'])
                self.assertTrue(str(calendar_list[i][0]['WORK_DATE'])[0:4], data_list[i]['yearInfo'])

            self.assertEqual(entity.moduleDesc, modlue_list[0]['desc'])
            self.assertEqual(entity.moduleLink, modlue_list[0]['link'])
            self.assertEqual(entity.moduleName, modlue_list[0]['name'])

    # 使用优惠券信用卡还款
    @file_data('test_data/test_creditcard_repay_using_coupon.json')
    def test_creditcard_repay_using_coupon(self, user_name, password, amt, trade_password, assert_info):
        card = self._db.get_cust_credit_card(mobile=str(user_name), sort='desc')
        self._restful_xjb.creditcard_repay_using_coupon(mobile=str(user_name), password=str(password),
                                                        card_id=str(card[0]['id']), amt=str(amt),
                                                        trade_password=str(trade_password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertTrue(assert_info['returnMsg'] in entity.returnMsg)

        if entity.returnCode == '000000':
            time.sleep(30)
            creditcard_repay_req = self._db.get_creditcard_repay_requests(mobile=str(user_name))
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            coupon_batch = self._db.get_coupon_batch(code='FULL_OFF_3_1_0070')
            discount_amount = coupon_batch[0]['AMOUNT']
            self.assertEqual(str(entity.info), '信用卡还款申请已受理！')
            self.assertEqual(str(entity.returnResult), 'I')

            self.assertEqual(creditcard_repay_req[0]['repay_type'], 'M')
            self.assertEqual(creditcard_repay_req[0]['amount'],
                             decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00')))
            self.assertEqual(creditcard_repay_req[0]['card_no'], str(card[0]['card_no']))
            self.assertEqual(creditcard_repay_req[0]['accept_mode'], 'M')
            self.assertEqual(creditcard_repay_req[0]['tran_st'], 'Y')
            self.assertEqual(creditcard_repay_req[0]['success_amount'],
                             decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00')))
            self.assertEqual(creditcard_repay_req[0]['real_pay_amount'],
                             decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00')) - discount_amount)

            self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '030')
            self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '030010')
            self.assertEqual(str(trade_order[0]['AP_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['SUCC_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_order[0]['FROM_PROD']), 'ZX05#000730')
            self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '0')
            self.assertEqual(str(trade_order[0]['STATUS']), 'Y')
            self.assertEqual(str(trade_order[0]['COUPON_AMOUNT']), str(discount_amount))

            self.assertEqual(str(trade_request[0]['APKIND']), '098')
            self.assertEqual(str(trade_request[0]['SUB_APKIND']), '098001')
            self.assertEqual(str(trade_request[0]['SUB_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00')) - discount_amount))
            self.assertEqual(str(trade_request[0]['SUCC_AMT']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00'))))
            self.assertEqual(str(trade_request[0]['PROD_ID']), 'ZX05#000730')
            self.assertEqual(str(trade_request[0]['RTTA_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
            self.assertEqual(str(trade_request[0]['PROD_TYPE']), '0')
            self.assertEqual(str(trade_request[0]['COUPON_AMOUNT']), str(discount_amount))

    # 使用优惠券预约还款信用卡 设置还款日在后天
    @file_data('test_data/test_creditcard_reserve_repay_using_coupon.json')
    def test_creditcard_reserve_repay_using_coupon(self, user_name, password, amt, trade_password, assert_info):
        card = self._db.get_cust_credit_card(mobile=str(user_name), sort='desc')
        self._db.update_creditcard_order_state(card_id=str(card[0]['id']), orign_state='N', update_state='C')
        self._restful_xjb.creditcard_reserve_repay_using_coupon(user_name=str(user_name), password=str(password),
                                                                repay_amt=str(amt), card_serial_no=str(card[0]['id']),
                                                                trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info['returnCode'])
        self.assertTrue(assert_info['returnMsg'] in entity.returnMsg)

        if entity.returnCode == '000000':
            coupon_batch = self._db.get_coupon_batch(code='FULL_OFF_3_1_0070')
            discount_amount = coupon_batch[0]['AMOUNT']
            credit_card_repay_order = self._db.get_creditcard_repay_order(card_id=str(card[0]['id']))

            self.assertEqual(credit_card_repay_order[0]['amount'],
                             decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00')))
            the_day_after_tomorrow = Utility.DateUtil().getToday() + datetime.timedelta(days=2)
            the_day_after_today = the_day_after_tomorrow - datetime.timedelta(days=1)
            # 还款日 D1
            self.assertEqual(str(credit_card_repay_order[0]['repay_date']),
                             the_day_after_tomorrow.strftime('%Y%m%d'))
            # 实际还款日 = 还款日的前一天，如果还款日是非工作日，如周六，周日，则实际扣款日为周五
            while self._db.determine_if_work_day(the_day_after_today.strftime('%Y%m%d')) is False:
                the_day_after_today = the_day_after_today - datetime.timedelta(days=1)

            self.assertEqual(str(credit_card_repay_order[0]['real_repay_date']),
                             the_day_after_today.strftime('%Y%m%d'))

            # 判断是否为工作日，不是获取下个工作日
            new_work_date = self._db.judge_is_work_date(day=str(the_day_after_tomorrow).replace('-', ''))
            the_day_after_tomorrow = new_work_date[0]['WORK_DATE']
            self.assertEqual(str(credit_card_repay_order[0]['repay_work_date']), str(the_day_after_tomorrow))
            self.assertEqual(str(credit_card_repay_order[0]['state']), 'N')
            self.assertEqual(str(credit_card_repay_order[0]['check_state']), 'N')
            self.assertEqual(str(credit_card_repay_order[0]['repay_state']), 'N')
            self.assertEqual(str(credit_card_repay_order[0]['real_pay_amount']),
                             str(decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00')) - discount_amount))

    # 通知中心-理财日历(V3.3)
    @file_data('test_data/test_fin_calendar.json')
    def test_fin_calendar(self, user_name, password, month, assert_info):
        self._restful_xjb.fin_calendar(user_name=str(user_name), password=str(password), month=str(month))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            noc_builder, noc_template = self._db.get_noc(user_name=str(user_name))

            # 计算每个周一的日期
            begin = datetime.date(2017, 11, 13)
            now = time.strftime('%Y%m%d', time.localtime(time.time()))
            calendar_list = {}
            j = 0
            for i in range(1, 100):
                if begin + datetime.timedelta(7 * i) <= datetime.date(int(now[0:4]), int(now[4:6]),
                                                                      int(now[6:8])):
                    if int(now[0:4]) == 2018:
                        if str(begin + datetime.timedelta(7 * i))[5:7] == '12':
                            calendar_list[j] = begin + datetime.timedelta(7 * i)
                            j += 1
                    else:
                        if str(begin + datetime.timedelta(7 * i))[5:7] == str(int(now[4:6]) - 1):
                            calendar_list[j] = begin + datetime.timedelta(7 * i)
                            j += 1

            has_product_sale_notice = '1' if noc_builder[0]['NOTICE_TYPE'] == 100000 else '0'

            data_list = entity.body_dataList
            self.assertTrue(noc_builder[0]['OUTER_KEY'] in data_list[0]['calendarLink'])
            self.assertEqual(str(calendar_list[0].strftime('%Y%m%d'))[6:8], data_list[0]['dateInfo'])
            self.assertEqual(str(data_list[0]['hasProductSaleNotice']), has_product_sale_notice)
            self.assertEqual(str(calendar_list[0].strftime('%Y%m%d'))[4:6], data_list[0]['monthInfo'])
            self.assertTrue(str(calendar_list[0].strftime('%Y%m%d')), data_list[0]['time'])
            self.assertEqual(str(noc_template[0]['TEMPLATE_NAME']), data_list[0]['title'])
            self.assertEqual(str(noc_template[0]['MARKET_FLAG']), data_list[0]['titleIntro'])
            self.assertEqual(str(noc_builder[0]['NOTICE_TYPE']), data_list[0]['type'])
            self.assertTrue(str(calendar_list[0].strftime('%Y%m%d'))[0:4], data_list[0]['yearInfo'])
            self.assertEqual(entity.moduleName, '个人事项提醒')

    # 产品-高端货币类产品历史收益(V3.4)
    @file_data('test_data/test_vip_product_history_profit.json')
    def test_vip_product_history_profit(self, user_name, password, product_id, assert_info):
        self._restful_xjb.vip_product_history_profit(user_name=str(user_name), password=str(password),
                                                     product_id=str(product_id))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            his_profit_list = self._db.get_vip_product_history_profit(product_id=str(product_id))

            l = len(his_profit_list) if len(his_profit_list) < 100 else 100
            data_list = entity.body_dataList
            self.assertEqual(str(l), str(entity.body_totalCount))
            if l > 0:
                for i in range(0, l):
                    self.assertEqual(str(data_list[i]['date']).replace('-', ''), str(his_profit_list[i]['nav_date']))
                    self.assertEqual(str(data_list[i]['fundIncomeUnit']),
                                     str(decimal.Decimal(str(his_profit_list[i]['fund_income_unit'])).quantize(
                                         decimal.Decimal('0.0000'))))
                    self.assertEqual(str(data_list[i]['sevenAnnualizedYield']),
                                     str(decimal.Decimal(str(his_profit_list[i]['yield'])).quantize(
                                         decimal.Decimal('0.000'))))

    # 产品-高端权益类产品历史收益(V3.4)
    @file_data('test_data/test_vip_product_history_nav.json')
    def test_vip_product_history_nav(self, user_name, password, product_id, assert_info):
        self._restful_xjb.vip_product_history_nav(user_name=str(user_name), password=str(password),
                                                  product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            his_nav_list = self._db.get_vip_product_history_profit(product_id=str(product_id))

            l = len(his_nav_list) if len(his_nav_list) < 100 else 100
            data_list = entity.body_dataList
            self.assertEqual(str(l), str(entity.body_totalCount))
            if l > 0:
                for i in range(0, l):
                    self.assertEqual(str(data_list[i]['date']).replace('-', ''), str(his_nav_list[i]['nav_date']))
                    self.assertEqual(str(data_list[i]['fundIncomeUnit']),
                                     '--' if str(his_nav_list[i]['fund_income_unit']) == 'None' else str(
                                         decimal.Decimal(str(his_nav_list[i]['fund_income_unit'])).quantize(
                                             decimal.Decimal('0.0000'))))
                    self.assertEqual(str(data_list[i]['sevenAnnualizedYield']),
                                     '-' if str(his_nav_list[i]['yield']) == 'None' else str(
                                         decimal.Decimal(str(his_nav_list[i]['yield'])).quantize(
                                             decimal.Decimal('0.000'))))

    # 产品-高端历史回报相关内容(V3.4)
    @file_data('test_data/test_vip_product_history_income.json')
    def test_vip_product_history_nav(self, user_name, password, product_id, assert_info):
        self._restful_xjb.vip_product_history_income(user_name=str(user_name), password=str(password),
                                                     product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            data_list = entity.body_dataList
            fund_rise_amplitude = self._db.get_fund_rise_amplitude(fund_id=str(product_id))
            highend_detail_list, highend_investor_list = self._db.get_highend_detail(product_id=str(product_id))
            invest_target = '暂无相关内容' if highend_detail_list[0]['invest_goal'] == '' \
                else str(highend_detail_list[0]['invest_goal'])
            if len(fund_rise_amplitude) == 0 and (len(highend_detail_list) > 0 or len(highend_investor_list) > 0):
                self.assertEqual(str(entity.body['totalCount']), '1')
                self.assertEqual(str(data_list[0]['channelName']), '投资目标')
                self.assertEqual(str(data_list[0]['channelType']), '1')
                for i in range(0, len(highend_detail_list)):
                    self.assertEqual(str(data_list[0]['dataList'][i]['investTarget']), invest_target)

    # 产品-高端详情概况(V3.4)
    @file_data('test_data/test_vip_product_survey.json')
    def test_vip_product_survey(self, user_name, password, product_id, assert_info):
        self._restful_xjb.vip_product_survey(user_name=str(user_name), password=str(password),
                                             product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 银行卡 - 重新签约(V3.4)
    @file_data('test_data/test_card_sign_again.json')
    def test_card_sign_again(self, mobile, password, bank_card_id, assert_info):
        self._restful_xjb.card_sign_again(mobile=str(mobile), password=str(password), bank_card_id=str(bank_card_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if entity.returnCode == '000000':
            self.assertEqual(str(entity.authResult), 'Y')
            self.assertEqual(str(entity.channelType), '快捷')
            card_info = self._db.get_bank_card_by_serial_id(serial_id=str(bank_card_id))[0]
            self.assertIn(str(card_info['card_no'][15:19]), str(entity.info))
            self.assertIn(str(card_info['serial_id']), str(bank_card_id))
            self.assertEqual(card_info['type'], '1')
            self.assertEqual(str(card_info['bank_mobile']), str(mobile))
            self.assertEqual(str(card_info['accept_mode']), 'M')
            self.assertEqual(str(card_info['sign_type']), '07')

    # 产品-高端详情规则(V3.4)
    @file_data('test_data/test_vip_product_ruler.json')
    def test_vip_product_ruler(self, user_name, password, product_id, assert_info):
        self._restful_xjb.vip_product_ruler(user_name=str(user_name), password=str(password),
                                            product_id=str(product_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            highend_detail_list, highend_investor_list = self._db.get_highend_detail(product_id=str(product_id))
            product_info_list = self._db.get_product_info(product_id=str(product_id))
            issue_info_list = self._db.get_issue_info(product_id=str(product_id))
            if len(highend_detail_list) < 1:
                open_desc = '暂无相关内容'
                profit_assign = '暂无相关内容'
            else:
                open_desc = '暂无相关内容' if highend_detail_list[0]['open_desc'] == '' else highend_detail_list[0][
                    'open_desc']
                profit_assign = '暂无相关内容' if highend_detail_list[0]['profit_assign'] == '' else highend_detail_list[0][
                    'profit_assign']
                profit_assign_desc = '' if highend_detail_list[0]['profit_assign'] == '' else highend_detail_list[0][
                    'profit_assign_desc']

            range_amount = '--' if product_info_list[0]['min_add_amount'] is None else str(decimal.Decimal(
                str(product_info_list[0]['min_add_amount'])).quantize(decimal.Decimal('0.1'))) + '元'

            if issue_info_list[0]['product_status'] == '4':
                min_subscribe_amount = str(decimal.Decimal(str(product_info_list[0]['min_buy_amount'])).quantize(
                    decimal.Decimal('0.1'))) + '元'
            else:
                min_subscribe_amount = str(
                    decimal.Decimal(str(product_info_list[0]['min_subscribe_amount'])).quantize(
                        decimal.Decimal('0.1'))) + '元'
            trustee_ratio = '0.00%' if product_info_list[0]['trustee_ratio'] == '' else product_info_list[0][
                'trustee_ratio']
            manage_rate = '0.00%' if product_info_list[0]['manager_ratio'] == '' else product_info_list[0][
                'manager_ratio']
            issue_face_value = '--' if product_info_list[0]['issue_facevalue'] == '' else str(
                product_info_list[0]['issue_facevalue'])[0:1] + '元'
            data_list = entity.body_dataList
            self.assertEqual(str(data_list['issueFacevalue']), issue_face_value)
            self.assertEqual(str(data_list['manageRate']), manage_rate)
            self.assertEqual(str(data_list['minSubscribeAmount']), min_subscribe_amount)
            self.assertEqual(str(data_list['openDesc']), open_desc)
            self.assertEqual(str(data_list['profitAssign']), profit_assign)
            self.assertEqual(str(data_list['profitAssignDesc']), profit_assign_desc)
            self.assertEqual(str(data_list['rangeAmount']), range_amount)
            self.assertEqual(str(data_list['trusteeRate']), trustee_ratio)

    # 通用 - 开锁页面格言（V3.4）
    @file_data('test_data/test_get_maxim.json')
    def test_get_maxim(self, user_name, password, assert_info):
        self._restful_xjb.get_maxim(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            maxim = self._db.get_pro_intro(user_name=str(user_name), categary_code='MAXIM')
            day = Utility.DateUtil().getToday().day
            if day > len(maxim):
                index = day % len(maxim)
                if index == 0:
                    self.assertEqual(entity.info, str(maxim[len(maxim) - 1]['value']))
                else:
                    self.assertEqual(entity.info, str(maxim[index - 1]['value']))
            else:
                self.assertEqual(entity.info, str(maxim[day - 1]['value']))

    # 消息中心-首页Tips（V3.4）
    @file_data('test_data/test_msg_index_tips.json')
    def test_msg_index_tips(self, user_name, password, position, assert_info):
        self._restful_xjb.msg_index_tips(user_name=str(user_name), password=str(password), position=str(position))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 基金-理财型基金自动续存提示文案(V3.4)
    @file_data('test_data/test_finance_fund_auto_purchase_tip.json')
    def test_finance_fund_auto_purchase_tip(self, user_name, password, fund_id, assert_info):
        self._restful_xjb.finance_fund_auto_purchase_tip(user_name=str(user_name), password=str(password),
                                                         fund_id=str(fund_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            prod_info_list = self._db.get_product_info(product_id=str(fund_id))
            operate_period_unit = prod_info_list[0]['operate_period_unit']
            operate_period = int(prod_info_list[0]['operate_period'])
            ack_buy_day = int(prod_info_list[0]['ack_buy_day'])
            now = datetime.datetime.now()
            now_date = now.strftime('%Y%m%d%H%M%S')
            if str(now_date)[8:14] < '150000':  # 交易当时为15：00之前
                now_date = now_date
            else:  # 交易当时为15：00之后
                now_date = now + datetime.timedelta(days=1)
                now_date = now_date.strftime('%Y%m%d%H%M%S')
            now_date_work_date = self._db.judge_is_work_date(day=str(now_date)[0:8])
            for i in range(0, ack_buy_day):
                ack_work_date = self._db.get_next_work_date(pre_work_date=str(now_date_work_date[0]['WORK_DATE']))
            ack_redeem_day = int(prod_info_list[0]['ack_redeem_day'])
            delivery_day = prod_info_list[0]['delivery_day']
            max_day = int(delivery_day) - 1 if (int(delivery_day) - 1) > 0 else 0
            day = ack_redeem_day + max_day
            if operate_period_unit == '4':
                unit = '年'
                after_year = int(str(now_date_work_date[0]['WORK_DATE'])[0:4]) + operate_period
                after_day = str(after_year) + str(now_date_work_date[0]['WORK_DATE'])[4:6] + \
                            str(now_date_work_date[0]['WORK_DATE'])[6:8]
                afetr_year_work_date = self._db.judge_is_work_date(day=str(after_day))
                for i in range(0, day):
                    arrival_date = self._db.get_next_work_date(pre_work_date=
                                                               str(afetr_year_work_date[0]['WORK_DATE']))
                arrival_date_final = str(arrival_date[0]['WORK_DATE'])[0:4] + '-' + \
                                     str(arrival_date[0]['WORK_DATE'])[4:6] + '-' + \
                                     str(arrival_date[0]['WORK_DATE'])[6:8]

            elif operate_period_unit == '3':
                unit = '月'
                after_month = int(str(now_date_work_date[0]['WORK_DATE'])[4:6]) + operate_period
                if after_month > 12:
                    after_month = after_month - 12
                    after_year = int(str(now_date_work_date[0]['WORK_DATE'])[0:4]) + 1
                else:
                    after_month = after_month
                    after_year = int(str(now_date_work_date[0]['WORK_DATE'])[0:4])
                after_month = '0' + str(after_month) if len(str(after_month)) == 1 else str(after_month)
                after_day = str(after_year) + str(after_month) + str(now_date_work_date[0]['WORK_DATE'])[6:8]
                after_year_work_date = self._db.judge_is_work_date(day=str(after_day))
                for i in range(0, day):
                    arrival_date = self._db.get_next_work_date(pre_work_date=
                                                               str(after_year_work_date[0]['WORK_DATE']))
                arrival_date_final = str(arrival_date[0]['WORK_DATE'])[0:4] + '-' + \
                                     str(arrival_date[0]['WORK_DATE'])[4:6] + '-' + \
                                     str(arrival_date[0]['WORK_DATE'])[6:8]
            elif operate_period_unit == '2':
                unit = '周'
                now_date_work_date = datetime.datetime.strptime(str(now_date_work_date[0]['WORK_DATE']), '%Y%m%d')
                day = operate_period * 7
                after_day = now_date_work_date + datetime.timedelta(days=day)
                after_day = after_day.strftime("%Y%m%d%H%M%S")
                afetr_year_work_date = self._db.judge_is_work_date(day=str(after_day)[0:8])
                for i in range(0, day):
                    arrival_date = self._db.get_next_work_date(pre_work_date=
                                                               str(afetr_year_work_date[0]['WORK_DATE']))
                arrival_date_final = str(arrival_date[0]['WORK_DATE'])[0:4] + '-' + \
                                     str(arrival_date[0]['WORK_DATE'])[4:6] + '-' + \
                                     str(arrival_date[0]['WORK_DATE'])[6:8]
            else:
                unit = '日'
                now_date_work_date = datetime.datetime.strptime(str(now_date_work_date[0]['WORK_DATE']), '%Y%m%d')
                after_day = now_date_work_date + datetime.timedelta(days=operate_period)
                after_day = after_day.strftime("%Y%m%d%H%M%S")
                afetr_year_work_date = self._db.judge_is_work_date(day=str(after_day)[0:8])
                for i in range(0, day):
                    arrival_date = self._db.get_next_work_date(pre_work_date=
                                                               str(afetr_year_work_date[0]['WORK_DATE']))
                arrival_date_final = str(arrival_date[0]['WORK_DATE'])[0:4] + '-' + \
                                     str(arrival_date[0]['WORK_DATE'])[4:6] + '-' + \
                                     str(arrival_date[0]['WORK_DATE'])[6:8]

            self.assertEqual(str(entity.body['close']), '自动续存关闭，到期后本金和收益自动转到现金宝，预计' +
                             arrival_date_final + '日24:00前到账')
            self.assertEqual(str(entity.body['open']), '自动续存开启，到期后本金和收益继续买入下一期，继续封闭' +
                             str(operate_period) + unit)

    # 基金 - 基金转换(V3.4)
    @file_data('test_data/test_fund_transfer.json')
    def test_fund_transfer(self, user_name, password, from_fund_id, to_fund_id, expire_dispose_type, transfer_share,
                           type, trade_password, assert_info):
        self._restful_xjb.fund_transfer(user_name=str(user_name), password=str(password),
                                        from_fund_id=str(from_fund_id), to_fund_id=str(to_fund_id),
                                        expire_dispose_type=str(expire_dispose_type), type=str(type),
                                        transfer_share=str(transfer_share), trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if entity.returnCode == '000000':
            user_trade_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            if str(user_trade_time)[8:14] < '150000':  # 交易当时为15：00之前
                tomorrow = Utility.DateUtil().getToday() + datetime.timedelta(days=1)
                excepted_day = self._db.judge_is_work_date(day=str(tomorrow).replace('-', ''))[0]['WORK_DATE']
            else:
                the_day_after_tomorrow = Utility.DateUtil().getToday() + datetime.timedelta(days=2)
                excepted_day = self._db.judge_is_work_date(
                    day=str(the_day_after_tomorrow).replace('-', ''))[0]['WORK_DATE']
            current_year = str(excepted_day)[0:4]
            current_month = str(excepted_day)[4:6]
            day = str(excepted_day)[6:8]

            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            asset_in_trasit = self._db.get_asset_in_transit(mobile=str(user_name))

            self.assertEqual(entity.info, '预计' + current_year + '年' + current_month + '月' + day + '日确认')
            self.assertEqual(entity.title, '转换申请已受理！')
            if type == '0':
                self.assertEqual(str(trade_order[0]['AP_AMT']),
                                 str(decimal.Decimal(str(transfer_share)).quantize(decimal.Decimal('0.00'))))
                self.assertEqual(str(trade_order[0]['FROM_PROD']), str(from_fund_id))
                self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '2')
                self.assertEqual(str(trade_order[0]['TO_PROD']), str(to_fund_id))
                self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '2')
                self.assertEqual(str(trade_order[0]['STATUS']), 'A')
                self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '036')
                self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '036010')

                self.assertEqual(str(trade_request[0]['PROD_TYPE']), '2')
                self.assertEqual(str(trade_request[0]['TO_PROD_TYPE']), '2')
                self.assertEqual(str(trade_request[0]['RTTA_ST']), 'N')
                self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
                self.assertEqual(str(trade_request[0]['PAY_ST']), 'N')
                self.assertEqual(str(trade_request[0]['PROD_ID']), str(from_fund_id))
                self.assertEqual(str(trade_request[0]['SUB_AMT']),
                                 str(decimal.Decimal(str(transfer_share)).quantize(decimal.Decimal('0.00'))))
                self.assertEqual(str(trade_request[0]['APKIND']), '036')
                self.assertEqual(str(trade_request[0]['SUB_APKIND']), '036001')
                self.assertEqual(str(trade_request[0]['REMARK']), '基金普通转换')

                self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '2')
                self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
                self.assertEqual(str(asset_in_trasit[0]['BRANCH_CODE']), '675')
                self.assertEqual(str(asset_in_trasit[0]['TANO']), str(from_fund_id).split('#')[0])
                self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(from_fund_id))
                self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                                 str(-decimal.Decimal(transfer_share).quantize(decimal.Decimal('0.00'))))
                self.assertEqual(str(asset_in_trasit[0]['APKIND']), '036')
                self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '036001')
            elif type == '1':
                fast_redeem_amt = decimal.Decimal(transfer_share) * (trade_order[0]['FAST_REDEEM_CASH_RATIO'] / 100)
                self.assertEqual(str(trade_order[0]['AP_AMT']),
                                 str(decimal.Decimal(str(transfer_share)).quantize(decimal.Decimal('0.00'))))
                self.assertEqual(str(trade_order[0]['FROM_PROD']), str(from_fund_id))
                self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '2')
                self.assertEqual(str(trade_order[0]['TO_PROD']), str(to_fund_id))
                self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '2')
                self.assertEqual(str(trade_order[0]['STATUS']), 'A')
                self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '037')
                self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '037010')
                self.assertEqual(str(trade_order[0]['FAST_REDEEM_SUB_AMT']), str(fast_redeem_amt))
                self.assertEqual(str(trade_order[0]['FAST_REDEEM_CASH_RATIO']), '80.00')
                self.assertEqual(str(trade_order[0]['FAST_REDEEM_CHARGE_TYPE']), '2')

                self.assertEqual(str(trade_request[0]['REMARK']), '基金极速转换')
                self.assertEqual(str(trade_request[0]['PROD_TYPE']), '2')
                self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['RTTA_ST']), 'N')
                self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
                if str(trade_request[0]['PROD_ID']) == str(from_fund_id):
                    self.assertEqual(str(trade_request[0]['PROD_ID']), str(from_fund_id))
                    self.assertEqual(str(trade_request[0]['TANO']), str(from_fund_id).split('#')[0])
                    self.assertEqual(str(trade_request[0]['SUB_AMT']),
                                     str(decimal.Decimal(str(transfer_share)).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(str(trade_request[0]['APKIND']), '024')
                    self.assertEqual(str(trade_request[0]['SUB_APKIND']), '024047')
                    self.assertEqual(str(trade_request[0]['PAY_ST']), 'N')
                    self.assertEqual(str(trade_request[0]['FAST_REDEEM_AMT']), str(fast_redeem_amt))
                    self.assertEqual(str(trade_request[0]['FAST_REDEEM_CASH_RATIO']), '80.00')
                    self.assertEqual(str(trade_request[0]['FAST_REDEEM_CHARGE_TYPE']), '1')
                elif str(trade_request[0]['PROD_ID']) == str(to_fund_id):
                    self.assertEqual(str(trade_request[0]['PROD_ID']), str(to_fund_id))
                    self.assertEqual(str(trade_request[0]['TANO']), str(to_fund_id).split('#')[0])
                    self.assertEqual(str(trade_request[0]['SUB_AMT']), str(fast_redeem_amt))
                    self.assertEqual(str(trade_request[0]['APKIND']), '022')
                    self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022229')
                    self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')

                self.assertEqual(str(asset_in_trasit[0]['PROD_TYPE']), '2')
                self.assertEqual(str(asset_in_trasit[0]['SHARE_TYPE']), 'A')
                self.assertEqual(str(asset_in_trasit[0]['BRANCH_CODE']), '675')
                if str(asset_in_trasit[0]['PROD_ID']) == str(from_fund_id):
                    self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(from_fund_id))
                    self.assertEqual(str(asset_in_trasit[0]['TANO']), str(from_fund_id).split('#')[0])
                    self.assertEqual(str(asset_in_trasit[0]['BALANCE']),
                                     str(-decimal.Decimal(transfer_share).quantize(decimal.Decimal('0.00'))))
                    self.assertEqual(str(asset_in_trasit[0]['FAST_REDEEM_CASH_RATIO']), '80.00')
                    # 024赎回 024047基金极速转换赎回
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '024')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '024047')
                elif str(asset_in_trasit[0]['PROD_ID']) == str(to_fund_id):
                    self.assertEqual(str(asset_in_trasit[0]['PROD_ID']), str(to_fund_id))
                    self.assertEqual(str(asset_in_trasit[0]['TANO']), str(to_fund_id).split('#')[0])
                    self.assertEqual(str(asset_in_trasit[0]['BALANCE']), str(fast_redeem_amt))
                    self.assertEqual(str(asset_in_trasit[0]['FAST_REDEEM_CASH_RATIO']), '100.00')
                    # 022申购 022229基金极速转换申购
                    self.assertEqual(str(asset_in_trasit[0]['APKIND']), '022')
                    self.assertEqual(str(asset_in_trasit[0]['SUB_APKIND']), '022229')

    # 产品 - 转换提示信息
    @file_data('test_data/test_transfer_to_fund_tip.json')
    def test_transfer_to_fund_tip(self, user_name, password, to_fund_id, from_fund_id, type, transfer_share,
                                  assert_info):
        self._restful_xjb.transfer_to_fund_tip(user_name=str(user_name), password=str(password),
                                               to_fund_id=str(to_fund_id), from_fund_id=str(from_fund_id),
                                               type=str(type), transfer_share=str(transfer_share))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if entity.returnCode == '000000':
            trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
            productinfo = self._db.get_product_info(product_id=str(to_fund_id))
            if type == '0':
                if str(productinfo[0]['transfer_discount']).__eq__('100.0000'):
                    self.assertEqual(str(entity.info), '温馨提示：交易费用=转出基金赎回费+转换补差费')
                else:
                    discount = productinfo[0]['transfer_discount'] / 10
                    self.assertEqual(str(entity.info), '温馨提示：交易费用=转出基金赎回费+转换补差费(' + str(discount) + ')')
                self.assertEqual(str(entity.normalTransferInfoLink),
                                 'hxxjb://commonh5?url=https%3A%2F%2Fappuat.shhxzq.com%2Fh5static%2Fapp%2FFundh5%2FConvertIntro.html%3FfundId%3D05%2523000811')
                self.assertEqual(str(entity.fastTransferInfoLink),
                                 'hxxjb://commonh5?url=https%3A%2F%2Fappuat.shhxzq.com%2Fh5static%2Fapp%2FFundh5%2FfastTransIntro.html%3FfromFundId%3D05%2523000811%26toFundId%3D05%2523000219')
            elif type == '1':
                fast_redeem_amt = decimal.Decimal(transfer_share) * (
                    trade_order[0]['FAST_REDEEM_CASH_RATIO'] / 100)
                self.assertEqual(str(entity.fastTransferInfoLink),
                                 'hxxjb://commonh5?url=https%3A%2F%2Fappuat.shhxzq.com%2Fh5static%2Fapp%2FFundh5%2FfastTransIntro.html%3FfromFundId%3D05%2523000810%26toFundId%3D74%2523000812')
                self.assertIn('温馨提示：交易费用=转出基金的赎回费+转入基金的申购费', str(entity.info))
                self.assertEqual(str(entity.normalTransferInfoLink),
                                 'hxxjb://commonh5?url=https%3A%2F%2Fappuat.shhxzq.com%2Fh5static%2Fapp%2FFundh5%2FConvertIntro.html%3FfundId%3D05%2523000810')
                self.assertEqual(str(entity.lineThroughInfo), '5.00%')
                self.assertEqual(str(entity.toAmtInfo), '转入金额=转出基金最新净值（1.0000）*转出份额*' + str(
                    trade_order[0]['FAST_REDEEM_CASH_RATIO']) + '%')

    # 交易-理财型基金修改到期处理方式(V3.4)
    @file_data('test_data/test_modify_finance_fund_expire_dispose_type.json')
    def test_modify_finance_fund_expire_dispose_type(self, user_name, password, trade_password,
                                                     expire_dispose_type,
                                                     expire_quit_amt, fund_id, value_date, expire_date,
                                                     assert_info):
        prod_renew_list = self._db.select_cts_prod_renew(user_name=str(user_name), fund_id=str(fund_id),
                                                         value_date=str(value_date))
        due_process_type_original = prod_renew_list[0]['DUE_PROCESS_TYPE']
        prod_id_original = prod_renew_list[0]['PROD_ID']
        value_date_original = prod_renew_list[0]['VALUE_DATE']
        red_amt_original = prod_renew_list[0]['RED_AMT']

        self._restful_xjb.modify_finance_fund_expire_dispose_type(user_name=str(user_name),
                                                                  password=str(password),
                                                                  trade_password=str(trade_password),
                                                                  expire_dispose_type=str(expire_dispose_type),
                                                                  expire_quit_amt=str(expire_quit_amt),
                                                                  fund_id=str(fund_id),
                                                                  value_date=str(value_date),
                                                                  expire_date=str(expire_date))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertTrue(assert_info["returnMsg"] in str(entity.returnMsg))

        if entity.returnCode == '000000':
            prod_renew_list = self._db.select_cts_prod_renew(user_name=str(user_name), fund_id=str(fund_id),
                                                             value_date=str(value_date))
            if str(expire_dispose_type) == '1':
                red_amt = decimal.Decimal(str(expire_quit_amt)).quantize(decimal.Decimal('0.00'))

                self.assertEqual(str(prod_renew_list[0]['DUE_PROCESS_TYPE']), 'AR')
                self.assertEqual(str(prod_renew_list[0]['RED_AMT']), str(red_amt))
            else:
                self.assertEqual(str(prod_renew_list[0]['DUE_PROCESS_TYPE']), 'AO')

            # 更新数据为转换前的数据
            self._db.update_cts_prod_renew(user_name=str(user_name), fund_id=str(prod_id_original),
                                           value_date=str(value_date_original),
                                           due_process_type=str(due_process_type_original),
                                           red_amt=str(red_amt_original))
        if entity.returnCode == '013032':
            prod_info = self._db.get_product_info(product_id=str(fund_id))
            min_hold_amount = prod_info[0]['min_hold_amount']
            self.assertTrue(str(min_hold_amount) in str(entity.returnMsg))

    # 产品 - 转换基本信息
    @file_data('test_data/test_transfer_to_fund_info.json')
    def test_transfer_to_fund_info(self, user_name, password, to_fund_id, type, from_fund_id, assert_info):
        self._restful_xjb.transfer_to_fund_info(user_name=str(user_name), password=str(password),
                                                to_fund_id=str(to_fund_id), type=str(type),
                                                from_fund_id=str(from_fund_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if entity.returnCode == '000000':
            user_trade_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            if str(user_trade_time)[8:14] < '150000':  # 交易当时为15：00之前
                tomorrow = Utility.DateUtil().getToday() + datetime.timedelta(days=1)
                excepted_day = self._db.judge_is_work_date(day=str(tomorrow).replace('-', ''))[0]['WORK_DATE']
            else:
                the_day_after_tomorrow = Utility.DateUtil().getToday() + datetime.timedelta(days=2)
                excepted_day = self._db.judge_is_work_date(
                    day=str(the_day_after_tomorrow).replace('-', ''))[0]['WORK_DATE']
            current_month = str(excepted_day)[4:6]
            day = str(excepted_day)[6:8]
            self.assertEqual(entity.confirmDateInfo, '预计' + current_month + '月' + day + '日确认份额')

    # 产品 - 检索可转换基金(V3.4)
    @file_data('test_data/test_search_can_transfer_fund_list.json')
    def test_search_can_transfer_fund_list(self, user_name, password, from_fund_id, keyword, assert_info):
        self._restful_xjb.search_can_transfer_fund_list(user_name=str(user_name), password=str(password),
                                                        from_fund_id=str(from_fund_id), keyword=str(keyword))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if entity.returnCode == '000000':
            data_list = entity.dataList
            search_transfer_fund_list = self._db.search_can_transfer_fast_fund(keyword=str(keyword),
                                                                               from_product_id=str(from_fund_id))
            len_search_transfer_fund_list = len(search_transfer_fund_list)
            if len_search_transfer_fund_list > 20:
                len_search_transfer_fund_list = 20
            for i in range(0, len_search_transfer_fund_list):
                min_amount = search_transfer_fund_list[i]['min_convert_amount']
                if min_amount is None:
                    min_amount = '0.00'
                self.assertEqual(str(data_list[i]['displayName']),
                                 str(search_transfer_fund_list[i]['product_short_name']) +
                                 str(search_transfer_fund_list[i]['product_no']))
                self.assertEqual(str(data_list[i]['firstLetterName']),
                                 str(search_transfer_fund_list[i]['product_pinyin']))
                self.assertEqual(str(data_list[i]['fundCode']), str(search_transfer_fund_list[i]['product_no']))
                self.assertEqual(str(data_list[i]['fundId']), str(search_transfer_fund_list[i]['productid']))
                self.assertEqual(str(data_list[i]['fundName']),
                                 str(search_transfer_fund_list[i]['product_short_name']))
                self.assertEqual(str(data_list[i]['fundType']), str(search_transfer_fund_list[i]['fund_type']))
                self.assertEqual(str(data_list[i]['isFav']), '0')
                self.assertEqual(str(data_list[i]['minTransferShare']), str(min_amount))
                self.assertEqual(str(data_list[i]['positionType']), '0')
                # self.assertEqual(str(data_list[i]['transferType']),
                #                  str(search_transfer_fund_list[i]['support_fast_transfer']))

    # 交易-理财型基金修改到期处理方式提示信息(V3.4)
    @file_data('test_data/test_modify_finance_fund_expire_dispose_type_tip.json')
    def test_modify_finance_fund_expire_dispose_type_tip(self, user_name, password, expire_dispose_type,
                                                         fund_id,
                                                         value_date, expire_date, order_no, holding_type,
                                                         redeem_value, assert_info):
        self._restful_xjb.modify_finance_fund_expire_dispose_type_tip(user_name=str(user_name),
                                                                      password=str(password),
                                                                      expire_dispose_type=str(
                                                                          expire_dispose_type),
                                                                      fund_id=str(fund_id),
                                                                      value_date=str(value_date),
                                                                      expire_date=str(expire_date),
                                                                      order_no=str(order_no),
                                                                      holding_type=str(holding_type),
                                                                      redeem_value=str(redeem_value))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            prod_detail_list = self._db.get_finance_fund_prod_detail(user_name=str(user_name),
                                                                     product_id=str(fund_id),
                                                                     value_date=str(value_date))
            total_balance = prod_detail_list[0]['total_balance']
            left_balance = decimal.Decimal(str(total_balance)).quantize(
                decimal.Decimal('0.00')) - decimal.Decimal(
                str(redeem_value)).quantize(decimal.Decimal('0.00'))
            if str(expire_dispose_type) == '1':
                # 计算到账日
                prod_info_list = self._db.get_product_info(product_id=str(fund_id))
                expire_work_date = self._db.judge_is_work_date(day=str(expire_date).replace('-', ''))
                ack_redeem_day = int(prod_info_list[0]['ack_redeem_day'])
                delivery_day = prod_info_list[0]['delivery_day']
                max_day = int(delivery_day) - 1 if (int(delivery_day) - 1) > 0 else 0
                day = ack_redeem_day + max_day
                for i in range(0, day):
                    arrival_date = self._db.get_next_work_date(pre_work_date=
                                                               str(expire_work_date[0]['WORK_DATE']))
                arrival_date_final = str(arrival_date[0]['WORK_DATE'])[0:4] + '-' + \
                                     str(arrival_date[0]['WORK_DATE'])[4:6] + '-' + \
                                     str(arrival_date[0]['WORK_DATE'])[6:8]

                if decimal.Decimal(str(redeem_value)).quantize(decimal.Decimal('0.00')) < decimal.Decimal(
                        str(total_balance)).quantize(decimal.Decimal('0.00')):
                    self.assertTrue('将于到期日自动赎回' + str(
                        decimal.Decimal(str(redeem_value)).quantize(
                            decimal.Decimal('0.00'))) + '份基金份额至您的现金宝账户' in str(
                        entity.body['info']).replace(',', ''))
                    self.assertTrue(
                        str(arrival_date_final) + ' 24:00' in str(entity.body['info']).replace(',', ''))
                    self.assertTrue(
                        '剩余' + str(left_balance) + '份及对应收益将自动续存，继续封闭一个周期。到期日当天15:00之前可修改' in str(
                            entity.body['info']).replace(',', ''))
                else:
                    self.assertTrue(str(arrival_date_final) + ' 24:00' in str(entity.body['info']))
                    self.assertTrue('本金及收益将于到期日自动赎回至您的现金宝账户' in str(entity.body['info']))
            else:
                self.assertTrue('本金及收益将于到期日继续封闭一个周期，收益不间断。到期日当天15:00之前可修改' in str(entity.body['info']))

    # 积分-福利中心(V3.4)
    @file_data('test_data/test_welfare_center.json')
    def test_welfare_center(self, user_name, password, assert_info):
        self._restful_xjb.welfare_center(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 积分-福利中心主页积分信息(V3.4)
    @file_data('test_data/test_my_points_info.json')
    def test_my_points_info(self, user_name, password, assert_info):
        self._restful_xjb.my_points_info(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            points_list = self._db.get_cust_total_points_amount(mobile=str(user_name))
            coin_list = self._db.get_coin(mobile=str(user_name))
            points_amount = decimal.Decimal(str(points_list[0]['AMOUNT']))
            points_frozen = decimal.Decimal(str(points_list[0]['FROZEN_AMOUNT']))
            coin_amount = decimal.Decimal(str(coin_list[0]['AMOUNT']))
            coin_frozen = decimal.Decimal(str(coin_list[0]['FROZEN_AMOUNT']))
            points_valid = points_amount - points_frozen
            coin_valid = coin_amount - coin_frozen
            self.assertEqual(str(entity.body['pointsCount']), str(points_valid))
            self.assertEqual(str(entity.body['ybCount']), str(coin_valid))

    # 基金-基金费率详情(V3.4)
    @file_data('test_data/test_get_fund_info.json')
    def test_get_fund_info(self, user_name, password, fund_id, fund_type, charge_rate_type, assert_info):
        self._restful_xjb.get_fund_info(user_name=str(user_name), password=str(password), fund_id=str(fund_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            prodinfo_list = self._db.get_product_info(product_id=str(fund_id))
            if str(fund_type) == '1':
                max_purchase_amt = prodinfo_list[0]['large_amount_per_day'] \
                    if prodinfo_list[0]['large_amount_per_day'] is not None else '无限额'
            else:
                max_purchase_amt = prodinfo_list[0]['large_amount_per_day'] \
                    if prodinfo_list[0]['large_amount_per_day'] is not None else ''
            min_increase_amt = prodinfo_list[0]['min_add_amount'] \
                if prodinfo_list[0]['min_add_amount'] is not None else '0.00'
            min_purchase_amt = prodinfo_list[0]['min_buy_amount'] \
                if prodinfo_list[0]['min_buy_amount'] is not None else '0.00'
            min_rsp_amount = prodinfo_list[0]['min_rsp_amount'] \
                if prodinfo_list[0]['min_rsp_amount'] is not None else '0.00'

            if str(charge_rate_type) == '11010':
                # 日常申购费前端
                fund_purchase_rate = self._db.get_fund_base_rate(product_id=str(fund_id),
                                                                 charge_rate_type=str(charge_rate_type))
                div_stand_unit = fund_purchase_rate[0]['div_stand_unit']
                start_div_stand = fund_purchase_rate[0]['start_div_stand']
                end_div_stand = fund_purchase_rate[0]['end_div_stand']
                if_apply_start = fund_purchase_rate[0]['if_apply_start']
                if_apply_end = fund_purchase_rate[0]['if_apply_end']
                tt = 'M'

            if str(charge_rate_type) == '12000':
                # 赎回费
                fund_redeem_rate = self._db.get_fund_base_rate(product_id=str(fund_id),
                                                               charge_rate_type=str(charge_rate_type))
                div_stand_unit = fund_redeem_rate[0]['div_stand_unit']
                start_div_stand = fund_redeem_rate[0]['start_div_stand']
                end_div_stand = fund_redeem_rate[0]['end_div_stand']
                if_apply_start = fund_redeem_rate[0]['if_apply_start']
                if_apply_end = fund_redeem_rate[0]['if_apply_end']
                tt = 'Y'

            if str(div_stand_unit) == '1':
                unit = '年'
            elif str(div_stand_unit) == '2':
                unit = '月'
            elif str(div_stand_unit) == '3':
                unit = '日'
            elif str(div_stand_unit) == '4':
                unit = '万元'
            elif str(div_stand_unit) == '5':
                unit = '万份'
            elif str(div_stand_unit) == '6':
                unit = '%'
            elif str(div_stand_unit) == '7':
                unit = '元'
            elif str(div_stand_unit) == '8':
                unit = '笔'
            elif str(div_stand_unit) == '9':
                unit = '次'
            else:
                amount = str(int(start_div_stand)) if str(start_div_stand) != '' else "0" + "&le;" + tt

            if str(if_apply_start) == '1':
                if str(int(start_div_stand)) == '0':
                    begin = str(int(start_div_stand)) + '&le;' + tt
                else:
                    begin = str(int(start_div_stand)) + unit + '&le;' + tt
            else:
                if str(int(start_div_stand)) == '0':
                    begin = str(int(start_div_stand)) + '&lt;M'
                else:
                    begin = str(int(start_div_stand)) + unit + '&lt;' + tt

            if str(int(end_div_stand)) != '0':
                if str(int(if_apply_end)) == '1':
                    end = '&le;' + str(int(end_div_stand)) + unit
                else:
                    end = '&lt;' + str(int(end_div_stand)) + unit
            amount = begin + end

        self.assertEqual(str(entity.body['maxPurchaseAmt']), max_purchase_amt)
        self.assertEqual(str(entity.body['minIncreaseAmt']), str(min_increase_amt))
        self.assertEqual(str(entity.body['minPurchaseAmt']), str(min_purchase_amt))
        self.assertEqual(str(entity.body['minRspAmount']), str(min_rsp_amount))

        if str(charge_rate_type) == '11010':
            self.assertEqual(str(entity.body['fundPurchaseRate'][0]['amount']), amount)
        if str(charge_rate_type) == '12000':
            self.assertEqual(str(entity.body['fundRedeemRate'][0]['timelimit']), amount)

    # 产品 - 可转换基金列表
    @file_data('test_data/test_can_transfer_fund_list.json')
    def test_can_transfer_fund_list(self, user_name, password, from_fund_id, type, assert_info):
        self._restful_xjb.can_transfer_fund_list(user_name=str(user_name), password=str(password),
                                                 from_fund_id=str(from_fund_id), type=str(type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            self.assertEqual(str(entity.productIntro), '基金普通转换和极速转换的区别......')
            normal_transfer_fund_list = self._db.get_normal_transfer_fund_list(product_id=str(from_fund_id))
            if type == '0':
                data_list = entity.dataList
                self.assertEqual(str(entity.totalCount), str(len(normal_transfer_fund_list)))
            elif type == '1':
                data_list = entity.dataList
                fast_transfer_fund_list = self._db.get_fast_transfer_fund_list()
                len_fast_transfer_fund_list = len(fast_transfer_fund_list)
                if len_fast_transfer_fund_list > 20:
                    len_fast_transfer_fund_list = 20
                for i in range(0, len_fast_transfer_fund_list):
                    charge_rate = '%s%%' % str(
                        decimal.Decimal(fast_transfer_fund_list[i]['max_charge_rate_subscribe']).quantize(
                            decimal.Decimal('0.00')))
                    if charge_rate == '0.00%':
                        charge_rate = ''
                    self.assertEqual(str(data_list[i]['discount']), charge_rate)
                    self.assertEqual(str(data_list[i]['fundCode']),
                                     str(fast_transfer_fund_list[i]['product_no']))
                    self.assertEqual(str(data_list[i]['fundId']), str(fast_transfer_fund_list[i]['productid']))
                    self.assertEqual(str(data_list[i]['fundName']),
                                     str(fast_transfer_fund_list[i]['product_short_name']))
                    self.assertEqual(str(data_list[i]['fundType']),
                                     str(fast_transfer_fund_list[i]['fund_type']))
                    self.assertEqual(str(data_list[i]['minBuyAmt']),
                                     str(format(fast_transfer_fund_list[i]['min_buy_amount'], ',')) + '元')
                    self.assertEqual(str(data_list[i]['minTransferShare']), '0.00')
                    self.assertIn(str(decimal.Decimal(fast_transfer_fund_list[i]['latest_nav']).quantize(
                        decimal.Decimal('0.0000'))), str(data_list[i]['nav']))
                    self.assertEqual(str(data_list[i]['positionType']), '0')
                    self.assertEqual(str(data_list[i]['transferType']), str(type))
                    self.assertEqual(str(entity.totalCount), str(len(fast_transfer_fund_list)))

    # 交易 - 我的历史持有列表(定期/高端/基金)
    @file_data('test_data/test_my_hold_list_history.json')
    def test_my_hold_list_history(self, user_name, password, product_type, fund_type, assert_info):
        self._restful_xjb.my_hold_list_history(user_name=str(user_name), password=str(password),
                                               product_type=str(product_type), fund_type=str(fund_type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if entity.returnCode == '000000':
            prod_holding_his, prod_info_list = self._db.get_holding_his(user_name=str(user_name),
                                                                        product_type=str(product_type),
                                                                        fund_type=str(fund_type))
            vip_prod_type_list = {}
            for i in range(0, len(prod_info_list)):
                if str(prod_info_list[i][0]['high_wealth_type']) == '1':
                    vip_prod_type = '1'
                    vip_prod_type_list[i] = vip_prod_type
                elif str(prod_info_list[i][0]['high_wealth_type']) == '2':
                    vip_prod_type = '0'
                    vip_prod_type_list[i] = vip_prod_type
                    if str(prod_info_list[i][0]['share_regist_type']) == '0':
                        vip_prod_type = '2'
                        vip_prod_type_list[i] = vip_prod_type
                else:
                    vip_prod_type = '3'
                    vip_prod_type_list[i] = vip_prod_type

            data_list = entity.body_dataList
            self.assertEqual(str(entity.body['totalCount']), str(len(prod_holding_his)))
            if str(product_type) == '2':
                for i in range(0, len(prod_holding_his)):
                    self.assertEqual(str(data_list[i]['batchNo']), str(prod_holding_his[i]['ID']))
                    self.assertEqual(str(data_list[i]['productId']), str(prod_holding_his[i]['PROD_ID']))
                    self.assertEqual(str(data_list[i]['totalIncomeValue']), str(prod_holding_his[i]['PERIOD_PROFIT']))
                    self.assertEqual(str(data_list[i]['vipProductType']), str(vip_prod_type_list[i]))
            else:
                for j in range(0, len(prod_holding_his)):
                    self.assertEqual(str(data_list[j]['batchNo']), str(prod_holding_his[j]['ID']))
                    self.assertEqual(str(data_list[j]['productId']), str(prod_holding_his[j]['PROD_ID']))
                    self.assertEqual(str(data_list[j]['totalIncomeValue']),
                                     str(prod_holding_his[j]['PERIOD_PROFIT']))
                    self.assertEqual(str(data_list[j]['vipProductType']), str(vip_prod_type_list[j]))

    # 交易 - 我的历史定期宝产品详情
    @file_data('test_data/test_my_dqb_detail_history.json')
    def test_my_dqb_detail_history(self, user_name, password, batch_no, assert_info):
        self._restful_xjb.my_dqb_detail_history(user_name=str(user_name), password=str(password),
                                                batch_no=str(batch_no))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            data_list = entity.body_detail
            prod_his, prod_info, prod_marketing, prod_issue, open_day = self._db.get_history_list_by_batch_no(
                user_name=str(user_name), batch_no=str(batch_no))
            last_work_date_list = self._db.get_last_work_date(day=str(open_day[0]['open_day']))
            arrival_date = str(prod_info[0]['money_to_account'])
            can_redeem_anytime = '1' if str(prod_marketing[0]['is_redem_anytime']) == '1' else '0'
            product_name = str(prod_his[0]['PROD_NAME'])
            total_income = str(prod_his[0]['PERIOD_PROFIT'])
            yield_type_original = str(prod_info[0]['yield_type'])
            if yield_type_original == '0':
                expected_annual_yield = str(prod_info[0]['fixed_yield'])[0:4] + '%'
            elif yield_type_original == '1':
                expected_annual_yield = str(prod_info[0]['float_yield'])
            elif yield_type_original == '2':
                expected_annual_yield = str(prod_info[0]['float_yield'])
            elif yield_type_original == '3':
                expected_annual_yield = str(prod_info[0]['float_yield'])
            elif yield_type_original == '4':
                expected_annual_yield = str(prod_info[0]['total_nav'])[0:4] \
                    if str(prod_info[0]['total_nav']) == 'none' else '--'
            elif yield_type_original == '5':
                expected_annual_yield = str(prod_info[0]['latest_nav'])[0:4] \
                    if str(prod_info[0]['total_nav']) == 'none' else '--'
            elif yield_type_original == '6':
                expected_annual_yield = str(prod_info[0]['frombuild_return'])[0:2] + '%' \
                    if str(prod_info[0]['total_nav']) == 'none' else '--'
            expire_date = str(prod_info[0]['share_next_carry_date'])[0:4] + '.' + \
                          str(prod_info[0]['share_next_carry_date'])[4:6] + '.' + \
                          str(prod_info[0]['share_next_carry_date'])[6:8]
            issue_time_org = str(prod_issue[0]['issue_time'])[0:8]
            issue_time = str(issue_time_org)[0:4] + '.' + str(issue_time_org)[4:6] + '.' + \
                         str(issue_time_org)[6:8]
            last_work_date = str(last_work_date_list[0]['WORK_DATE'])
            redeem_anytime_start_date = last_work_date[4:6] + '.' + last_work_date[6:8] + " " + "15:00"
            redeem_anytime_end_date = str(open_day[0]['open_day_enddate'])[4:6] + '.' + \
                                      str(open_day[0]['open_day_enddate'])[6:8] + " " + "15:00"
            value_date = str(prod_info[0]['share_carry_date'])[0:4] + '.' + \
                         str(prod_info[0]['share_carry_date'])[4:6] + '.' + \
                         str(prod_info[0]['share_carry_date'])[6:8]

            self.assertEqual(str(data_list['arrivalDate']), arrival_date)
            self.assertEqual(str(data_list['canRedeemAnytime']), can_redeem_anytime)
            self.assertEqual(str(data_list['expectedAnnualYield']), expected_annual_yield)
            self.assertEqual(str(data_list['expiryDate']), expire_date)
            self.assertEqual(str(data_list['issueTime']), issue_time)
            self.assertEqual(str(data_list['productId']), str(prod_info[0]['productid']))
            self.assertEqual(str(data_list['productName']), product_name)
            self.assertEqual(str(data_list['redeemAnytimeStartDate']), redeem_anytime_start_date)
            self.assertEqual(str(data_list['redeemAnytimeEndDate']), redeem_anytime_end_date)
            self.assertEqual(str(data_list['totalIncome']), total_income)
            self.assertEqual(str(data_list['valueDate']), value_date)

    # 交易 - 我的历史高端产品详情
    @file_data('test_data/test_my_vip_detail_history.json')
    def test_my_vip_product_list_history(self, user_name, password, batch_no, assert_info):
        self._restful_xjb.my_vip_product_detail_history(user_name=str(user_name), password=str(password),
                                                        batch_no=str(batch_no))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            data_list = entity.body_detail
            prod_his, prod_info, prod_marketing, prod_issue, open_day = self._db.get_history_list_by_batch_no(
                user_name=str(user_name), batch_no=str(batch_no))
            arrival_date = str(prod_info[0]['money_to_account'])
            product_name = str(prod_his[0]['PROD_NAME'])
            total_income = str(prod_his[0]['PERIOD_PROFIT'])
            yield_type_original = str(prod_info[0]['yield_type'])
            if yield_type_original == '0':
                expected_annual_yield = str(prod_info[0]['fixed_yield'])[0:4] + '%'
            elif yield_type_original == '1':
                expected_annual_yield = str(prod_info[0]['float_yield'])
            elif yield_type_original == '2':
                expected_annual_yield = str(prod_info[0]['float_yield'])
            elif yield_type_original == '3':
                expected_annual_yield = str(prod_info[0]['float_yield'])
            elif yield_type_original == '4':
                expected_annual_yield = str(prod_info[0]['total_nav'])[0:4] \
                    if str(prod_info[0]['total_nav']) == 'none' else '--'
            elif yield_type_original == '5':
                expected_annual_yield = str(prod_info[0]['latest_nav'])[0:4] \
                    if str(prod_info[0]['total_nav']) == 'none' else '--'
            elif yield_type_original == '6':
                expected_annual_yield = str(prod_info[0]['frombuild_return'])[0:2] + '%' \
                    if str(prod_info[0]['total_nav']) == 'none' else '--'

            str_expire_date = str(prod_info[0]['share_next_carry_date'])[0:4] + '.' + \
                              str(prod_info[0]['share_next_carry_date'])[4:6] + '.' + \
                              str(prod_info[0]['share_next_carry_date'])[6:8]
            expire_date = '--' if str(prod_info[0]['share_next_carry_date']) == '' else str_expire_date

            str_value_date = str(prod_info[0]['share_carry_date'])[0:4] + '.' + \
                             str(prod_info[0]['share_carry_date'])[4:6] + '.' + \
                             str(prod_info[0]['share_carry_date'])[6:8]
            value_date = '--' if str(prod_info[0]['share_carry_date']) == '' else str_value_date

            if str(prod_info[0]['high_wealth_type']) == '1':
                vip_prod_type = '1'
            elif str(prod_info[0]['high_wealth_type']) == '2':
                vip_prod_type = '0'
                if str(prod_info[0]['share_regist_type']) == '0':
                    vip_prod_type = '2'
            else:
                vip_prod_type = '3'

            self.assertEqual(str(data_list['arrivalDate']), arrival_date)
            self.assertEqual(str(data_list['expectedAnnualYield']), expected_annual_yield)
            self.assertEqual(str(data_list['expiryDate']), expire_date)
            self.assertEqual(str(data_list['productId']), str(prod_info[0]['productid']))
            self.assertEqual(str(data_list['productName']), product_name)
            self.assertEqual(str(data_list['totalIncome']), total_income)
            self.assertEqual(str(data_list['valueDate']), value_date)
            self.assertEqual(str(data_list['vipProductType']), str(vip_prod_type))

    # 交易 - 我的历史基金产品详情
    @file_data('test_data/test_my_fund_detail_history.json')
    def test_my_fund_detail_history(self, user_name, password, batch_no, assert_info):
        self._restful_xjb.my_fund_detail_history(user_name=str(user_name), password=str(password),
                                                 batch_no=str(batch_no))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            data_list = entity.body_detail
            prod_his, prod_info, prod_marketing, prod_issue, open_day = self._db.get_history_list_by_batch_no(
                user_name=str(user_name), batch_no=str(batch_no))
            fund_nav, fund_nav_count = self._db.get_fund_nav(fund_id=str(prod_his[0]['PROD_ID']))
            fund_id = str(prod_his[0]['PROD_ID'])
            fund_name = str(prod_his[0]['PROD_NAME'])
            total_income = str(prod_his[0]['PERIOD_PROFIT'])
            net_value = '--' if str(fund_nav[0]['nav']) == '' or str(fund_nav[0]['nav']) == 'null' else str(
                fund_nav[0]['nav'])[0:6]
            nav_date = str(fund_nav[0]['nav_date'])[4:8]
            net_value_date = '-' if str(fund_nav[0]['nav_date']) == '' else nav_date[0:2] + '-' + nav_date[2:4]
            self.assertEqual(str(data_list['fundId']), fund_id)
            self.assertEqual(str(data_list['fundName']), fund_name)
            self.assertEqual(str(data_list['netValue']), net_value)
            self.assertEqual(str(data_list['netValueDate']), net_value_date)
            self.assertEqual(str(data_list['totalIncome']), total_income)

    # 风险测评-测评结果预确认(V3.4)
    @file_data('test_data/test_get_risk_type_by_answer.json')
    def test_get_risk_type_by_answer(self, user_name, password, question_no, answer, score, assert_info):
        self._restful_xjb.get_risk_type_by_answer(user_name=str(user_name), password=str(password),
                                                  question_no=str(question_no), answer=str(answer), score=str(score))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            cust_base = self._db.get_cust_base(user_name=str(user_name))
            cal_total_score = self._db.cal_total_score(question_no=str(question_no))
            answer_str = str(answer).split(',')

            total_score = 0
            for i in range(0, len(answer_str)):
                if 'score' + answer_str[i] == 'scorea':
                    score = cal_total_score[i]['scorea']
                elif 'score' + answer_str[i] == 'scoreb':
                    score = cal_total_score[i]['scoreb']
                elif 'score' + answer_str[i] == 'scorec':
                    score = cal_total_score[i]['scorec']
                elif 'score' + answer_str[i] == 'scored':
                    score = cal_total_score[i]['scored']
                else:
                    score = cal_total_score[i]['scoree']

                total_score = total_score + score

            if str(cust_base[0]['type']) == '0':
                if total_score <= 27:
                    risk_level = '1'
                    risk_level_desc = '保守型'
                    risk_level_detail_desc = '您对风险容忍度非常低，在任何投资中，保护本金不受损失和保持资产的流动性是您的首要目标。' \
                                             '您对投资的态度是希望投资收益率极度稳定，不愿承担高风险以换取高收益，追求稳定。' \
                                             '您比较适合投资存款、国债、保本保收益的理财产品、货币型基金、保本基金。'
                elif total_score <= 41:
                    risk_level = '2'
                    risk_level_desc = '谨慎型'
                    risk_level_detail_desc = '您的风险容忍度较低，您希望在保护本金不受损失和保持资产流动性的前提下，' \
                                             '追求适当的增值收入，但您不愿意承担较大风险以换取高收益，在投资波动比较大的情况下，' \
                                             '您会比较紧张。您比较适合投资存款、国债、保本保收益的理财产品、货币型基金、保本基金。'
                elif total_score <= 72:
                    risk_level = '3'
                    risk_level_desc = '稳健型'
                    risk_level_detail_desc = '您的风险承受能力一般。在任何投资中，稳定是您首要考虑的因素，一般您希望在保证本金安全' \
                                             '的基础上能有一些增值收入，追求较低的风险，对投资回报的要求不高。对比较适合投资存款、' \
                                             '国债、保本型理财产品、债券型仅和货币型基金等，也可配置少部分混合基金。'
                elif total_score <= 86:
                    risk_level = '4'
                    risk_level_desc = '积极型'
                    risk_level_detail_desc = '在任何投资中，您希望有较高的投资收益，可以承受一定的投资波动，但是希望自己的投资风险' \
                                             '小于市场的整体风险。您有较高的收益目标，且对风险有清醒的认识，您比较适合投资与浮动型' \
                                             '结构性理财产品、混合型基金、股票型基金、指数型基金。'
                else:
                    risk_level = '5'
                    risk_level_desc = '激进型'
                    risk_level_detail_desc = '在任何投资中，您通常专注于投资的长期增值，并愿意为此承受较大的风险。短期的投资波动并' \
                                             '不会对您造成大的影响，追求超高的回报才是您关注的目标。您比较适合投资浮动收益型理财' \
                                             '产品、股票型基金、指数型基金、股票、权证、衍生工具等投资产品。'
            else:
                if total_score <= 19:
                    risk_level = '1'
                    risk_level_desc = '保守型'
                    risk_level_detail_desc = '您对风险容忍度非常低，在任何投资中，保护本金不受损失和保持资产的流动性是您的首要目标。' \
                                             '您对投资的态度是希望投资收益率极度稳定，不愿承担高风险以换取高收益，追求稳定。' \
                                             '您比较适合投资存款、国债、保本保收益的理财产品、货币型基金、保本基金。'
                elif total_score <= 36:
                    risk_level = '2'
                    risk_level_desc = '谨慎型'
                    risk_level_detail_desc = '您的风险容忍度较低，您希望在保护本金不受损失和保持资产流动性的前提下，' \
                                             '追求适当的增值收入，但您不愿意承担较大风险以换取高收益，在投资波动比较大的情况下，' \
                                             '您会比较紧张。您比较适合投资存款、国债、保本保收益的理财产品、货币型基金、保本基金。'
                elif total_score <= 53:
                    risk_level = '3'
                    risk_level_desc = '稳健型'
                    risk_level_detail_desc = '您的风险承受能力一般。在任何投资中，稳定是您首要考虑的因素，一般您希望在保证本金安全' \
                                             '的基础上能有一些增值收入，追求较低的风险，对投资回报的要求不高。对比较适合投资存款、' \
                                             '国债、保本型理财产品、债券型仅和货币型基金等，也可配置少部分混合基金。'
                elif total_score <= 82:
                    risk_level = '4'
                    risk_level_desc = '积极型'
                    risk_level_detail_desc = '在任何投资中，您希望有较高的投资收益，可以承受一定的投资波动，但是希望自己的投资风险' \
                                             '小于市场的整体风险。您有较高的收益目标，且对风险有清醒的认识，您比较适合投资与浮动型' \
                                             '结构性理财产品、混合型基金、股票型基金、指数型基金。'
                else:
                    risk_level = '5'
                    risk_level_desc = '激进型'
                    risk_level_detail_desc = '在任何投资中，您通常专注于投资的长期增值，并愿意为此承受较大的风险。短期的投资波动并' \
                                             '不会对您造成大的影响，追求超高的回报才是您关注的目标。您比较适合投资浮动收益型理财' \
                                             '产品、股票型基金、指数型基金、股票、权证、衍生工具等投资产品。'
            self.assertEqual(str(entity.body_result['errNo']), '000000')
            self.assertEqual(str(entity.body_result['riskLevel']), risk_level)
            self.assertEqual(str(entity.body_result['riskLevelDesc']), risk_level_desc)
            self.assertEqual(str(entity.body_result['riskLevelDetailDesc']), risk_level_detail_desc)
            self.assertEqual(str(entity.body_result['totalScore']), str(total_score))

    # 账户-税收居民身份申明(V3.4)
    @file_data('test_data/test_save_tax_type.json')
    def test_save_tax_type(self, user_name, password, assert_info):
        self._restful_xjb.save_tax_type(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 账户-查询税收居民身份(V3.4)
    @file_data('test_data/test_get_tax_type.json')
    def test_get_tax_type(self, user_name, password, assert_info):
        self._restful_xjb.get_tax_type(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            tax_type = self._db.get_tax_type(user_name=str(user_name))
            tax_declare = tax_type[0]['tax_declare']
            if str(tax_declare) == '1':
                info = '仅为中国税收居民'
            elif str(tax_declare) == '2':
                info = '仅为非居民'
            else:
                info = '既是中国税收居民又是其他国家(地区)税收居民'
            self.assertEqual(str(entity.body['info']), info)
            self.assertEqual(str(entity.body['type']), str(tax_declare))

    # 账户-解绑资金账户提交(V3.4)
    @file_data('test_data/test_unbinding_capital_account.json')
    def test_unbinding_capital_account(self, user_name, password, mobile_code, assert_info):
        self._restful_xjb.unbinding_capital_account(user_name=str(user_name), password=str(password),
                                                    mobile_code=str(mobile_code))
        entity = self._restful_xjb.entity.current_entity

        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 用户-校验手机号(V3.4)
    @file_data('test_data/test_mobile_validate.json')
    def test_mobile_validate(self, user_name, password, assert_info):
        self._restful_xjb.mobile_validate(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 积分-福利中心交易明细
    @file_data('test_data/test_trade_detail.json')
    def test_trade_detail(self, user_name, password, points_type, type, assert_info):
        self._restful_xjb.trade_detail(user_name=str(user_name), password=str(password),
                                       points_type=str(points_type),
                                       type=str(type))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        if entity.returnCode == '000000':
            wealf_list = self._db.get_trade_detail_points_or_coin(user_name=str(user_name),
                                                                  points_type=str(points_type), type=str(type))
            data_list = entity.body_dataList
            today = Utility.DateUtil().getToday()
            yester_day = today + datetime.timedelta(days=-1)
            if str(type) == '0':
                if len(wealf_list) > 0:
                    n = 100 if len(wealf_list) > 100 else len(wealf_list)
                    self.assertEqual(str(entity.body_totalCount), str(len(wealf_list)))
                    for i in range(0, n):
                        amount_before = decimal.Decimal(str(wealf_list[i]['AMOUNT_BEFORE']))
                        amount_after = decimal.Decimal(str(wealf_list[i]['AMOUNT_AFTER']))
                        amount_add = amount_after - amount_before
                        self.assertEqual(str(data_list[i]['pointsCount']), '+' +
                                         str(decimal.Decimal(str(amount_add)).quantize(decimal.Decimal('0.00'))))
                        self.assertEqual(str(data_list[i]['serialDate']), str(wealf_list[i]['CREATED_AT'])[0:10])
                        if str(data_list[i]['serialDate']).__eq__(str(today)):
                            prefix = '今天'
                        elif str(data_list[i]['serialDate']).__eq__(str(yester_day)):
                            prefix = '昨天'
                        else:
                            prefix = str(wealf_list[i]['CREATED_AT'])[5:10]
                        self.assertEqual(str(data_list[i]['serialTime']),
                                         prefix + str(wealf_list[i]['CREATED_AT'])[10:19])
                        self.assertEqual(str(data_list[i]['title']), str(wealf_list[i]['REMARK']))
                else:
                    self.assertEqual(str(entity.body_totalCount), '0')
            else:
                if len(wealf_list) > 0:
                    n = 100 if len(wealf_list) > 100 else len(wealf_list)
                    self.assertEqual(str(entity.body_totalCount), str(len(wealf_list)))
                    for i in range(0, n):
                        frozen_amount_before = decimal.Decimal(str(wealf_list[i]['FROZEN_AMOUNT_BEFORE']))
                        frozen_amount_after = decimal.Decimal(str(wealf_list[i]['FROZEN_AMOUNT_AFTER']))
                        frozen_amount_add = frozen_amount_after - frozen_amount_before
                        self.assertEqual(str(data_list[i]['pointsCount']), '-' +
                                         str(decimal.Decimal(str(frozen_amount_add)).quantize(
                                             decimal.Decimal('0.00'))))
                        self.assertEqual(str(data_list[i]['serialDate']), str(wealf_list[i]['CREATED_AT'])[0:10])
                        if str(data_list[i]['serialDate']).__eq__(str(today)):
                            prefix = '今天'
                        elif str(data_list[i]['serialDate']).__eq__(str(yester_day)):
                            prefix = '昨天'
                        else:
                            prefix = str(wealf_list[i]['CREATED_AT'])[5:10]
                        self.assertEqual(str(data_list[i]['serialTime']),
                                         prefix + str(wealf_list[i]['CREATED_AT'])[10:19])
                        self.assertEqual(str(data_list[i]['title']), str(wealf_list[i]['REMARK']))
                else:
                    self.assertEqual(str(entity.body_totalCount), '0')

    # 积分-兑换积分商品(V3.4)
    @file_data('test_data/test_exchange_points_goods.json')
    def test_exchange_points_goods(self, user_name, password, goods_id, exchange_count, pay_type, trade_password,
                                   assert_info):
        goods_exchange_batch_list_before = self._db.get_goods_exchange_batch(id=str(goods_id))
        points_amount_list_before = self._db.get_cust_total_points_amount(mobile=str(user_name))
        coin_amount_list_before = self._db.get_coin(mobile=str(user_name))
        coupon_batch_list_before = self._db.get_coupon_batch(
            code=str(goods_exchange_batch_list_before[0]['GOODS_CODE']))
        points_amount_before = 0.00 if len(points_amount_list_before) == 0 else decimal.Decimal(
            points_amount_list_before[0]['AMOUNT'])
        coin_amount_before = 0.00 if len(coin_amount_list_before) == 0 else decimal.Decimal(
            coin_amount_list_before[0]['AMOUNT'])
        coupon_available_quantity_before = 0.00 if len(coupon_batch_list_before) == 0 else decimal.Decimal(
            coupon_batch_list_before[0]['AVAILABLE_QUANTITY'])

        self._restful_xjb.exchange_points_goods(user_name=str(user_name), password=str(password),
                                                goods_id=str(goods_id), exchange_count=str(exchange_count),
                                                pay_type=str(pay_type), trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        if entity.returnCode == '000000':
            goods_exchange_batch_list_after = self._db.get_goods_exchange_batch(id=str(goods_id))
            points_amount_list_after = self._db.get_cust_total_points_amount(mobile=str(user_name))
            coupon_batch_list_after = self._db.get_coupon_batch(
                code=str(goods_exchange_batch_list_after[0]['GOODS_CODE']))
            coin_amount_list_after = self._db.get_coin(mobile=str(user_name))
            points_amount_after = 0.00 if len(points_amount_list_after) == 0 else decimal.Decimal(
                points_amount_list_after[0]['AMOUNT'])
            coin_amount_after = 0.00 if len(coin_amount_list_after) == 0 else decimal.Decimal(
                coin_amount_list_after[0]['AMOUNT'])
            coupon_available_quantity_after = 0.00 if len(coupon_batch_list_after) == 0 else decimal.Decimal(
                coupon_batch_list_after[0]['AVAILABLE_QUANTITY'])

            points_chg = points_amount_before - points_amount_after
            coin_chg = coin_amount_before - coin_amount_after
            coupon_chg = coupon_available_quantity_before - coupon_available_quantity_after

            if str(pay_type) == 'SINGLE_POINT':
                self.assertEqual(str(decimal.Decimal(str(points_chg)).quantize(decimal.Decimal('0.00'))),
                                 str(goods_exchange_batch_list_after[0]['SINGLE_POINTS_AMOUNT']))
                self.assertEqual(str(decimal.Decimal(str(coupon_chg)).quantize(decimal.Decimal('0.00'))), '1.00')
            elif str(pay_type) == 'SINGLE_COIN':
                self.assertEqual(str(decimal.Decimal(str(coin_chg)).quantize(decimal.Decimal('0.00'))),
                                 str(goods_exchange_batch_list_after[0]['SINGLE_COIN_AMOUNT']))
                self.assertEqual(str(decimal.Decimal(str(coupon_chg)).quantize(decimal.Decimal('0.00'))), '1.00')
            else:
                self.assertEqual(str(decimal.Decimal(str(points_chg)).quantize(decimal.Decimal('0.00'))),
                                 str(goods_exchange_batch_list_after[0]['MIX_POINTS_AMOUNT']))
                self.assertEqual(str(decimal.Decimal(str(coin_chg)).quantize(decimal.Decimal('0.00'))),
                                 str(goods_exchange_batch_list_after[0]['MIX_COIN_AMOUNT']))
                self.assertEqual(str(decimal.Decimal(str(coupon_chg)).quantize(decimal.Decimal('0.00'))), '1.00')

    # 积分 - 查询积分、元宝说明
    @file_data('test_data/test_get_points_description.json')
    def test_get_points_description(self, user_name, password, description_code, assert_info):
        self._restful_xjb.get_points_description(user_name=str(user_name), password=str(password),
                                                 description_code=str(description_code))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(str(entity.result['success']), 'True')
        if entity.returnCode == '000000':
            data = entity.data
            points_description = self._db.get_points_description(code=str(description_code))
            self.assertEqual(str(data['code']), str(description_code))
            self.assertEqual(str(data['id']), str(points_description[0]['id']))
            self.assertEqual(str(data['name']), str(points_description[0]['NAME']))
            self.assertEqual(str(data['status']), str(points_description[0]['STATUS']))
            self.assertEqual(str(data['text']), str(points_description[0]['TEXT']))
            self.assertEqual(str(data['version']), str(points_description[0]['VERSION']))

    # 积分 - 查询积分获取规则
    @file_data('test_data/test_get_points_deducte_rules.json')
    def test_get_points_deducte_rules(self, user_name, password, assert_info):
        self._restful_xjb.get_points_deducte_rules(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        points_deducte_rule = self._db.get_points_deducte_rule()
        data_list = entity.dataList['data']
        for i in range(0, len(data_list)):
            self.assertEqual(str(data_list[i]['comment']), '单笔抵扣上限500积分')
            self.assertEqual('%.2f' % data_list[i]['maxAmount'], str(points_deducte_rule[i]['MAX_AMOUNT']))
            self.assertEqual('%.2f' % data_list[i]['maxAmountDay'], str(points_deducte_rule[i]['MAX_AMOUNT_DAY']))
            self.assertEqual('%.2f' % data_list[i]['maxAmountMon'], str(points_deducte_rule[i]['MAX_AMOUNT_MON']))
            self.assertEqual('%.2f' % data_list[i]['maxAmountYear'], str(points_deducte_rule[i]['MAX_AMOUNT_YEAR']))
            self.assertEqual('%.4f' % data_list[i]['maxDeducteRation'],
                             str(points_deducte_rule[i]['MAX_DEDUCTE_RATION']))
            self.assertEqual('%.2f' % data_list[i]['minAmount'], str(points_deducte_rule[i]['MIN_AMOUNT']))
            self.assertEqual('%.2f' % data_list[i]['pointAmountRation'],
                             str(points_deducte_rule[i]['POINT_AMOUNT_RATION']))
            self.assertEqual(str(data_list[i]['productType']), str(points_deducte_rule[i]['PRODUCT_TYPE']))
            self.assertEqual(str(data_list[i]['productTypeName']), str(points_deducte_rule[i]['PRODUCT_TYPE_NAME']))
            self.assertEqual(str(data_list[i]['status']), str(points_deducte_rule[i]['STATUS']))
            self.assertEqual(str(data_list[i]['url']), str(points_deducte_rule[i]['URL']))

    # 积分-签到
    @file_data('test_data/test_get_points_sign_in.json')
    def test_get_points_sign_in(self, user_name, password, assert_info):
        self._restful_xjb.get_points_sign_in(user_name=str(user_name), password=str(password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            sign_in_list = self._db.get_points_sign_in()
            self.assertEqual(str(entity.body_amount), str(sign_in_list[0]['ISSUE_AMOUNT']))
            self.assertEqual(str(entity.body_status), '1')

    # 积分 - 查询积分发放规则
    @file_data('test_data/test_get_points_issue_event_rules.json')
    def test_get_points_issue_event_rules(self, user_name, password, assert_info):
        self._restful_xjb.get_points_issue_event_rules(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        points_issue_event_rules = self._db.get_points_issue_event_rules()
        data_list = entity.dataList['data']
        for i in range(0, len(data_list)):
            self.assertEqual(str(data_list[i]['display']), str(points_issue_event_rules[i]['DISPLAY']))
            self.assertEqual(str(data_list[i]['eventDesc']), str(points_issue_event_rules[i]['EVENT_DESC']))
            self.assertEqual(str(data_list[i]['eventKey']), str(points_issue_event_rules[i]['EVENT_KEY']))
            self.assertEqual(str(data_list[i]['id']), str(points_issue_event_rules[i]['id']))
            self.assertEqual('%.2f' % data_list[i]['issueAmount'], str(points_issue_event_rules[i]['ISSUE_AMOUNT']))
            self.assertEqual('%.2f' % data_list[i]['maxAmount'], str(points_issue_event_rules[i]['MAX_AMOUNT']))
            self.assertEqual('%.2f' % data_list[i]['maxAmountDay'], str(points_issue_event_rules[i]['MAX_AMOUNT_DAY']))
            self.assertEqual('%.2f' % data_list[i]['maxAmountMon'], str(points_issue_event_rules[i]['MAX_AMOUNT_MON']))
            self.assertEqual('%.2f' % data_list[i]['maxAmountYear'],
                             str(points_issue_event_rules[i]['MAX_AMOUNT_YEAR']))
            self.assertEqual(str(data_list[i]['orderBy']), str(points_issue_event_rules[i]['ORDER_BY']))
            self.assertEqual(str(data_list[i]['rcmd']), str(points_issue_event_rules[i]['RCMD']))
            self.assertEqual(str(data_list[i]['roles']), str(points_issue_event_rules[i]['ROLES']))
            self.assertEqual(str(data_list[i]['status']), str(points_issue_event_rules[i]['STATUS']))

    # 积分-保存分享结果(3.4)
    @file_data('test_data/test_save_share_result.json')
    def test_save_share_result(self, user_name, password, share_url, assert_info):
        self._restful_xjb.save_share_result(user_name=str(user_name), password=str(password), share_url=str(share_url))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 积分-查询签到结果(3.4)
    @file_data('test_data/test_get_sign_result.json')
    def test_get_sign_result(self, user_name, password, assert_info):
        self._restful_xjb.get_sign_result(user_name=str(user_name), password=str(password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            self.assertEqual(str(entity.body_result), 'VALID')

    # 基金-基金申购、认购、赎回费率接口(3.4)
    @file_data('test_data/test_get_fund_transaction_date.json')
    def test_get_fund_transaction_date(self, user_name, password, fund_id, assert_info):
        self._restful_xjb.get_fund_transaction_date(user_name=str(user_name), password=str(password),
                                                    fund_id=str(fund_id))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            product_ext = self._db.get_product_ext(product_id=str(fund_id))
            carry_over_type = str(product_ext[0]['carry_over_type'])
            carry_over_date = str(product_ext[0]['carry_over_date'])
            ack_buy_day = 0 if str(product_ext[0]['ack_buy_day']) == '' else int(product_ext[0]['ack_buy_day'])
            is_regular_open = 1 if product_ext[0]['is_regular_open'] == 1 else 0
            operate_period = product_ext[0]['operate_period']
            operate_period_unit = product_ext[0]['operate_period_unit']
            ack_redeem_day = 0 if str(product_ext[0]['ack_redeem_day']) == '' else int(product_ext[0]['ack_redeem_day'])
            redeem_n_day = product_ext[0]['allow_redeem_day']
            delivery_day = 0 if str(product_ext[0]['delivery_day']) == '' else int(product_ext[0]['delivery_day'])
            max_day = max(redeem_n_day, redeem_n_day + delivery_day - 1)
            fund_type = str(product_ext[0]['fund_type'])
            is_new_issue = str(product_ext[0]['is_new_issue'])
            is_sale = str(product_ext[0]['is_sale'])

            self.assertEqual(str(entity.body_ackBuyDay), str(ack_buy_day))
            self.assertEqual(str(entity.body_isRegularOpen), str(is_regular_open))

            if carry_over_type == '1':
                self.assertEqual(str(entity.body_ackBuyLookDay), str(ack_buy_day + 1))
                self.assertEqual(str(entity.body_ackBuyLookType), '0')
            if carry_over_type == '30':
                self.assertEqual(str(entity.body_ackBuyLookType), '1')
                if str(carry_over_date) == '400':
                    self.assertEqual(str(entity.body_ackBuyLookDay), '每月')
                elif str(carry_over_date) == '401':
                    self.assertEqual(str(entity.body_ackBuyLookDay), '每月第一个工作日')
                elif str(carry_over_date) == '402':
                    self.assertEqual(str(entity.body_ackBuyLookDay), '每月初')
                elif str(carry_over_date) == '429':
                    self.assertEqual(str(entity.body_ackBuyLookDay), '每月倒数第二个工作日')
                elif str(carry_over_date) == '430':
                    self.assertEqual(str(entity.body_ackBuyLookDay), '每月最后一个工作日')
                elif str(carry_over_date) == '431':
                    self.assertEqual(str(entity.body_ackBuyLookDay), '每月末')
                elif str(carry_over_date) == '999':
                    self.assertEqual(str(entity.body_ackBuyLookDay), '每日')
                else:
                    self.assertEqual(str(entity.body_ackBuyLookDay), '每月' + str(carry_over_date) + '日')

            self.assertEqual(str(entity.body_ackRedeemDay), str(ack_redeem_day))
            self.assertEqual(str(entity.body_closeDay),
                             '' if str(operate_period) == 'None' else str(
                                 int(operate_period) + int(operate_period_unit)))
            self.assertEqual(str(entity.body_deliveryDay), str(max_day))
            self.assertEqual(str(entity.body_fundType), str(fund_type))
            self.assertEqual(str(entity.body_isNewIssue), str(is_new_issue))
            self.assertEqual(str(entity.body_isSale), str(is_sale))
            self.assertEqual(str(entity.body_redeemMaxDay), str(max_day - 1))
            self.assertEqual(str(entity.body_redeemNDay), str(redeem_n_day))

    # 会员等级-权益专属产品
    @file_data('test_data/test_get_exclusive_products.json')
    def test_get_exclusive_products(self, user_name, password, member_level, rights_id, parent_rights_id,
                                    assert_info):
        self._restful_xjb.get_exclusive_products(user_name=str(user_name), password=str(password),
                                                 member_level=str(member_level), rights_id=str(rights_id),
                                                 parent_rights_id=str(parent_rights_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if entity.returnCode == '000000':
            exclusive_list = self._db.get_exclusive_product_list(member_level=str(member_level))
            if len(exclusive_list) > 0:
                if str(exclusive_list[0]['yield_type']) == '0':
                    income_type = '年化业绩比较基准'
                    income_intro = str(
                        decimal.Decimal(str(exclusive_list[0]['fixed_yield'])).quantize(decimal.Decimal(
                            '0.00'))) + '%'
                elif str(exclusive_list[0]['yield_type']) == '1':
                    income_type = '年化业绩比较基准'
                    income_intro = str(exclusive_list[0]['float_yield'])
                elif str(exclusive_list[0]['yield_type']) == '2':
                    income_type = '浮动收益'
                    income_intro = str(exclusive_list[0]['float_yield'])
                elif str(exclusive_list[0]['yield_type']) == '3':
                    income_type = '七日年化收益率'
                    income_intro = str(exclusive_list[0]['float_yield'])
                    xjb_income_info = '万分收益'
                    xjb_income_unit = '--' if str(exclusive_list[0]['fund_income_unit']) == '' else str(
                        str(decimal.Decimal(str(exclusive_list[0]['fund_income_unit'])).quantize(
                            decimal.Decimal('0.0000'))))
                elif str(exclusive_list[0]['yield_type']) == '4':
                    income_type = '累计净值'
                    income_intro = '--' if str(exclusive_list[0]['total_nav']) == '' else str(
                        str(decimal.Decimal(str(exclusive_list[0]['total_nav'])).quantize(
                            decimal.Decimal('0.0000'))))
                elif str(exclusive_list[0]['yield_type']) == '5':
                    income_type = '单位净值'
                    income_intro = '--' if str(exclusive_list[0]['latest_nav']) == '' else str(
                        str(decimal.Decimal(str(exclusive_list[0]['latest_nav'])).quantize(
                            decimal.Decimal('0.0000'))))
                else:
                    income_type = '累计回报率'
                    income_intro = '--' if str(exclusive_list[0]['frombuild_return']) == '' else str(
                        decimal.Decimal(str(exclusive_list[0]['frombuild_return'])).quantize(
                            decimal.Decimal('0.00')))

                prod_status = str(exclusive_list[0]['product_status'])
                if prod_status == '4':
                    min_amount = str(exclusive_list[0]['min_buy_amount'])
                else:
                    min_amount = str(exclusive_list[0]['min_subscribe_amount'])

                if str(exclusive_list[0]['product_type']) == '1':
                    type = '1'
                    product_detail_url = 'hxxjb://product?commonType=' + '1' + '&productId='
                elif str(exclusive_list[0]['product_type']) == '2':
                    type = '2'
                    product_detail_url = 'hxxjb://product?commonType=' + '2' + '&fundId='
                else:
                    type = ' 3'
                    product_detail_url = 'hxxjb://product?commonType=' + '1' + '&productId='

                data_list = entity.body_dataList
                self.assertEqual(str(data_list[0]['canRedeemAnytime']), str(exclusive_list[0]['is_redem_anytime']))
                self.assertEqual(str(data_list[0]['clientType']), '0' if str(exclusive_list[0]['client_type']) == ''
                else str(exclusive_list[0]['client_type']))
                self.assertEqual(str(data_list[0]['incomeIntro']), income_intro)
                self.assertEqual(str(data_list[0]['incomeType']), income_type)
                self.assertEqual(str(data_list[0]['minAmount']), min_amount[0:1])
                self.assertEqual(str(data_list[0]['onsaleStatus']), str(data_list[0]['productStatus']))
                self.assertTrue(product_detail_url in str(data_list[0]['productDetailUrl']))
                self.assertEqual(str(data_list[0]['productId']), str(exclusive_list[0]['productid']))
                self.assertEqual(str(data_list[0]['productTitle']), str(exclusive_list[0]['product_short_name']))
                self.assertEqual(str(data_list[0]['productType']), str(exclusive_list[0]['product_type']))
                self.assertEqual(str(data_list[0]['type']), type)

    # 会员等级 - 权益表格数据
    @file_data('test_data/test_cust_level_form_data.json')
    def test_cust_level_form_data(self, user_name, password, member_level, rights_id, parent_rights_id, assert_info):
        self._restful_xjb.cust_level_form_data(user_name=str(user_name), password=str(password),
                                               member_level=str(member_level), rights_id=str(rights_id),
                                               parent_rights_id=str(parent_rights_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity == '000000':
            member_level = self._db.get_member_level(code=str(member_level))
            member_interests = self._db.get_member_level_right_detail_db(code=str(rights_id))
            data_list = entity.dataList
            for i in range(0, len(member_level)):
                self.assertEqual(str(data_list[i]['code']), str(member_level[i]['NAME']))
                self.assertEqual(str(data_list[i]['value']), str(member_interests[i]['NAME']))

    # 注册实名认证绑卡
    @data(
        (Utility.GetData().mobile(), '12qwaszx', '0', '20250826', '620522', '135790',
         {'returnCode': '000000', 'returnMsg': ''}),
    )
    @unpack
    def test_register_binding_card(self, mobile, login_password, cert_type, cert_validate_date, card_bin,
                                   trade_password, assert_info):
        self._restful_xjb.register_name_auth_binding_card(mobile=str(mobile), login_password=login_password,
                                                          cert_type=str(cert_type),
                                                          cert_validate_date=str(cert_validate_date),
                                                          card_bin=card_bin, trade_password=trade_password)

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

        cards = self._db.get_cust_debit_card(bank_mobile=str(mobile))
        self.assertEqual(str(cards[0]['card_no']), self._restful_xjb.entity.card_no)
        self.assertEqual(cards[0]['type'], '1')
        self.assertEqual(str(cards[0]['accept_mode']), 'M')

    # 账户 - 用户实名信息验证（异常校验）
    @file_data('test_data/test_real_name_auth.json')
    def test_real_name_auth(self, user_name, password, name, cert_type, cert_no, cert_validate_date, assert_info):
        self._restful_xjb.real_name_auth_validate(user_name=str(user_name), password=str(password), name=str(name),
                                                  cert_type=str(cert_type), cert_no=str(cert_no),
                                                  cert_validate_date=str(cert_validate_date))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])

    # 会员等级 - 权益优惠券 / 积分礼包
    @file_data('test_data/test_get_gift_bag.json')
    def test_get_gift_bag(self, user_name, password, member_level, rights_id, parent_rights_id, assert_info):
        self._restful_xjb.get_gift_bag(user_name=str(user_name), password=str(password),
                                       member_level=str(member_level), rights_id=str(rights_id),
                                       parent_rights_id=str(parent_rights_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if entity.returnCode == '000000':
            gift_bag_list = self._db.get_member_level_right_detail_db(code=str(rights_id))
            data_list = entity.body_dataList
            status = gift_bag_list[0]['STATUS']
            if str(status) == '已发放':
                can_over_load_info = '已发放'
            else:
                can_over_load_info = '未发放'
            coupon_desc = gift_bag_list[0]['NAME']
            self.assertEqual(str(data_list[0]['canOverloadInfo']), can_over_load_info)
            self.assertEqual(str(data_list[0]['couponDesc']), coupon_desc)
            if 'COUPON' in str(rights_id):
                can_use_money = '0.00' if str(gift_bag_list[0]['GIFT_PACK_MONEY']) == '' else str(
                    gift_bag_list[0]['GIFT_PACK_MONEY'])
                self.assertEqual(str(data_list[0]['purchaseInfo']), '优惠券大礼包，用于部分产品抵扣，详情请至我的优惠券查看')
            else:
                self.assertEqual(str(data_list[0]['purchaseInfo']), '1积分等于1元，可用于部分产品抵扣，永久有效')
                can_use_money = '0.00' if str(gift_bag_list[0]['POINT_AMOUNT']) == '' else str(
                    gift_bag_list[0]['POINT_AMOUNT'])
            self.assertEqual(str(data_list[0]['canUseAmt']), can_use_money)

    # 会员等级-权益生日特权
    @file_data('test_data/test_get_birthday_rights.json')
    def test_get_birthday_rights(self, user_name, password, member_level, rights_id, parent_rights_id, assert_info):
        self._restful_xjb.get_birthday_rights(user_name=str(user_name), password=str(password),
                                              member_level=str(member_level), rights_id=str(rights_id),
                                              parent_rights_id=str(parent_rights_id))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            cust_base = self._db.get_cust_base(user_name=str(user_name))
            member_acco = self._db.get_my_member_role(mobile=str(user_name))
            if str(member_acco[0]['MEMBER_LEVEL']) != (str(member_level)):
                self.assertEqual(str(entity.body_sendStatus), '2')
            else:
                if str(cust_base[0]['is_verified']) != 'Y':
                    self.assertEqual(str(entity.body_sendStatus), '3')
                else:
                    if str(cust_base[0]['cert_type']) != '0':
                        self.assertEqual(str(entity.body_sendStatus), '2')
                    else:
                        now = str(datetime.datetime.now()).replace('-', '')[0:8]
                        cert_no = str(cust_base[0]['cert_no'])[10:14]
                        if now < now[0:4] + cert_no:  # 生日还没到
                            self.assertEqual(str(entity.body_birthday),
                                             now[0:4] + '.' + cert_no[0:2] + '.' + cert_no[2:4])
                            self.assertEqual(str(entity.body_sendStatus), '4')
                        else:  # 生日已过
                            year = int(now[0:4]) + 1
                            self.assertEqual(str(entity.body_birthday),
                                             str(year) + '.' + cert_no[0:2] + '.' + cert_no[2:4])
                            self.assertEqual(str(entity.body_sendStatus), '5')

    # 账户-登录（新）
    @file_data('test_data/test_login_new.json')
    def test_login_new(self, user_name, password, type, assert_info):
        self._restful_xjb.login_new(user_name=str(user_name), password=str(password), type=str(type))
        entity = self._restful_xjb.entity.current_entity

        self.assertIn(assert_info["returnMsg"], entity.returnMsg)
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if assert_info["returnCode"] == '000000':
            self.assertIsNotNone(entity.body['token'])
            self.assertIsNotNone(entity.body['serialNo'])

    # 用户风等级与产品风险不匹配
    @file_data('test_data/test_buy_product_unmatch.json')
    def test_buy_product_unmatch(self, user_name, password, product_id, pay_type, amt, trade_password,
                         is_confirm_beyond_risk,
                         assert_info):
        self._restful_xjb.buy_product_nomatch_risk(user_name=str(user_name), login_password=str(password),
                                                   product_id=str(product_id), pay_type=str(pay_type),
                                                   amt=str(amt), is_confirm_beyond_risk=str(is_confirm_beyond_risk),
                                                   trade_password=str(trade_password))

        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        self.assertTrue(assert_info["returnMsg"] in entity.returnMsg)
        if entity.returnCode == '081636' or entity.returnCode == '081602' or entity.returnCode == '081610':
            self.assertEqual(str(entity.body_smsTitle), '输入短信验证码')
            self.assertEqual(str(entity.showType), '2')

    # 交易-一键随心取提交(V3.5)
    @file_data('test_data/test_one_key_redeem_validate.json')
    def test_one_key_redeem_validate(self, user_name, password, product_ids, redeem_amts, trade_password,
                                     assert_info):
        self._db.update_xjb_recharge_amount()
        self._restful_xjb.one_key_redeem_validate(user_name=str(user_name), password=str(password),
                                                  product_ids=str(product_ids), redeem_amts=str(redeem_amts),
                                                  trade_password=str(trade_password))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])

        if entity.returnCode == '000000':
            if str(product_ids).__contains__(','):
                self._db.insert_prod_quty(user_name=str(user_name), product_id=str(product_ids).split(',')[0],
                                          amt=str(redeem_amts).split(',')[0])
                self._db.insert_prod_quty(user_name=str(user_name), product_id=str(product_ids).split(',')[1],
                                          amt=str(redeem_amts).split(',')[1])
            else:
                self._db.insert_prod_quty(user_name=str(user_name), product_id=str(product_ids),
                                          amt=str(redeem_amts))

            if str(product_ids).__contains__(','):  # 一键随心取2支产品
                time.sleep(5)
                # 查父订单
                parent_trade_order = self._db.get_parent_trade_order(mobile=str(user_name))

                # 查询子订单
                trade_request, trade_order_redeem, trade_order_recharge = self._db.get_trade_request_order(mobile=
                str(
                    user_name),
                    product_id=
                    str(
                        product_ids),
                    parent_order_no=
                    str(
                        parent_trade_order[
                            0][
                            'ORDER_NO']))
                prod_info_one = self._db.get_product_info(product_id=str(product_ids).split(',')[0])
                prod_info_two = self._db.get_product_info(product_id=str(product_ids).split(',')[1])

                amt_one = str(redeem_amts).split(',')[0]
                amt_two = str(redeem_amts).split(',')[1]

                # 计算定活宝随心取本金+收益
                day1_prod_one = datetime.datetime(2018, 01, 22)
                day1_prod_two = datetime.datetime(2018, 01, 22)
                day2_prod_one = datetime.datetime(int(trade_order_redeem[0]['AP_DATE'][0:4]),
                                                  int(trade_order_redeem[0]['AP_DATE'][4:6]),
                                                  int(trade_order_redeem[0]['AP_DATE'][6:8]))
                day2_prod_two = datetime.datetime(int(trade_order_redeem[1]['AP_DATE'][0:4]),
                                                  int(trade_order_redeem[1]['AP_DATE'][4:6]),
                                                  int(trade_order_redeem[1]['AP_DATE'][6:8]))
                fix_yield_one = prod_info_one[0]['fixed_yield']
                fix_yield_two = prod_info_two[0]['fixed_yield']

                redeem_yield_one = decimal.Decimal(str(amt_one)) * decimal.Decimal(
                    str(fix_yield_one)) / decimal.Decimal(
                    100.00) * decimal.Decimal(str(day2_prod_one - day1_prod_one).split(' ')[0]) * decimal.Decimal(
                    1 / 365.00)
                redeem_amt_one = round(decimal.Decimal(str(amt_one)) + redeem_yield_one, 2)

                redeem_yield_two = decimal.Decimal(str(amt_two)) * decimal.Decimal(
                    str(fix_yield_two)) / decimal.Decimal(
                    100.00) * decimal.Decimal(str(day2_prod_two - day1_prod_two).split(' ')[0]) * decimal.Decimal(
                    1 / 365.00)
                redeem_amt_two = round(decimal.Decimal(str(amt_two)) + redeem_yield_two, 2)
                redeem_amt_all = round(
                    decimal.Decimal(str(amt_one)) + redeem_yield_one + decimal.Decimal(str(amt_two)) +
                    redeem_yield_two, 2)

                parent_ap_amt = decimal.Decimal(str(redeem_amts).split(',')[0]) + decimal.Decimal(
                    str(redeem_amts).split(',')[1])

                # 父订单信息校验
                self.assertEqual(str(parent_trade_order[0]['ORDER_APKIND']), '018')
                self.assertEqual(str(parent_trade_order[0]['ORDER_SUB_APKIND']), '018100')
                # self.assertEqual(str(parent_trade_order[0]['TO_PROD']), 'ZX05#000730')
                # self.assertEqual(str(parent_trade_order[0]['AP_AMT']), 'decimal.Decimal(str(parent_ap_amt))')

                # 赎回订单信息校验
                for i in range(0, len(trade_order_redeem)):
                    self.assertEqual(str(trade_order_redeem[i]['ORDER_APKIND']), '018')
                    self.assertEqual(str(trade_order_redeem[i]['ORDER_SUB_APKIND']), '018101')
                    self.assertEqual(str(trade_order_redeem[i]['FROM_PROD_TYPE']), '1')
                    time.sleep(5)
                    self.assertTrue(str(trade_order_redeem[i]['STATUS']) in ('A', 'I'))
                    if str(trade_order_redeem[i]['FROM_PROD']) == str(product_ids).split(',')[0]:
                        self.assertEqual(trade_order_redeem[i]['AP_AMT'], decimal.Decimal(str(amt_one)))
                        self.assertEqual(str(trade_order_redeem[i]['FROM_PROD']), str(product_ids).split(',')[0])
                    else:
                        self.assertEqual(trade_order_redeem[i]['AP_AMT'], decimal.Decimal(str(amt_two)))
                        self.assertEqual(str(trade_order_redeem[i]['FROM_PROD']), str(product_ids).split(',')[1])

                # 充值现金宝订单信息校验
                ap_amt_recharge_larger = decimal.Decimal(str(redeem_amt_all)) + decimal.Decimal('0.01')
                ap_amt_recharge_lowrer = decimal.Decimal(str(redeem_amt_all)) - decimal.Decimal('0.01')
                self.assertEqual(str(trade_order_recharge[0]['ORDER_APKIND']), '001')
                self.assertEqual(str(trade_order_recharge[0]['ORDER_SUB_APKIND']), '001101')
                self.assertEqual(str(trade_order_recharge[0]['TO_PROD']), 'ZX05#000730')
                self.assertEqual(str(trade_order_recharge[0]['TO_PROD_TYPE']), '0')
                time.sleep(5)
                self.assertTrue(str(trade_order_recharge[0]['STATUS']) in ('Y', 'I', 'A', 'P'))
                self.assertTrue(
                    str(trade_order_recharge[0]['AP_AMT']) in (str(decimal.Decimal(str(redeem_amt_all))),
                                                               str(ap_amt_recharge_larger),
                                                               str(ap_amt_recharge_lowrer)))
                time.sleep(5)
                # self.assertEqual(str(trade_order_recharge[0]['SUCC_AMT']), str(decimal.Decimal(str(redeem_amt))))

                # 校验交易表信息
                user_trade_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                near_work_date = self._db.judge_is_work_date(day=str(user_trade_time)[0:8])[0]['WORK_DATE']
                if str(user_trade_time)[0:8] == str(near_work_date):  # 交易当天为工作日
                    if '090000' < str(user_trade_time)[8:14] < '150000':  # 交易为9:00-15：00之间
                        self.assertIn('随心取处理中，您可稍后通过交易记录查询交易转态', str(entity.info))
                        # self.assertEqual(str(entity.returnResult), 'Y')
                        self.assertEqual(str(entity.title), '随心取处理中')
                        for i in range(0, len(trade_request)):
                            if str(trade_request[i]['APKIND']) == '022':
                                self.assertEqual(str(trade_request[i]['SUB_APKIND']), '022230')
                                # self.assertEqual(str(trade_request[i]['REMARK']), 'T+0赎回，实时申购现金宝')
                                self.assertEqual(str(trade_request[i]['PROD_ID']), 'ZX05#000730')
                                self.assertTrue(str(trade_request[i]['SUB_AMT']) in (
                                    str(decimal.Decimal(str(redeem_amt_one)).quantize(decimal.Decimal('0.00'))),
                                    str(decimal.Decimal(str(redeem_amt_two)).quantize(decimal.Decimal('0.00')))))
                            else:
                                self.assertIn('随心取处理中，您可稍后通过交易记录查询交易转态', str(entity.info))
                                # self.assertEqual(str(entity.returnResult), 'Y')
                                self.assertEqual(str(entity.title), '随心取处理中')
                                self.assertTrue(str(trade_request[i]['PROD_ID']) in str(product_ids))
                                self.assertEqual(str(trade_request[i]['APKIND']), '024')
                                self.assertEqual(str(trade_request[i]['SUB_APKIND']), '024050')
                                self.assertTrue(str(trade_request[i]['SUB_AMT']) in (
                                    str(decimal.Decimal(str(decimal.Decimal(str(amt_one)) / decimal.Decimal(1.0))).
                                        quantize(decimal.Decimal('0.00'))), str(decimal.Decimal(str(decimal.Decimal(
                                        str(amt_two)) / decimal.Decimal(100.0))).quantize(
                                        decimal.Decimal('0.00')))))
                    else:
                        self.assertIn('随心取处理中，您可稍后通过交易记录查询交易转态', str(entity.info))
                        # self.assertEqual(str(entity.returnResult), 'Y')
                        self.assertEqual(str(entity.title), '随心取处理中')
                        trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
                        for i in range(0, len(trade_request)):
                            self.assertEqual(str(trade_request[i]['SUB_APKIND']), '022230')
                            self.assertEqual(str(trade_request[i]['PROD_ID']), 'ZX05#000730')
                            # self.assertEqual(str(trade_request[0]['REMARK']), '收益凭证t+0预约赎回')
                            self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
                            self.assertEqual(str(trade_reserve[0]['APKIND']), '024')
                            self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '024051')
                            self.assertTrue(str(trade_reserve[0]['PROD_ID']), str(product_ids))
                            self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '1')
                            self.assertTrue(str(trade_reserve[0]['SUB_AMT']) in (str(decimal.Decimal(
                                str(decimal.Decimal(str(amt_one)) / decimal.Decimal(1.0))).quantize(decimal.Decimal(
                                '0.00'))), str(decimal.Decimal(str(decimal.Decimal(str(amt_two)) / decimal.Decimal(
                                100.0))).quantize(decimal.Decimal('0.00')))))
                            self.assertEqual(str(trade_reserve[0]['REMARK']), '产品预约信息')
                            # self.assertEqual(str(trade_reserve[0]['RES_ST']), 'N')
            else:  # 一键随心取1只产品
                trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
                trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
                pro_info = self._db.get_product_info(product_id=str(product_ids))

                # 计算定活宝赎回本金+收益
                day1 = datetime.datetime(2018, 01, 22)
                day2 = datetime.datetime(int(trade_order[0]['AP_DATE'][0:4]), int(trade_order[0]['AP_DATE'][4:6]),
                                         int(trade_order[0]['AP_DATE'][6:8]))
                fix_yield = pro_info[0]['fixed_yield']
                redeem_yield = decimal.Decimal(str(redeem_amts)) * decimal.Decimal(
                    str(fix_yield)) / decimal.Decimal(
                    100.00) * decimal.Decimal(str(day2 - day1).split(' ')[0]) * decimal.Decimal(1 / 365.00)
                redeem_amt = round(decimal.Decimal(str(redeem_amts)) + redeem_yield, 2)

                redeem_amt_larger = decimal.Decimal(str(redeem_amt)) + decimal.Decimal('0.01')
                redeem_amt_lower = decimal.Decimal(str(redeem_amt)) - decimal.Decimal('0.01')

                self.assertIn('资金已到达您的现金宝帐户，您可立即快速取出到银行卡或购买更多理财产品。', str(entity.info))
                self.assertEqual(str(entity.returnResult), 'Y')
                self.assertEqual(str(entity.title), '成功')
                self.assertEqual(str(trade_order[0]['ORDER_APKIND']), '018')
                self.assertEqual(str(trade_order[0]['ORDER_SUB_APKIND']), '018010')
                self.assertTrue(str(trade_order[0]['AP_AMT']) in (str(decimal.Decimal(str(redeem_amt))),
                                                                  str(redeem_amt_larger), str(redeem_amt_lower)))
                self.assertTrue(str(trade_order[0]['SUCC_AMT']) in (str(decimal.Decimal(str(redeem_amt))),
                                                                    str(redeem_amt_larger), str(redeem_amt_lower)))
                self.assertEqual(str(trade_order[0]['TO_PROD']), 'ZX05#000730')
                self.assertEqual(str(trade_order[0]['FROM_PROD']), str(product_ids))
                self.assertEqual(str(trade_order[0]['FROM_PROD_TYPE']), '1')
                self.assertEqual(str(trade_order[0]['TO_PROD_TYPE']), '0')
                self.assertEqual(str(trade_order[0]['STATUS']), 'Y')

                user_trade_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                near_work_date = self._db.judge_is_work_date(day=str(user_trade_time)[0:8])[0]['WORK_DATE']
                self.assertEqual(str(trade_request[0]['PROD_ID']), 'ZX05#000730')
                self.assertEqual(str(trade_request[0]['PROD_TYPE']), '0')
                self.assertEqual(trade_request[0]['SUB_AMT'], decimal.Decimal(str(redeem_amt)))
                self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['RTTA_ST']), 'Y')
                self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
                if str(user_trade_time)[0:8] == str(near_work_date):  # 交易当天为工作日
                    if '090000' < str(user_trade_time)[8:14] < '150000':  # 交易为9:00-15：00之间
                        self.assertEqual(str(trade_request[0]['APKIND']), '022')
                        self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022115')
                        self.assertEqual(str(trade_request[0]['REMARK']), 'T+0赎回，实时申购现金宝')
                    else:
                        self.assertEqual(str(trade_request[0]['APKIND']), '022')
                        self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022118')
                        self.assertEqual(str(trade_request[0]['REMARK']), '定期宝预约赎回，实时申购现金宝')
                else:
                    self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
                    self.assertEqual(str(trade_reserve[0]['APKIND']), '024')
                    self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '024016')
                    self.assertTrue(str(trade_reserve[0]['PROD_ID']) in str(product_ids))
                    self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '1')
                    self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
                                     decimal.Decimal(str(redeem_amts)).quantize(decimal.Decimal('0.00')))
                    self.assertEqual(str(trade_reserve[0]['REMARK']), '产品预约信息')
                    self.assertEqual(str(trade_reserve[0]['RES_ST']), 'Y')

    # 账户-打开/关闭短信验证码登录
    @file_data('test_data/test_save_sms_login_status.json')
    def test_save_sms_login_status(self, user_name, password, open_status, assert_info):
        self._restful_xjb.save_sms_login_status(user_name=str(user_name), password=str(password),
                                                open_status=str(open_status))
        entity = self._restful_xjb.entity.current_entity
        self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
        self.assertEqual(entity.returnCode, assert_info["returnCode"])
        if entity.returnCode == '000000':
            cust_info = self._db.get_tax_type(user_name=str(user_name))
            if "1".__eq__(str(open_status)):
                sms_status = 'Y'
            else:
                sms_status = 'N'
            self.assertEqual(str(sms_status), str(cust_info[0]['sms_login']))

@ddt
class XjbServiceTest_02(unittest.TestCase):
    def setUp(self):
        self._restful_xjb = RestfulXjbTools()
        self._db = MysqlXjbTools()


    # # 交易-使用组合支付手段购买产品
    # @file_data('test_data/test_get_combination_payment_confirm_info_confirm.json')
    # def test_buy_product_using_super_payment(self, user_name, password, pay_type, product_id, should_pay_amt,
    #                                          serial_no, product_ids, redeem_amts, set_default, trade_password,
    #                                          assert_info):
    #     self._restful_xjb.buy_product_using_super_payment(user_name=str(user_name),
    #                                                       login_password=str(password),
    #                                                       product_id=str(product_id),
    #                                                       should_pay_amt=str(should_pay_amt),
    #                                                       serial_no=str(serial_no),
    #                                                       product_ids=str(product_ids),
    #                                                       redeem_amts=str(redeem_amts),
    #                                                       set_default=str(set_default),
    #                                                       trade_password=str(trade_password),
    #                                                       pay_type=str(pay_type))
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # # 交易-使用超级支付手段购买高端并撤单
    # @file_data('test_data/test_purchase_using_super_pay_then_cancel.json')
    # def test_purchase_using_super_pay_then_cancel(self, user_name, password, pay_type, product_id, should_pay_amt,
    #                                               serial_no, product_ids, redeem_amts, set_default, trade_password,
    #                                               assert_info):
    #     self._restful_xjb.purchase_using_super_pay_then_cancel(user_name=str(user_name),
    #                                                            login_password=str(password),
    #                                                            product_id=str(product_id),
    #                                                            should_pay_amt=str(should_pay_amt),
    #                                                            serial_no=str(serial_no),
    #                                                            product_ids=str(product_ids),
    #                                                            redeem_amts=str(redeem_amts),
    #                                                            set_default=str(set_default),
    #                                                            trade_password=str(trade_password),
    #                                                            pay_type=str(pay_type))
    #
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])



    # # 交易-查询组合支付确认信息(V3.5)
    # @file_data('test_data/test_get_combination_payment_confirm_info.json')
    # def test_get_combination_payment_confirm_info(self, user_name, password, product_id, should_pay_amt, serial_no,
    #                                               product_ids, redeem_amts, set_default, assert_info):
    #     self._restful_xjb.get_combination_payment_confirm_info(user_name=str(user_name), password=str(password),
    #                                                            product_id=str(product_id),
    #                                                            should_pay_amt=str(should_pay_amt),
    #                                                            serial_no=str(serial_no), product_ids=str(product_ids),
    #                                                            redeem_amts=str(redeem_amts),
    #                                                            set_default=str(set_default))
    #
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])


    # # 交易-修改组合支付方案(3.5)
    # @file_data('test_data/test_modify_combination_payment_plan.json')
    # def test_modify_combination_payment_plan(self, user_name, password, product_id, should_pay_amt, serial_no,
    #                                          product_ids, redeem_amts, set_default, assert_info):
    #     self._restful_xjb.modify_combination_payment_plan(user_name=str(user_name), password=str(password),
    #                                                       product_id=str(product_id),
    #                                                       should_pay_amt=str(should_pay_amt),
    #                                                       serial_no=str(serial_no), product_ids=str(product_ids),
    #                                                       redeem_amts=str(redeem_amts),
    #                                                       set_default=str(set_default))
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])


    # # 交易-查询组合支付方案(3.5)
    # @file_data('test_data/test_get_combination_payment_plan.json')
    # def test_get_combination_payment_plan(self, user_name, password, product_id, should_pay_amt, serial_no,
    #                                       assert_info):
    #     self._restful_xjb.get_combination_payment_plan(user_name=str(user_name), password=str(password),
    #                                                    product_id=str(product_id), should_pay_amt=str(should_pay_amt),
    #                                                    serial_no=str(serial_no))
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])


    # # 交易-查询组合支付权限(3.5)
    # @file_data('test_data/test_get_combination_payment_auth.json')
    # def test_get_combination_payment_auth(self, user_name, password, product_id, should_pay_amt, serial_no,
    #                                       assert_info):
    #     self._restful_xjb.get_combination_payment_auth(user_name=str(user_name), password=str(password),
    #                                                    product_id=str(product_id), should_pay_amt=str(should_pay_amt),
    #                                                    serial_no=str(serial_no))
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # if entity.returnCode == '000000':
    #     #
    #     trade_request, trade_order = self._db.get_trade_request(mobile=str(user_name))
    #     trade_reserve = self._db.get_cust_latest_trade_reserve(mobile=str(user_name))
    #     pro_info = self._db.get_product_info(product_id=str(product_id))
    #
    #     # 计算定活宝赎回本金+收益
    #     day1 = datetime.datetime(2018, 01, 22)
    #     day2 = datetime.datetime(int(trade_order[0]['AP_DATE'][0:4]), int(trade_order[0]['AP_DATE'][4:6]),
    #                              int(trade_order[0]['AP_DATE'][6:8]))
    #     fix_yield = pro_info[0]['fixed_yield']
    #     redeem_yield = decimal.Decimal(str(redeem_amts)) * decimal.Decimal(str(fix_yield)) / decimal.Decimal(
    #         100.00) * decimal.Decimal(str(day2 - day1).split(' ')[0]) * decimal.Decimal(1 / 365.00)
    #     redeem_amt = round(decimal.Decimal(str(redeem_amts)) + redeem_yield, 2)
    #
    #     user_trade_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    #     near_work_date = self._db.judge_is_work_date(day=str(user_trade_time)[0:8])[0]['WORK_DATE']
    #     self.assertEqual(str(trade_request[0]['PROD_ID']), 'ZX05#000730')
    #     self.assertEqual(str(trade_request[0]['PROD_TYPE']), '0')
    #     self.assertEqual(trade_request[0]['SUB_AMT'], decimal.Decimal(str(redeem_amt)))
    #     self.assertEqual(str(trade_request[0]['APPLY_ST']), 'Y')
    #     self.assertEqual(str(trade_request[0]['PAY_ST']), 'Y')
    #     self.assertEqual(str(trade_request[0]['RTTA_ST']), 'Y')
    #     self.assertEqual(str(trade_request[0]['TA_ST']), 'N')
    #     if str(user_trade_time)[0:8] == str(near_work_date):  # 交易当天为工作日
    #         if '090000' < str(user_trade_time)[8:14] < '150000':  # 交易为9:00-15：00之间
    #             self.assertEqual(str(trade_request[0]['APKIND']), '022')
    #             self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022115')
    #             self.assertEqual(str(trade_request[0]['REMARK']), 'T+0赎回，实时申购现金宝')
    #         else:
    #             self.assertEqual(str(trade_request[0]['APKIND']), '022')
    #             self.assertEqual(str(trade_request[0]['SUB_APKIND']), '022118')
    #             self.assertEqual(str(trade_request[0]['REMARK']), '定期宝预约赎回，实时申购现金宝')
    #     else:
    #         self.assertEqual(str(trade_reserve[0]['ACCPT_MODE']), 'M')
    #         self.assertEqual(str(trade_reserve[0]['APKIND']), '024')
    #         self.assertEqual(str(trade_reserve[0]['SUB_APKIND']), '024016')
    #         self.assertEqual(str(trade_reserve[0]['PROD_ID']), str(product_id))
    #         self.assertEqual(str(trade_reserve[0]['PROD_TYPE']), '1')
    #         self.assertEqual(str(trade_reserve[0]['SUB_AMT']),
    #                          decimal.Decimal(str(amt)).quantize(decimal.Decimal('0.00')))
    #         self.assertEqual(str(trade_reserve[0]['REMARK']), '产品预约信息')
    #         self.assertEqual(str(trade_reserve[0]['RES_ST']), 'Y')


    # # 交易-一键随心取金额校验(V3.5)
    # @file_data('test_data/test_one_key_redeem_amt_validate.json')
    # def test_one_key_redeem_amt_validate(self, user_name, password, product_id, redeem_amt, assert_info):
    #     self._restful_xjb.one_key_redeem_amt_validate(user_name=str(user_name), password=str(password),
    #                                                   product_id=str(product_id), redeem_amt=str(redeem_amt))
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])
    #
    #     if entity.returnCode == '000000':
    #         prod_list = self._db.get_product_info(product_id=str(product_id))
    #
    #         # 计算定活宝赎回本金+收益
    #         day1 = datetime.datetime(2018, 01, 22)
    #         now = datetime.datetime.today().strftime('%Y%m%d')
    #         day2 = datetime.datetime(int(str(now)[0:4]), int(str(now)[4:6]), int(str(now)[6:8]))
    #         fix_yield = prod_list[0]['fixed_yield']
    #         redeem_yield = decimal.Decimal(str(redeem_amt)) * decimal.Decimal(str(fix_yield)) / decimal.Decimal(
    #             100.00) * decimal.Decimal(str(day2 - day1).split(' ')[0]) * decimal.Decimal(1 / 365.00)
    #         red_amt = round(decimal.Decimal(str(redeem_amt)) + redeem_yield, 2)
    #         self.assertTrue('本次将取出本金及对应收益共' in str(entity.body_info).replace(',', ''))
    #         self.assertTrue(str(red_amt) in str(entity.body_info).replace(',', ''))
    #         self.assertEqual(str(entity.body_info).replace(',', ''), '本次将取出本金及对应收益共'+str(red_amt)+'元')

    # # 交易-锁定用途列表(V3.5)
    # @file_data('test_data/test_locked_purpose_list.json')
    # def test_locked_purpose_list(self, user_name, password, order_no, product_id, holding_type, value_date,
    #                              assert_info):
    #     self._restful_xjb.locked_purpose_list(user_name=str(user_name), password=str(password),
    #                                           order_no=str(order_no),
    #                                           product_id=str(product_id),
    #                                           holding_type=str(holding_type),
    #                                           value_date=str(value_date))
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # # 交易-基金赎回提示信息(V3.5)
    # @file_data('test_data/test_fund_redeem_tip.json')
    # def test_fund_redeem_tip(self, user_name, password, fund_id, redeem_share, assert_info):
    #     self._restful_xjb.fund_redeem_tip(user_name=str(user_name), password=str(password), fund_id=str(fund_id),
    #                                       redeem_share=str(redeem_share))
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # # 交易-产品剩余额度
    # @file_data('test_data/test_left_amt.json')
    # def test_product_left_amt(self, user_name, password, assert_info):ui
    #     self._restful_xjb.product_left_amt(user_name=str(user_name), password=str(password))
    #
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # 现金宝炒股-获取资产信息
    # @file_data('test_data/test_get_stock_asset_info.json')
    # def test_get_stock_asset_info(self, user_name, password, assert_info):
    #     self._restful_xjb.get_stock_asset_info(user_name=str(user_name), password=str(password))
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])
    #
    #     self.assertIsNotNone(entity.detail)

    # # 基金-估值排行
    # @file_data('test_data/test_fund_estimate_leader_board.json')
    # def test_fund_estimate_leader_board(self, user_name, password, fund_type, sort_type, order_desc, assert_info):
    #     self._restful_xjb.fund_estimate_leader_board(user_name=str(user_name), password=str(password),
    #                                                  fund_type=str(fund_type), sort_type=str(sort_type),
    #                                                  order_desc=str(order_desc))
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # # 基金-最新估值
    # @file_data('test_data/test_get_current_estimate_nav.json')
    # def test_get_current_estimate_nav(self, user_name, password, fund_id, assert_info):
    #     self._restful_xjb.get_current_estimate_nav(user_name=str(user_name), password=str(password),
    #                                                fund_id=str(fund_id))
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])

    # # 基金-自选基金最新估值
    # @file_data('test_data/test_fav_fund_estimate_nav.json')
    # def test_fav_fund_estimate_nav(self, user_name, password, fund_ids, assert_info):
    #     self._restful_xjb.fav_fund_estimate_nav(user_name=str(user_name), password=str(password),
    #                                             fund_ids=str(fund_ids))
    #     entity = self._restful_xjb.entity.current_entity
    #     self.assertEqual(entity.returnMsg, assert_info["returnMsg"])
    #     self.assertEqual(entity.returnCode, assert_info["returnCode"])

    def tearDown(self):
        return


if __name__ == '__main__':
    TestSuiteRun().run_test(XjbServiceTest_01)
    # TestSuiteRun().run_test(XjbServiceTest_02)