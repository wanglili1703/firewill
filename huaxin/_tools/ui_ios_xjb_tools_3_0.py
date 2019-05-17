# coding=utf-8
import re
import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

# from _common.app_compatibility_install import AppCompatibilityInstall
from _common.global_config import GlobalConfig, ASSERT_DICT, ASSERT_DICT_
from _common.global_controller import GlobalController
from _common.ios_deploy import IosDeploy
from _common.utility import Utility
from _common.web_driver import WebDriver
from _tools.mysql_xjb_tools import MysqlXjbTools
from _tools.restful_cms_tools import RestfulCmsTools
from _tools.restful_xjb_tools import RestfulXjbTools
from huaxin_ui.ui_ios_xjb_3_0.main_page import MainPage
from _common.data_base import DataBase
import decimal

RE = "[a-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\ \'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]"


class IOSXjbTools30(object):
    def __init__(self, app_path, platform_version, device_id, port, package_name, app_status, os):
        self._db = MysqlXjbTools()
        self._rt = RestfulXjbTools()
        self._cms = RestfulCmsTools()
        self.app_status = app_status

        # AppCompatibilityInstall().app_install_handle(device_id=device_id, app_path=app_path, package_name=package_name,
        #                                              app_status=app_status, os=os)

        self.web_driver = WebDriver.Appium().open_ios_app(app_path, platform_version, device_id, port, package_name)
        self.main_page = MainPage(self.web_driver)

        # AppCompatibilityInstall().after_launch_handle(device_id=device_id, os=os, web_driver=self.web_driver)

    def old_user(self, user_name, login_password):
        if self.app_status == 'Y':
            self.main_page.go_to_home_page_()
            self.main_page.go_to_login_page()
            self.main_page.login(user_name, login_password, 'HomePage')
        else:
            self.main_page.go_to_home_page()
            self.main_page.go_to_login_page_()
            self.main_page.login(user_name, login_password, 'HomePage')

    def home_page_recharge(self, user_name, login_password, recharge_amount, trade_password, non_superposed_coupon,
                           non_superposed_coupon_quantity):
        self.old_user(user_name=user_name, login_password=login_password)
        self._cms.issue_coupon(code=non_superposed_coupon, mobile=user_name,
                               quantity=non_superposed_coupon_quantity, env='UAT')
        self.main_page.go_to_recharge_page()
        self.main_page.recharge(recharge_amount=recharge_amount, trade_password=trade_password,
                                non_superposed_coupon='Y')
        self.main_page.confirm_trade()
        # 满10减1不可叠加
        total_asset_expected = float(str(ASSERT_DICT['total_asset'])) + float(recharge_amount)
        xjb_asset_expected = float(str(ASSERT_DICT['xjb_asset'])) + float(recharge_amount)
        self.main_page.go_to_assets_page()

        total_asset = str(self.main_page.get_total_asset()).replace(',', '')
        self.main_page.assert_values(decimal.Decimal(total_asset_expected).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(total_asset).quantize(decimal.Decimal('0.00')), '==')

        xjb_asset = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]")
        self.main_page.assert_values(decimal.Decimal(xjb_asset_expected).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(str(xjb_asset).replace(',', '')).quantize(decimal.Decimal('0.00')),
                                     '==')
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_trade_detail_page()

        cunru = self.main_page.get_text('(存入)', 'find_element_by_accessibility_id')
        bank_cunru = self.main_page.get_text('(银行卡存入)', 'find_element_by_accessibility_id')
        recharge_amount_actual = self.main_page.get_text('(+%.2f)' % float(recharge_amount),
                                                         'find_element_by_accessibility_id')
        self.main_page.assert_values('存入', str(cunru))
        self.main_page.assert_values('银行卡存入', str(bank_cunru))
        self.main_page.assert_values('+%.2f' % (float(str(recharge_amount))),
                                     str(recharge_amount_actual))

    def home_page_recharge_negative(self, user_name, login_password, recharge_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_recharge_page()
        self.main_page.recharge(recharge_amount=recharge_amount, trade_password=trade_password)
        self.main_page.verify_at_recharge_page()

    def home_page_regular_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_withdraw_page()
        self.main_page.regular_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password)
        self.main_page.confirm_trade()
        total_asset = float(ASSERT_DICT['total_asset']) - float(withdraw_amount)
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(withdraw_amount)
        self.main_page.go_to_assets_page()

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(',', '')

        self.main_page.assert_values(decimal.Decimal(float(total_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(total_asset_actual)).quantize(decimal.Decimal('0.00')), '==')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(xjb_asset_actual).quantize(decimal.Decimal('0.00')), '==')

        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_trade_detail_page()

        trade_type = self.main_page.get_text('(取出)', 'find_element_by_accessibility_id')
        sub_trade_type = self.main_page.get_text('(普通取出)', 'find_element_by_accessibility_id')

        self.main_page.assert_values('取出', trade_type)
        self.main_page.assert_values('普通取出', sub_trade_type)

        withdraw_amount_actual = self.main_page.get_text('(-%.2f)' % float(withdraw_amount),
                                                         'find_element_by_accessibility_id').replace(',', '')
        self.main_page.assert_values('-%.2f' % float(withdraw_amount), withdraw_amount_actual)

        left_amt = self.main_page.get_text('(余额%s)' % format(xjb_asset, ','), 'find_element_by_accessibility_id')
        self.main_page.assert_values('余额%s' % format(xjb_asset, ','), left_amt)

    def home_page_fast_withdraw_negative(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_withdraw_page()
        self.main_page.fast_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password)
        self.main_page.verify_at_withdraw_page()

    def home_page_regular_withdraw_negative(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_withdraw_page()
        self.main_page.regular_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password)
        self.main_page.verify_at_withdraw_page()

    def home_page_fast_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_withdraw_page()
        self.main_page.fast_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password)
        self.main_page.confirm_trade()
        total_asset = float(ASSERT_DICT['total_asset']) - float(withdraw_amount)
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(withdraw_amount)
        self.main_page.go_to_assets_page()

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(',', '')

        self.main_page.assert_values(str(float(total_asset)), str(float(total_asset_actual)), '==')
        self.main_page.assert_values(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(xjb_asset_actual).quantize(decimal.Decimal('0.00')), '==')

        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_trade_detail_page()

        trade_type = self.main_page.get_text('(取出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('取出', trade_type)

        sub_trade_type = self.main_page.get_text('(快速取出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('快速取出', sub_trade_type)

        withdraw_amount_actual = self.main_page.get_text('(-%.2f)' % float(withdraw_amount),
                                                         'find_element_by_accessibility_id')
        self.main_page.assert_values('-%.2f' % float(withdraw_amount), withdraw_amount_actual)

        left_amt = self.main_page.get_text('(余额%s)' % format(xjb_asset, ','), 'find_element_by_accessibility_id')
        self.main_page.assert_values('余额%s' % format(xjb_asset, ','), left_amt)

    def home_page_view_essence_recommend_list(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.view_essence_recommend_list()

    def register(self, phone_number, login_password):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page_()
        self.main_page.go_to_register_page()
        self.main_page.register(phone_number=phone_number, login_password=login_password)
        self.main_page.go_to_assets_page()
        total_asset_actual = self.main_page.get_total_asset()
        self.main_page.assert_values(0.00, float(total_asset_actual), '==')

    # 手动输入身份信息, 港澳通行证
    def register_binding_card(self, phone_number, login_password, trade_password, user_name, id_no, bank_card_no):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page_()
        self.main_page.go_to_register_page()
        self.main_page.register_binding_card(phone_number=phone_number, login_password=login_password,
                                             trade_password=trade_password)
        self.main_page.go_to_user_input_id_info_page()
        self.main_page.input_user_id_info(user_name, '港澳通行证', id_no)
        self.main_page.binding_card(user_name=user_name, id_no=id_no,
                                    bank_card_no=bank_card_no,
                                    phone_number=phone_number)
        self.main_page.binding_card_confirm()

    def bank_card_manage_binding_card(self, user_name, login_password, bank_card_no, phone_number):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_bank_card_management_page()
        self.main_page.binding_card(bank_card_no=bank_card_no, phone_number=phone_number)
        self.main_page.verify_action_debit_card_success()

    def bank_card_manage_binding_nan_yue_card(self, user_name, login_password, bank_card_no, phone_number):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_bank_card_management_page()
        self.main_page.binding_card(bank_card_no=bank_card_no, phone_number=phone_number)
        self.main_page.verify_action_debit_card_success()

    def delete_bank_card(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_bank_card_management_page()
        self.main_page.delete_band_card(trade_password=trade_password)
        self.main_page.verify_action_debit_card_success()

    def security_center_modify_mobile(self, user_name, login_password, trade_password, mobile_new):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        # self.main_page.go_to_personal_center_page()
        self.main_page.go_to_setting_modify_mobile_page()
        self.main_page.modify_mobile(mobile_old=user_name, trade_password=trade_password, mobile_new=mobile_new)

    def security_center_modify_trade_password(self, user_name, login_password, trade_password_old, trade_password_new):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        # self.main_page.go_to_personal_center_page()
        self.main_page.go_to_security_center_page()
        self.main_page.go_to_setting_trade_password_page()
        self.main_page.modify_trade_password(trade_password_old=trade_password_old,
                                             trade_password_new=trade_password_new)
        self.main_page.verify_at_trade_password_page()

    def security_center_modify_login_password(self, user_name, login_password, login_password_new):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        # self.main_page.go_to_personal_center_page()
        self.main_page.go_to_security_center_page()
        self.main_page.go_to_setting_login_password_page()
        self.main_page.modify_login_password(login_password_old=login_password, login_password_new=login_password_new)
        self.main_page.login(user_name, login_password_new, 'HomePage')

    def security_center_find_trade_password(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        # self.main_page.go_to_personal_center_page()
        self.main_page.go_to_security_center_page()
        self.main_page.go_to_setting_trade_password_page()
        self.main_page.find_trade_password()
        self.main_page.verify_at_security_center_page()

    def buy_high_end_product(self, user_name, login_password, trade_password, product_name, amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.finance_product_search(product_name=product_name, prd_tag=0)
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            points='N', mobile=user_name)
        self.main_page.confirm_trade()

        total_asset = float(ASSERT_DICT['total_asset'])
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(amount)
        vip_asset = float(ASSERT_DICT['vip_asset']) + float(amount)
        amount_new = float(amount)
        self.main_page.go_to_assets_page()

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(str(float(total_asset)), str(float(total_asset_actual)))

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual))

        vip_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(高端)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(vip_asset), float(vip_asset_actual))

        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_trade_detail_page()

        type = self.main_page.get_text('(冻结)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('冻结', type)

        sub_trade_type = self.main_page.get_text('(预约申购冻结)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('预约申购冻结', sub_trade_type)

        amount_new = format(decimal.Decimal(-amount_new).quantize(decimal.Decimal('0.00')), ',')
        amount_new_actual = self.main_page.get_text('(%s)' % amount_new, 'find_element_by_accessibility_id')
        self.main_page.assert_values('%s' % amount_new, amount_new_actual)

        left_amt = self.main_page.get_text(
            '(余额%s)' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ',')
            , 'find_element_by_accessibility_id')
        self.main_page.assert_values('余额%s' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ','),
                                     left_amt)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_trade_record()

        title = self.main_page.get_text('(买入)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入', title)

        status = self.main_page.get_text('(已受理)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('已受理', status)

        product_name_actual = self.main_page.get_text('(%s)' % product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values(product_name, product_name_actual)

        amount_1 = format(decimal.Decimal(amount).quantize(decimal.Decimal('0.00')), ',')
        amt_actual = self.main_page.get_text('(%s元)' % amount_1, 'find_element_by_accessibility_id')
        self.main_page.assert_values('%s元' % amount_1, amt_actual)

        self.main_page.go_to_assets_page()
        self.main_page.go_to_assets_analysis_page()

        total_asset_actual_1 = self.main_page.get_text(
            "//UIAStaticText[@name='总资产(元)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(total_asset), float(total_asset_actual_1))

        xjb_asset_actual_1 = self.main_page.get_text(
            "//UIAStaticText[@name='现金宝']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual_1))

        vip_asset_actual_1 = self.main_page.get_text(
            "//UIAStaticText[@name='端']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(vip_asset), float(vip_asset_actual_1))

    def buy_dqb_product(self, user_name, login_password, product_name, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.finance_product_search(product_name=product_name, prd_tag=1)
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       mobile=user_name)
        self.main_page.confirm_trade()

        total_asset = ASSERT_DICT['total_asset']
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(amount)
        dhb_asset = float(ASSERT_DICT['dhb_asset']) + float(amount)
        self.main_page.go_to_assets_page()

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(total_asset), float(total_asset_actual))

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual))

        dhb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(定活宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(dhb_asset), float(dhb_asset_actual))

        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_trade_detail_page()

        title = self.main_page.get_text('(取出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('取出', title)

        buy_dhb = self.main_page.get_text('(买入定活宝)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入定活宝', buy_dhb)

        amt = self.main_page.get_text('(-%s)' % format(decimal.Decimal(amount).quantize(decimal.Decimal('0.00')), ','),
                                      'find_element_by_accessibility_id')
        self.main_page.assert_values('-%s' % format(decimal.Decimal(amount).quantize(decimal.Decimal('0.00')), ','),
                                     amt)

        xjb_asset_actual_2 = self.main_page.get_text(
            '(余额%s)' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ',')
            , 'find_element_by_accessibility_id')
        self.main_page.assert_values('余额%s' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ','),
                                     xjb_asset_actual_2)

        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.view_dqb_trade_record()

        title = self.main_page.get_text('(买入)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入', title)
        status = self.main_page.get_text('(已受理)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('已受理', status)
        buy_product = self.main_page.get_text('(%s)' % product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values(product_name, buy_product)
        amount_1 = format(decimal.Decimal(amount).quantize(decimal.Decimal('0.00')), ',')
        amt_actual = self.main_page.get_text('(%s元)' % amount_1, 'find_element_by_accessibility_id')
        self.main_page.assert_values('%s元' % amount_1, amt_actual)

        self.main_page.go_to_assets_page()
        self.main_page.go_to_assets_analysis_page()

        total_asset_actual_1 = self.main_page.get_text(
            "//UIAStaticText[@name='总资产(元)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(total_asset), float(total_asset_actual_1))
        xjb_asset_actual_3 = self.main_page.get_text(
            "//UIAStaticText[@name='现金宝']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual_3))
        dhb_asset_actual_1 = self.main_page.get_text(
            "//UIAStaticText[@name='定活宝']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(dhb_asset), float(dhb_asset_actual_1))

    def hot_switch_to_dqb_product_list_page(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_hot_product_list_page()
        self.main_page.hot_switch_to_dqb_product_list_page()

    def hot_switch_to_high_end_product_list_page(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_hot_product_list_page()
        self.main_page.hot_switch_to_high_end_product_list_page()

    def finance_product_search_with_full_name_at_home_page(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.finance_product_search(product_name=product_name)
        self.main_page.verify_search_result(product_name=product_name, expected=True)

    def finance_product_search_with_short_name_at_home_page(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.finance_product_search(product_name=product_name)
        self.main_page.verify_search_result(product_name=product_name, expected=True)

    def assets_xjb_detail_page_recharge(self, user_name, login_password, recharge_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_recharge_page()
        self.main_page.recharge(recharge_amount=recharge_amount, trade_password=trade_password,
                                return_page='AssetsPage')
        self.main_page.confirm_trade_from_xjb_page()
        total_asset = float(ASSERT_DICT['total_asset']) + float(recharge_amount)
        xjb_asset = float(ASSERT_DICT['xjb_asset']) + float(recharge_amount)

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(total_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(total_asset_actual)).quantize(decimal.Decimal('0.00')), "==")

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), "==")

        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_trade_detail_page()

        trade_type = self.main_page.get_text('(存入)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('存入', trade_type)

        sub_trade_type = self.main_page.get_text('(银行卡存入)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('银行卡存入', sub_trade_type)

        recharge_amount_actual = self.main_page.get_text(
            '(+%s)' % format(decimal.Decimal(recharge_amount).quantize(decimal.Decimal('0.00')), ','),
            'find_element_by_accessibility_id')
        self.main_page.assert_values(
            '+%s' % format(decimal.Decimal(recharge_amount).quantize(decimal.Decimal('0.00')), ','),
            recharge_amount_actual)

        xjb_asset_actual_1 = self.main_page.get_text(
            '(余额%s)' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ',')
            , 'find_element_by_accessibility_id')
        self.main_page.assert_values('余额%s' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ','),
                                     xjb_asset_actual_1)

    def assets_xjb_detail_page_regular_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_withdraw_page()
        self.main_page.regular_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password,
                                        return_page='AssetsPage')
        self.main_page.confirm_trade_from_xjb_page()

        total_asset = float(ASSERT_DICT['total_asset']) - float(withdraw_amount)
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(withdraw_amount)

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(total_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(total_asset_actual)).quantize(decimal.Decimal('0.00')), "==")
        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), "==")

        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_trade_detail_page()

        trade_type = self.main_page.get_text('(取出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('取出', trade_type)

        sub_trade_type = self.main_page.get_text('(普通取出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('普通取出', sub_trade_type)

        withdraw_amount_actual = self.main_page.get_text(
            '(-%s)' % format(decimal.Decimal(withdraw_amount).quantize(decimal.Decimal('0.00')), ','),
            'find_element_by_accessibility_id')
        self.main_page.assert_values(
            '-%s' % format(decimal.Decimal(withdraw_amount).quantize(decimal.Decimal('0.00')), ','),
            withdraw_amount_actual)

        xjb_asset_actual_1 = self.main_page.get_text(
            '(余额%s)' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ',')
            , 'find_element_by_accessibility_id')
        self.main_page.assert_values('余额%s' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ','),
                                     xjb_asset_actual_1)

    def assets_xjb_detail_page_fast_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_withdraw_page()
        self.main_page.fast_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password,
                                     return_page='AssetsPage')
        self.main_page.confirm_trade_from_xjb_page()

        total_asset = float(ASSERT_DICT['total_asset']) - float(withdraw_amount)
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(withdraw_amount)

        time.sleep(1)
        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(total_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(total_asset_actual)).quantize(decimal.Decimal('0.00')), "==")
        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), "==")

        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_trade_detail_page()

        trade_type = self.main_page.get_text('(取出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('取出', trade_type)

        sub_trade_type = self.main_page.get_text('(快速取出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('快速取出', sub_trade_type)

        withdraw_amount_actual = self.main_page.get_text(
            '(-%s)' % format(decimal.Decimal(withdraw_amount).quantize(decimal.Decimal('0.00')), ','),
            'find_element_by_accessibility_id')
        self.main_page.assert_values(
            '-%s' % format(decimal.Decimal(withdraw_amount).quantize(decimal.Decimal('0.00')), ','),
            withdraw_amount_actual)

        xjb_asset_actual_1 = self.main_page.get_text(
            '(余额%s)' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ',')
            , 'find_element_by_accessibility_id')
        self.main_page.assert_values('余额%s' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ','),
                                     xjb_asset_actual_1)

    def delete_credit_card(self, user_name, login_password, last_card_no, trade_password):
        self._db.update_deleted_cust_credit_card_to_normal(card_id='166', state='N')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.delete_credit_card(last_card_no=last_card_no, trade_password=trade_password)
        self.main_page.verify_action_credit_card_success()

    def add_credit_card(self, user_name, login_password, credit_card_no):
        self._db.update_deleted_cust_credit_card_to_normal(card_id='166', state='D')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.add_credit_card(credit_card_no=credit_card_no, phone_no=user_name)
        self.main_page.verify_action_credit_card_success()

    def view_message(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_message_center_page()
        self.main_page.view_message()

    def view_xjb_trade_detail(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_trade_detail_page()
        self.main_page.view_xjb_trade_detail()

    def dqb_detail_page_view_trade_detail(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_at_trade_detail_page()
        self.main_page.view_trade_detail()

    def view_dqb_more_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.view_dqb_more_product()
        self.main_page.verify_at_dhb_page()

    def view_dqb_history_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.view_dqb_history_product()
        self.main_page.verify_at_dhb_history_page()

    def fund_detail_page_view_trade_detail(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.view_trade_detail(default_type='基金')

    def view_fund_more_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_more_product_page()
        self.main_page.verify_at_all_fund_page()
        self.main_page.switch_to_other_fund_type_list()

    def high_end_detail_page_view_trade_detail(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.view_trade_detail(default_type='高端理财')

    def view_high_end_more_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_more_product()
        self.main_page.verify_at_high_end_page()

    # 现金管理系列页面
    def view_high_end_cash_management_series(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_more_product()
        self.main_page.go_to_cash_management_series()
        self.main_page.verify_at_cash_management_series_page()

    # 固定收益系列页面
    def view_high_end_fixed_rate_series(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_more_product()
        self.main_page.go_to_fixed_rate_series()
        self.main_page.verify_at_fixed_rate_series_page()

    # 精选系列页面
    def view_high_end_best_recommend_series(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_more_product()
        self.main_page.go_to_best_recommend_series()
        self.main_page.verify_at_best_recommend_series_page()

    def redeem_high_end_product(self, user_name, login_password, redeem_amount, trade_password, high_end_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.redeem_high_end_product(redeem_amount=redeem_amount, trade_password=trade_password,
                                               high_end_product=high_end_product)
        self.main_page.confirm_trade_from_xjb_page()
        self.main_page.verify_at_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_trade_record(high_end_product=high_end_product)

        trade_type = self.main_page.get_text('(卖出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('卖出', trade_type)

        status = self.main_page.get_text('已受理', 'find_element_by_accessibility_id')
        self.main_page.assert_values('已受理', status)

        product_name = self.main_page.get_text('(%s)' % high_end_product, 'find_element_by_accessibility_id')
        self.main_page.assert_values(high_end_product, product_name)

        redeem_amount_1 = format(decimal.Decimal(redeem_amount).quantize(decimal.Decimal("0.00")), ',')
        redeem_amount_actual = self.main_page.get_text('(%s份)' % redeem_amount_1, 'find_element_by_accessibility_id')
        self.main_page.assert_values('%s份' % str(redeem_amount_1), redeem_amount_actual)

    def redeem_high_end_product_max(self, user_name, login_password, redeem_amount, trade_password, high_end_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.redeem_high_end_product(redeem_amount=redeem_amount, trade_password=trade_password,
                                               high_end_product=high_end_product)

    def redeem_high_end_product_min(self, user_name, login_password, redeem_amount, trade_password, high_end_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.redeem_high_end_product(redeem_amount=redeem_amount, trade_password=trade_password,
                                               high_end_product=high_end_product)

    def redeem_dqb_product(self, user_name, login_password, redeem_amount, trade_password, dqb_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.redeem_dqb_product(redeem_amount=redeem_amount, trade_password=trade_password,
                                          dqb_product=dqb_product)
        self.main_page.confirm_trade_from_xjb_page()
        self.main_page.verify_at_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.view_dqb_trade_record(dqb_product=dqb_product)

        trade_type = self.main_page.get_text('(取回)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('取回', trade_type)

        status = self.main_page.get_text('成功', 'find_element_by_accessibility_id')
        self.main_page.assert_values('成功', status)

        product_name = self.main_page.get_text('(%s)' % dqb_product, 'find_element_by_accessibility_id')
        self.main_page.assert_values(dqb_product, product_name)

        redeem_amount_1 = format(
            decimal.Decimal(str(ASSERT_DICT['dhb_redeem_actual'])).quantize(decimal.Decimal("0.00")),
            ',')
        redeem_amount_actual = self.main_page.get_text('(%s元)' % redeem_amount_1, 'find_element_by_accessibility_id')
        self.main_page.assert_values('%s元' % redeem_amount_1, redeem_amount_actual)

    def redeem_dqb_product_max(self, user_name, login_password, redeem_amount, trade_password, dqb_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.redeem_dqb_product(redeem_amount=redeem_amount, trade_password=trade_password,
                                          dqb_product=dqb_product)

    def redeem_dqb_product_min(self, user_name, login_password, redeem_amount, trade_password, dqb_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.redeem_dqb_product(redeem_amount=redeem_amount, trade_password=trade_password,
                                          dqb_product=dqb_product)

    def my_referee(self, user_name, login_password, phone_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.my_referee(phone_no=phone_no)

    def risk_evaluating_new_user(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_account_info_page()
        self.main_page.risk_evaluating()

    def fund_non_money_product_search_with_name(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_product_search(product_name=product_name)
        self.main_page.verify_at_fund_detail_page()
        # 验证非货币基金标识
        self.main_page.verify_equity_fund_detail_page()

    def fund_money_product_search_with_code(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_product_search(product_name=product_name)
        # 验证货币基金标识
        self.main_page.verify_money_fund_detail_page()

    def buy_fund_product(self, user_name, login_password, fund_product_name, amount, trade_password, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.finance_product_search(product_name=fund_product_name, product_code=fund_product_code, prd_tag=2)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, mobile=user_name)
        self.main_page.confirm_fund_trade()
        self.main_page.verify_at_fund_detail_page()
        self.main_page.back_to_home_page()
        self.main_page.cancel_search()

        total_asset = float(ASSERT_DICT['total_asset'])
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(amount)
        fund_asset = float(ASSERT_DICT['fund_asset']) + float(amount)
        self.main_page.go_to_assets_page()

        time.sleep(1)
        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(total_asset), float(total_asset_actual))
        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual))

        fund_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(基金)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(fund_asset), float(fund_asset_actual))

        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_trade_detail_page()
        time.sleep(1)

        title = self.main_page.get_text('(取出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('取出', title)
        sub_type = self.main_page.get_text('(申购基金)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('申购基金', sub_type, "==")

        amount_new = format(decimal.Decimal(str(amount)).quantize(decimal.Decimal('0.00')), ',')
        amount_new_actual = self.main_page.get_text('(-%s)' % amount_new, 'find_element_by_accessibility_id')
        self.main_page.assert_values('-%s' % amount_new, amount_new_actual)

        left_amt = self.main_page.get_text(
            '(余额%s)' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ',')
            , 'find_element_by_accessibility_id')
        self.main_page.assert_values('余额%s' % format(decimal.Decimal(xjb_asset).quantize(decimal.Decimal('0.00')), ','),
                                     left_amt)

        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.view_fund_trade_record()

        title = self.main_page.get_text('(买入)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入', title)
        status = self.main_page.get_text('(已受理)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('已受理', status)
        buy_product = self.main_page.get_text('(%s)' % fund_product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values(fund_product_name, buy_product)

        buy_amount = format(decimal.Decimal(str(amount)).quantize(decimal.Decimal('0.00')), ',')
        amt_actual = self.main_page.get_text('(%s元)' % buy_amount, 'find_element_by_accessibility_id')
        self.main_page.assert_values('%s元' % buy_amount, amt_actual)

        self.main_page.go_to_assets_page()
        self.main_page.go_to_assets_analysis_page()

        total_asset_actual_1 = self.main_page.get_text(
            "//UIAStaticText[@name='总资产(元)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(total_asset), float(total_asset_actual_1))

        xjb_asset_actual_2 = self.main_page.get_text(
            "//UIAStaticText[@name='现金宝']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual_2))

        fund_asset_actual_1 = self.main_page.get_text(
            "//UIAStaticText[@name='金']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(fund_asset), float(fund_asset_actual_1))

    def invite_friend(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_invite_friend_page()
        self.main_page.verify_at_invite_friend_page()

    # 用户自身有绑定的预约码, 使用其他预约码
    # flag = 1, 用户自身有预约码, flag = 0, 用户自身没有预约码, 默认 flag = 0
    def use_other_reservation_code(self, user_name, login_password, reservation_code, trade_password, buy_quota,
                                   buy_count, reserve_quota, reserve_count, product_id):
        self._db.reservation_code_status_modify(buy_quota=buy_quota, buy_count=buy_count,
                                                reserve_quota=reserve_quota,
                                                reserve_count=reserve_count, mobile=user_name,
                                                reserve_code=reservation_code,
                                                product_id=product_id)

        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_reservation_code_page()
        self.main_page.use_other_reservation_code(reserve_code=reservation_code, trade_password=trade_password,
                                                  amount=reserve_quota, mobile=user_name, flag=1)
        self.main_page.confirm_trade_from_xjb_page()
        self.main_page.verify_at_assets_page()

    # 预约码--用户未绑定预约码, 使用其他预约码
    def use_other_reservation_code_without_reservation_code(self, user_name, login_password, reservation_code,
                                                            trade_password, buy_quota,
                                                            buy_count, reserve_quota, reserve_count, product_id,
                                                            user_name_have_reservation_code):
        self._db.reservation_code_status_modify(buy_quota=buy_quota, buy_count=buy_count,
                                                reserve_quota=reserve_quota,
                                                reserve_count=reserve_count, mobile=user_name_have_reservation_code,
                                                reserve_code=reservation_code,
                                                product_id=product_id)

        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_reservation_code_page()
        self.main_page.use_other_reservation_code(reserve_code=reservation_code, trade_password=trade_password,
                                                  amount=reserve_quota, mobile=user_name)

        self.main_page.confirm_trade_from_xjb_page()
        self.main_page.verify_at_assets_page()

    # 预约码--使用自己的预约码
    def use_reservation_code(self, user_name, login_password, trade_password, buy_quota, buy_count, reserve_quota,
                             reserve_count, reservation_code, product_id):
        self._db.reservation_code_status_modify(buy_quota=buy_quota, buy_count=buy_count,
                                                reserve_quota=reserve_quota,
                                                reserve_count=reserve_count, mobile=user_name,
                                                reserve_code=reservation_code,
                                                product_id=product_id)

        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_reservation_code_page()
        self.main_page.use_reservation_code(trade_password=trade_password, amount=reserve_quota, mobile=user_name)
        self.main_page.confirm_trade_from_xjb_page()
        self.main_page.verify_at_assets_page()

    def redeem_fund_product(self, user_name, login_password, amount, trade_password, fund_product_name_for_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.redeem_fund_product(amount=amount, trade_password=trade_password,
                                           fund_product_name_for_redeem=fund_product_name_for_redeem)

        self.main_page.confirm_fund_redeem()
        self.main_page.view_fund_trade_record(fund_product_name_for_redeem=fund_product_name_for_redeem)

        trade_type = self.main_page.get_text('(卖出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('卖出', trade_type)
        status = self.main_page.get_text('(已受理)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('已受理', status)
        fund_product_name_for_redeem = re.sub(RE, "", fund_product_name_for_redeem)
        redeem_product = self.main_page.get_text('(%s)' % fund_product_name_for_redeem,
                                                 'find_element_by_accessibility_id')
        self.main_page.assert_values(fund_product_name_for_redeem, redeem_product)

        redeem_amount_1 = format(decimal.Decimal(amount).quantize(decimal.Decimal("0.00")), ',')
        redeem_amount_actual = self.main_page.get_text('(%s份)' % redeem_amount_1, 'find_element_by_accessibility_id')
        self.main_page.assert_values("%s份" % redeem_amount_1, redeem_amount_actual)

    def redeem_fund_product_max(self, user_name, login_password, amount, trade_password, fund_product_name_for_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.redeem_fund_product(amount=amount, trade_password=trade_password,
                                           fund_product_name_for_redeem=fund_product_name_for_redeem)

    def redeem_fund_product_min(self, user_name, login_password, amount, trade_password, fund_product_name_for_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.redeem_fund_product(amount=amount, trade_password=trade_password,
                                           fund_product_name_for_redeem=fund_product_name_for_redeem)

    def earn_points(self, user_name, login_password, amount, trade_password, fund_product_name, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.earn_points_by_buy_fund(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, mobile=user_name)
        self.main_page.confirm()

    # 赚积分--推荐用户注册绑卡
    def earn_points_by_recommend_user_register(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.earn_points_by_recommend_user_register()
        self.main_page.verify_at_invite_friend_page()

    # 信用卡还款
    def credit_card_repay(self, user_name, login_password, repay_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.repay(repay_amount, trade_password)
        self.main_page.verify_action_credit_card_success()
        self.main_page.verify_at_credit_card_list_page()

    # 信用卡预约还款
    def credit_card_reserved_pay(self, user_name, login_password, reserved_pay_amount, trade_password,
                                 user_credit_card_id):
        # repay_order = self._db.get_creditcard_repay_order(card_id=str(user_credit_card_id))
        # if repay_order[0]['state'] == 'N':
        #     self._db.update_creditcard_order_state(card_id=str(user_credit_card_id), orign_state='N', update_state='C')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.go_to_reserved_pay_page()
        self.main_page.reserved_pay(reserved_pay_amount, trade_password)
        self.main_page.verify_action_credit_card_success()
        self.main_page.verify_at_credit_card_list_page()

    # 取消预约还款
    def cancel_reserved_pay(self, user_name, login_password, user_credit_card_id):
        # repay_order = self._db.get_creditcard_repay_order(card_id=str(user_credit_card_id))
        # if repay_order[0]['state'] == 'C':
        #     self._db.update_creditcard_order_state(card_id=str(user_credit_card_id), orign_state='C', update_state='N')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.cancel_reservation()

    # 花积分--买定期宝
    def spend_points_by_buy_dqb(self, user_name, login_password, amount, trade_password, dqb_product_name, ):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.spend_points_by_buy_dqb(dqb_product_name=dqb_product_name)
        self.main_page.buy_dqb_product(product_name=None, amount=amount, trade_password=trade_password,
                                       mobile=user_name, points='Y')
        self.main_page.confirm_trade_from_xjb_page()

        usable_points = float(ASSERT_DICT['usable_points'])
        total_asset = float(ASSERT_DICT['total_asset']) + usable_points
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(amount) + usable_points

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(total_asset), float(total_asset_actual))

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual))

        self.main_page.go_to_dqb_detail_page()
        self.main_page.view_dqb_trade_record()

        buy_amt = format(decimal.Decimal(amount).quantize(decimal.Decimal('0.00')), ',')
        amount_actual = self.main_page.get_text('(%s元)' % buy_amt, 'find_element_by_accessibility_id')
        self.main_page.assert_values('%s元' % buy_amt, amount_actual)

        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.view_points_trade_record()

        buy_product = self.main_page.get_text('(买入|%s抵扣)' % dqb_product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入|%s抵扣' % dqb_product_name, buy_product)

        use_points = self.main_page.get_text('(-%s)' % decimal.Decimal(usable_points).quantize(decimal.Decimal("0.00")),
                                             'find_element_by_accessibility_id')
        self.main_page.assert_values('-%.2f' % float(usable_points), str(use_points))

    # 花积分--买基金
    def spend_points_by_buy_fund(self, user_name, login_password, amount, trade_password, fund_product_name,
                                 fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.spend_points_by_buy_fund(fund_product_name=fund_product_name,
                                                fund_product_code=fund_product_code)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, points='Y', mobile=user_name)
        self.main_page.confirm_fund_trade()
        self.main_page.verify_at_fund_detail_page()
        self.main_page.back_to_home_page()
        self.main_page.cancel_search_to_all_fund_page()
        self.main_page.back_to_assets_page()

        time.sleep(1)
        usable_points = float(ASSERT_DICT['usable_points'])
        total_asset = float(ASSERT_DICT['total_asset']) + usable_points
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(amount) + usable_points

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(total_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(total_asset_actual)).quantize(decimal.Decimal('0.00')), "==")

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), "==")

        self.main_page.go_to_fund_detail_page()
        self.main_page.view_fund_trade_record()

        amount_1 = format(decimal.Decimal(amount).quantize(decimal.Decimal('0.00')), ',')
        amt_actual = self.main_page.get_text('(%s元)' % amount_1, 'find_element_by_accessibility_id')
        self.main_page.assert_values('%s元' % amount_1, amt_actual)

        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.view_points_trade_record()

        buy_product = self.main_page.get_text('(买入|%s抵扣)' % fund_product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入|%s抵扣' % fund_product_name, buy_product)

        use_points = self.main_page.get_text('(-%s)' % decimal.Decimal(usable_points).quantize(decimal.Decimal("0.00")),
                                             'find_element_by_accessibility_id')
        self.main_page.assert_values('-%.2f' % float(usable_points), str(use_points))

    # 花积分--买高端产品
    def spend_points_by_buy_vipproduct_use_product_name(self, user_name, login_password, product_name, amount,
                                                        trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.spend_points_by_buy_vipproduct_use_product_name(product_name=product_name)
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            points='Y', mobile=user_name)
        self.main_page.confirm_trade()

        usable_points = float(ASSERT_DICT['usable_points'])
        total_asset = float(ASSERT_DICT['total_asset']) + usable_points
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(amount) + usable_points
        vip_asset = float(ASSERT_DICT['vip_asset']) + float(amount)
        amount_new = float(amount) - usable_points

        self.main_page.go_to_assets_page()

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(str(float(total_asset)), str(float(total_asset_actual)))

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), '==')

        vip_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(高端)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(vip_asset), float(vip_asset_actual))

        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_trade_detail_page()

        trade_type = self.main_page.get_text('(冻结)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('冻结', trade_type)

        sub_trade_type = self.main_page.get_text('(预约申购冻结)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('预约申购冻结', sub_trade_type)

        amount_new = format(decimal.Decimal(-amount_new).quantize(decimal.Decimal('0.00')), ',')
        amount_new_actual = self.main_page.get_text('(%s)' % amount_new, 'find_element_by_accessibility_id')
        self.main_page.assert_values('%s' % amount_new, amount_new_actual)

        left_amt = self.main_page.get_text('(余额%s)' % format(xjb_asset, ',')
                                           , 'find_element_by_accessibility_id')
        self.main_page.assert_values('余额%s' % format(xjb_asset, ','), left_amt)

        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_trade_record()

        title = self.main_page.get_text('(买入)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入', title)

        status = self.main_page.get_text('(已受理)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('已受理', status)

        product_name_actual = self.main_page.get_text('(%s)' % product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values(product_name, product_name_actual)

        amount_1 = format(decimal.Decimal(amount).quantize(decimal.Decimal('0.00')), ',')
        amt_actual = self.main_page.get_text('(%s元)' % amount_1, 'find_element_by_accessibility_id')
        self.main_page.assert_values('%s元' % amount_1, amt_actual)

        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.view_points_trade_record()

        buy_product = self.main_page.get_text('(买入|%s抵扣)' % product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入|%s抵扣' % product_name, buy_product)

        use_points = self.main_page.get_text('(-%s)' % decimal.Decimal(usable_points).quantize(decimal.Decimal("0.00")),
                                             'find_element_by_accessibility_id')
        self.main_page.assert_values('-%.2f' % float(usable_points), str(use_points))

        self.main_page.go_to_assets_page()
        self.main_page.go_to_assets_analysis_page()

        total_asset_actual_1 = self.main_page.get_text(
            "//UIAStaticText[@name='总资产(元)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(total_asset), float(total_asset_actual_1))

        xjb_asset_actual_1 = self.main_page.get_text(
            "//UIAStaticText[@name='现金宝']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual_1))

        vip_asset_actual_1 = self.main_page.get_text(
            "//UIAStaticText[@name='端']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(vip_asset), float(vip_asset_actual_1))

    # 添加信用卡还款提醒
    def add_credit_card_repayment_warn(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.add_repayment_warn()

    # 取消信用卡还款提醒
    def cancel_credit_card_repayment_warn(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.cancel_repayment_warn()

    # 高端普通卖出
    def normal_redeem_vipproduct(self, user_name, login_password, redeem_amount, trade_password,
                                 high_end_product_for_fast_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.normal_redeem_vipproduct(redeem_amount=redeem_amount, trade_password=trade_password,
                                                high_end_product_for_fast_redeem=high_end_product_for_fast_redeem)

        self.main_page.confirm_trade_from_xjb_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_trade_detail_page()

        trade_type = self.main_page.get_text("//UIATableCell[1]/UIAStaticText[@label='卖出']")
        self.main_page.assert_values('卖出', trade_type)
        status = self.main_page.get_text('(已受理)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('已受理', status)
        redeem_product = self.main_page.get_text('(%s)' % high_end_product_for_fast_redeem,
                                                 'find_element_by_accessibility_id')
        self.main_page.assert_values(high_end_product_for_fast_redeem, redeem_product)

        redeem_amount_1 = format(decimal.Decimal(redeem_amount).quantize(decimal.Decimal("0.00")), ',')
        redeem_amount_actual = self.main_page.get_text('(%s份)' % redeem_amount_1, 'find_element_by_accessibility_id')
        self.main_page.assert_values("%s份" % redeem_amount_1, redeem_amount_actual)

    # 高端急速卖出
    def fast_redeem_vipproduct(self, user_name, login_password, redeem_amount, trade_password,
                               high_end_product_for_fast_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.fast_redeem_vipproduct(redeem_amount=redeem_amount, trade_password=trade_password,
                                              high_end_product_for_fast_redeem=high_end_product_for_fast_redeem)
        self.main_page.confirm_trade_from_xjb_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_trade_detail_page()

        trade_type = self.main_page.get_text("//UIATableCell[1]/UIAStaticText[@label='极速卖出']")
        self.main_page.assert_values('极速卖出', trade_type)
        status = self.main_page.get_text('(尾款充值中)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('尾款充值中', status)
        redeem_product = self.main_page.get_text('(%s)' % high_end_product_for_fast_redeem,
                                                 'find_element_by_accessibility_id')
        self.main_page.assert_values(high_end_product_for_fast_redeem, redeem_product)

        redeem_amount_1 = format(decimal.Decimal(redeem_amount).quantize(decimal.Decimal("0.00")), ',')
        redeem_amount_actual = self.main_page.get_text('(%s份)' % redeem_amount_1, 'find_element_by_accessibility_id')
        self.main_page.assert_values("%s份" % redeem_amount_1, redeem_amount_actual)

    # 基金普通卖出
    def normal_redeem_fund_product(self, user_name, login_password, redeem_amount, trade_password,
                                   fund_product_name_for_fast_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.normal_redeem_fund_product(fund_product_name_for_fast_redeem=fund_product_name_for_fast_redeem,
                                                  redeem_amount=redeem_amount, trade_password=trade_password)

        self.main_page.confirm_fund_redeem()
        self.main_page.view_fund_trade_record(fund_product_name_for_redeem=fund_product_name_for_fast_redeem)

        trade_type = self.main_page.get_text('(卖出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('卖出', trade_type)
        status = self.main_page.get_text('(已受理)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('已受理', status)
        fund_product_name_for_redeem = re.sub(RE, "", fund_product_name_for_fast_redeem)
        redeem_product = self.main_page.get_text('(%s)' % fund_product_name_for_redeem,
                                                 'find_element_by_accessibility_id')
        self.main_page.assert_values(fund_product_name_for_redeem, redeem_product)

        redeem_amount_1 = format(decimal.Decimal(redeem_amount).quantize(decimal.Decimal("0.00")), ',')
        redeem_amount_actual = self.main_page.get_text('(%s份)' % redeem_amount_1, 'find_element_by_accessibility_id')
        self.main_page.assert_values("%s份" % redeem_amount_1, redeem_amount_actual)

    # 基金极速卖出
    def fast_redeem_fund_product(self, user_name, login_password, redeem_amount, trade_password,
                                 fund_product_name_for_fast_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.fast_redeem_fund_product(fund_product_name_for_fast_redeem=fund_product_name_for_fast_redeem,
                                                redeem_amount=redeem_amount, trade_password=trade_password)

        self.main_page.confirm_fund_redeem()
        self.main_page.view_fund_trade_record(fund_product_name_for_redeem=fund_product_name_for_fast_redeem)

        trade_type = self.main_page.get_text('(极速卖出)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('极速卖出', trade_type)
        status = self.main_page.get_text('(尾款充值中)', 'find_element_by_accessibility_id')
        self.main_page.assert_values('尾款充值中', status)
        fund_product_name_for_redeem = re.sub(RE, "", fund_product_name_for_fast_redeem)
        redeem_product = self.main_page.get_text('(%s)' % fund_product_name_for_redeem,
                                                 'find_element_by_accessibility_id')
        self.main_page.assert_values(fund_product_name_for_redeem, redeem_product)

        redeem_amount_1 = format(decimal.Decimal(redeem_amount).quantize(decimal.Decimal("0.00")), ',')
        redeem_amount_actual = self.main_page.get_text('(%s份)' % redeem_amount_1, 'find_element_by_accessibility_id')
        self.main_page.assert_values("%s份" % redeem_amount_1, redeem_amount_actual)

    # 积分明细
    def assets_my_points_details(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.my_points_details()

    # 新基金频道--研究报告
    def fund_research_report(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_info_page()
        self.main_page.fund_info()

    # 基金频道--资讯
    def fund_info_report(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_info_page()
        self.main_page.fund_info()

    # 基金频道--机构观点
    def fund_institution_viewpoint(self):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.fund_institution_viewpoint()

    # 基金频道--达人论基
    def fund_talent_fund_discussion(self):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.fund_talent_fund_discussion()

    # 基金频道--市场指数
    def fund_market_index(self, csi_index):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.fund_market_index(csi_index=csi_index)

    # 基金频道--全部基金
    def fund_all_funds(self):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.fund_all_funds()

    # 基金频道--评级排行
    def fund_rating_and_ranking(self):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_rating_page()
        self.main_page.verify_at_fund_rating_page()
        self.main_page.fund_rating_and_ranking()

    # 基金频道--自选基金(基金详情页面加)
    def fund_selected_funds(self, fund_product_name, user_name, login_password,
                            fund_company):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_selected_page()
        self.main_page.fund_selected_funds(fund_product_name=fund_product_name,
                                           fund_company=fund_company)

    # 基金频道--删除自选基金
    def fund_selected_funds_deleted(self, fund_product_name, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_selected_page()
        self.main_page.go_to_fund_detail_page(fund_product_name=fund_product_name)
        self.main_page.fund_selected_delete_click()
        self.main_page.back_to_previous_page(return_page='FundSelectedPage')
        self.main_page.verify_fund_if_exist(fund_product_name, False)

    # 基金频道--对比分析
    def fund_comparison_and_analysis(self, fund_product_code, fund_product_code_2):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_compare_and_combination_page()
        self.main_page.fund_compare_and_analysis(fund_product_code=fund_product_code,
                                                 fund_product_code_2=fund_product_code_2)

    # 购买定期宝使用优惠券(不可叠加)
    def buy_dqb_use_nonsuperposed_coupon(self, user_name, login_password, product_name, amount, trade_password,
                                         non_superposed_coupon_code, non_superposed_coupon_quantity):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        # self._cms.issue_coupon(code=non_superposed_coupon_code, mobile=user_name,
        #                        quantity=non_superposed_coupon_quantity, env='UAT')
        self.main_page.finance_product_search(product_name=product_name, prd_tag=1)
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       mobile=user_name, nonsuperposed_coupon='Y')
        self.main_page.confirm_trade()
        self.main_page.go_to_assets_page()
        # 满10减1不可叠加
        coupon_amount = float(1)
        total_asset = float(ASSERT_DICT['total_asset']) + coupon_amount
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - (float(amount) - coupon_amount)

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(total_asset), float(total_asset_actual))

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), '==')
        self.main_page.go_to_dqb_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_at_trade_record_detail_page()

        self.main_page.verify_trade_record_info(product_name=product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 购买定期宝使用优惠券(可叠加)
    def buy_dqb_use_superposed_coupon(self, user_name, login_password, product_name, amount, trade_password,
                                      superposed_coupon_code, superposed_coupon_quantity):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name, quantity=superposed_coupon_quantity,
        #                        env='UAT')
        self.main_page.finance_product_search(product_name=product_name, prd_tag=1)
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       mobile=user_name, superposed_coupon='Y')
        self.main_page.confirm_trade()
        self.main_page.go_to_assets_page()
        # 满10减1不可叠加
        coupon_amount = float(2)
        total_asset = float(ASSERT_DICT['total_asset']) + coupon_amount
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - (float(amount) - coupon_amount)

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(total_asset), float(total_asset_actual))

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), '==')
        self.main_page.go_to_dqb_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_at_trade_record_detail_page()

        self.main_page.verify_trade_record_info(product_name=product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 购买高端使用优惠券(不可叠加)
    def buy_vipproduct_use_nonsuperposed_coupon(self, user_name, login_password, product_name, amount,
                                                trade_password, non_superposed_coupon_code,
                                                non_superposed_coupon_quantity):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        # self._cms.issue_coupon(code=non_superposed_coupon_code, mobile=user_name,
        #                        quantity=non_superposed_coupon_quantity, env='UAT')
        self.main_page.finance_product_search(product_name=product_name, prd_tag=0)
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            nonsuperposed_coupon='Y', mobile=user_name)
        self.main_page.confirm_trade()
        # 满10减1不可叠加
        coupon_amount = float(1)
        total_asset = float(ASSERT_DICT['total_asset']) + coupon_amount
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - (float(amount) - coupon_amount)
        self.main_page.go_to_assets_page()

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(str(float(total_asset)), str(float(total_asset_actual)))

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), '==')

        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_trade_record()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_trade_record_info(product_name=product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 购买高端使用优惠券(可叠加)
    def buy_vipproduct_use_superposed_coupon(self, user_name, login_password, product_name, amount,
                                             trade_password, superposed_coupon_code, superposed_coupon_quantity):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name,
        #                        quantity=superposed_coupon_quantity, env='UAT')
        self.main_page.finance_product_search(product_name=product_name, prd_tag=0)
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            superposed_coupon='Y', mobile=user_name)
        self.main_page.confirm_trade()
        # 满10减1可叠加, 买两张
        coupon_amount = float(2)
        total_asset = float(ASSERT_DICT['total_asset']) + coupon_amount
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - (float(amount) - coupon_amount)
        self.main_page.go_to_assets_page()

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(str(float(total_asset)), str(float(total_asset_actual)))

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual))

        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_trade_record()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_trade_record_info(product_name=product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 购买基金使用优惠券(不可叠加)
    def buy_fund_use_nonsuperposed_coupon(self, user_name, login_password, product_name, amount,
                                          trade_password, fund_product_code, non_superposed_coupon_code,
                                          non_superposed_coupon_quantity):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        # self._cms.issue_coupon(code=non_superposed_coupon_code, mobile=user_name,
        #                        quantity=non_superposed_coupon_quantity, env='UAT')
        self.main_page.fund_product_search(product_name=product_name)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, nonsuperposed_coupon='Y',
                                        mobile=user_name)
        self.main_page.confirm_fund_trade()
        self.main_page.verify_at_fund_detail_page()
        self.main_page.back_to_home_page()
        self.main_page.cancel_search()

        # 满10减1不可叠加
        coupon_amount = float(1)
        total_asset = float(ASSERT_DICT['total_asset']) + coupon_amount
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - (float(amount) - coupon_amount)
        self.main_page.go_to_assets_page()

        time.sleep(1)
        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(total_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(total_asset_actual)).quantize(decimal.Decimal('0.00')), '==')
        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), '==')

        self.main_page.go_to_fund_detail_page()
        self.main_page.view_fund_trade_record()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_trade_record_info(product_name=product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 购买基金使用优惠券(可叠加)
    def buy_fund_use_superposed_coupon(self, user_name, login_password, product_name, amount, trade_password,
                                       fund_product_code, superposed_coupon_code, superposed_coupon_quantity):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name,
        #                        quantity=superposed_coupon_quantity, env='UAT')
        self.main_page.fund_product_search(product_name=product_name)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, superposed_coupon='Y',
                                        mobile=user_name)
        self.main_page.confirm_fund_trade()
        self.main_page.verify_at_fund_detail_page()
        self.main_page.back_to_home_page()
        self.main_page.cancel_search()

        # 满10减1可叠加, 买2张
        coupon_amount = float(2)
        total_asset = float(ASSERT_DICT['total_asset']) + coupon_amount
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - (float(amount) - coupon_amount)
        self.main_page.go_to_assets_page()

        time.sleep(1)
        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(total_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(total_asset_actual)).quantize(decimal.Decimal('0.00')), '==')
        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), '==')

        self.main_page.go_to_fund_detail_page()
        self.main_page.view_fund_trade_record()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_trade_record_info(product_name=product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 购买定期宝使用积分+优惠券(不可叠加)
    def buy_dqb_use_points_and_nonsuperposed_coupon(self, user_name, login_password, product_name, amount,
                                                    trade_password, non_superposed_coupon_code,
                                                    non_superposed_coupon_quantity
                                                    ):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        # self._cms.issue_coupon(code=non_superposed_coupon_code, mobile=user_name,
        #                        quantity=non_superposed_coupon_quantity, env='UAT')
        self.main_page.finance_product_search(product_name=product_name, prd_tag=1)
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       mobile=user_name, points='Y', nonsuperposed_coupon='Y')
        self.main_page.confirm_trade()
        self.main_page.go_to_assets_page()
        # 满10减1不可叠加
        coupon_amount = float(1)
        usable_points = float(ASSERT_DICT['usable_points'])
        total_asset = float(ASSERT_DICT['total_asset']) + coupon_amount + usable_points
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - (float(amount) - coupon_amount - usable_points)

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(total_asset), float(total_asset_actual))

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual))

        self.main_page.go_to_my_points_page()
        self.main_page.view_points_trade_record()

        buy_product = self.main_page.get_text('(买入|%s抵扣)' % product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入|%s抵扣' % product_name, buy_product)

        use_points = self.main_page.get_text('(-%s)' % decimal.Decimal(usable_points).quantize(decimal.Decimal("0.00")),
                                             'find_element_by_accessibility_id')
        self.main_page.assert_values('-%.2f' % float(usable_points), str(use_points))

        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_at_trade_record_detail_page()

        self.main_page.verify_trade_record_info(product_name=product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 购买定期宝使用积分+优惠券(可叠加)
    def buy_dqb_use_points_and_superposed_coupon(self, user_name, login_password, product_name, amount,
                                                 trade_password, superposed_coupon_code,
                                                 superposed_coupon_quantity
                                                 ):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name,
        #                        quantity=superposed_coupon_quantity, env='UAT')
        self.main_page.finance_product_search(product_name=product_name, prd_tag=1)
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       mobile=user_name, points='Y', superposed_coupon='Y')
        self.main_page.confirm_trade()
        self.main_page.go_to_assets_page()
        # 满10减1可叠加, 2张
        coupon_amount = float(2)
        usable_points = float(ASSERT_DICT['usable_points'])
        total_asset = float(ASSERT_DICT['total_asset']) + coupon_amount + usable_points
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - (float(amount) - coupon_amount - usable_points)

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(total_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(total_asset_actual)).quantize(decimal.Decimal('0.00')), '==')

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), '==')

        self.main_page.go_to_my_points_page()
        self.main_page.view_points_trade_record()

        buy_product = self.main_page.get_text('(买入|%s抵扣)' % product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入|%s抵扣' % product_name, buy_product)

        use_points = self.main_page.get_text('(-%s)' % decimal.Decimal(usable_points).quantize(decimal.Decimal("0.00")),
                                             'find_element_by_accessibility_id')
        self.main_page.assert_values('-%.2f' % float(usable_points), str(use_points))

        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_at_trade_record_detail_page()

        self.main_page.verify_trade_record_info(product_name=product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 购买高端使用积分+优惠券(不可叠加)
    def buy_vipproduct_use_points_and_nonsuperposed_coupon(self, user_name, login_password, product_name, amount,
                                                           trade_password, non_superposed_coupon_code,
                                                           non_superposed_coupon_quantity
                                                           ):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        # self._cms.issue_coupon(code=non_superposed_coupon_code, mobile=user_name,
        #                        quantity=non_superposed_coupon_quantity, env='UAT')
        self.main_page.finance_product_search(product_name=product_name, prd_tag=0)
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            points='Y', nonsuperposed_coupon='Y', mobile=user_name)
        self.main_page.confirm_trade()
        self.main_page.go_to_assets_page()
        # 满10减1可叠加, 买1张
        coupon_amount = float(1)
        usable_points = float(ASSERT_DICT['usable_points'])
        total_asset = float(ASSERT_DICT['total_asset']) + usable_points + coupon_amount
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(amount) + usable_points + coupon_amount

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(str(float(total_asset)), str(float(total_asset_actual)))

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual))

        self.main_page.go_to_my_points_page()
        self.main_page.view_points_trade_record()

        buy_product = self.main_page.get_text('(买入|%s抵扣)' % product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入|%s抵扣' % product_name, buy_product)

        use_points = self.main_page.get_text('(-%s)' % decimal.Decimal(usable_points).quantize(decimal.Decimal("0.00")),
                                             'find_element_by_accessibility_id')
        self.main_page.assert_values('-%.2f' % float(usable_points), str(use_points))

        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_trade_record()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_trade_record_info(product_name=product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 购买高端使用积分+优惠券(可叠加)
    def buy_vipproduct_use_points_and_superposed_coupon(self, user_name, login_password, product_name, amount,
                                                        trade_password, superposed_coupon_code,
                                                        superposed_coupon_quantity
                                                        ):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name,
        #                        quantity=superposed_coupon_quantity, env='UAT')
        self.main_page.finance_product_search(product_name=product_name, prd_tag=0)
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            points='Y', superposed_coupon='Y', mobile=user_name)
        self.main_page.confirm_trade()
        self.main_page.go_to_assets_page()
        # 满10减1可叠加, 买两张
        coupon_amount = float(2)
        usable_points = float(ASSERT_DICT['usable_points'])
        total_asset = float(ASSERT_DICT['total_asset']) + usable_points + coupon_amount
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - float(amount) + usable_points + coupon_amount

        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(str(float(total_asset)), str(float(total_asset_actual)))

        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(float(xjb_asset), float(xjb_asset_actual))

        self.main_page.go_to_my_points_page()
        self.main_page.view_points_trade_record()

        buy_product = self.main_page.get_text('(买入|%s抵扣)' % product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入|%s抵扣' % product_name, buy_product)

        use_points = self.main_page.get_text('(-%s)' % decimal.Decimal(usable_points).quantize(decimal.Decimal("0.00")),
                                             'find_element_by_accessibility_id')
        self.main_page.assert_values('-%.2f' % float(usable_points), str(use_points))

        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_trade_record()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_trade_record_info(product_name=product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 购买基金使用积分+优惠券(不可叠加)
    def buy_fund_use_points_and_nonsuperposed_coupon(self, user_name, login_password, fund_product_name, amount,
                                                     trade_password, fund_product_code, non_superposed_coupon_code,
                                                     non_superposed_coupon_quantity
                                                     ):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        # self._cms.issue_coupon(code=non_superposed_coupon_code, mobile=user_name,
        #                        quantity=non_superposed_coupon_quantity, env='UAT')
        self.main_page.go_to_fund_detail_page(fund_product_name=fund_product_name,
                                              fund_product_code=fund_product_code)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, points='Y',
                                        nonsuperposed_coupon='Y', mobile=user_name)

        self.main_page.confirm_fund_trade()
        self.main_page.verify_at_fund_detail_page()
        self.main_page.back_to_home_page()
        self.main_page.cancel_search()
        self.main_page.go_to_assets_page()

        # 满10减1可叠加, 买1张
        coupon_amount = float(1)
        usable_points = float(ASSERT_DICT['usable_points'])
        total_asset = float(ASSERT_DICT['total_asset']) + coupon_amount + usable_points
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - (float(amount) - coupon_amount - usable_points)

        time.sleep(1)
        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(total_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(total_asset_actual)).quantize(decimal.Decimal('0.00')), "==")
        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), "==")

        self.main_page.go_to_my_points_page()
        self.main_page.view_points_trade_record()

        buy_product = self.main_page.get_text('(买入|%s抵扣)' % fund_product_name, 'find_element_by_accessibility_id')
        self.main_page.assert_values('买入|%s抵扣' % fund_product_name, buy_product)

        use_points = self.main_page.get_text('(-%s)' % decimal.Decimal(usable_points).quantize(decimal.Decimal("0.00")),
                                             'find_element_by_accessibility_id')
        self.main_page.assert_values('-%.2f' % float(usable_points), str(use_points))

        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.view_fund_trade_record()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_trade_record_info(product_name=fund_product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 购买基金使用积分+优惠券(可叠加)
    def buy_fund_use_points_and_superposed_coupon(self, user_name, login_password, fund_product_name, amount,
                                                  trade_password,
                                                  fund_product_code, superposed_coupon_code,
                                                  superposed_coupon_quantity
                                                  ):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name,
        #                        quantity=superposed_coupon_quantity, env='UAT')
        self.main_page.go_to_fund_detail_page(fund_product_name=fund_product_name,
                                              fund_product_code=fund_product_code)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, points='Y',
                                        superposed_coupon='Y', mobile=user_name)
        self.main_page.confirm_fund_trade()
        self.main_page.verify_at_fund_detail_page()
        self.main_page.back_to_home_page()
        self.main_page.cancel_search()

        # 满10减1可叠加, 买2张
        coupon_amount = float(2)
        usable_points = float(ASSERT_DICT['usable_points'])
        total_asset = float(ASSERT_DICT['total_asset']) + coupon_amount + usable_points
        xjb_asset = float(ASSERT_DICT['xjb_asset']) - (float(amount) - coupon_amount - usable_points)
        self.main_page.go_to_assets_page()

        time.sleep(1)
        total_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(total_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(total_asset_actual)).quantize(decimal.Decimal('0.00')), '==')
        xjb_asset_actual = self.main_page.get_text(
            "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(
            ',', '')
        self.main_page.assert_values(decimal.Decimal(float(xjb_asset)).quantize(decimal.Decimal('0.00')),
                                     decimal.Decimal(float(xjb_asset_actual)).quantize(decimal.Decimal('0.00')), '==')

        self.main_page.go_to_fund_detail_page()
        self.main_page.view_fund_trade_record()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_trade_record_info(product_name=fund_product_name, trade_type="买入", status="已受理",
                                                amount=str(amount))

    # 基金定投 (基金详情页面为入口)
    def fund_plan(self, user_name, login_password, fund_product_name, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_product_search(product_name=fund_product_name)
        self.main_page.go_to_fund_plan_page()
        self.main_page.make_fund_plan(amount=amount, trade_password=trade_password, mobile=user_name)
        self.main_page.user_operation_complete(return_page='FundPageFundDetail')
        self.main_page.verify_at_fund_detail_page()
        # self._db.delete_fund_invest_plan(mobile=user_name)
        self._db.update_fund_invest_plan_status(status='E', mobile=user_name, is_delete='1')

    # 查看历史定投(用户没有历史定投)
    def check_empty_fund_history_plan(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_my_fund_plan_page()
        if ASSERT_DICT['page'] == 'StartFundPlanPage':
            self.main_page.go_to_fund_page_all_fund_page()
            self.main_page.go_to_assets_fund_detail_page()
            self.main_page.go_to_my_fund_plan_page()
        self.main_page.go_to_fund_history_plan_page()
        self.main_page.verify_page_title()
        self.main_page.verify_page_elements()

    # 暂停定投计划
    def pause_fund_plan(self, user_name, login_password, trade_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_fund_invest_plan_status(status='N', id='737')
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.go_to_fund_plan_detail_page(fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_fund_plan_status('定投进行中')
        self.main_page.pause_fund_plan(trade_password=trade_password)
        self.main_page.verify_fund_plan_status('定投已暂停')

    # 恢复定投计划
    def restart_fund_plan(self, user_name, login_password, trade_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_fund_invest_plan_status(status='P', id='737')
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.go_to_fund_plan_detail_page(fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_fund_plan_status('定投已暂停')
        self.main_page.restart_fund_plan(trade_password=trade_password, mobile=user_name)
        self.main_page.verify_fund_plan_status('定投进行中')

    # 终止定投计划
    def stop_fund_plan(self, user_name, login_password, trade_password, fund_product_name):
        self._db.update_fund_invest_plan_status(status='N', id='737')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.go_to_fund_plan_detail_page(fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_fund_plan_status('定投进行中')
        self.main_page.get_fund_plan_details()
        self.main_page.stop_fund_plan(trade_password=trade_password)
        self.main_page.go_to_fund_history_plan_page()
        self.main_page.verify_page_title()
        self.main_page.verify_fund_history_details(fund_product_name=fund_product_name)

    # 修改定投计划
    def modify_fund_plan(self, user_name, login_password, trade_password, fund_product_name, amount):
        self._db.update_fund_invest_plan_status(period='1#W', day='W#1', amount='10.00', status='P', id='737')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.go_to_fund_plan_detail_page(fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.go_to_make_fund_plan_page()
        self.main_page.verify_page_title()
        self.main_page.make_fund_plan(amount=amount, trade_password=trade_password, return_page='FundPlanDetailPage',
                                      mobile=user_name)
        self.main_page.user_operation_complete(return_page='FundPlanDetailPage')
        self.main_page.verify_page_title()
        self.main_page.verify_fund_plan_details(amount=amount)

    # 新增定投计划
    def add_fund_plan(self, user_name, login_password, fund_product_name, fund_product_code, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.add_fund_plan()
        self.main_page.close_tips()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.verify_page_title()
        self.main_page.search_fund_products(fund_product_name=fund_product_name)
        self.main_page.go_to_fund_plan_page()
        self.main_page.verify_page_title()
        self.main_page.make_fund_plan(amount=amount, trade_password=trade_password, mobile=user_name)
        self.main_page.verify_page_title()
        try:
            self.main_page.user_operation_complete(return_page='FundPlanPage')
            self.main_page.verify_at_my_fund_plan_list_page()
            # self._db.delete_fund_invest_plan(mobile=user_name)
        finally:
            self._db.update_fund_invest_plan_status(status='E', mobile=user_name, is_delete='1')

    # 随心借
    def vip_product_pledge(self, user_name, login_password, product_name, pledge_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_pledge_list_page()
        self.main_page.verify_at_pledge_list_page()
        self.main_page.go_to_select_pledge_product_page()
        self.main_page.verify_at_pledge_product_select_page()
        self.main_page.select_pledge_product_page(product_name)
        self.main_page.verify_at_pledge_borrow_page()
        self.main_page.pledge_detail(pledge_amount=pledge_amount, trade_password=trade_password)
        self.main_page.confirm_trade(return_page="PledgePage")
        self.main_page.verify_pledge_record(product_name)

    # 随心还(必须一次还清)
    def vip_product_pledge_repay(self, user_name, login_password, product_name, pledge_repay_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_pledge_list_page()
        self.main_page.go_to_pledge_repay_page(product_name)
        self.main_page.verify_page_title()
        self.main_page.pledge_repay(pledge_repay_amount=pledge_repay_amount, trade_password=trade_password)
        self.main_page.confirm_trade(return_page='PledgePage')
        self.main_page.verify_at_pledge_list_page()
        self.main_page.go_to_pledge_history_page()
        self.main_page.verify_at_pledge_repay_history_page()
        self.main_page.verify_pledge_repay_status(product_name=product_name)
        self.main_page.go_to_pledge_repay_history_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_pledge_repay_history_details(product_name=product_name,
                                                           pledge_repay_amount=pledge_repay_amount)

    # 会员中心
    def associate_level(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.associator_rank_verify()
        self.main_page.go_to_associator_center()
        level = self.main_page.get_text('com.shhxzq.xjb:id/tv_member_lv', 'find_element_by_accessibility_id')
        self.main_page.current_level_verify()

    # 员工理财--开启工资代发
    def salary_issuing(self, user_name, login_password):
        self._db.update_employee_protocol_status(mobile=user_name, protocol_status='0')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_deposit_salary_page()
        self.main_page.start_salary_issuing()

    # 员工理财--终止工资代发
    def stop_salary_issuing(self, user_name, login_password, trade_password):
        self._db.update_employee_protocol_status(mobile=user_name, protocol_status='1')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_deposit_salary_page()
        self.main_page.stop_salary_issuing(trade_password=trade_password)
        self.main_page.verify_at_salary_detail_title()

    # 开启工资理财计划
    def start_financing_plan(self, user_name, login_password, last_no, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_make_financing_plan_page()
        self.main_page.make_financing_plan(last_no=last_no, amount=amount, trade_password=trade_password)
        try:
            self.main_page.confirm_trade(return_page='DepositSalaryPage')
            self.main_page.verify_page_title()
            # self._db.delete_fund_invest_plan(mobile=user_name)
        finally:
            self._db.update_fund_invest_plan_status(status='E', mobile=user_name, is_delete='1')

    # 新增工资理财计划
    def add_financing_plan(self, user_name, login_password, last_no, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_make_financing_plan_page()
        self.main_page.make_financing_plan(last_no=last_no, amount=amount, trade_password=trade_password)
        self.main_page.confirm_trade(return_page='DepositSalaryPage')
        self.main_page.verify_page_title()
        # self._db.delete_fund_invest_plan(mobile=user_name)
        self._db.update_fund_invest_plan_status(status='E', mobile=user_name, is_delete='1')

    # 暂停工资理财计划
    def pause_financing_plan(self, user_name, login_password, trade_password):
        self._db.update_fund_invest_plan_status(status='N', id='1095')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_salary_financing_plan_detail_page()
        self.main_page.pause_salary_financing_plan(trade_password=trade_password)

    # 启用工资理财计划
    def restart_financing_plan(self, user_name, login_password, trade_password):
        self._db.update_fund_invest_plan_status(status='P', id='1095')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_salary_financing_plan_detail_page()
        self.main_page.restart_salary_financing_plan(trade_password=trade_password)
        self.main_page.verify_at_salary_detail_title()

    # 我的优惠券-立即使用-买入
    def use_coupon_from_my_coupon_list(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_coupon_list()
        self.main_page.use_coupon_to_buy_page()
        self.main_page.verify_at_high_end_purchase_page()
        print '点击左上角箭头'
        self.main_page.go_back_previous_page(return_page='MyCouponsListPage')
        print '验证当前在我的优惠券页面'
        self.main_page.verify_page_title()

    # 历史优惠券
    def history_coupon_list(self, user_name, password):
        print '登录现金宝'
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.go_to_assets_page()
        print '点击我的优惠券'
        self.main_page.go_to_my_coupon_list()

        print '点击历史优惠券'
        self.main_page.go_to_history_page()

        print '验证当前在历史优惠券页面'
        self.main_page.verify_page_title()

        print '验证优惠券已使用标签'
        self.main_page.verify_used_coupon_icon()

        print '点击左上角箭头'
        self.main_page.go_back_to_my_coupon()

        print '验证当前在我的优惠券页面'
        self.main_page.verify_page_title()

    # 优惠券说明页面
    def coupon_description(self, user_name, password):
        print '登录现金宝'
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.go_to_assets_page()
        print '点击我的优惠券'
        self.main_page.go_to_my_coupon_list()

        print '点击说明'
        self.main_page.go_to_coupon_description_page()

        print "验证当前在优惠券说明页面"
        self.main_page.verify_page_elements()

        print '点击左上角箭头'
        self.main_page.go_back_to_my_coupon()

        print '验证当前在我的优惠券页面'
        self.main_page.verify_page_title()

    # 我的优惠券列表为空
    def my_coupon_empty_list(self, user_name, password):
        print '登录现金宝'
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.go_to_assets_page()

        print '点击我的优惠券'
        self.main_page.go_to_my_coupon_list()

        self.main_page.verify_page_title()

        self.main_page.verify_empty_coupon_record()

        print '点击左上角箭头'
        self.main_page.go_back_to_assets_page()

        print '验证当前在我的资产页面'
        self.main_page.verify_at_assets_page()

    # 修改工资理财计划
    def modify_financing_plan(self, user_name, login_password, trade_password, last_no, amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_fund_invest_plan_status(status='N', id='1095', bank_account='6222023886786003555', amount='150',
                                                bank_serial_no='0000000001060661')
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_salary_financing_plan_detail_page()
        self.main_page.go_to_modify_financing_plan_page()
        self.main_page.modify_salary_financing_plan(trade_password=trade_password, last_no=last_no, amount=amount)
        self.main_page.confirm_trade(return_page='SalaryFinancingPlanDetailPage')
        self.main_page.verify_at_salary_detail_title()

    # 终止工资理财计划
    def stop_financing_plan(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_fund_invest_plan_status(status='N', id='1095')
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_salary_financing_plan_detail_page()
        self.main_page.stop_salary_financing_plan(trade_password=trade_password)
        self.main_page.verify_at_salary_detail_title()

    # 还房贷
    def make_repay_housing_loan_plan(self, user_name, login_password, last_no, trade_password, repay_amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_make_repay_plan_page()
        self.main_page.make_repay_loan_plan(trade_password=trade_password, last_no=last_no,
                                            repay_amount=repay_amount,
                                            repay_type='housing_loan')
        self.main_page.confirm_trade(return_page='RepayLoanPage')
        self.main_page.verify_repay_loan(repay_type='housing_loan', repay_amount=repay_amount, last_no=last_no)
        self._db.update_plan_status(mobile=user_name, status='D')

    # 还车贷
    def make_repay_car_loan_plan(self, user_name, login_password, last_no, trade_password, repay_amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_make_repay_plan_page()
        self.main_page.make_repay_loan_plan(trade_password=trade_password, last_no=last_no, repay_amount=repay_amount,
                                            repay_type='car_loan')
        self.main_page.confirm_trade(return_page='RepayLoanPage')
        self.main_page.verify_repay_loan(repay_type='car_loan', repay_amount=repay_amount, last_no=last_no)
        self._db.update_plan_status(mobile=user_name, status='D')

    # 还其他
    def make_repay_other_loan_plan(self, user_name, login_password, last_no, trade_password, repay_amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_make_repay_plan_page()
        self.main_page.make_repay_loan_plan(trade_password=trade_password, last_no=last_no, repay_amount=repay_amount,
                                            repay_type='others', other_purpose=u'其他用途')
        self.main_page.confirm_trade(return_page='RepayLoanPage')
        self.main_page.verify_repay_loan(repay_type='others', repay_amount=repay_amount, last_no=last_no)
        self._db.update_plan_status(mobile=user_name, status='D')

    # 暂停还贷款计划
    def pause_repay_loan_plan(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='N', repay_type='H', repay_plan_id='317')
        self.main_page.go_to_assets_page()
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='housing_loan')
        self.main_page.pause_repay_loan_plan(trade_password=trade_password)
        self.main_page.confirm_trade(return_page='RepayLoanPlanDetailPage')
        self.main_page.verify_at_repay_loan_detail_page(status='已暂停')

    # 启用还贷款计划
    def restart_repay_loan_plan(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='P', repay_type='H', repay_plan_id='317')
        self.main_page.go_to_assets_page()
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='housing_loan')
        self.main_page.restart_repay_loan_plan(trade_password=trade_password)
        self.main_page.confirm_trade(return_page='RepayLoanPlanDetailPage')
        self.main_page.verify_at_repay_loan_detail_page(status='正在执行中')

    # 修改还房贷为还车贷
    def modify_repay_housing_loan_to_repay_car_loan(self, user_name, login_password, trade_password, last_no,
                                                    repay_amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='N', repay_type='H', repay_plan_id='317', bank_acco='6222023886786003555')
        self.main_page.go_to_assets_page()
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='housing_loan')
        self.main_page.go_to_modify_repay_loan_plan_page()
        self.main_page.modify_repay_loan_plan(trade_password=trade_password, last_no=last_no, repay_amount=repay_amount,
                                              repay_type='car_loan')
        self.main_page.confirm_trade(return_page='RepayLoanPlanDetailPage')
        self.main_page.verify_at_repay_loan_detail_page()

    # 修改还车贷为还其他贷款
    def modify_repay_car_loan_to_repay_other_loan(self, user_name, login_password, trade_password, last_no,
                                                  repay_amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='N', repay_type='C', repay_plan_id='317', bank_acco='6222023886786003555')
        self.main_page.go_to_assets_page()
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='car_loan')
        self.main_page.go_to_modify_repay_loan_plan_page()
        self.main_page.modify_repay_loan_plan(trade_password=trade_password, last_no=last_no, repay_amount=repay_amount,
                                              repay_type='others', other_purpose=u'其他用途')
        self.main_page.confirm_trade(return_page='RepayLoanPlanDetailPage')
        self.main_page.verify_at_repay_loan_detail_page()

    # 修改还其他贷款为还房贷
    def modify_repay_other_loan_to_repay_housing_loan(self, user_name, login_password, trade_password, last_no,
                                                      repay_amount):
        self._db.update_plan_status(status='N', repay_type='O', repay_plan_id='317', bank_acco='6222023886786003555')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='others', other_purpose='其他用途')
        self.main_page.go_to_modify_repay_loan_plan_page()
        self.main_page.modify_repay_loan_plan(trade_password=trade_password, last_no=last_no, repay_amount=repay_amount,
                                              repay_type='housing_loan')
        self.main_page.confirm_trade(return_page='RepayLoanPlanDetailPage')
        self.main_page.verify_at_repay_loan_detail_page()

    # 删除还贷款计划
    def delete_repay_loan_plan(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='N', repay_type='H', repay_plan_id='317')
        self.main_page.go_to_assets_page()
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='housing_loan')
        self.main_page.delete_repay_loan_plan(trade_password=trade_password)
        self.main_page.confirm_trade(return_page='RepayLoanPage')
        self.main_page.verify_at_repay_loan_page()
        self.main_page.verify_loan_count()

    # 实名用户重绑删除的卡（只有一张卡）
    def certificated_user_rebind_deleted_card(self, user_name, login_password, bank_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_bank_card_management_page_by_clicking_tips()
        self.main_page.binding_card(bank_card_no=bank_card_no, phone_number=user_name, flag=1)
        self.main_page.verify_action_debit_card_success()
        self.main_page.verify_bank_card_management_page()
        self._db.update_bank_card_delete_status(card_no=bank_card_no, is_delete='Y')

    # 现金宝页面点击万份收益,进入万份收益页面
    def view_xjb_income_per_wan(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_interest_page_per_wan()
        self.main_page.verify_at_income_detail_page(title='万份收益')

    # 现金宝页面点击累计收益,进入累计收益页面
    def view_xjb_income_accumulated(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_interest_page_accumulated()
        self.main_page.verify_at_income_detail_page(title='累计收益')

    # 现金宝页面点击七日年化收益率,进入七日年化收益率页面
    def view_xjb_seven_days_annual_rate_of_return(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_seven_days_annual_rate_of_return_page()
        self.main_page.verify_at_income_detail_page(title='七日年化收益率')

    # 查看资产分析
    def view_assets_analysis(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.verify_assets_items()

    # 下载资产证明
    def download_assets_certification(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.go_to_assets_certification_preview_page(trade_password)
        self.main_page.verify_page_title()
        self.main_page.download_assets_certification()
        self.main_page.verify_alert_title()

    # 持有高端产品详情页面
    def view_vip_product_details(self, user_name, login_password, high_end_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_high_end_holding_detail_page(high_end_product=high_end_product)
        self.main_page.verify_at_vip_holding_detail_page(product_name=high_end_product)

    # 基金撤单
    def cancel_fund_order(self, user_name, login_password, product_name, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.go_to_specific_trade_detail_page(product_name=product_name)
        self.main_page.verify_at_trade_record_detail_page()
        self.main_page.cancel_order(trade_password=trade_password)
        self.main_page.confirm_trade(return_page='AssetsFundDetailPage')
        self.main_page.verify_at_fund_holding_list_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.go_to_specific_trade_detail_page(product_name=product_name)
        self.main_page.verify_trade_record_info(product_name=product_name, trade_type='买入', status='已撤销')

    # 高端撤单
    def cancel_vip_product_order(self, user_name, login_password, product_name, trade_password, amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.go_to_specific_trade_detail_page(product_name=product_name)
        self.main_page.cancel_order(trade_password=trade_password)
        self.main_page.confirm_trade(return_page='AssetsHighEndDetailPage')
        self.main_page.verify_at_high_end_holding_list_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.go_to_specific_trade_detail_page(product_name=product_name)
        self.main_page.verify_trade_record_info(product_name=product_name, trade_type='买入', status='已撤销', amount=amount)

    # 现金宝持有页面查看在途资产(资产分析页面进)
    def view_xjb_asset_in_transit(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_asset_in_transit_page()
        self.main_page.verify_at_assets_in_transit_page()
        self.main_page.verify_asset_in_transit_details()

    # 现金宝持有页面查看产品详情(资产分析页面进)
    def view_xjb_product_detail(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_product_detail_page()
        self.main_page.verify_at_fund_detail_page()
        self.main_page.verify_money_fund_detail_page()
        self.main_page.verify_fund_name("博时现金宝货币")

    # 现金宝持有页面查看七日年化收益率曲线
    def view_xjb_seven_days_annual_rate_of_return_curve(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.view_xjb_seven_days_annual_rate_of_return(term='1个月')
        self.main_page.verify_at_xjb_detail_page()
        self.main_page.view_xjb_seven_days_annual_rate_of_return(term='3个月')
        self.main_page.verify_at_xjb_detail_page()

    # 查看基金资产, 资产结构配置页面(资产分析页面进)
    def view_holding_fund_asset_structure(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.go_to_assets_fund_detail_page()
        self.main_page.go_to_fund_assets_structure_page()
        self.main_page.verify_fund_assets_structure_details()
        self.main_page.go_to_fund_assets_page(fund_type='混合型')
        self.main_page.verify_at_fund_assets_page()
        self.main_page.verify_fund_assets_details(fund_type='混合型')
        self.main_page.back_to_fund_assets_structure_page()
        self.main_page.verify_at_fund_assets_structure_page()
        self.main_page.go_to_fund_assets_page(fund_type='货币型')
        self.main_page.verify_at_fund_assets_page()
        self.main_page.verify_fund_assets_details(fund_type='货币型')

    # 查看高端资产（资产分析页面进）的说明
    def view_high_end_holding_assets_description(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.go_to_assets_high_end_detail_page()
        self.main_page.go_to_high_end_description()
        self.main_page.verify_description('高端理财总资产：', return_page='AssetsHighEndDetailPage')
        self.main_page.verify_at_high_end_holding_list_page()

    # 查看持有定活宝资产（资产分析页面进）的说明
    def view_dhb_holding_assets_description(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.go_to_assets_dhb_detail_page()
        self.main_page.go_to_dhb_description()
        self.main_page.verify_description('定期理财：', return_page='AssetsDqbDetailPage')
        self.main_page.verify_at_dhb_holding_list_page()

    # 查看持有现金宝资产的说明
    def view_xjb_holding_assets_description(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_xjb_description()
        self.main_page.verify_description('现金宝资产：', return_page='AssetsXjbDetailPage')
        self.main_page.verify_at_xjb_detail_page()

    # 查看持有基金资产的说明
    def view_fund_holding_assets_description(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_description()
        self.main_page.verify_description('基金总资产：', return_page='AssetsFundDetailPage')
        self.main_page.verify_at_fund_holding_list_page()

    # 持有高端追加购买产品(购买确认中和确认后)
    def high_end_continue_purchase(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_confirmed_high_end_holding_detail_page(product_name=product_name)
        self.main_page.verify_at_vip_holding_detail_page(product_name=product_name)
        self.main_page.vip_product_supplementary_purchase()
        self.main_page.verify_at_product_purchase_page()
        self.main_page.back_to_previous_page("HighEndHoldingDetailPage")
        self.main_page.back_to_previous_page("AssetsHighEndDetailPage")
        self.main_page.go_to_high_end_holding_detail_page(product_name=product_name)
        self.main_page.verify_at_vip_holding_detail_page(product_name=product_name)
        self.main_page.vip_product_supplementary_purchase()
        self.main_page.verify_at_product_purchase_page()

    # 持有定活宝追加购买产品
    def dhb_continue_purchase(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.go_to_dhb_holding_details_page(product_name=product_name)
        self.main_page.verify_at_dhb_holding_detail_page(product_name=product_name)
        self.main_page.dhb_product_supplementary_purchase()
        self.main_page.verify_at_product_purchase_page()

    # 持有基金追加购买产品(购买确认中和确认后)
    def fund_continue_purchase(self, user_name, login_password, product_name, product_code, product_name_confirmed):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_confirmed_fund_holding_detail_page(product_name_confirmed)
        self.main_page.verify_at_fund_holding_detail_page(product_name_confirmed)
        self.main_page.fund_product_supplementary_purchase()
        self.main_page.verify_at_product_purchase_page()
        self.main_page.back_to_previous_page("FundHoldingDetailPage")
        self.main_page.back_to_previous_page("AssetsFundDetailPage")
        self.main_page.go_to_fund_holding_detail_page(product_name, product_code)
        self.main_page.verify_at_fund_holding_detail_page(product_name)
        self.main_page.fund_product_supplementary_purchase()
        self.main_page.verify_at_product_purchase_page()

    # 短信验证码登录
    def login_use_verification_code(self, user_name):
        self.main_page.go_to_login_page_()
        self.main_page.login_use_verification_code(user_name=user_name)
        self.main_page.verify_at_assets_page()

    # 现金支付手段买高端
    def buy_vip_product_use_cash_management_product(self, user_name, login_password, product_name, trade_password,
                                                    amount, cash_management_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        self.main_page.finance_product_search(product_name=product_name)
        self.main_page.go_to_product_purchase_page()
        self.main_page.buy_finance_product(mobile=user_name, amount=amount, trade_password=trade_password,
                                           cash_management_product=cash_management_product, cash_management='Y')
        self.main_page.confirm_trade(return_page='FinanceHighEndPage')
        self.main_page.finance_product_search(product_name=product_name)
        self.main_page.go_to_product_purchase_page()
        self.main_page.verify_cash_management_left_amount(amount, cash_management_product)

    # 现金管理系列作为支付手段买基金
    def buy_fund_product_use_cash_management_product(self, user_name, login_password, fund_product_name, amount,
                                                     trade_password, cash_management_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_search(product_name=fund_product_name)
        self.main_page.go_to_product_purchase_page()
        self.main_page.buy_finance_product(mobile=user_name, amount=amount, trade_password=trade_password,
                                           cash_management_product=cash_management_product, cash_management='Y')
        self.main_page.confirm_trade(return_page='ProductDetailPage')
        self.main_page.verify_page_title(product_type=2)
        self.main_page.go_to_product_purchase_page()
        self.main_page.verify_cash_management_left_amount(amount, cash_management_product)

    # 现金管理系列作为支付手段买定活宝
    def buy_dhb_product_use_cash_management_product(self, user_name, login_password, trade_password, product_name,
                                                    amount, cash_management_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_dqb_product_list_page()
        self.main_page.finance_product_search(product_name=product_name)
        self.main_page.go_to_product_purchase_page()
        self.main_page.buy_finance_product(mobile=user_name, amount=amount, trade_password=trade_password,
                                           cash_management_product=cash_management_product, cash_management='Y')
        self.main_page.confirm_trade(return_page='FinanceDqbPage')
        self.main_page.finance_product_search(product_name=product_name)
        self.main_page.go_to_product_purchase_page()
        self.main_page.verify_cash_management_left_amount(amount, cash_management_product)
        self.main_page.back_to_previous_page(return_page='ProductDetailPage')
        self.main_page.back_to_previous_page(return_page='FinanceDqbPage')
        self.main_page.cancel_search()
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_confirmed_high_end_holding_detail_page(product_name=cash_management_product)
        self.main_page.go_to_trade_record_page()
        self.main_page.go_to_specific_trade_detail_page(product_name=product_name)
        self.main_page.verify_trade_record_info(product_name=product_name, trade_type='买入', status='已受理', amount=amount)

    # 信用卡还款使用优惠券(从理财日历入口)
    def credit_card_repay_use_coupon(self, user_name, login_password, repay_amount, trade_password, last_card_no,
                                     non_superposed_coupon_code, non_superposed_coupon_quantity):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_calendar_page()
        self.main_page.go_to_personal_event_setting_page()
        self.main_page.go_to_credit_card_list_page()
        # self._cms.issue_coupon(code=non_superposed_coupon_code, mobile=user_name,
        #                        quantity=non_superposed_coupon_quantity)
        self.main_page.repay(repay_amount, trade_password, non_superposed_coupon='Y')
        self.main_page.verify_action_credit_card_success()
        self.main_page.verify_at_credit_card_list_page()
        self.main_page.select_credit_card(last_card_no)
        self.main_page.go_to_credit_repay_record_page()
        self.main_page.verify_at_repay_record_page()
        self.main_page.verify_repay_record_details(last_card_no=last_card_no, amount=repay_amount,
                                                   bank=ASSERT_DICT['bank'])

    # 信用卡预约还款使用优惠券
    def credit_card_reserve_repay_use_coupon(self, user_name, login_password, repay_amount, trade_password,
                                             last_card_no, user_credit_card_id,
                                             superposed_coupon_code, superposed_coupon_quantity):
        # repay_order = self._db.get_creditcard_repay_order(card_id=str(user_credit_card_id))
        # if repay_order[0]['state'] == 'N':
        #     self._db.update_creditcard_order_state(card_id=str(user_credit_card_id), orign_state='N', update_state='C')
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name,
        #                        quantity=superposed_coupon_quantity)
        self.main_page.go_to_reserved_pay_page()
        self.main_page.reserved_pay(repay_amount, trade_password, use_coupon='Y')
        self.main_page.verify_action_credit_card_success()
        self.main_page.verify_at_credit_card_list_page()
        self.main_page.verify_reserve_pay_info(last_card_no, repay_amount)

    # 理财日历查看提醒事项
    def check_event_reminder_in_calendar(self, user_name, password):
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.view_calendar_event()

    # 滑动理财日历,页面显示正常
    def swipe_calendar(self, user_name, password):
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.go_to_calendar_page_by_clicking_more()
        self.main_page.swipe_calendar()

    # 定活宝收益计算器
    def dhb_income_calculator(self, user_name, password, product_name, amount):
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name, prd_tag=2)
        self.main_page.income_calculator(amount)
        self.main_page.verify_page_title()

    # 定活宝收益计算器金额少于起投金额
    def dhb_income_calculator_less_than_start_amount(self, user_name, password, product_name, amount):
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name, prd_tag=2)
        self.main_page.income_calculator(amount)
        self.main_page.verify_page_title()

    # 定活宝收益计算器金额大于最大认购金额
    def dhb_income_calculator_greater_than_max_amount(self, user_name, password, product_name, amount):
        max_amount = self._db.get_product_info(product_name=product_name)[0]['max_subscribe_amount']
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name, prd_tag=2)
        self.main_page.income_calculator(amount, max_amount=max_amount)
        self.main_page.verify_page_title()

    # 高端收益计算器
    def vip_income_calculator(self, user_name, password, product_name, amount):
        min_amount = self._db.get_product_info(product_name=product_name)[0]['min_buy_amount']
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name, prd_tag=2)
        self.main_page.income_calculator(amount=amount, product_type=3, min_amount=min_amount)
        self.main_page.verify_page_title()

    # 高端收益计算器少于起投金额
    def vip_income_calculator_less_than_start_amount(self, user_name, password, product_name, amount):
        min_amount = self._db.get_product_info(product_name=product_name)[0]['min_buy_amount']
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name, prd_tag=2)
        self.main_page.income_calculator(amount=amount, product_type=3, min_amount=min_amount)
        self.main_page.verify_page_title()

    # 高端收益计算器大于最大购买金额
    def vip_income_calculator_greater_than_max_amount(self, user_name, password, product_name, amount):
        product_info = self._db.get_product_info(product_name=product_name)[0]
        min_amount = product_info['min_buy_amount']
        max_amount = product_info['max_buy_amount']
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name, prd_tag=2)
        self.main_page.income_calculator(amount=amount, product_type=3, min_amount=min_amount, max_amount=max_amount)
        self.main_page.verify_page_title()

    # 定投排行
    def view_fund_plan_rankings(self):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_invest_ranking_page()
        self.main_page.verify_at_fund_invest_ranking_page()
        self.main_page.click_different_fund_type()
        self.main_page.verify_at_fund_invest_ranking_page()
        self.main_page.go_to_fund_details_page()
        self.main_page.verify_page_title(product_type=2)
        self.main_page.back_to_previous_page(return_page='FundInvestRankingPage')
        self.main_page.verify_at_fund_invest_ranking_page()

    # 查看非货币性基金详情信息(基金频道页面进)
    def view_non_monetary_fund_info(self, fund_product_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.fund_search(product_name=fund_product_name)
        self.main_page.fund_details_info(fund_type=2)
        self.main_page.go_to_history_nav()
        self.main_page.verify_at_fund_nav_page(title=fund_product_name)
        self.main_page.non_monetary_fund_history_nav_page()
        self.main_page.switch_to_dividends_split()
        self.main_page.verify_at_fund_nav_page(title=fund_product_name)

    # 查看货币性基金详情信息(基金频道页面进)
    def view_monetary_fund_info(self, fund_product_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.fund_search(product_name=str(fund_product_name).split('(')[0])
        self.main_page.fund_details_info(fund_type=1)

    # 查看货币性基金的七日年化收益和万份收益
    def view_monetary_fund_annual_rate(self, fund_product_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.fund_search(product_name=str(fund_product_name).split('(')[0])
        self.main_page.view_monetary_fund_annual_rate_info_by_clicking_more()
        self.main_page.verify_at_fund_annual_rate_page(str(fund_product_name).split('(')[0])
        self.main_page.back_to_previous_page()
        self.main_page.view_monetary_fund_annual_rate_info_by_clicking_view_history()
        self.main_page.verify_at_fund_annual_rate_page(str(fund_product_name).split('(')[0])
        self.main_page.back_to_previous_page()
        self.main_page.go_to_history_nav()
        self.main_page.verify_at_monetary_fund_history_nav_page(str(fund_product_name).split('(')[0])

    # 查看现金管理系列产品详情
    def view_cash_management_high_end_info(self, product_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name, prd_tag=2)
        self.main_page.high_end_product_details(vip_type=1)

    # 查看固定收益系列产品详情
    def view_fixed_rated_high_end_info(self, product_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name, prd_tag=2)
        self.main_page.high_end_product_details(vip_type=2)

    # 查看精选收益系列产品详情
    def view_best_recommend_high_end_info(self, product_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name, prd_tag=2)
        self.main_page.high_end_product_details(vip_type=3)

    # 查看精选收益产品的历史净值
    def view_high_end_history_nav(self, product_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name, prd_tag=2)
        self.main_page.go_to_history_nav()
        self.main_page.high_end_history_nav_page()

    # 查看现金管理系列产品的历史收益
    def view_cash_management_high_end_annual_rate(self, product_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name, prd_tag=2)
        self.main_page.view_monetary_fund_annual_rate_info_by_clicking_more()
        self.main_page.verify_at_vip_history_income()
        self.main_page.back_to_previous_page()
        self.main_page.view_monetary_fund_annual_rate_info_by_clicking_view_history()
        self.main_page.verify_at_vip_history_income()
        self.main_page.back_to_previous_page()
        self.main_page.go_to_history_nav()
        self.main_page.verify_at_vip_history_income()

    # 福利中心去推荐
    def welfare_center_invite_friend(self, user_name, password):
        self.old_user(user_name, password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_welfare_center()
        self.main_page.experience_immediately()
        self.main_page.verify_at_welfare_center_page_title()
        self.main_page.recommend()
        self.main_page.verify_at_invite_friend_page()

    # 福利中心去分享
    def welfare_center_go_to_share(self, user_name, password):
        self.old_user(user_name, password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_welfare_center()
        self.main_page.experience_immediately()
        self.main_page.verify_at_welfare_center_page_title()
        self.main_page.share()

    # 福利中心去关注
    def welfare_center_go_to_focus(self, user_name, password):
        self.old_user(user_name, password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_welfare_center()
        self.main_page.experience_immediately()
        self.main_page.verify_at_welfare_center_page_title()
        self.main_page.focus()

    # 福利中心去点赞
    def welfare_center_go_to_good(self, user_name, password):
        self.old_user(user_name, password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_welfare_center()
        self.main_page.experience_immediately()
        self.main_page.verify_at_welfare_center_page_title()
        self.main_page.bind()

    # 福利中心查看积分明细
    def welfare_center_points_details(self, user_name, password):
        self.old_user(user_name, password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_welfare_center()
        self.main_page.experience_immediately()
        self.main_page.go_to_my_points()
        self.main_page.verify_at_details_page_title()
        self.main_page.verify_points_details()
        self.main_page.back_to_previous_page(return_page='WelfareCenterPage')
        self.main_page.go_to_my_points_description_page()
        self.main_page.verify_points_details()

    # 福利中心查看元宝明细
    def welfare_center_yb_details(self, user_name, password):
        self.old_user(user_name, password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_welfare_center()
        self.main_page.experience_immediately()
        self.main_page.go_to_my_yb()
        self.main_page.verify_at_details_page_title()
        self.main_page.verify_yb_details()
        self.main_page.back_to_previous_page(return_page='WelfareCenterPage')
        self.main_page.go_to_my_yb_description_page()
        self.main_page.verify_yb_details()

    # 福利中心签到
    def welfare_center_check_in(self, user_name, password):
        self.old_user(user_name, password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_welfare_center()
        self.main_page.experience_immediately()
        self.main_page.check_in()

    # 福利中心限时特惠
    def welfare_center_timed_discount(self, user_name, password):
        self.old_user(user_name, password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_welfare_center()
        self.main_page.experience_immediately()
        self.main_page.discount_more()

    # 福利中心边逛边兑-优惠券
    def welfare_center_exchange_coupon(self, user_name, password):
        self.old_user(user_name, password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_welfare_center()
        self.main_page.experience_immediately()
        self.main_page.exchange_coupon()
        self.main_page.exchange_immediately()
        self.main_page.verify_coupon_description('兑换-满800减8')
        self.main_page.go_back_to_welfare_center_page()
        actual_yb = self.main_page.get_text("//UIAStaticText[@label='我的元宝']/following-sibling::UIAStaticText")
        actual_points = self.main_page.get_text("//UIAStaticText[@label='我的积分']/following-sibling::UIAStaticText")
        expected_yb = decimal.Decimal(ASSERT_DICT['yb']).quantize(decimal.Decimal('0.00')) - decimal.Decimal('6.00')
        expected_points = decimal.Decimal(ASSERT_DICT['points']).quantize(decimal.Decimal('0.00')) - decimal.Decimal(
            '3.00')
        self.main_page.assert_values(actual_yb, str(expected_yb), '==')
        self.main_page.assert_values(actual_points, str(expected_points), '==')

    # 查看基金历史持仓
    def view_fund_history_holding(self, user_name, password, fund_product_name):
        self.old_user(user_name=user_name, login_password=password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_history_detail_page(fund_product_name)
        self.main_page.verify_history_fund_holding_detail(fund_product_name)
        self.main_page.view_monetary_fund_annual_rate_info_by_clicking_more()
        self.main_page.verify_at_fund_annual_rate_page(fund_product_name)

    # 查看定活宝历史持仓
    def view_dhb_history_holding(self, user_name, login_password, product_name, name, risk_type):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.login(user_name=user_name, password=login_password, return_page='PersonalSettingPage',
                             flag='setting_page_login')
        self.main_page.verify_setting_page_details(name=name, risk_type=risk_type)
        self.main_page.back_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.go_to_dhb_history_holding_list_page()
        self.main_page.verify_dhb_history_holding_detail(product_name=product_name)
        self.main_page.go_to_history_holding_page(product_name=product_name)
        self.main_page.verify_page_title(product_name=product_name)
        self.main_page.verify_history_holding_page_details(product_type='dhb')

    # 查看高端历史持仓
    def view_high_end_history_holding(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_vip_history_detail_page(product_name)
        self.main_page.verify_history_vip_holding_detail(product_name)
        self.main_page.view_monetary_fund_annual_rate_info_by_clicking_more()
        self.main_page.verify_at_vip_history_income()

    # 基金分红方式切换
    def fund_dividend_type_switch(self, user_name, login_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_confirmed_fund_holding_detail_page(product_name=fund_product_name)
        self.main_page.fund_dividend_type_switch(dividend_type='红利再投')
        self.main_page.fund_dividend_type_switch(dividend_type='现金分红')

    # 基金极速转换
    def fund_fast_convert(self, user_name, login_password, fund_convert_from, fund_convert_to, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_confirmed_fund_holding_detail_page(product_name=fund_convert_from)
        self.main_page.go_to_select_convert_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=str(fund_convert_to).split('(')[0],
                                            operation_type='fund_convert', mobile=user_name)
        self.main_page.verify_at_fund_convert_page()
        self.main_page.verify_fund_convert_details(fund_convert_from=str(fund_convert_from).split('(')[0],
                                                   fund_convert_to=str(fund_convert_to).split('(')[0])
        self.main_page.fund_convert(amount=amount, trade_password=trade_password)
        self.main_page.confirm_trade(return_page='FundHoldingDetailPage')
        # self.main_page.cancel_search(return_page='SelectConvertToFundPage')
        # self.main_page.back_to_fund_holding_page()
        self.main_page.verify_at_fund_holding_detail_page(product_name=fund_convert_from)
        # self.main_page.verify_available_amount()
        self.main_page.go_to_trade_records_page()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_at_trade_record_detail_page()
        self.main_page.verify_trade_record_info(product_name=str(fund_convert_to).split('(')[0], trade_type='极速转换',
                                                status='已受理', amount=amount, product_type='2')

    # 基金极速转换撤单
    def cancel_fund_fast_convert_order(self, user_name, login_password, fund_convert_from, fund_convert_to,
                                       trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_confirmed_fund_holding_detail_page(product_name=fund_convert_from)
        self.main_page.go_to_trade_records_page()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_at_trade_record_detail_page()
        self.main_page.cancel_order(trade_password=trade_password)
        self.main_page.confirm_trade(return_page='AssetsFundDetailPage')
        self.main_page.verify_at_fund_holding_list_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_at_trade_detail_page()
        self.main_page.go_to_trade_record_detail_page()
        self.main_page.verify_trade_record_info(product_name=str(fund_convert_to).split('(')[0], trade_type='极速转换',
                                                status='已撤销',
                                                product_type='2')

    # 理财型基金到期处理方式切换(全部赎回至现金宝切换为部分赎回至现金宝)
    def financial_fund_expiry_processing_all_to_part(self, user_name, login_password, fund_product_name,
                                                     fund_product_code, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self._db.update_cts_prod_renew(user_name=user_name, fund_id=fund_product_code, value_date='20170908',
                                       due_process_type='AR', red_amt='1000000.00')
        self.main_page.go_to_fund_redeem_page(fund_product=fund_product_name)
        self.main_page.verify_expiry_processing_type_details(processing_type='全部赎回至现金宝', expiry_date='12月29日')
        self.main_page.go_to_expiry_processing_type_page(processing_type='全部赎回至现金宝')
        self.main_page.verify_page_title()
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='全部赎回至现金宝',
                                                        expiry_dispose_amount='1,000,000.00')
        self.main_page.financial_fund_expiry_processing_type_switch(switch_to='部分赎回至现金宝', expiry_redeem_amount='1000',
                                                                    trade_password=trade_password)
        self.main_page.verify_page_title(fund_product=fund_product_name)
        self.main_page.verify_expiry_processing_type_details(processing_type='部分赎回至现金宝', expiry_date='12月29日')

    # 理财型基金到期处理方式切换(部分赎回至现金宝切换为自动续存)
    def financial_fund_expiry_processing_part_to_automatic(self, user_name, login_password, fund_product_name,
                                                           fund_product_code, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self._db.update_cts_prod_renew(user_name=user_name, fund_id=fund_product_code, value_date='20170908',
                                       due_process_type='AR', red_amt='1,000.00')
        self.main_page.go_to_fund_redeem_page(fund_product=fund_product_name)
        self.main_page.verify_expiry_processing_type_details(processing_type='部分赎回至现金宝', expiry_date='12月29日')
        self.main_page.go_to_expiry_processing_type_page(processing_type='部分赎回至现金宝')
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='部分赎回至现金宝',
                                                        expiry_dispose_amount='1,000.00')
        self.main_page.financial_fund_expiry_processing_type_switch(switch_to='自动续存', trade_password=trade_password)
        self.main_page.verify_expiry_processing_type_details(processing_type='自动续存', expiry_date='12月29日')

    # 理财型基金到期处理方式切换(自动续存转全部赎回至现金宝)
    def financial_fund_expiry_processing_automatic_to_all(self, user_name, login_password, fund_product_name,
                                                          fund_product_code, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self._db.update_cts_prod_renew(user_name=user_name, fund_id=fund_product_code, value_date='20170908',
                                       due_process_type='AO', red_amt='0.00')
        self.main_page.go_to_fund_redeem_page(fund_product=fund_product_name)
        self.main_page.verify_expiry_processing_type_details(processing_type='自动续存', expiry_date='12月29日')
        self.main_page.go_to_expiry_processing_type_page(processing_type='自动续存')
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='自动续存')
        self.main_page.financial_fund_expiry_processing_type_switch(switch_to='全部赎回至现金宝', trade_password=trade_password)
        self.main_page.verify_expiry_processing_type_details(processing_type='全部赎回至现金宝', expiry_date='12月29日')

    # 设置-修改个人信息
    def modify_personal_information(self, user_name, login_password, email, address):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_information_page()
        self.main_page.modify_personal_photo()
        self.main_page.go_to_email_page()
        self.main_page.modify_email_address(email=email)
        self.main_page.go_to_address_page()
        self.main_page.modify_residential_address(address=address)
        self.main_page.verify_personal_information_details(email=email, address=u'北京市密云县test')

    # 首次绑卡上传已有身份证图片，提示该身份信息已注册。
    def bind_card_upload_id_info_negative(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_bank_card_management_page()
        self.main_page.click_bind_card(trade_password=trade_password, real_named=0)
        self.main_page.upload_id_card()
        self.main_page.verify_at_upload_id_card_page()

    # 删除历史定投
    def delete_fund_history_plan(self, user_name, login_password, fund_product_name, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.go_to_fund_history_plan_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_plan_detail_page(fund_product_name=fund_product_name,
                                                   fund_product_code=fund_product_code)
        self.main_page.verify_page_title()
        self.main_page.delete_fund_history_plan()
        self.main_page.verify_page_title()

    # 实名用户没有绑定的储蓄卡，点击进入信用卡页面。
    def click_credit_card_without_bank_card_certificated_user(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.go_to_bind_bank_card_page()
        self.main_page.verify_at_binding_card_page()

    # 热门页查看全部产品
    def view_all_products(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_all_products_page()
        self.main_page.verify_at_all_products_page()
        self.main_page.view_all_products()

    # 理财频道全部产品--筛选器
    def all_products_filter(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_all_products_page()
        self.main_page.go_to_filter_detail_page()
        self.main_page.verify_filter_details()
        self.main_page.products_filter()
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(amount_type='1分-5万')
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(amount_type='5-100万')
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(amount_type='100万以上')
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(product_type='定活宝')
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(product_type='高端现金管理')
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(product_type='高端固定收益')
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(product_type='高端精选权益')
        self.main_page.verify_at_all_products_page()

    # 基金主题
    def view_fund_topics(self):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_topics_page()
        self.main_page.switch_tabs()
        self.main_page.verify_at_fund_topic_page()

    # 基金估值排行
    def view_fund_estimated_value_ranking(self):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_estimated_value_ranking_page()
        self.main_page.switch_tabs()
        self.main_page.verify_at_fund_estimated_value_ranking_page()

    # 高端报价式产品修改到期处理方式(全部退出切换为部分退出)(产品处于续约日期前5个工作日,持有列表页面进)
    def high_end_quotation_product_expiry_processing_all_to_part(self, user_name, login_password, trade_password,
                                                                 product_code):
        # date = str(Utility.DateUtil().getToday()).replace('-', '')
        # new_work_date = self._db.judge_is_work_date(day=date)
        # self._db.modify_expire_date(user_name=user_name, product_id=product_code, value_date='20170908',
        #                             expired_date=new_work_date)
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        # self._db.update_cts_prod_renew(user_name=user_name, fund_id=product_code, value_date='20170908',
        #                                due_process_type='AR', red_amt='1000000.00')
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.verify_page_title()
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='到期退出', product_type='vip')
        self.main_page.product_expiry_processing_type_switch(switch_to='部分退出', trade_password=trade_password,
                                                             product_type='vip', expiry_redeem_amount='10,000.00',
                                                             return_page='AssetsHighEndDetailPage')
        self.main_page.verify_at_high_end_holding_list_page()
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='到期退出', expiry_dispose_amount='10,000.00',
                                                        product_type='vip')

    # 高端报价式产品修改到期处理方式(部分退出切换为自动续存)(持有列表页面进)
    def high_end_quotation_product_expiry_processing_part_to_auto(self, user_name, login_password, trade_password,
                                                                  product_code):
        date = str(Utility.DateUtil().getToday()).replace('-', '')
        # new_work_date = self._db.judge_is_work_date(day=date)
        # self._db.modify_expire_date(user_name=user_name, product_id=product_code, value_date='20170908',
        #                             expired_date=new_work_date)
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        # self._db.update_cts_prod_renew(user_name=user_name, fund_id=product_code, value_date='20170908',
        #                                due_process_type='AR', red_amt='10000.00')
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.product_expiry_processing_type_switch(switch_to='自动续存', trade_password=trade_password,
                                                             product_type='vip', return_page='AssetsHighEndDetailPage')
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='自动续存', product_type='vip')

    # 高端报价式产品修改到期处理方式(自动续存切换为全部退出)(持有列表页面进)
    def high_end_quotation_product_expiry_processing_auto_to_all(self, user_name, login_password, trade_password,
                                                                 product_code):
        # date = str(Utility.DateUtil().getToday()).replace('-', '')
        # new_work_date = self._db.judge_is_work_date(day=date)
        # self._db.modify_expire_date(user_name=user_name, product_id=product_code, value_date='20170908',
        #                             expired_date=new_work_date)
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        # self._db.update_cts_prod_renew(user_name=user_name, fund_id=product_code, value_date='20170908',
        #                                due_process_type='AO', red_amt='0.00')
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.product_expiry_processing_type_switch(switch_to='全部退出', trade_password=trade_password,
                                                             expiry_redeem_amount='1,000,000.00',
                                                             product_type='vip', return_page='AssetsHighEndDetailPage')
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='到期退出',
                                                        expiry_dispose_amount='1,000,000.00',
                                                        product_type='vip')

    # 税收居民身份证明
    def tax_dweller_identity_declaration(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_account_info_page()
        self.main_page.go_to_identity_declaration_page()
        self.main_page.verify_page_title()
        self.main_page.select_tax_dweller_identity(identity='既为中国税收居民又是其他国家（地区）税收居民')
        self.main_page.verify_tax_dweller_identity_result()
        self.main_page.select_tax_dweller_identity(identity='仅为非居民')
        self.main_page.verify_tax_dweller_identity_result()
        self.main_page.select_tax_dweller_identity(identity='仅为中国税收居民')

    # 最佳表现基金和最高成交量
    def best_performance_highest_turnovers_fund(self):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_best_performance_page()
        self.main_page.view_best_performance_funds()
        self.main_page.view_highest_turnovers()

    # 更改登陆方式
    def change_sms_login_method(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_security_center_page()
        self.main_page.change_login_method(flag=0)
        self.main_page.back_to_settings_page()
        self.main_page.logout_app()
        self.main_page.go_to_login_page_()
        self.main_page.login_use_verification_code(user_name=user_name, can_login=False)
        self.main_page.login(user_name, login_password, 'HomePage')
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_security_center_page()
        self.main_page.change_login_method(trade_password=trade_password, flag=1)
        self.main_page.back_to_settings_page()
        self.main_page.logout_app()
        self.main_page.go_to_login_page_()
        self.main_page.login_use_verification_code(user_name=user_name)

    # 查看会员中心
    def view_member_center(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_member_center_page()
        self.main_page.click_different_member_level()
        self.main_page.go_to_description_page()

    # 安全中心查看登录记录
    def security_center_view_login_record(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_security_center_page()
        self.main_page.go_to_login_record_page()
        self.main_page.verify_page_title()
        self.main_page.view_login_records()

    # 查看新发基金
    def view_newly_raised_funds(self, product_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_newly_raised_funds_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_newly_raised_fund_details(product_name=product_name)
        self.main_page.go_to_fund_detail_page(product_name=product_name)
        self.main_page.verify_at_fund_detail_page()
        self.main_page.view_newly_raised_fund_details()

    # 查看未实名用户账户信息
    def view_user_account_information(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_account_info_page()
        self.main_page.view_user_account_information(title='姓名', content='未实名', type='uncertificated')
        self.main_page.view_user_account_information(title='证件类型', content='未实名', type='uncertificated')
        self.main_page.view_user_account_information(title='证件号码', content='未实名', type='uncertificated')
        self.main_page.view_user_account_information(title='资金账户', content='未绑定', type='uncertificated')
        self.main_page.view_user_account_information(title='风险测评', content='未测评', type='uncertificated')
        self.main_page.view_user_account_information(title='税收居民身份声明', content='待填写', type='uncertificated')

    # 修改手机号码(不能接收短信)
    def modify_mobile_without_sms(self, user_name, login_password, trade_password, mobile_new):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_setting_modify_mobile_page()
        self.main_page.modify_mobile_without_sms(trade_password=trade_password, mobile_new=mobile_new)
        self.main_page.verify_at_personal_setting_page()


if __name__ == '__main__':
    try:
        phone_number = Utility.GetData().mobile()
        mobile_new = phone_number
        print 'mobile_new: ' + mobile_new
        print 'phone_number: ' + phone_number
        user_name = Utility.GetData().english_name()
        id_no = Utility.GetData().id_no()
        bank_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]
        bank_card_no_nan_yue = Utility.GetData().bank_card_no(card_bin='623595').split('-')[0]
        # user_new, login_password, trade_password, card_no = RestfulXjbTools().new_user(user_name=phone_number,
        #                                                                                login_password='a0000000',
        #                                                                                card_bin='456351',
        #                                                                                trade_password='135790',
        #                                                                                recharge_amount='10000')

        # app_path = GlobalController.XJB_CONNECT
        # app_path = GlobalConfig.XjbApp.Xjb_App_2_0_IOS_UAT
        # bank_card_no = '6222022718057180939'
        user_new = '13578041829'
        # user_new = '15384087067'
        login_password = 'a0000000'
        # login_password = 'a1111111'
        trade_password = '135790'
        print 'user_new: %s' % user_new
        app_path = '/Users/wanglili/xjb/build/HXXjb.xcarchive/Products/Applications/HXXjb.app'
        # app_path = '/Users/linkinpark/xjb/build/DerivedData/Build/Products/Debug-iphoneos/HXXjb.app'
        platform_version = '9.3'
        device_id = '56a36d750ab8d2c6e5b73365099bdbf7bc05d9d2'
        # device_id = 'a2c995b55b69e2059b475e2c9b8ddc6f2811a0d0'
        # package_name = 'com.shhxzq.xjb'
        port = '4723'
        package_name = 'com.shhxzq.xjbEnt'
        # package_name = 'com.shhxzq.xjbDev'
        m = IOSXjbTools30(app_path='', platform_version=platform_version, device_id=device_id, port=port,
                          package_name=package_name, app_status='N', os='IOS')
        # user = GlobalConfig.XjbAccountInfo.XJB_CI_USER_1
        user = GlobalConfig.XjbAccountInfo.XJB_UAT_USER_1
        # user = GlobalConfig.XjbAccountInfo.XJB_UAT_USER_2

        # m.home_page_recharge(user_name=user['u1']['user_name'],
        #                      login_password=user['u1']['login_password'],
        #                      recharge_amount='10',
        #                      trade_password=user['u1']['trade_password'],
        #                      non_superposed_coupon_quantity=user['u1']['non_superposed_coupon_quantity'],
        #                      non_superposed_coupon=user['u1']['non_superposed_coupon_code']
        #                      )

        # m.home_page_regular_withdraw(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              withdraw_amount='0.1',
        #                              trade_password=user['u1']['trade_password'])

        # m.home_page_fast_withdraw_negative(user_name=user['u1']['user_name'],
        #                                    login_password=user['u1']['login_password'],
        #                                    withdraw_amount='100000000000000000',
        #                                    trade_password=user['u1']['trade_password'])

        # m.home_page_regular_withdraw_negative(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password'],
        #                                       withdraw_amount='0',
        #                                       trade_password=user['u1']['trade_password'])

        # m.home_page_fast_withdraw(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           withdraw_amount='0.1',
        #                           trade_password=user['u1']['trade_password'])

        # m.home_page_view_essence_recommend_list(user_name=user['u1']['user_name'],
        #                                         login_password=user['u1']['login_password'])

        # m.register(phone_number=phone_number, login_password='a0000000')

        # m.register_binding_card(phone_number=phone_number, login_password='a0000000', trade_password='135790',
        #                         user_name=user_name, id_no=id_no, bank_card_no=str(bank_card_no))

        # m.bank_card_manage_binding_card(user_name=user_new,
        #                                 login_password=login_password,
        #                                 bank_card_no=bank_card_no,
        #                                 phone_number=user_new)

        # m.bank_card_manage_binding_nan_yue_card(user_name=user_new,
        #                                         login_password=login_password,
        #                                         bank_card_no=bank_card_no_nan_yue,
        #                                         phone_number=user_new)

        # m.delete_bank_card(user_name=user_new,
        #                    login_password=login_password,
        #                    trade_password=trade_password)

        # m.security_center_modify_mobile(user_name=user_new,
        #                                 login_password=login_password,
        #                                 trade_password=trade_password,
        #                                 mobile_new=mobile_new)

        # m.security_center_modify_trade_password(user_name=user_new,
        #                                         login_password=login_password,
        #                                         trade_password_old=trade_password,
        #                                         trade_password_new='147258')

        # m.security_center_modify_login_password(user_name=user_new,
        #                                         login_password=login_password,
        #                                         login_password_new='a1111111')

        # m.security_center_find_trade_password(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password'])

        # # 使用现金宝购买高端
        # m.buy_high_end_product(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'],
        #                        trade_password=user['u1']['trade_password'],
        #                        product_name=user['u1']['high_end_product'],
        #                        amount=user['u1']['high_end_product_amount'])

        # # 使用现金宝购买定期
        # m.buy_dqb_product(user_name=user['u1']['user_name'],
        #                   login_password=user['u1']['login_password'],
        #                   product_name=user['u1']['dqb_product'],
        #                   amount=user['u1']['dqb_product_amount'],
        #                   trade_password=user['u1']['trade_password'])

        # m.hot_switch_to_dqb_product_list_page(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password'])

        # m.hot_switch_to_high_end_product_list_page(user_name=user['u1']['user_name'],
        #                                            login_password=user['u1']['login_password'])

        # m.finance_product_search_with_full_name_at_home_page(user_name=user['u1']['user_name'],
        #                                                      login_password=user['u1']['login_password'],
        #                                                      product_name=user['u1']['search_with_full_name'])
        # m.finance_product_search_with_short_name_at_home_page(user_name=user['u1']['user_name'],
        #                                                       login_password=user['u1']['login_password'],
        #                                                       product_name=user['u1']['search_with_short_name'])

        # m.assets_xjb_detail_page_recharge(user_name=user['u1']['user_name'],
        #                                   login_password=user['u1']['login_password'],
        #                                   recharge_amount='100',
        #                                   trade_password=user['u1']['trade_password'])

        # m.assets_xjb_detail_page_regular_withdraw(user_name=user['u1']['user_name'],
        #                                           login_password=user['u1']['login_password'],
        #                                           withdraw_amount='0.1',
        #                                           trade_password=user['u1']['trade_password'])

        m.assets_xjb_detail_page_fast_withdraw(user_name=user['u1']['user_name'],
                                               login_password=user['u1']['login_password'],
                                               withdraw_amount='0.1',
                                               trade_password=user['u1']['trade_password'])

        # m.add_credit_card(user_name=user['u1']['user_name'],
        #                   login_password=user['u1']['login_password'],
        #                   credit_card_no=user['u1']['credit_card_no'])

        # m.delete_credit_card(user_name=user['u1']['user_name'],
        #                      login_password=user['u1']['login_password'],
        #                      last_card_no=user['u1']['last_card_no'],
        #                      trade_password=user['u1']['trade_password'])

        #
        # m.view_message(user_name=user['u1']['user_name'],
        #                login_password=user['u1']['login_password'])

        # m.view_xjb_trade_detail(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'])

        # m.dqb_detail_page_view_trade_detail(user_name=user['u1']['user_name'],
        #                                     login_password=user['u1']['login_password'])

        # m.view_dqb_more_product(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'])

        # m.view_dqb_history_product(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'])

        # m.fund_detail_page_view_trade_detail(user_name=user['u1']['user_name'],
        #                                      login_password=user['u1']['login_password'])

        # m.view_fund_more_product(user_name=user['u1']['user_name'],
        #                          login_password=user['u1']['login_password'])

        # m.high_end_detail_page_view_trade_detail(user_name=user['u1']['user_name'],
        #                                          login_password=user['u1']['login_password'])
        #
        # m.view_high_end_more_product(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'])
        # m.view_high_end_cash_management_series(user_name=user['u1']['user_name'],
        #                                        login_password=user['u1']['login_password'])

        # m.view_high_end_best_recommend_series(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password']
        #                                       )

        # m.view_high_end_fixed_rate_series(user_name=user['u1']['user_name'],
        #                                   login_password=user['u1']['login_password']
        #                                   )
        #
        # m.redeem_high_end_product(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           redeem_amount=user['u1']['high_end_product_amount'],
        #                           trade_password=user['u1']['trade_password'],
        #                           high_end_product=user['u1']['high_end_product'])
        #
        # m.redeem_high_end_product_max(user_name=user['u1']['user_name'],
        #                               login_password=user['u1']['login_password'],
        #                               redeem_amount='999999999999',
        #                               trade_password=user['u1']['trade_password'],
        #                               high_end_product=user['u1']['high_end_product'])

        # m.redeem_high_end_product_min(user_name=user['u1']['user_name'],
        #                               login_password=user['u1']['login_password'],
        #                               redeem_amount='0',
        #                               trade_password=user['u1']['trade_password'],
        #                               high_end_product=user['u1']['high_end_product'])

        # m.redeem_dqb_product(user_name=user['u1']['user_for_redeem_dqb'],
        #                      login_password='qq789123',
        #                      redeem_amount=user['u1']['dqb_product_amount_2'],
        #                      trade_password='121212',
        #                      dqb_product=user['u1']['dqb_product_2'])

        # m.redeem_dqb_product_max(user_name=user['u1']['user_for_redeem_dqb'],
        #                          login_password='qq789123',
        #                          redeem_amount='999999999999',
        #                          trade_password=user['u1']['trade_password'],
        #                          dqb_product=user['u1']['dqb_product_2'])

        # m.redeem_dqb_product_min(user_name=user['u1']['user_for_redeem_dqb'],
        #                          login_password='qq789123',
        #                          redeem_amount='0',
        #                          trade_password='121212',
        #                          dqb_product=user['u1']['dqb_product_2'])

        # m.my_referee(user_name=user['u1']['user_name'],
        #              login_password=user['u1']['login_password'],
        #              phone_no=user['u2']['user_name'])
        #

        # m.risk_evaluating_new_user(user_name=user_new,
        #                            login_password=login_password)

        #
        # m.fund_non_money_product_search_with_name(user_name=user['u1']['user_name'],
        #                                           login_password=user['u1']['login_password'],
        #                                           product_name=user['u1']['fund_product_name'])

        # m.fund_money_product_search_with_code(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password'],
        #                                       product_name=user['u1']['fund_product_code'])

        # m.buy_fund_product(user_name=user['u1']['user_name'],
        #                    login_password=user['u1']['login_password'],
        #                    fund_product_name=user['u1']['fund_product_name'],
        #                    amount=user['u1']['fund_product_amount'],
        #                    trade_password=user['u1']['trade_password'],
        #                    fund_product_code=user['u1']['non_money_fund_product_code'])

        # m.invite_friend(user_name=user['u1']['user_name'],
        #                 login_password=user['u1']['login_password'])

        # # 用户本身有绑定的预约码 - 直接使用其他预约码
        # m.use_other_reservation_code(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              reservation_code=user['u1']['reserve_code'],
        #                              trade_password=user['u1']['trade_password'],
        #                              buy_quota=user['u1']['reservation_code_buy_quota'],
        #                              buy_count=user['u1']['reservation_code_buy_count'],
        #                              reserve_quota=user['u1']['reservation_code_reserve_quota'],
        #                              reserve_count=user['u1']['reservation_code_reserve_count'],
        #                              product_id=user['u1']['product_id_for_reservation_code']
        #                              )

        # # 预约码--用户没有绑定预约码, 使用其他预约码
        # m.use_other_reservation_code_without_reservation_code(user_name=user['u1']['user_name_for_reservation_code'],
        #                                                       login_password=user['u1'][
        #                                                           'login_password_for_reservation_code'],
        #                                                       reservation_code=user['u1']['reserve_code'],
        #                                                       trade_password=user['u1'][
        #                                                           'trade_password_for_reservation_code'],
        #                                                       buy_quota=user['u1']['reservation_code_buy_quota'],
        #                                                       buy_count=user['u1']['reservation_code_buy_count'],
        #                                                       reserve_quota=user['u1'][
        #                                                           'reservation_code_reserve_quota'],
        #                                                       reserve_count=user['u1'][
        #                                                           'reservation_code_reserve_count'],
        #                                                       product_id=user['u1']['product_id_for_reservation_code'],
        #                                                       user_name_have_reservation_code=user['u1']['user_name'],
        #                                                       )

        # # 预约码--使用自己的预约码
        # m.use_reservation_code(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'],
        #                        trade_password=user['u1']['trade_password'],
        #                        buy_quota=user['u1']['reservation_code_buy_quota'],
        #                        buy_count=user['u1']['reservation_code_buy_count'],
        #                        reserve_quota=user['u1']['reservation_code_reserve_quota'],
        #                        reserve_count=user['u1']['reservation_code_reserve_count'],
        #                        reservation_code=user['u1']['reserve_code'],
        #                        product_id=user['u1']['product_id_for_reservation_code']
        #                        )

        # m.redeem_fund_product(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       amount=user['u1']['fund_product_amount'],
        #                       trade_password=user['u1']['trade_password'],
        #                       fund_product_name_for_redeem=user['u1']['fund_product_name_for_redeem'], )

        # m.redeem_fund_product_max(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           amount='999999999999',
        #                           trade_password=user['u1']['trade_password'],
        #                           fund_product_name_for_redeem=user['u1']['fund_product_name_for_redeem'], )

        # m.redeem_fund_product_min(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           amount='0',
        #                           trade_password=user['u1']['trade_password'],
        #                           fund_product_name_for_redeem=user['u1']['fund_product_name_for_redeem'], )

        # m.earn_points(user_name=user['u1']['user_name'],
        #               login_password=user['u1']['login_password'],
        #               amount=user['u1']['fund_product_amount'],
        #               trade_password=user['u1']['trade_password'],
        #               fund_product_name=user['u1']['fund_product_name'],
        #               fund_product_code=user['u1']['non_money_fund_product_code'],
        #               )

        # # 信用卡还款
        # m.credit_card_repay(user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'],
        #                     repay_amount=user['u1']['credit_card_repay_amount'],
        #                     trade_password=user['u1']['trade_password'])

        # # 信用卡预约还款
        # m.credit_card_reserved_pay(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            reserved_pay_amount=user['u1']['credit_card_reserved_pay_amount'],
        #                            trade_password=user['u1']['trade_password'],
        #                            user_credit_card_id=user['u1']['user_credit_card_id'])

        # # 取消预约还款
        # m.cancel_reserved_pay(user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       user_credit_card_id=user['u1']['user_credit_card_id'])

        # # 赚积分--推荐用户注册绑卡
        # m.earn_points_by_recommend_user_register(user['u1']['user_name'],
        #                                          login_password=user['u1']['login_password'])

        # # 花积分--买定期宝
        # m.spend_points_by_buy_dqb(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           amount=user['u1']['dqb_product_amount'],
        #                           trade_password=user['u1']['trade_password'],
        #                           dqb_product_name=user['u1']['dqb_product'], )

        # # 花积分--买基金
        # m.spend_points_by_buy_fund(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            amount=user['u1']['fund_product_amount'],
        #                            trade_password=user['u1']['trade_password'],
        #                            fund_product_name=user['u1']['fund_product_name'],
        #                            fund_product_code=user['u1']['non_money_fund_product_code'],
        #                            )

        # # 花积分--买高端产品
        # m.spend_points_by_buy_vipproduct_use_product_name(user_name=user['u1']['user_name'],
        #                                                   login_password=user['u1']['login_password'],
        #                                                   amount=user['u1']['high_end_product_amount'],
        #                                                   trade_password=user['u1']['trade_password'],
        #                                                   product_name=user['u1']['high_end_product_for_points_offset'],
        #                                                   )

        # # 添加还款提醒
        # m.add_credit_card_repayment_warn(user_name=user['u1']['user_name'],
        #                                  login_password=user['u1']['login_password']
        #                                  )

        # # 取消还款提醒
        # m.cancel_credit_card_repayment_warn(user_name=user['u1']['user_name'],
        #                                  login_password=user['u1']['login_password']
        #                                  )

        # # 高端普通卖出
        # m.normal_redeem_vipproduct(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            redeem_amount=user['u1']['high_end_product_amount'],
        #                            trade_password=user['u1']['trade_password'],
        #                            high_end_product_for_fast_redeem=user['u1']['high_end_product_for_fast_redeem']
        #                            )

        # # 高端极速卖出
        # m.fast_redeem_vipproduct(user_name=user['u1']['user_name'],
        #                          login_password=user['u1']['login_password'],
        #                          redeem_amount=user['u1']['high_end_product_amount'],
        #                          trade_password=user['u1']['trade_password'],
        #                          high_end_product_for_fast_redeem=user['u1']['high_end_product_for_fast_redeem']
        #                          )

        # # 基金普通卖出
        # m.normal_redeem_fund_product(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              redeem_amount=user['u1']['fund_product_amount'],
        #                              trade_password=user['u1']['trade_password'],
        #                              fund_product_name_for_fast_redeem=user['u1']['fund_product_name_for_fast_redeem']
        #                              )

        # # 基金极速卖出
        # m.fast_redeem_fund_product(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            redeem_amount=user['u1']['fund_product_amount'],
        #                            trade_password=user['u1']['trade_password'],
        #                            fund_product_name_for_fast_redeem=user['u1']['fund_product_name_for_fast_redeem']
        #                            )

        # # 积分明细
        # m.assets_my_points_details(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password']
        #                            )

        # # 新基金频道--研究报告
        # m.fund_info_report(user_name=user['u1']['user_name'],
        #                    login_password=user['u1']['login_password']
        #                    )

        # # 基金频道--机构观点
        # m.fund_institution_viewpoint()

        # # 基金频道--达人论基
        # m.fund_talent_fund_discussion()

        # # 基金频道--市场指数
        # m.fund_market_index(csi_index=user['u1']['csi_index'])

        # # 基金频道--全部基金
        # m.fund_all_funds()

        # # 基金频道--评级排行
        # m.fund_rating_and_ranking()

        # # 基金频道--自选基金
        # m.fund_selected_funds(fund_product_name=user['u1']['fund_product_name'],
        #                       user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       fund_company=user['u1']['fund_company']
        #                       )

        # # 基金频道--删除自选基金
        # m.fund_selected_funds_deleted(fund_product_name=user['u1']['fund_product_name'],
        #                               user_name=user['u1']['user_name'],
        #                               login_password=user['u1']['login_password'])

        # # 基金频道--对比分析
        # m.fund_comparison_and_analysis(fund_product_code=user['u1']['non_money_fund_product_code'],
        #                                fund_product_code_2=user['u1']['fund_product_code_2'],
        #                                )

        # # 购买定期宝使用优惠券(不可叠加)
        # m.buy_dqb_use_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                    login_password=user['u1']['login_password'],
        #                                    non_superposed_coupon_code=user['u1'][
        #                                        'non_superposed_coupon_code'],
        #                                    non_superposed_coupon_quantity=user['u1'][
        #                                        'non_superposed_coupon_quantity'],
        #                                    amount=user['u1']['dqb_product_amount'],
        #                                    trade_password=user['u1']['trade_password'],
        #                                    product_name=user['u1']['dqb_product']
        #                                    )

        # # 购买定期宝使用优惠券(可叠加)
        # m.buy_dqb_use_superposed_coupon(user_name=user['u1']['user_name'],
        #                                 login_password=user['u1']['login_password'],
        #                                 amount=user['u1']['dqb_product_amount_for_superposed_coupon'],
        #                                 trade_password=user['u1']['trade_password'],
        #                                 product_name=user['u1']['dqb_product'],
        #                                 superposed_coupon_code=user['u1']['superposed_coupon_code'],
        #                                 superposed_coupon_quantity=user['u1']['superposed_coupon_quantity']
        #                                 )

        # # 购买高端使用优惠券(不可叠加)
        # m.buy_vipproduct_use_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                           login_password=user['u1']['login_password'],
        #                                           amount=user['u1']['high_end_product_amount'],
        #                                           trade_password=user['u1']['trade_password'],
        #                                           product_name=user['u1']['high_end_product'],
        #                                           non_superposed_coupon_quantity=user['u1'][
        #                                               'non_superposed_coupon_quantity'],
        #                                           non_superposed_coupon_code=user['u1']['non_superposed_coupon_code']
        #                                           )

        # # 购买高端使用优惠券(可叠加)
        # m.buy_vipproduct_use_superposed_coupon(user_name=user['u1']['user_name'],
        #                                        login_password=user['u1']['login_password'],
        #                                        amount=user['u1']['high_end_amount_for_superposed_coupon'],
        #                                        trade_password=user['u1']['trade_password'],
        #                                        product_name=user['u1']['high_end_product']
        #                                        )

        # # 购买基金使用优惠券(不可叠加)
        # m.buy_fund_use_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                     login_password=user['u1']['login_password'],
        #                                     product_name=user['u1']['fund_product_name'],
        #                                     amount=user['u1']['fund_product_amount_for_nonsuperposed_coupon'],
        #                                     trade_password=user['u1']['trade_password'],
        #                                     fund_product_code=user['u1']['non_money_fund_product_code'],
        #                                     non_superposed_coupon_code=user['u1']['non_superposed_coupon_code'],
        #                                     non_superposed_coupon_quantity=user['u1']['non_superposed_coupon_quantity']
        #                                     )

        # # 购买基金使用优惠券(可叠加)
        # m.buy_fund_use_superposed_coupon(user_name=user['u1']['user_name'],
        #                                  login_password=user['u1']['login_password'],
        #                                  product_name=user['u1']['fund_product_name'],
        #                                  amount=user['u1']['fund_product_amount'],
        #                                  trade_password=user['u1']['trade_password'],
        #                                  fund_product_code=user['u1']['non_money_fund_product_code']
        #                                  )

        # # 购买定期宝使用积分+优惠券(不可叠加)
        # m.buy_dqb_use_points_and_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                               login_password=user['u1']['login_password'],
        #                                               amount=user['u1']['dqb_product_amount_for_superposed_coupon'],
        #                                               trade_password=user['u1']['trade_password'],
        #                                               product_name=user['u1']['dqb_product'],
        #                                               non_superposed_coupon_code=user['u1'][
        #                                                   'non_superposed_coupon_code'],
        #                                               non_superposed_coupon_quantity=user['u1'][
        #                                                   'non_superposed_coupon_quantity']
        #                                               )

        # # 购买定期宝使用积分+优惠券(可叠加)
        # m.buy_dqb_use_points_and_superposed_coupon(user_name=user['u1']['user_name'],
        #                                            login_password=user['u1']['login_password'],
        #                                            amount=user['u1']['dqb_product_amount'],
        #                                            trade_password=user['u1']['trade_password'],
        #                                            product_name=user['u1']['dqb_product'],
        #                                            superposed_coupon_code=user['u1'][
        #                                                'superposed_coupon_code'],
        #                                            superposed_coupon_quantity=user['u1'][
        #                                                'superposed_coupon_quantity'],
        #                                            )

        # # 购买高端使用积分+优惠券(不可叠加)
        # m.buy_vipproduct_use_points_and_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                                      login_password=user['u1']['login_password'],
        #                                                      amount=user['u1']['high_end_product_amount'],
        #                                                      trade_password=user['u1']['trade_password'],
        #                                                      product_name=user['u1']['high_end_product'],
        #                                                      non_superposed_coupon_code=user['u1'][
        #                                                          'non_superposed_coupon_code'],
        #                                                      non_superposed_coupon_quantity=user['u1'][
        #                                                          'non_superposed_coupon_quantity'],
        #                                                      )

        # # 购买高端使用积分+优惠券(可叠加)
        # m.buy_vipproduct_use_points_and_superposed_coupon(user_name=user['u1']['user_name'],
        #                                                   login_password=user['u1']['login_password'],
        #                                                   amount=user['u1']['high_end_product_amount'],
        #                                                   trade_password=user['u1']['trade_password'],
        #                                                   product_name=user['u1']['high_end_product'],
        #                                                   superposed_coupon_code=user['u1'][
        #                                                       'superposed_coupon_code'],
        #                                                   superposed_coupon_quantity=user['u1'][
        #                                                       'superposed_coupon_quantity'],
        #                                                   )

        # # 购买基金使用积分+优惠券(不可叠加)
        # m.buy_fund_use_points_and_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                                login_password=user['u1']['login_password'],
        #                                                fund_product_name=user['u1']['fund_product_name'],
        #                                                amount=user['u1']['fund_product_amount'],
        #                                                trade_password=user['u1']['trade_password'],
        #                                                fund_product_code=user['u1']['non_money_fund_product_code'],
        #                                                non_superposed_coupon_quantity=user['u1'][
        #                                                    'non_superposed_coupon_quantity'],
        #                                                non_superposed_coupon_code=user['u1'][
        #                                                    'non_superposed_coupon_code']
        #                                                )

        # # 购买基金使用积分+优惠券(可叠加)
        # m.buy_fund_use_points_and_superposed_coupon(user_name=user['u1']['user_name'],
        #                                             login_password=user['u1']['login_password'],
        #                                             fund_product_name=user['u1']['fund_product_name'],
        #                                             amount=user['u1']['fund_product_amount'],
        #                                             trade_password=user['u1']['trade_password'],
        #                                             fund_product_code=user['u1']['non_money_fund_product_code']
        #                                             )

        # # 基金定投
        # m.fund_plan(user_name=user['u1']['user_name'],
        #             login_password=user['u1']['login_password'],
        #             fund_product_name=user['u1']['fund_product_name'],
        #             amount=user['u1']['fund_product_amount'],
        #             trade_password=user['u1']['trade_password'],
        #             )

        # # 查看历史定投(用户没有历史定投)
        # m.check_empty_fund_history_plan(user_name=user['u2']['user_name'],
        #                                 login_password=user['u2']['login_password'],
        #                                 )

        # # 暂停基金定投
        # m.pause_fund_plan(user_name=user['u1']['user_name'],
        #                   login_password=user['u1']['login_password'],
        #                   trade_password=user['u1']['trade_password'],
        #                   fund_product_name=user['u1']['fund_product_name']
        #                   )

        # # 恢复定投
        # m.restart_fund_plan(user_name=user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'],
        #                     trade_password=user['u1']['trade_password'],
        #                     fund_product_name=user['u1']['fund_product_name'])

        # # 终止定投
        # m.stop_fund_plan(user_name=user['u1']['user_name'],
        #                  login_password=user['u1']['login_password'],
        #                  trade_password=user['u1']['trade_password'],
        #                  fund_product_name=user['u1']['fund_product_name'])

        # # 修改基金定投计划
        # m.modify_fund_plan(user_name=user['u1']['user_name'],
        #                    login_password=user['u1']['login_password'],
        #                    fund_product_name=user['u1']['fund_product_name'],
        #                    amount='2.00',
        #                    trade_password=user['u1']['trade_password'])

        # # 新增定投计划
        # m.add_fund_plan(user_name=user['u1']['user_name'],
        #                 login_password=user['u1']['login_password'],
        #                 fund_product_name=user['u1']['fund_product_name'],
        #                 fund_product_code=user['u1']['fund_product_code'],
        #                 trade_password=user['u1']['trade_password'],
        #                 amount=user['u1']['fund_product_amount'])

        # # 随心借
        # m.vip_product_pledge(user_name=user['u1']['user_name'],
        #                      login_password=user['u1']['login_password'],
        #                      product_name=user['u1']['product_name_for_vipproduct_pledge'],
        #                      pledge_amount=user['u1']['pledge_amount'],
        #                      trade_password=user['u1']['trade_password'],
        #                      )

        # # 随心还
        # m.vip_product_pledge_repay(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            product_name=user['u1']['product_name_for_vipproduct_pledge'],
        #                            pledge_repay_amount=user['u1']['pledge_repay_amount'],
        #                            trade_password=user['u1']['trade_password'],
        #                            )

        # # 还房贷
        # m.make_repay_housing_loan_plan(user_name=user['u1']['user_name'],
        #                                login_password=user['u1']['login_password'],
        #                                last_no=user['u1']['pay_card_last_no'],
        #                                repay_amount=user['u1']['repay_loan_amount'],
        #                                trade_password=user['u1']['trade_password']
        #                                )

        # # 现金宝页面点击万份收益, 进入万份收益页面
        # m.view_xjb_income_per_wan(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password']
        #                           )

        # # 现金宝页面点击累计收益,进入累计收益页面
        # m.view_xjb_income_accumulated(user_name=user['u1']['user_name'],
        #                               login_password=user['u1']['login_password']
        #                               )

        # # 现金宝页面点击七日年化收益率,进入七日年化收益率页面
        # m.view_xjb_seven_days_annual_rate_of_return(user_name=user['u1']['user_name'],
        #                                             login_password=user['u1']['login_password']
        #                                             )

        # # 测试立即使用功能
        # m.use_coupon_from_my_coupon_list(user_name=user['u1']['user_name'],
        #                                  login_password=user['u1']['login_password'])

        # # 历史优惠券
        # m.history_coupon_list(user_name=user['u1']['user_name'], password=user['u1']['login_password'])

        # # 优惠券说明页面
        # m.coupon_description(user_name=user['u1']['user_name'], password=user['u1']['login_password'])

        # # 无优惠券页面展示
        # m.my_coupon_empty_list(user_name=user['u2']['user_name'], password=user['u2']['login_password'])

        # # 开启工资代发
        # m.salary_issuing(user_name=user['u1']['user_name'], login_password=user['u1']['login_password'])

        # # 终止工资代发
        # m.stop_salary_issuing(user_name=user['u1']['user_name'], login_password=user['u1']['login_password'],
        #                       trade_password=user['u1']['trade_password'])

        # # 工资理财——新增计划
        # m.add_financing_plan(user_name=user['u1']['user_name'],
        #                      login_password=user['u1']['login_password'],
        #                      last_no=user['u1']['pay_card_last_no'],
        #                      amount=user['u1']['financing_amount'],
        #                      trade_password=user['u1']['trade_password'])

        # # 工资理财——暂停计划
        # m.pause_financing_plan(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'],
        #                        trade_password=user['u1']['trade_password'])

        # # 工资理财——启用计划
        # m.restart_financing_plan(user_name=user['u1']['user_name'],
        #                          login_password=user['u1']['login_password'],
        #                          trade_password=user['u1']['trade_password'])

        # # 修改理财计划
        # m.modify_financing_plan(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'],
        #                         trade_password=user['u1']['trade_password'],
        #                         last_no=user['u1']['pay_card_last_no_for_modification'],
        #                         amount=user['u1']['financing_amount'])

        # # 终止理财计划
        # m.stop_financing_plan(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       trade_password=user['u1']['trade_password'])

        # # 还车贷
        # m.make_repay_car_loan_plan(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            last_no=user['u1']['pay_card_last_no'],
        #                            repay_amount=user['u1']['repay_loan_amount'],
        #                            trade_password=user['u1']['trade_password']
        #                            )

        # # 暂停还贷款计划
        # m.pause_repay_loan_plan(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'],
        #                         trade_password=user['u1']['trade_password'])

        # # 开启工资理财计划
        # m.start_financing_plan(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'],
        #                        last_no=user['u1']['pay_card_last_no'],
        #                        amount=user['u1']['financing_amount'],
        #                        trade_password=user['u1']['trade_password']
        #                        )

        # # 开启还贷款计划
        # m.restart_repay_loan_plan(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           trade_password=user['u1']['trade_password'])

        # # 还其他贷款
        # m.make_repay_other_loan_plan(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              last_no=user['u1']['pay_card_last_no'],
        #                              trade_password=user['u1']['trade_password'],
        #                              repay_amount=user['u1']['repay_loan_amount'])

        # # 修改还房贷为还车贷
        # m.modify_repay_housing_loan_to_repay_car_loan(user_name=user['u1']['user_name'],
        #                                               login_password=user['u1']['login_password'],
        #                                               trade_password=user['u1']['trade_password'],
        #                                               last_no=user['u1']['pay_card_last_no_for_modification'],
        #                                               repay_amount=user['u1']['repay_loan_amount'])

        # # 修改还车贷为还其他贷款
        # m.modify_repay_car_loan_to_repay_other_loan(user_name=user['u1']['user_name'],
        #                                               login_password=user['u1']['login_password'],
        #                                               trade_password=user['u1']['trade_password'],
        #                                               last_no=user['u1']['pay_card_last_no_for_modification'],
        #                                               repay_amount=user['u1']['repay_loan_amount'])

        # # 修改还其他贷款为还房贷
        # m.modify_repay_other_loan_to_repay_housing_loan(user_name=user['u1']['user_name'],
        #                                                 login_password=user['u1']['login_password'],
        #                                                 trade_password=user['u1']['trade_password'],
        #                                                 last_no=user['u1']['pay_card_last_no_for_modification'],
        #                                                 repay_amount=user['u1']['repay_loan_amount'])

        # # 删除还贷款计划
        # m.delete_repay_loan_plan(user_name=user['u1']['user_name'],
        #                          login_password=user['u1']['login_password'],
        #                          trade_password=user['u1']['trade_password'])

        # # 资产证明
        # m.download_assets_certification(user_name=user['u1']['user_name'],
        #                                 login_password=user['u1']['login_password'],
        #                                 trade_password=user['u1']['trade_password'],
        #                                 )

        # # 现金宝持有页面查看在途资产
        # m.view_xjb_asset_in_transit(user_name=user['u1']['user_name'],
        #                             login_password=user['u1']['login_password']
        #                             )

        # # 现金宝持有页面查看产品详情
        # m.view_xjb_product_detail(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password']
        #                           )

        # #  现金宝持有页面查看七日年化收益率曲线
        # m.view_xjb_seven_days_annual_rate_of_return_curve(user_name=user['u1']['user_name'],
        #                                                   login_password=user['u1']['login_password']
        #                                                   )

        # # 查看基金资产(资产分析页面进)
        # m.view_holding_fund_asset_structure(user_name=user['u1']['user_name'],
        #                                     login_password=user['u1']['login_password']
        #                                     )

        # # 查看持有高端资产说明(资产分析页面进)
        # m.view_high_end_holding_assets_description(user_name=user['u1']['user_name'],
        #                                            login_password=user['u1']['login_password']
        #                                            )

        # # 查看持有定活宝资产说明(资产分析页面进)
        # m.view_dhb_holding_assets_description(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password']
        #                                       )

        # # 查看持有现金宝资产说明(我的页面进)
        # m.view_xjb_holding_assets_description(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password']
        #                                       )

        # # 查看持有基金资产说明(我的页面进)
        # m.view_fund_holding_assets_description(user_name=user['u1']['user_name'],
        #                                        login_password=user['u1']['login_password']
        #                                        )

        # # 持有高端产品追加购买(包括购买确认中和确认后)
        # m.high_end_continue_purchase(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              product_name=user['u1']['high_end_product']
        #                              )

        # # 持有定活宝产品追加购买(只有购买确认中)
        # m.dhb_continue_purchase(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'],
        #                         product_name=user['u1']['dqb_product']
        #                         )

        # # 持有基金产品追加购买
        # m.fund_continue_purchase(user_name=user['u1']['user_name'],
        #                          login_password=user['u1']['login_password'],
        #                          product_name=user['u1']['fund_product_name'],
        #                          product_code=user['u1']['non_money_fund_product_code'],
        #                          product_name_confirmed=user['u1']['fund_product_name_for_fast_redeem']
        #                          )

        # # 短信验证码登录
        # m.login_use_verification_code(user_name=user['u2']['user_name'])

        # # 现金支付手段买定活宝(金额正常)
        # m.buy_dhb_product_use_cash_management_product(user_name=user['u1']['user_name'],
        #                                               login_password=user['u1']['login_password'],
        #                                               product_name=user['u1']['dqb_product'],
        #                                               trade_password=user['u1']['trade_password'],
        #                                               amount=user['u1']['dqb_product_amount'],
        #                                               cash_management_product=user['u1']['cash_management_product'])

        # # 信用卡还款使用优惠券
        # m.credit_card_repay_use_coupon(user_name=user['u1']['user_name'],
        #                                login_password=user['u1']['login_password'],
        #                                repay_amount=user['u1']['credit_card_repay_amount'],
        #                                trade_password=user['u1']['trade_password'],
        #                                last_card_no=user['u1']['last_card_no_for_repay'],
        #                                non_superposed_coupon_code=user['u1']['non_superposed_coupon_code'],
        #                                non_superposed_coupon_quantity=user['u1']['non_superposed_coupon_quantity'])

        # # 信用卡预约还款使用优惠券
        # m.credit_card_reserve_repay_use_coupon(user_name=user['u1']['user_name'],
        #                                        login_password=user['u1']['login_password'],
        #                                        repay_amount=user['u1']['credit_card_repay_amount'],
        #                                        trade_password=user['u1']['trade_password'],
        #                                        last_card_no=user['u1']['last_card_no_for_repay'],
        #                                        superposed_coupon_code=user['u1']['superposed_coupon_code'],
        #                                        superposed_coupon_quantity=user['u1'][
        #                                            'non_superposed_coupon_quantity'],
        #                                        user_credit_card_id=user['u1']['user_credit_card_id'])

        # # 基金撤单
        # m.cancel_fund_order(user_name=user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'],
        #                     product_name=user['u1']['fund_product_name'],
        #                     trade_password=user['u1']['trade_password'],
        #                     )

        # # 高端撤单
        # m.cancel_vip_product_order(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            product_name=user['u1']['high_end_product'],
        #                            trade_password=user['u1']['trade_password'],
        #                            amount=user['u1']['high_end_product_amount']
        #                            )

        # m.home_page_recharge_negative(user_name=user['u1']['user_name'],
        #                               login_password=user['u1']['login_password'],
        #                               recharge_amount='999999999',
        #                               trade_password=user['u1']['trade_password'])

        # # 理财日历查看提醒事项
        # m.check_event_reminder_in_calendar(user_name=user['u1']['user_name'], password=user['u1']['login_password'])

        # # 理财日历滑动
        # m.swipe_calendar(user_name=user['u1']['user_name'], password=user['u1']['login_password'])

        # # 定活宝收益计算器
        # m.dhb_income_calculator(user_name=user['u1']['user_name'], password=user['u1']['login_password'],
        #                         product_name=user['u1']['dqb_product'], amount='600')

        # # 定活宝收益计算器小于起投金额
        # m.dhb_income_calculator_less_than_start_amount(user_name=user['u1']['user_name'],
        #                                                password=user['u1']['login_password'],
        #                                                product_name=user['u1']['dqb_product'], amount='400')

        # # 定活宝收益计算器大于最大金额
        # m.dhb_income_calculator_greater_than_max_amount(user_name=user['u1']['user_name'],
        #                                                 password=user['u1']['login_password'],
        #                                                 product_name=user['u1']['dqb_product'], amount='9999999')

        # # 高端收益计算器
        # m.vip_income_calculator(user_name=user['u1']['user_name'],
        #                         password=user['u1']['login_password'],
        #                         product_name=user['u1'][
        #                             'high_end_product_for_income_calculator'], amount='25000')

        # # 高端收益计算器少于起投金额
        # m.vip_income_calculator_less_than_start_amount(user_name=user['u1']['user_name'],
        #                                                password=user['u1']['login_password'],
        #                                                product_name=user['u1'][
        #                                                    'high_end_product_for_income_calculator'], amount='0')

        # # 高端收益计算器大于最大购买金额
        # m.vip_income_calculator_greater_than_max_amount(user_name=user['u1']['user_name'],
        #                                                 password=user['u1']['login_password'],
        #                                                 product_name=user['u1'][
        #                                                     'high_end_product_for_income_calculator'],
        #                                                 amount='9999999999999')

        # # 定投排行
        # m.view_fund_plan_rankings()

        # # 现金管理系列购买高端
        # m.buy_vip_product_use_cash_management_product(user_name=user['u1']['user_name'],
        #                                               login_password=user['u1']['login_password'],
        #                                               product_name=user['u1']['high_end_product'],
        #                                               trade_password=user['u1']['trade_password'],
        #                                               amount=user['u1']['high_end_product_amount'],
        #                                               cash_management_product=user['u1']['cash_management_product'])

        # # 现金管理系列购买基金
        # m.buy_fund_product_use_cash_management_product(user_name=user['u1']['user_name'],
        #                                                login_password=user['u1']['login_password'],
        #                                                fund_product_name=user['u1']['fund_product_name'],
        #                                                trade_password=user['u1']['trade_password'],
        #                                                amount=user['u1']['fund_product_amount'],
        #                                                cash_management_product=user['u1']['cash_management_product'])

        # # 查看非货币型基金详情信息
        # m.view_non_monetary_fund_info(fund_product_name=user['u1']['fund_product_name'])

        # # 查看货币型基金详情信息
        # m.view_monetary_fund_info(fund_product_name=user['u1']['fund_product_name_for_redeem'])

        # # 查看货币型基金的7日年化收益和万份收益
        # m.view_monetary_fund_annual_rate(fund_product_name=user['u1']['fund_product_name_for_redeem'])

        # # 查看现金管理系列产品详情
        # m.view_cash_management_high_end_info(product_name=user['u1']['high_end_product_for_income_calculator'])

        # # 查看固定收益系列产品详情
        # m.view_fixed_rated_high_end_info(product_name=user['u1']['high_end_product'])

        # # 查看精选收益系列产品详情
        # m.view_best_recommend_high_end_info(product_name=user['u1']['best_recommend_high_end_product'])

        # # 查看精选收益产品的历史净值
        # m.view_high_end_history_nav(product_name=user['u1']['best_recommend_high_end_product'])

        # 查看现金管理系列产品的历史收益
        # m.view_cash_management_high_end_annual_rate(product_name=user['u1']['high_end_product_for_income_calculator'])

        # # 福利中心去推荐
        # m.welfare_center_invite_friend(user_name=user['u1']['user_name'],
        #                                password=user['u1']['login_password'])

        # # 福利中心去分享
        # m.welfare_center_go_to_share(user_name=user['u1']['user_name'],
        #                              password=user['u1']['login_password'])

        # # 福利中心去关注
        # m.welfare_center_go_to_focus(user_name=user['u1']['user_name'],
        #                              password=user['u1']['login_password'])

        # # 福利中心去点赞
        # m.welfare_center_go_to_good(user_name=user['u1']['user_name'],
        #                             password=user['u1']['login_password'])

        # # 福利中心查看积分明细
        # m.welfare_center_points_details(user_name=user['u1']['user_name'],
        #                                 password=user['u1']['login_password'])

        # # 福利中心查看元宝明细
        # m.welfare_center_yb_details(user_name=user['u1']['user_name'],
        #                             password=user['u1']['login_password'])

        # # 福利中心签到
        # m.welfare_center_check_in(user_name=user['u3']['user_name'],
        #                           password=user['u3']['login_password'])

        # # 福利中心限时特惠
        # m.welfare_center_timed_discount(user_name=user['u1']['user_name'],
        #                                 password=user['u1']['login_password'])

        # # 福利中心边逛边兑-优惠券
        # m.welfare_center_exchange_coupon(user_name=user['u1']['user_name'],
        #                                  password=user['u1']['login_password'])

        # # 查看基金历史持仓
        # m.view_fund_history_holding(user_name=user['u1']['user_name'],
        #                             password=user['u1']['login_password'], fund_product_name='华夏现金增利货币B')

        # # 查看高端现金管理历史持仓
        # m.view_high_end_history_holding(user_name=user['u1']['user_name'],
        #                                 login_password=user['u1']['login_password'], product_name='现金管理3号')

        # # 基金分红方式切换
        # m.fund_dividend_type_switch(user_name=user['u1']['user_name'],
        #                             login_password=user['u1']['login_password'],
        #                             fund_product_name=user['u1']['fund_product_name_for_redeem'])

        # # 基金快速转换
        # m.fund_fast_convert(user_name=user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'],
        #                     fund_convert_from=user['u1']['fund_product_name_for_redeem'],
        #                     fund_convert_to=user['u1']['fund_product_name_for_fast_convert'], amount='100',
        #                     trade_password=user['u1']['trade_password'])

        # # 基金快速转换撤单
        # m.cancel_fund_fast_convert_order(user_name=user['u1']['user_name'],
        #                                  login_password=user['u1']['login_password'],
        #                                  fund_convert_from=user['u1']['fund_product_name_for_redeem'],
        #                                  fund_convert_to=user['u1']['fund_product_name_for_fast_convert'],
        #                                  trade_password=user['u1']['trade_password'])

        # # 修改个人信息
        # m.modify_personal_information(user_name=user['u1']['user_name'], login_password=user['u1']['login_password'],
        #                               email='test@shhxzq.com', address='test')

        # # 首次绑卡上传已有身份证图片，显示用户已注册。
        # m.bind_card_upload_id_info_negative(login_password='a0000000', trade_password='135790',
        #                                     user_name=user['u3']['user_name'])

        # # 删除历史定投
        # m.delete_fund_history_plan(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            fund_product_name=user['u1']['fund_product_name'],
        #                            fund_product_code=user['u1']['non_money_fund_product_code'])

        # # 实名用户重绑删除的卡（只有一张卡）
        # m.certificated_user_rebind_deleted_card(user_name=user['u2']['user_name'],
        #                                         login_password=user['u2']['login_password'],
        #                                         bank_card_no='45635178090586794')

        # # 实名用户没有绑定的储蓄卡，点击进入信用卡页面。
        # m.click_credit_card_without_bank_card_certificated_user(user_name=user['u2']['user_name'],
        #                                                         login_password=user['u2']['login_password'])

        # # 热门页查看全部产品
        # m.view_all_products(user_name=user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'])

        # # 热门全部产品页面筛选
        # m.all_products_filter(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'])

        # # 基金主题
        # m.view_fund_topics()

        # # 基金估值排行
        # m.view_fund_estimated_value_ranking()

        # # 税收居民身份证明
        # m.tax_dweller_identity_declaration(user_name=user['u1']['user_name'],
        #                                    login_password=user['u1']['login_password'])

        # # 最佳表现基金和最高成交量
        # m.best_performance_highest_turnovers_fund()

        # # 更改登陆方式
        # m.change_sms_login_method(user_name=user['u2']['user_name'],
        #                           login_password=user['u2']['login_password'],
        #                           trade_password=user['u2']['trade_password'])

        # # 查看会员中心
        # m.view_member_center(user_name=user['u1']['user_name'],
        #                      login_password=user['u1']['login_password'])

        # # 查看新发基金
        # m.view_newly_raised_funds(product_name=user['u1']['fund_product_name_for_newly_raised_fund'])

        # # 高端报价式产品修改到期处理方式(全部退出切换为部分退出)
        # m.high_end_quotation_product_expiry_processing_all_to_part(user_name=user['u1']['user_name'],
        #                                                            login_password=user['u1']['login_password'],
        #                                                            trade_password=user['u1']['trade_password'],
        #                                                            product_code=user['u1'][
        #                                                                'high_end_quotation_product_code'])

        # 高端报价式产品修改到期处理方式(部分退出切换为自动续存)
        # m.high_end_quotation_product_expiry_processing_part_to_auto(user_name=user['u1']['user_name'],
        #                                                             login_password=user['u1']['login_password'],
        #                                                             trade_password=user['u1']['trade_password'],
        #                                                             product_code=user['u1'][
        #                                                                 'high_end_quotation_product_code'])

        # # 高端报价式产品修改到期处理方式(自动续存切换为全部退出)
        # m.high_end_quotation_product_expiry_processing_auto_to_all(user_name=user['u1']['user_name'],
        #                                                            login_password=user['u1']['login_password'],
        #                                                            trade_password=user['u1']['trade_password'],
        #                                                            product_code=user['u1'][
        #                                                                'high_end_quotation_product_code'])

        # # 安全中心查看登录记录
        # m.security_center_view_login_record(user_name=user['u1']['user_name'],
        #                                     login_password=user['u1']['login_password'], )

        # # 查看未实名用户账户信息
        # m.view_user_account_information(user_name=user['u3']['user_name'],
        #                                 login_password=user['u3']['login_password'], )

        # # 修改手机号码(不能接收短信)
        # m.modify_mobile_without_sms(user_name=user['u1']['user_name_for_modify_mobile_without_sms'],
        #                             login_password='a0000000', trade_password='135790', mobile_new=mobile_new)


    except Exception, e:
        print e
    finally:
        m.web_driver.quit()
