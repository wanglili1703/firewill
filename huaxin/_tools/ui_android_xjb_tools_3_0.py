# coding=utf-8
from selenium.common.exceptions import NoSuchElementException

from _common.adb import Adb
# from _common.app_compatibility_install import AppCompatibilityInstall

from _common.page_object import PageObject

import time
import datetime
from _common.global_config import GlobalConfig, ASSERT_DICT
from _common.global_controller import GlobalController
from _common.utility import Utility
from _common.web_driver import WebDriver
from _tools.mysql_xjb_tools import MysqlXjbTools
from _tools.restful_xjb_tools import RestfulXjbTools
from _tools.restful_cms_tools import RestfulCmsTools
from huaxin_ui.ui_android_xjb_3_0.main_page import MainPage

from _common.data_base import DataBase

current_page = []

ALLOW = "//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button']"
FORBBID = "//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_deny_button']"
SYSTEM_FORBBID = "//android.widget.Button[@resource-id='com.huawei.systemmanager:id/btn_forbbid']"
# XM_ALLOW = "//android.widget.Button[@resource-id='com.lbe.security.miui:id/permission_allow_button']"  # 小米
XM_ALLOW = "//android.widget.Button[@resource-id='android:id/button1']"  # 小米


class AndroidXjbTools30(object):
    device_id = None

    def __init__(self, app_path, platform_version, device_id, port, package_name, app_status, os):
        self._db = MysqlXjbTools()
        self._rt = RestfulXjbTools()
        self._cms = RestfulCmsTools()

        self.web_driver = WebDriver.Appium().open_android_app(app_path, platform_version, device_id, port, package_name)
        self.main_page = MainPage(self.web_driver)
        self.device_id = device_id

        if device_id == 'PBV7N16924004496':
            if self.main_page.element_exist(
                    "//android.widget.Button[@resource-id='com.huawei.systemmanager:id/btn_forbbid']"):
                self.web_driver.find_element_by_xpath(SYSTEM_FORBBID).click()
                print "click "
            if self.main_page.element_exist(
                    "//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_deny_button']"):
                self.web_driver.find_element_by_xpath(FORBBID).click()
            if self.main_page.element_exist(
                    "//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button']"):
                self.web_driver.find_element_by_xpath(ALLOW).click()

        elif device_id == 'ac3997d9':
            self.web_driver.find_element_by_xpath(XM_ALLOW).click()

    def get_today_date(self):
        today_date = str(datetime.date.today())
        year = str(datetime.date.today().year)
        month = today_date.split('-')[1]
        day = today_date.split('-')[2]
        date = year + month + day

        return date

    def old_user(self, user_name, login_password):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.verify_login_button()
        self.main_page.login(user_name=user_name, password=login_password, return_page='AssetsPage')

    # 现金宝存入--首页
    def home_page_recharge(self, user_name, login_password, recharge_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_recharge_page_from_home_page()
        self.main_page.verify_page_title()
        self.main_page.recharge(recharge_amount=recharge_amount, trade_password=trade_password)
        if ASSERT_DICT['success_flag'] != '0':
            self.main_page.verify_page_title()
            self.main_page.user_operation_complete(return_page='HomePage')
            self.main_page.go_to_assets_page()
            self.main_page.verify_page_title()
            self.main_page.go_to_xjb_detail_page()
            self.main_page.verify_page_title()
            self.main_page.verify_xjb_total_assets(amount=recharge_amount)
            self.main_page.go_to_xjb_trade_detail_page()
            self.main_page.verify_trade_record_values(amount=recharge_amount)
        else:
            self.main_page.back_to_home_page()
            self.main_page.go_to_assets_page()
            self.main_page.verify_page_title()
            self.main_page.verify_xjb_total_assets(amount='0')

    def home_page_regular_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_withdraw_page()
        self.main_page.verify_page_title()
        self.main_page.withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password, type='regular_withdraw')
        if ASSERT_DICT['success_flag'] != '0':
            self.main_page.verify_page_title()
            self.main_page.user_operation_complete(return_page='HomePage')
            self.main_page.go_to_assets_page()
            self.main_page.verify_page_title()
            self.main_page.go_to_xjb_detail_page()
            self.main_page.verify_page_title()
            self.main_page.verify_xjb_total_assets(amount=withdraw_amount, operate_type='regular_withdraw')
            self.main_page.go_to_xjb_trade_detail_page()
            self.main_page.verify_trade_record_values(amount=withdraw_amount, operate_type='regular_withdraw')
        else:
            self.main_page.back_to_home_page()
            self.main_page.go_to_assets_page()
            self.main_page.verify_page_title()
            self.main_page.verify_xjb_total_assets(amount='0')

    def home_page_fast_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_withdraw_page()
        self.main_page.verify_page_title()
        self.main_page.withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password, type='fast_withdraw')
        if ASSERT_DICT['success_flag'] != '0':
            self.main_page.verify_page_title()
            self.main_page.user_operation_complete(return_page='HomePage')
            self.main_page.go_to_assets_page()
            self.main_page.verify_page_title()
            self.main_page.go_to_xjb_detail_page()
            self.main_page.verify_page_title()
            self.main_page.verify_xjb_total_assets(amount=withdraw_amount, operate_type='fast_withdraw')
            self.main_page.go_to_xjb_trade_detail_page()
            self.main_page.verify_trade_record_values(amount=withdraw_amount, operate_type='fast_withdraw')
        else:
            self.main_page.back_to_home_page()
            self.main_page.go_to_assets_page()
            self.main_page.verify_page_title()
            self.main_page.verify_xjb_total_assets(amount='0')

    def home_page_view_essence_recommend_list(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_essence_recommend_page()
        # self.main_page.view_essence_recommend_list()

    def register(self, phone_number, login_password):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.go_to_register_page(device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.register(phone_number=phone_number, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.stroll_first()
        self.main_page.verify_page_title()
        self.main_page.verify_total_assets()

    def register_binding_card(self, phone_number, login_password, trade_password, user_name, id_no, band_card_no):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.verify_login_button()
        self.main_page.go_to_register_page(device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.register(phone_number=phone_number, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_set_trade_password_page()
        self.main_page.verify_page_title()
        self.main_page.set_trade_password(trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.confirm_trade_password(trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.input_id_information_manually(device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.binding_card_input_user_information(banding_card_user_name=user_name,
                                                           id_no=id_no)
        self.main_page.binding_card_first_time(bank_card_no=band_card_no, mobile=phone_number)
        self.main_page.verify_page_title()
        self.main_page.binding_card_confirm()
        self.main_page.verify_page_title()
        self.main_page.go_to_bank_card_management_page()
        self.main_page.verify_bank_card_details(bank_name='工商银行', last_card_no=band_card_no[-4:])

    def bank_card_manage_binding_card(self, user_name, login_password, bank_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_bank_card_management_page(device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.go_to_binding_card_detail_page(device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.binding_card(bank_card_no=bank_card_no, mobile=user_name)
        self.main_page.user_operation_complete(return_page='BankCardManagementPage')
        self.main_page.verify_page_title()
        self.main_page.verify_bank_card_details('工商银行', last_card_no=bank_card_no[-4:])

    def bank_card_manage_binding_nan_yue_card(self, user_name, login_password, banding_card_user_name, bank_card_no,
                                              id_no, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.verify_bind_card_status()
        self.main_page.go_to_bank_card_management_page(device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.go_to_set_trade_password_page()
        self.main_page.verify_page_title()
        self.main_page.set_trade_password(trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.confirm_trade_password(trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.input_id_information_manually(device_id=self.device_id)
        # self.main_page.go_to_binding_card_detail_page(device_id=self.device_id)
        self.main_page.binding_card_input_user_information(banding_card_user_name=banding_card_user_name,
                                                           id_no=id_no)
        self.main_page.binding_card_first_time(bank_card_no=bank_card_no, mobile=user_name)
        self.main_page.stroll_first()
        self.main_page.verify_page_title()
        self.main_page.verify_bank_card_details(bank_name='南粤银行', last_card_no=bank_card_no[-4:])

    def delete_bank_card(self, user_name, login_password, trade_password, last_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_bank_card_management_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_my_bank_card_page(last_card_no=last_card_no)
        self.main_page.verify_bank_card_details(last_card_no=last_card_no)
        self.main_page.delete_bank_card(trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='BankCardManagementPage')
        self.main_page.verify_bank_card_existence(last_card_no=last_card_no)

    def modify_mobile(self, user_name, login_password, trade_password, mobile_new):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_personal_setting_page()
        self.main_page.verify_page_title()
        # self.main_page.go_to_security_center_page()
        # self.main_page.verify_page_title()
        self.main_page.go_to_setting_modify_mobile_page(device_id=self.device_id)
        self.main_page.modify_mobile(mobile_old=user_name, trade_password=trade_password, mobile_new=mobile_new)
        self.main_page.verify_login_button()
        self.main_page.login(user_name=mobile_new, password=login_password, return_page='PersonalSettingPage',
                             flag='modify_mobile')
        self.main_page.verify_page_title()

    def security_center_modify_trade_password(self, user_name, login_password, trade_password_old, trade_password_new):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.verify_login_button()
        self.main_page.login(user_name, login_password, 'AssetsPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_personal_setting_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_security_center_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_security_center_trade_password_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_modify_trade_password_page()
        self.main_page.modify_trade_password(trade_password_old=trade_password_old,
                                             trade_password_new=trade_password_new)
        self.main_page.verify_page_title()

    def security_center_modify_login_password(self, user_name, login_password, login_password_new):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.verify_login_button()
        self.main_page.login(user_name, login_password, 'AssetsPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_personal_setting_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_security_center_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_setting_login_password_page()
        self.main_page.modify_login_password(login_password_old=login_password, login_password_new=login_password_new)
        self.main_page.verify_login_button()
        self.main_page.login(user_name=user_name, password=login_password_new, return_page='SecurityCenterPage',
                             flag='modify_password')
        self.main_page.verify_page_title()

    def security_center_find_trade_password(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_personal_setting_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_security_center_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_security_center_trade_password_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_upload_materials_page()
        self.main_page.upload_photo()
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='SecurityCenterPage')
        self.main_page.verify_page_title()

    def buy_high_end_product(self, user_name, login_password, trade_password, product_name, amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_product_list_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_product_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_product_name(product_name=product_name, product_type='vip')
        self.main_page.go_to_product_purchase_page()
        self.main_page.verify_page_title()
        self.main_page.verify_product_purchase_page_details(product_name=product_name)
        self.main_page.buy_finance_product(amount=amount, trade_password=trade_password)
        self.main_page.verify_page_title()
        if ASSERT_DICT['success_flag'] != '0':
            self.main_page.user_operation_complete(return_page='FinanceHighEndPage')
            self.main_page.verify_page_title()
            self.main_page.go_to_assets_page()
            self.main_page.verify_page_title()
            self.main_page.go_to_high_end_detail_page()
            self.main_page.verify_page_title()
            self.main_page.go_to_high_end_supplementary_purchase_page()
            self.main_page.verify_page_title(product_name=product_name)
            self.main_page.verify_high_end_supplementary_purchase_page_details(amount=amount)
            # self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    def buy_dqb_product(self, user_name, login_password, product_name, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_dqb_product_list_page_()
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_product_search_page()
        self.main_page.go_to_product_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_product_name(product_name=product_name, product_type='dqb')
        self.main_page.go_to_product_purchase_page()
        self.main_page.verify_page_title()
        self.main_page.verify_product_purchase_page_details(product_name=product_name)
        self.main_page.buy_finance_product(amount=amount, trade_password=trade_password)
        self.main_page.verify_page_title()
        if ASSERT_DICT['success_flag'] != '0':
            self.main_page.user_operation_complete(return_page='FinanceDqbPage')
            self.main_page.verify_page_title()
            self.main_page.go_to_assets_page()
            self.main_page.verify_page_title()
            self.main_page.go_to_dqb_detail_page()
            self.main_page.verify_page_title()
            self.main_page.go_to_dqb_supplementary_purchase_page_(product_name=product_name)
            self.main_page.verify_page_title(product_name=product_name)
            self.main_page.verify_dqb_supplementary_purchase_page_details(product_name=product_name, amount=amount)
            self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    def hot_switch_to_dqb_product_list_page(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_hot_product_list_page()
        self.main_page.hot_switch_to_dqb_product_list_page()
        self.main_page.verify_page_title()

    def hot_switch_to_high_end_product_list_page(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_hot_product_list_page()
        self.main_page.hot_switch_to_high_end_product_list_page()
        self.main_page.verify_page_title()

    def finance_product_search_with_full_name(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_product_search_page()
        self.main_page.finance_product_search(product_name=product_name)
        self.main_page.verify_product_name_search_result(product_name=product_name, name_type='full')

    def finance_product_search_with_short_name(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_product_search_page()
        self.main_page.finance_product_search(product_name=product_name)
        self.main_page.verify_product_name_search_result(product_name=product_name, name_type='short')

    def assets_xjb_detail_page_recharge(self, user_name, login_password, recharge_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_xjb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.get_xjb_total_assets()
        self.main_page.go_to_recharge_page_from_assets_page()
        self.main_page.verify_page_title()
        self.main_page.recharge(recharge_amount=recharge_amount, trade_password=trade_password)
        if ASSERT_DICT['success_flag'] != '0':
            self.main_page.verify_page_title()
            self.main_page.user_operation_complete(return_page='AssetsXjbDetailPage')
            self.main_page.verify_xjb_total_assets(amount=recharge_amount)
            self.main_page.go_to_xjb_trade_detail_page()
            self.main_page.verify_trade_record_values(amount=recharge_amount)
        else:
            self.main_page.back_to_xjb_detail_page()
            self.main_page.verify_xjb_total_assets(amount='0')

    def assets_xjb_detail_page_regular_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_withdraw_page()
        self.main_page.verify_page_title()
        self.main_page.withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password, type='regular_withdraw')
        if ASSERT_DICT['success_flag'] != '0':
            self.main_page.verify_page_title()
            self.main_page.user_operation_complete(return_page='AssetsPage')
            self.main_page.verify_xjb_total_assets(amount=withdraw_amount, operate_type='withdraw')
            self.main_page.go_to_xjb_detail_page()
            self.main_page.verify_xjb_total_assets(amount=withdraw_amount, operate_type='withdraw')
            self.main_page.go_to_xjb_trade_detail_page()
            self.main_page.verify_trade_record_values(amount=withdraw_amount, operate_type='regular_withdraw')
        else:
            self.main_page.back_to_xjb_detail_page()
            self.main_page.verify_xjb_total_assets(amount='0')

    def assets_xjb_detail_page_fast_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_withdraw_page()
        self.main_page.verify_page_title()
        self.main_page.withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password)
        if ASSERT_DICT['success_flag'] != '0':
            self.main_page.verify_page_title()
            self.main_page.user_operation_complete(return_page='AssetsPage')
            self.main_page.verify_xjb_total_assets(amount=withdraw_amount, operate_type='withdraw')
            self.main_page.go_to_xjb_detail_page()
            self.main_page.verify_xjb_total_assets(amount=withdraw_amount, operate_type='withdraw')
            self.main_page.go_to_xjb_trade_detail_page()
            self.main_page.verify_trade_record_values(amount=withdraw_amount, operate_type='fast_withdraw')
        else:
            self.main_page.back_to_xjb_detail_page()
            self.main_page.verify_xjb_total_assets(amount='0')

    def delete_credit_card(self, user_name, login_password, last_card_no, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self._db.update_deleted_cust_credit_card_to_normal(card_id='318', state='N')
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_detail_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.go_to_my_credit_card_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.delete_credit_card(trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='CreditCardRepayPage')
        self.main_page.verify_page_title()
        self.main_page.verify_credit_card_delete_result(last_card_no=last_card_no)

    def add_credit_card(self, user_name, login_password, credit_card_no, last_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_page(device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.go_to_add_card_repay_page()
        self.main_page.verify_page_title()
        self._db.update_deleted_cust_credit_card_to_normal(card_id='318', state='D')
        self.main_page.add_credit_card(credit_card_no=credit_card_no, phone_no=user_name)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='CreditCardRepayPage')
        self.main_page.verify_credit_card_add_result(last_card_no=last_card_no)
        self._db.update_deleted_cust_credit_card_to_normal(card_id='318', state='D')

    def view_message(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_message_center_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_financing_message_page()
        self.main_page.verify_page_title()
        self.main_page.view_message()

        # def view_xjb_trade_detail(self, user_name, login_password):
        #     self.old_user(user_name=user_name, login_password=login_password)
        #     self.main_page.go_to_xjb_detail_page()
        #     self.main_page.go_to_xjb_trade_detail_page()
        # self.main_page.view_xjb_trade_detail(trade_type='all')

    def dqb_detail_page_view_trade_detail(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.view_trade_detail()

    def view_dqb_more_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.view_dqb_more_product()
        self.main_page.verify_page_title()

    def view_dqb_history_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_dqb_product_list_page_()
        self.main_page.verify_page_title()
        self.main_page.go_to_dhb_history_product_page()
        self.main_page.verify_page_title()
        self.main_page.verify_history_product_details()

    def fund_detail_page_view_trade_detail(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.view_trade_detail()

    def view_fund_more_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_more_product_page()
        self.main_page.view_fund_more_product()

    def high_end_detail_page_view_trade_detail(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.view_trade_detail()

    def view_high_end_more_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_more_product()
        self.main_page.verify_page_title()

    # def view_high_end_history_product(self, user_name, login_password):
    #     self.old_user(user_name=user_name, login_password=login_password)
    #     self.main_page.go_to_high_end_detail_page()
    #     self.main_page.view_high_end_history_product()

    def redeem_high_end_product(self, user_name, login_password, redeem_amount, trade_password, high_end_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_redeem_page(high_end_product=high_end_product)
        self.main_page.verify_page_title(product_name=high_end_product)
        self.main_page.go_to_redeem_detail_page()
        self.main_page.verify_page_title()
        self.main_page.redeem_product(redeem_amount=redeem_amount, trade_password=trade_password, product_type='vip')
        if ASSERT_DICT['success_flag'] != '0':
            self.main_page.verify_page_title()
            self.main_page.user_operation_complete(return_page='AssetsHighEndDetailPage')
            self.main_page.verify_page_title()
            self.main_page.go_to_high_end_redeem_page(high_end_product=high_end_product)
            self.main_page.go_to_trade_records_page()
            self.main_page.verify_page_title()
            self.main_page.verify_trade_details(trade_type='卖出', product_name=high_end_product, status='已受理',
                                                amount=redeem_amount)

    def redeem_dqb_product(self, user_name, login_password, redeem_amount, trade_password, dqb_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_dqb_detail_page()
        self.main_page.go_to_dqb_redeem_page(product_name=dqb_product)
        self.main_page.verify_page_title(product_name=dqb_product)
        self.main_page.go_to_redeem_detail_page()
        self.main_page.verify_page_title(product_type='DHB')
        self.main_page.redeem_product(redeem_amount=redeem_amount, trade_password=trade_password, product_type='dhb')
        if ASSERT_DICT['success_flag'] != '0':
            self.main_page.verify_page_title()
            self.main_page.user_operation_complete(return_page='AssetsDqbDetailPage')
            self.main_page.verify_page_title()
            self.main_page.go_to_dqb_redeem_page(product_name=dqb_product)
            self.main_page.go_to_trade_records_page()
            self.main_page.verify_page_title()
            self.main_page.verify_trade_details(trade_type='取回', product_name=dqb_product, status='成功',
                                                amount=redeem_amount)

    def my_referee(self, user_name, login_password, phone_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_my_referee_page()
        self.main_page.verify_page_title()
        self.main_page.my_referee(phone_no=phone_no)

    def risk_evaluating_new_user(self, user_name, login_password):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.login(user_name, login_password, 'AssetsPage')
        self.main_page.go_to_personal_setting_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_user_account_information_page()
        self.main_page.verify_page_title()
        self.main_page.verify_risk_evaluation_status()
        self.main_page.go_to_risk_evaluation_page()
        self.main_page.verify_page_title()
        self.main_page.risk_evaluating()
        self.main_page.verify_page_title()
        self.main_page.verify_risk_evaluation_result(risk_type=ASSERT_DICT['risk_type'])

    # 重新测评
    def user_risk_reevaluating(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_setting_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_user_account_information_page()
        self.main_page.verify_page_title()
        self.main_page.verify_risk_evaluation_result()
        self.main_page.go_to_risk_evaluation_page()
        self.main_page.verify_page_title()
        self.main_page.risk_evaluating(test='重新测评')
        self.main_page.verify_page_title()
        self.main_page.verify_risk_evaluation_result(risk_type=ASSERT_DICT['risk_type'])

    def fund_product_search_with_name(self, user_name, login_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products_with_names(fund_product_name=fund_product_name)
        self.main_page.verify_page_title()

    def fund_product_search_with_code(self, user_name, login_password, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.fund_product_search_with_code(fund_product_code=fund_product_code)
        self.main_page.verify_page_title()

    def buy_fund_product(self, user_name, login_password, fund_product_name, amount, trade_password, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.go_to_fund_purchase_page()
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password)
        self.main_page.verify_page_title()
        if ASSERT_DICT['success_flag'] == '1':
            self.main_page.user_operation_complete(return_page='FundPageFundDetail')
            self.main_page.verify_page_title()
            self.main_page.back_to_fund_product_search_page()
            self.main_page.back_to_fund_page()
            self.main_page.go_to_assets_page()
            self.main_page.go_to_fund_detail_page()
            self.main_page.go_to_fund_supplementary_purchase_page(fund_product=fund_product_name)
            self.main_page.verify_fund_purchase_result(amount=amount)
            # self._db.delete_asset_in_transit(mobile=user_name, prod_name=fund_product_name, balance=amount)

    def invite_friend(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_invite_friend_page()

    # 使用其他预约码(有预约码)
    def use_other_reservation_code(self, user_name, login_password, trade_password, buy_quota,
                                   buy_count, reserve_quota, reserve_count, reserve_code, product_id):
        self._db.reservation_code_status_modify(buy_quota=buy_quota, buy_count=buy_count, reserve_quota=reserve_quota,
                                                reserve_count=reserve_count, mobile=user_name,
                                                reserve_code=reserve_code, product_id=product_id)
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_reservation_code_page()
        self.main_page.verify_page_title()
        self.main_page.verify_reservation_code_details()
        self.main_page.use_other_reservation_code(reserve_code=reserve_code, have_reserve_code='yes')
        self.main_page.buy_finance_product(amount='1.00', trade_password=trade_password, mobile=user_name)
        self.main_page.user_operation_complete(return_page='AssetsPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='买入', status='已受理', amount='1.00',
                                            product_name='UI自动化定期预约认购-预约码')

        # self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_id, balance=amount)

    # 使用其他预约码(无预约码)
    def use_other_reservation_code_without_reservation_code(self, user_name, login_password, trade_password, buy_quota,
                                                            buy_count, reserve_quota, reserve_count, reserve_code,
                                                            product_id, mobile):
        self._db.reservation_code_status_modify(buy_quota=buy_quota, buy_count=buy_count, reserve_quota=reserve_quota,
                                                reserve_count=reserve_count, mobile=mobile, reserve_code=reserve_code,
                                                product_id=product_id)
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_reservation_code_page()
        self.main_page.verify_page_title()
        self.main_page.use_other_reservation_code(reserve_code=reserve_code)
        self.main_page.verify_page_title()
        self.main_page.buy_finance_product(amount='1.00', trade_password=trade_password, mobile=user_name, age=70)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='AssetsPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='买入', status='已受理', amount='1.00',
                                            product_name='UI自动化定期预约认购-预约码')

    # 预约码--使用自己的预约码
    def use_reservation_code(self, user_name, login_password, trade_password, buy_quota, buy_count, reserve_quota,
                             reserve_count, reserve_code, product_id):
        self._db.reservation_code_status_modify(buy_quota=buy_quota, buy_count=buy_count, reserve_quota=reserve_quota,
                                                reserve_count=reserve_count, mobile=user_name,
                                                reserve_code=reserve_code, product_id=product_id)
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_reservation_code_page()
        self.main_page.use_reservation_code(trade_password=trade_password)

    def redeem_fund_product(self, user_name, login_password, fund_product, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_redeem_page(fund_product=fund_product)
        self.main_page.verify_page_title(fund_product=fund_product)
        self.main_page.verify_redeem_page_details(fund_product=fund_product)
        self.main_page.go_to_redeem_detail_page()
        self.main_page.verify_page_title()
        self.main_page.redeem_product(redeem_amount=amount, trade_password=trade_password, product_type='fund')
        self.main_page.verify_page_title()
        if ASSERT_DICT['success_flag'] == '1':
            self.main_page.user_operation_complete(return_page='FundRedeemPage')
            self.main_page.verify_page_title(fund_product=fund_product)
            self.main_page.go_to_trade_records_page()
            self.main_page.verify_page_title()
            self.main_page.verify_trade_details(trade_type='卖出', status='已受理', amount=amount, product_name=fund_product)

    def earn_points(self, user_name, login_password, amount, trade_password, fund_product_name, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_my_points_page()
        self.main_page.earn_points_by_buy_fund(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, source='0')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=fund_product_name, balance=amount)

    # 赚积分--推荐用户注册绑卡
    def earn_points_by_recommend_user_register(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_my_points_page()
        self.main_page.earn_points_by_recommend_user_register()

    # 信用卡还款
    def credit_card_repay(self, user_name, login_password, repay_amount, trade_password, last_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_detail_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.verify_credit_card_details(last_card_no=last_card_no)
        self.main_page.repay(repay_amount, trade_password)
        self.main_page.user_operation_complete(return_page='CreditCardRepayPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_detail_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_record_page()
        self.main_page.verify_page_title(last_card_no=last_card_no)
        self.main_page.verify_credit_card_repay_record_details(last_card_no=last_card_no, amount=repay_amount)

    # 信用卡预约还款
    def credit_card_reserved_pay(self, user_name, login_password, reserved_pay_amount, trade_password, last_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self._db.update_creditcard_order_state(card_id='422', orign_state='N', update_state='C')
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_detail_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.go_to_reserved_pay_page()
        self.main_page.verify_page_title()
        self.main_page.verify_credit_card_details(last_card_no=last_card_no)
        self.main_page.reserved_pay(reserved_pay_amount, trade_password)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='CreditCardRepayPage')
        self.main_page.verify_credit_card_repay_details(reserved_pay_amount=reserved_pay_amount)

    # 取消预约还款
    def cancel_reserved_pay(self, user_name, login_password, last_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self._db.update_creditcard_order_state(card_id='422', update_state='N')
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_detail_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.verify_credit_card_details(last_card_no=last_card_no)
        self.main_page.cancel_reservation()
        self.main_page.verify_page_title()
        self.main_page.verify_credit_card_reserved_pay_flag()

    # 花积分--买基金
    def spend_points_by_buy_fund(self, user_name, login_password, amount, trade_password, fund_product_name,
                                 fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_my_points_page()
        self.main_page.spend_points_by_buy_fund(fund_product_name=fund_product_name,
                                                fund_product_code=fund_product_code)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, points='Y', source='0')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=fund_product_name, balance=amount)

    # 花积分--买高端产品
    def spend_points_by_buy_vipproduct_use_product_name(self, user_name, login_password, product_name, amount,
                                                        trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_my_points_page()
        self.main_page.spend_points_by_buy_vipproduct_use_product_name()
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            points='Y', source='0')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    # 花积分--买定期宝
    def spend_points_by_buy_dqb(self, user_name, login_password, dqb_product, dqb_product_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_my_points_page()
        self.main_page.spend_points_by_buy_dqb()
        self.main_page.buy_dqb_product(product_name=dqb_product, amount=dqb_product_amount,
                                       trade_password=trade_password, points='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=dqb_product_amount, balance=dqb_product_amount)

    # 添加信用卡还款提醒
    def add_credit_card_repayment_warn(self, user_name, login_password, last_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self._db.modify_credit_card_reminder_status(status='0', card_no='5309854552866685')
        self._db.update_creditcard_order_state(card_id='422', update_state='C')
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_detail_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.go_to_my_credit_card_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.add_repayment_warn()
        self.main_page.back_to_credit_card_repay_detail_page()
        self.main_page.verify_page_title()
        self.main_page.back_to_credit_card_repay_page()
        self.main_page.verify_page_title()
        self.main_page.verify_credit_card_repay_reminder_details()

    # 取消信用卡还款提醒
    def cancel_credit_card_repayment_warn(self, user_name, login_password, last_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self._db.modify_credit_card_reminder_status(status='1', card_no='5309854552866685')
        self._db.update_creditcard_order_state(card_id='422', orign_state='N', update_state='C')
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_detail_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.go_to_my_credit_card_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.cancel_repayment_warn()
        self.main_page.verify_page_title()
        self.main_page.verify_repayment_warn_flag()

    # 高端普通卖出
    def normal_redeem_vipproduct(self, user_name, login_password, redeem_amount, trade_password,
                                 high_end_product_for_fast_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_high_end_redeem_page(high_end_product=high_end_product_for_fast_redeem)
        self.main_page.go_to_redeem_detail_page()
        self.main_page.redeem_product(redeem_amount=redeem_amount, trade_password=trade_password, product_type='vip')
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='AssetsHighEndDetailPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_redeem_page(high_end_product=high_end_product_for_fast_redeem)
        self.main_page.go_to_trade_records_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='卖出', status='已受理', amount=redeem_amount,
                                            product_name=high_end_product_for_fast_redeem)

    # 高端快速卖出
    def fast_redeem_vipproduct(self, user_name, login_password, redeem_amount, trade_password,
                               high_end_product_for_fast_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_high_end_redeem_page(high_end_product=high_end_product_for_fast_redeem)
        self.main_page.verify_page_title(product_name=high_end_product_for_fast_redeem)
        self.main_page.go_to_redeem_detail_page()
        self.main_page.redeem_product(redeem_amount=redeem_amount, trade_password=trade_password, redeem_type='fast',
                                      product_type='vip')
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='AssetsHighEndDetailPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_redeem_page(high_end_product=high_end_product_for_fast_redeem)
        self.main_page.go_to_trade_records_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='极速卖出', status='尾款充值中', amount=redeem_amount,
                                            product_name=high_end_product_for_fast_redeem)

    # 基金普通卖出
    def normal_redeem_fund_product(self, user_name, login_password, redeem_amount, trade_password,
                                   fund_product_name_for_fast_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_redeem_page(fund_product=fund_product_name_for_fast_redeem)
        self.main_page.verify_page_title(fund_product=fund_product_name_for_fast_redeem)
        self.main_page.verify_redeem_page_details(fund_product=fund_product_name_for_fast_redeem)
        self.main_page.go_to_redeem_detail_page()
        self.main_page.verify_page_title()
        self.main_page.redeem_product(redeem_amount=redeem_amount, trade_password=trade_password,
                                      product_type='fund')
        self.main_page.verify_page_title()
        if ASSERT_DICT['success_flag'] == '1':
            self.main_page.user_operation_complete(return_page='FundRedeemPage')
            self.main_page.verify_page_title(fund_product=fund_product_name_for_fast_redeem)

            # self.main_page.normal_redeem_fund_product(fund_product_name_for_fast_redeem=fund_product_name_for_fast_redeem,
            #                                           redeem_amount=redeem_amount, trade_password=trade_password)

    # 基金极速卖出
    def fast_redeem_fund_product(self, user_name, login_password, redeem_amount, trade_password,
                                 fund_product_name_for_fast_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_redeem_page(fund_product=fund_product_name_for_fast_redeem)
        self.main_page.verify_page_title(fund_product=fund_product_name_for_fast_redeem)
        self.main_page.verify_redeem_page_details(fund_product=fund_product_name_for_fast_redeem)
        self.main_page.go_to_redeem_detail_page()
        self.main_page.verify_page_title()
        self.main_page.redeem_product(redeem_amount=redeem_amount, trade_password=trade_password,
                                      product_type='fund', redeem_type='fast')
        self.main_page.verify_page_title()
        if ASSERT_DICT['success_flag'] == '1':
            self.main_page.user_operation_complete(return_page='FundRedeemPage')
            self.main_page.verify_page_title(fund_product=fund_product_name_for_fast_redeem)
            self.main_page.go_to_trade_records_page()
            self.main_page.verify_page_title()
            self.main_page.verify_trade_details(trade_type='极速卖出', status='尾款充值中', amount=redeem_amount,
                                                product_name=fund_product_name_for_fast_redeem)

    # 积分明细
    def assets_my_points_details(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_my_points_page()
        self.main_page.my_points_details()

    # 基金频道--研究报告
    def fund_research_report(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_research_report()

    # 基金频道--机构观点
    def fund_institution_viewpoint(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_institution_viewpoint()

    # 基金频道--达人论基
    def fund_talent_fund_discussion(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_talent_fund_discussion()

    # 基金频道--市场指数
    def fund_market_index(self, user_name, login_password, csi_index):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_market_index_page()
        self.main_page.verify_page_title()
        self.main_page.fund_market_index(csi_index=csi_index)

    # 基金频道--全部基金
    def fund_all_funds(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_page_all_fund_page()
        # self.main_page.verify_page_title()
        self.main_page.fund_all_funds(fund_type='全部')
        self.main_page.fund_all_funds(fund_type='股票型')
        self.main_page.fund_all_funds(fund_type='混合型')
        self.main_page.fund_all_funds(fund_type='债券型')
        self.main_page.fund_all_funds(fund_type='货币型')
        self.main_page.fund_all_funds(fund_type='QDII')
        self.main_page.fund_all_funds(fund_type='指数型')
        self.main_page.fund_all_funds(fund_type='其他')

    # 基金筛选器
    def fund_filter(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_page_all_fund_page()
        self.main_page.go_to_fund_filter_page()
        self.main_page.verify_page_title()
        self.main_page.fund_filter()
        self.main_page.verify_fund_filter_results()

    # 基金频道--星级排行
    def fund_rating_and_ranking(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_rating_and_ranking()

    # 基金频道--最佳表现基金
    def fund_best_performance_fund(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_best_performance_fund_page()
        self.main_page.verify_page_title(title='最佳表现基金')
        self.main_page.verify_page_details()
        self.main_page.view_best_performance_funds(period='近1周')
        self.main_page.verify_page_details()
        self.main_page.view_best_performance_funds(period='近3月')
        self.main_page.verify_page_details()
        self.main_page.view_best_performance_funds(period='近6月')
        self.main_page.verify_page_details()
        self.main_page.view_best_performance_funds(period='近1年')
        self.main_page.verify_page_details()
        self.main_page.view_best_performance_funds(period='近3年')
        self.main_page.verify_page_details()
        self.main_page.view_best_turnover_funds()
        self.main_page.verify_page_title(title='最高成交量')

    def fund_selected_funds(self, user_name, login_password, fund_product_name, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_fav_fund(mobile=user_name)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_selected_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.verify_page_title()
        self.main_page.select_fund()
        self.main_page.back_to_fund_selected_page()
        self.main_page.verify_selected_fund_details(fund_product_name=fund_product_name,
                                                    fund_product_code=fund_product_code)
        self._db.update_fav_fund(mobile=user_name, fund_id='05#050026')

    # 基金频道--删除自选基金
    def fund_selected_funds_deleted(self, user_name, login_password, fund_product_name, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self._db.update_fav_fund(mobile=user_name, id=2347)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_selected_page()
        self.main_page.verify_selected_fund_details(fund_product_name=fund_product_name,
                                                    fund_product_code=fund_product_code)
        self.main_page.go_to_selected_fund_management_page()
        self.main_page.verify_page_title()
        self.main_page.delete_selected_fund()
        self.main_page.verify_no_selected_fund_tip()
        self.main_page.back_to_fund_selected_page()
        self.main_page.verify_no_selected_fund(fund_product_name=fund_product_name, fund_product_code=fund_product_code)

    # 基金频道--删除自选基金（从自选基金详情页面删除）
    def fund_selected_funds_deleted_at_fund_detail_page(self, user_name, login_password, fund_product_name,
                                                        fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self._db.update_fav_fund(mobile=user_name, id=2347)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.verify_page_title()
        self.main_page.delete_selected_fund()
        self.main_page.back_to_fund_product_search_page()
        self.main_page.back_to_fund_page()
        self.main_page.go_to_fund_selected_page()
        self.main_page.verify_no_selected_fund(fund_product_name=fund_product_name, fund_product_code=fund_product_code)

    # 基金频道--对比分析
    def fund_comparasion_and_analysis(self, user_name, login_password, fund_product_code, fund_product_code_2):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_comparasion_and_analysis(fund_product_code=fund_product_code,
                                                     fund_product_code_2=fund_product_code_2)

    # 购买定期宝使用优惠券(不可叠加)
    def buy_dqb_use_nonsuperposed_coupon(self, user_name, login_password, nonsuperposed_coupon_code,
                                         nonsuperposed_coupon_quantity, product_name, amount,
                                         trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_dqb_product_list_page()
        # self._cms.issue_coupon(code=nonsuperposed_coupon_code, mobile=user_name, quantity=nonsuperposed_coupon_quantity)
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       nonsuperposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    # 购买定期宝使用优惠券(可叠加)
    def buy_dqb_use_superposed_coupon(self, user_name, login_password, superposed_coupon_code,
                                      superposed_coupon_quantity, product_name, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_dqb_product_list_page()
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name, quantity=superposed_coupon_quantity)
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       superposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    # 购买高端使用优惠券(不可叠加)
    def buy_vipproduct_use_nonsuperposed_coupon(self, user_name, login_password, nonsuperposed_coupon_code,
                                                nonsuperposed_coupon_quantity, product_name, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        # self._cms.issue_coupon(code=nonsuperposed_coupon_code, mobile=user_name, quantity=nonsuperposed_coupon_quantity)
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            nonsuperposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    # 购买高端使用优惠券(可叠加)
    def buy_vipproduct_use_superposed_coupon(self, user_name, login_password, superposed_coupon_code,
                                             superposed_coupon_quantity, product_name, amount,
                                             trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name, quantity=superposed_coupon_quantity)
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            superposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    # 购买基金使用优惠券(不可叠加)
    def buy_fund_use_nonsuperposed_coupon(self, user_name, login_password, fund_product_name, nonsuperposed_coupon_code,
                                          nonsuperposed_coupon_quantity, amount, trade_password, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        # self._cms.issue_coupon(code=nonsuperposed_coupon_code, mobile=user_name, quantity=nonsuperposed_coupon_quantity)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, nonsuperposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=fund_product_name, balance=amount)

    # 购买基金使用优惠券(可叠加)
    def buy_fund_use_superposed_coupon(self, user_name, login_password, superposed_coupon_code,
                                       superposed_coupon_quantity, fund_product_name, amount, trade_password,
                                       fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name, quantity=superposed_coupon_quantity)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, superposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=fund_product_name, balance=amount)

    # 购买定期宝使用积分+优惠券(不可叠加)
    def buy_dqb_use_points_and_nonsuperposed_coupon(self, user_name, login_password, nonsuperposed_coupon_code,
                                                    nonsuperposed_coupon_quantity, product_name, amount,
                                                    trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_dqb_product_list_page()
        # self._cms.issue_coupon(code=nonsuperposed_coupon_code, mobile=user_name, quantity=nonsuperposed_coupon_quantity)
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       points='Y', nonsuperposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    # 购买定期宝使用积分+优惠券(可叠加)
    def buy_dqb_use_points_and_superposed_coupon(self, user_name, login_password, superposed_coupon_code,
                                                 superposed_coupon_quantity, product_name, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_dqb_product_list_page()
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name, quantity=superposed_coupon_quantity)
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       points='Y', superposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    # 购买高端使用积分+优惠券(不可叠加)
    def buy_vipproduct_use_points_and_nonsuperposed_coupon(self, user_name, login_password, nonsuperposed_coupon_code,
                                                           nonsuperposed_coupon_quantity, product_name, amount,
                                                           trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        # self._cms.issue_coupon(code=nonsuperposed_coupon_code, mobile=user_name, quantity=nonsuperposed_coupon_quantity)
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            points='Y', nonsuperposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    # 购买高端使用积分+优惠券(可叠加)
    def buy_vipproduct_use_points_and_superposed_coupon(self, user_name, login_password, superposed_coupon_code,
                                                        superposed_coupon_quantity, product_name, amount,
                                                        trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name, quantity=superposed_coupon_quantity)
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            points='Y', superposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    # 购买基金使用积分+优惠券(不可叠加)
    def buy_fund_use_points_and_nonsuperposed_coupon(self, user_name, login_password, nonsuperposed_coupon_code,
                                                     nonsuperposed_coupon_quantity, fund_product_name, amount,
                                                     trade_password, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        # self._cms.issue_coupon(code=nonsuperposed_coupon_code, mobile=user_name, quantity=nonsuperposed_coupon_quantity)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, points='Y',
                                        nonsuperposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=fund_product_name, balance=amount)

    # 购买基金使用积分+优惠券(可叠加)
    def buy_fund_use_points_and_superposed_coupon(self, user_name, login_password, superposed_coupon_code,
                                                  superposed_coupon_quantity, fund_product_name, amount, trade_password,
                                                  fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        # self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name, quantity=superposed_coupon_quantity)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, points='Y', superposed_coupon='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=fund_product_name, balance=amount)

    # 基金定投
    def fund_plan(self, user_name, login_password, fund_product_name, amount, trade_password, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.go_to_fund_plan_page()
        self.main_page.make_fund_plan(amount=amount, trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='FundPageFundDetail')
        self.main_page.verify_page_title()
        protocol_no = self._db.delete_fund_invest_plan(mobile=user_name)
        self._db.delete_noc_builder_useless_data(user_name=user_name, order_serial_no_delete=protocol_no)

    # 查看历史定投(用户没有历史定投)
    def check_empty_fund_history_plan(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_fund_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.verify_page_title()
        if ASSERT_DICT['page'] == 'StartFundPlanPage':
            self.main_page.go_to_fund_page_all_fund_page()
            self.main_page.go_to_assets_fund_detail_page()
            self.main_page.verify_page_title()
            self.main_page.go_to_my_fund_plan_page()
            self.main_page.verify_page_title()
        self.main_page.go_to_fund_history_plan_page()
        self.main_page.verify_page_title()
        self.main_page.verify_page_elements()

    # 删除历史定投
    def delete_fund_history_plan(self, user_name, login_password, fund_product_name):
        self._db.update_fund_invest_plan_status(status='E', id='2281', is_delete=0)
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_fund_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.verify_page_title()
        if ASSERT_DICT['page'] == 'StartFundPlanPage':
            self.main_page.go_to_fund_page_all_fund_page()
            self.main_page.go_to_assets_fund_detail_page()
            self.main_page.verify_page_title()
            self.main_page.go_to_my_fund_plan_page()
            self.main_page.verify_page_title()
        self.main_page.go_to_fund_history_plan_page(history_type='empty')
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_plan_detail_page(fund_product_name=fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_fund_plan_status(status='定投已终止')
        self.main_page.delete_fund_history_plan()
        self.main_page.verify_page_title()
        self.main_page.verify_page_elements()

    # 暂停定投计划
    def pause_fund_plan(self, user_name, login_password, trade_password, fund_product_name):
        self._db.update_fund_invest_plan_status(status='N', id='2281', is_delete=0)
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_fund_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_plan_detail_page(fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_fund_plan_status('定投进行中')
        self.main_page.pause_fund_plan(trade_password=trade_password)
        self.main_page.verify_fund_plan_status('定投已暂停')
        # self._db.update_fund_invest_plan_status(status='E', id='2281')

    # 恢复定投计划
    def restart_fund_plan(self, user_name, login_password, trade_password, fund_product_name):
        self._db.update_fund_invest_plan_status(status='P', id='2281', is_delete=0)
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_fund_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_plan_detail_page(fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_fund_plan_status('定投已暂停')
        self.main_page.restart_fund_plan(trade_password=trade_password)
        self.main_page.verify_fund_plan_status('定投进行中')
        # self._db.update_fund_invest_plan_status(status='E', id='2281')

    # 终止定投计划
    def stop_fund_plan(self, user_name, login_password, trade_password, fund_product_name):
        self._db.update_fund_invest_plan_status(status='N', id='2281', is_delete=0)
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_fund_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_plan_detail_page(fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_fund_plan_status('定投进行中')
        self.main_page.get_fund_plan_details()
        self.main_page.stop_fund_plan(trade_password=trade_password)
        self.main_page.go_to_fund_history_plan_page()
        self.main_page.verify_page_title()
        self.main_page.verify_fund_history_details(fund_product_name=fund_product_name)
        # self._db.update_fund_invest_plan_status(status='E', id='2281')

    # 修改定投计划
    def modify_fund_plan(self, user_name, login_password, trade_password, fund_product_name, amount):
        self._db.update_fund_invest_plan_status(period='2#M', day='W#2', amount='10.00', status='N', id='2281',
                                                is_delete=0)
        self.old_user(user_name=user_name, login_password=login_password)
        # self._db.update_fund_invest_plan_status(period='2#M', day='W#2', amount='10.00', status='N', id='2281')
        self.main_page.go_to_assets_fund_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_plan_detail_page(fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.go_to_make_fund_plan_page()
        self.main_page.verify_page_title()
        self.main_page.make_fund_plan(amount=amount, trade_password=trade_password, return_page='FundPlanDetailPage')
        self.main_page.user_operation_complete(return_page='FundPlanDetailPage')
        self.main_page.verify_page_title()
        self.main_page.verify_fund_plan_details(amount=amount)

    # 新增定投计划
    def add_fund_plan(self, user_name, login_password, fund_product_name, fund_product_code, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_fund_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_my_fund_plan_page()
        self.main_page.verify_page_title()
        self.main_page.add_fund_plan()
        self.main_page.close_tips()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.verify_page_title()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.go_to_fund_plan_page()
        self.main_page.verify_page_title()
        self.main_page.make_fund_plan(amount=amount, trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='FundPageFundDetail')
        self.main_page.verify_page_title()
        protocol_no = self._db.delete_fund_invest_plan(mobile=user_name)
        self._db.delete_noc_builder_useless_data(user_name=user_name, order_serial_no_delete=protocol_no)

    # 随心借
    def vipproduct_pledge(self, user_name, login_password, product_name, pledge_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_pledge_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_select_pledge_product_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_pledge_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.pledge(pledge_amount=pledge_amount, trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='Pledge_page')
        self.main_page.verify_page_title()
        self.main_page.verify_pledge_details(product_name=product_name, pledge_amount=pledge_amount)

    # 随心还(必须一次还清)
    def vipproduct_pledge_repay(self, user_name, login_password, product_name, pledge_repay_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_pledge_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_pledge_repay_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.pledge_repay(pledge_repay_amount=pledge_repay_amount, trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='Pledge_page')
        self.main_page.verify_page_title()
        self.main_page.go_to_pledge_history_page()
        # self.main_page.verify_page_title()
        self.main_page.verify_pledge_repay_status(product_name=product_name)
        # self.main_page.go_to_pledge_repay_history_detail_page(product_name=product_name)
        # self.main_page.verify_page_title()
        # self.main_page.verify_pledge_repay_history_details(product_name=product_name,
        #                                                    pledge_repay_amount=pledge_repay_amount)

    # 会员中心
    def associator_level(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        # self.main_page.associator_rank_verify()
        self.main_page.go_to_associator_center()
        self.main_page.verify_page_title()
        # level = self.main_page.get_text('com.shhxzq.xjb:id/tv_member_lv', 'find_element_by_id')
        # self.main_page.current_level_verify()

    # 员工理财--开启工资代发
    def salary_issuing(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_employee_protocol_status(mobile=user_name, protocol_status='0')
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_deposit_salary_page()
        self.main_page.start_salary_issuing()
        self._db.update_employee_protocol_status(mobile=user_name, protocol_status='3')

    # 员工理财--终止工资代发
    def stop_salary_issuing(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_employee_protocol_status(mobile=user_name, protocol_status='1')
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_deposit_salary_page()
        self.main_page.stop_salary_issuing(trade_password=trade_password)
        self._db.update_employee_protocol_status(mobile=user_name, protocol_status='3')

    # 开启工资理财计划
    def start_financing_plan(self, user_name, login_password, last_no, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_make_financing_plan_page()
        self.main_page.make_financing_plan(last_no=last_no, amount=amount, trade_password=trade_password)
        protocol_no = self._db.delete_fund_invest_plan(mobile=user_name)
        self._db.delete_noc_builder_useless_data(user_name=user_name, order_serial_no_delete=protocol_no)

    # 新增工资理财计划
    def add_financing_plan(self, user_name, login_password, last_no, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_fund_invest_plan_status(status='N', id='1944')
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_make_financing_plan_page()
        self.main_page.make_financing_plan(last_no=last_no, amount=amount, trade_password=trade_password)
        protocol_no = self._db.delete_fund_invest_plan(mobile=user_name)
        self._db.delete_noc_builder_useless_data(user_name=user_name, order_serial_no_delete=protocol_no)
        self._db.update_fund_invest_plan_status(status='D', id='1944')

    # 暂停工资理财计划
    def pause_financing_plan(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_fund_invest_plan_status(status='N', id='1944')
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_salary_financing_plan_detail_page()
        self.main_page.pause_salary_financing_plan(trade_password=trade_password)
        self._db.update_fund_invest_plan_status(status='D', id='1944')

    # 启用工资理财计划
    def restart_financing_plan(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_fund_invest_plan_status(status='P', id='1944')
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_salary_financing_plan_detail_page()
        self.main_page.restart_salary_financing_plan(trade_password=trade_password)
        self._db.update_fund_invest_plan_status(status='D', id='1944')

    # 我的优惠券-立即使用-买入
    def use_coupon_from_my_coupon_list(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_my_coupon_list()
        self.main_page.use_coupon_to_buy_page()
        # self.main_page.verify_page_title()
        print '点击左上角箭头'
        self.main_page.go_back_to_my_coupon()
        print '验证当前在我的优惠券页面'
        # self.main_page.verify_page_title()

    # 历史优惠券
    def history_coupon_list(self, user_name, password):
        print '登录现金宝'
        self.old_user(user_name=user_name, login_password=password)

        print '点击我的优惠券'
        self.main_page.go_to_my_coupon_list()

        print '点击历史优惠券'
        self.main_page.go_to_history_page()

        print '验证当前在历史优惠券页面'
        # self.main_page.verify_page_title()

        print '验证优惠券已使用标签'
        self.main_page.verify_used_coupon_icon()

        print '点击左上角箭头'
        self.main_page.go_back_to_my_coupon()

        print '验证当前在我的优惠券页面'
        # self.main_page.verify_page_title()

    # 优惠券说明页面
    def coupon_description(self, user_name, password):
        print '登录现金宝'
        self.old_user(user_name=user_name, login_password=password)

        print '点击我的优惠券'
        self.main_page.go_to_my_coupon_list()

        print '点击说明'
        self.main_page.go_to_coupon_description_page()

        print "验证当前在优惠券说明页面"
        # self.main_page.verify_page_elements()

        print '点击左上角箭头'
        self.main_page.go_back_to_my_coupon()

        print '验证当前在我的优惠券页面'
        # self.main_page.verify_page_title()

    # 我的优惠券列表为空
    def my_coupon_empty_list(self, user_name, login_password):
        print '登录现金宝'
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()

        print '点击我的优惠券'
        self.main_page.go_to_my_empty_coupon_list(index='3')
        self.main_page.verify_page_title()

        self.main_page.verify_empty_coupon_record()

        print '点击左上角箭头'
        self.main_page.go_back_to_assets_page()

        print '验证当前在我的资产页面'
        self.main_page.verify_page_title()

    # 修改工资理财计划
    def modify_financing_plan(self, user_name, login_password, trade_password, last_no, amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_fund_invest_plan_status(status='N', id='1944')
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_salary_financing_plan_detail_page()
        self.main_page.go_to_modify_financing_plan_page()
        self.main_page.modify_salary_financing_plan(trade_password=trade_password, last_no=last_no, amount=amount)
        self._db.update_fund_invest_plan_status(status='D', id='1944', bank_account='62220240842461360', amount='10.00')

    # 终止工资理财计划
    def stop_financing_plan(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_fund_invest_plan_status(status='N', id='1944')
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_deposit_salary_page()
        self.main_page.go_to_salary_financing_plan_detail_page()
        self.main_page.stop_salary_financing_plan(trade_password=trade_password)

    # 还房贷
    def make_repay_housing_loan_plan(self, user_name, login_password, last_no, trade_password, repay_amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='D', repay_plan_id='75')
        self._db.delete_all_unnecessary_plans(id=75)
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_make_repay_plan_page()
        self.main_page.make_repay_loan_plan(trade_password=trade_password, last_no=last_no, repay_amount=repay_amount,
                                            repay_type='housing_loan')
        serial_no = self._db.delete_repay_loan_plan(mobile=user_name)
        self._db.delete_noc_builder_useless_data(user_name=user_name, order_serial_no_delete=serial_no)
        # self._db.update_plan_status(status='D')

    # 还车贷
    def make_repay_car_loan_plan(self, user_name, login_password, last_no, trade_password, repay_amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='N', repay_plan_id='75')
        self._db.delete_all_unnecessary_plans(id=75)
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_make_repay_plan_page()
        self._db.update_plan_status(status='D', repay_plan_id='75')
        self.main_page.make_repay_loan_plan(trade_password=trade_password, last_no=last_no, repay_amount=repay_amount,
                                            repay_type='car_loan')
        serial_no = self._db.delete_repay_loan_plan(mobile=user_name)
        self._db.delete_noc_builder_useless_data(user_name=user_name, order_serial_no_delete=serial_no)

    # 还其他
    def make_repay_other_loan_plan(self, user_name, login_password, last_no, trade_password, repay_amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='D', repay_plan_id='75')
        self._db.delete_all_unnecessary_plans(id=75)
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_make_repay_plan_page()
        self.main_page.make_repay_loan_plan(trade_password=trade_password, last_no=last_no, repay_amount=repay_amount,
                                            repay_type='others', other_purpose=u'其他用途')
        serial_no = self._db.delete_repay_loan_plan(mobile=user_name)
        self._db.delete_noc_builder_useless_data(user_name=user_name, order_serial_no_delete=serial_no)

    # 暂停还贷款计划
    def pause_repay_loan_plan(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='N', repay_type='H', repay_plan_id='75')
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='housing_loan')
        self.main_page.pause_repay_loan_plan(trade_password=trade_password)
        self._db.update_plan_status(status='D', repay_plan_id='75')

    # 启用还贷款计划
    def restart_repay_loan_plan(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='P', repay_type='H', repay_plan_id='75')
        self._db.delete_all_unnecessary_plans(id=75)
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='housing_loan')
        self.main_page.restart_repay_loan_plan(trade_password=trade_password)
        self._db.update_plan_status(status='D', repay_plan_id='75')

    # 修改还房贷为还车贷
    def modify_repay_housing_loan_to_repay_car_loan(self, user_name, login_password, trade_password, last_no,
                                                    repay_amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='N', repay_type='H', repay_plan_id='75')
        self._db.delete_all_unnecessary_plans(id=75)
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='housing_loan')
        self.main_page.go_to_modify_repay_loan_plan_page()
        self.main_page.modify_repay_loan_plan(trade_password=trade_password, last_no=last_no, repay_amount=repay_amount,
                                              repay_type='car_loan')
        self._db.update_plan_status(status='D', repay_plan_id='75')

    # 修改还车贷为还其他贷款
    def modify_repay_car_loan_to_repay_other_loan(self, user_name, login_password, trade_password, last_no,
                                                  repay_amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='N', repay_type='C', repay_plan_id='75')
        self._db.delete_all_unnecessary_plans(id=75)
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='car_loan')
        self.main_page.go_to_modify_repay_loan_plan_page()
        self.main_page.modify_repay_loan_plan(trade_password=trade_password, last_no=last_no, repay_amount=repay_amount,
                                              repay_type='others', other_purpose=u'其他用途')
        self._db.update_plan_status(status='D', repay_plan_id='75')

    # 修改还其他贷款为还房贷
    def modify_repay_other_loan_to_repay_housing_loan(self, user_name, login_password, trade_password, last_no,
                                                      repay_amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='N', repay_type='O', repay_purpose='其他用途', repay_plan_id='75')
        self._db.delete_all_unnecessary_plans(id=75)
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='others')
        self.main_page.go_to_modify_repay_loan_plan_page()
        self.main_page.modify_repay_loan_plan(trade_password=trade_password, last_no=last_no, repay_amount=repay_amount,
                                              repay_type='housing_loan')
        self._db.update_plan_status(status='D', repay_plan_id='75')

    # 删除还贷款计划
    def delete_repay_loan_plan(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_plan_status(status='N', repay_plan_id='75')
        self.main_page.go_to_repay_loan_page()
        self.main_page.go_to_repay_loan_plan_detail_page(repay_type='housing_loan')
        self.main_page.delete_repay_loan_plan(trade_password=trade_password)

    # 现金支付手段买高端(金额正常)
    def buy_vipproduct_use_cash_management_product(self, user_name, login_password, product_name, trade_password,
                                                   amount, cash_management_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            cash_management_product=cash_management_product, cash_management='Y')
        self._db.delete_asset_in_transit(mobile=user_name, prod_name=product_name, balance=amount)

    # 已实名用户绑卡
    def certificated_user_binding_card(self, user_name, login_password, bank_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_bank_card_management_page(device_id=self.device_id)
        self.main_page.go_to_binding_card_detail_page(device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.binding_card(bank_card_no=bank_card_no, mobile=user_name)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='BankCardManagementPage')
        self.main_page.verify_page_title()
        self.main_page.verify_bank_card_details(bank_name='工商银行', last_card_no=bank_card_no[-4:])
        self._db.delete_bank_card(mobile=user_name, card_no=bank_card_no)

    # 现金宝页面点击万份收益,进入万份收益页面
    def view_xjb_income_per_wan(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_interest_page_per_wan()
        self.main_page.verify_at_income_detail_page(title='万份收益')

    # 现金宝页面点击累计收益,进入累计收益页面
    def view_xjb_income_accumulated(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_interest_page_accumulated()
        self.main_page.verify_at_income_detail_page(title='累计收益')

    # 现金宝页面点击七日年化收益率,进入七日年化收益率页面
    def view_xjb_seven_days_annual_rate_of_return(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_seven_days_annual_rate_of_return_page()
        self.main_page.verify_at_income_detail_page(title='七日年化收益率')

    # 查看现金管理系列
    def view_high_end_cash_management_series(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.verify_page_title()
        self.main_page.view_high_end_more_product()
        self.main_page.verify_page_title()
        self.main_page.go_to_cash_management_series_page(series='现金管理系列')
        self.main_page.verify_at_cash_management_series_page()

    # 查看固定收益管理系列
    def view_high_end_fixed_rate_series(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.verify_page_title()
        self.main_page.view_high_end_more_product()
        self.main_page.verify_page_title()
        self.main_page.go_to_fixed_rate_series(series='固定收益系列')
        self.main_page.verify_at_fixed_rate_series_page()

    # 查看精选系列
    def view_high_end_best_recommend_series(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.verify_page_title()
        self.main_page.view_high_end_more_product()
        self.main_page.verify_page_title()
        self.main_page.go_to_best_recommend_series(series='精选系列')
        self.main_page.verify_at_best_recommend_series_page()

    # 查看资产分析
    def view_assets_analysis(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.verify_page_title()
        self.main_page.verify_assets_items()
        # self.main_page.go_to_xjb_detail_page()
        # self.main_page.verify_page_title()
        # self.main_page.back_to_assets_analysis_page()
        # # self.main_page.verify_page_title()
        # self.main_page.go_to_assets_dhb_detail_page()
        # self.main_page.verify_page_title()
        # self.main_page.back_to_assets_analysis_page()
        # # self.main_page.verify_page_title()
        # self.main_page.go_to_assets_fund_detail_page()
        # self.main_page.verify_page_title()
        # self.main_page.back_to_assets_analysis_page()
        # # self.main_page.verify_page_title()
        # self.main_page.go_to_assets_high_end_detail_page()
        # self.main_page.verify_page_title()

    # 下载资产证明
    def download_assets_certification(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_certification_preview_page(trade_password=trade_password)
        # self.main_page.close_alert()
        self.main_page.verify_page_title()
        self.main_page.download_assets_certification()
        self.main_page.verify_alert_title()

    # 持有页面查看产品详情
    def view_product_details(self, user_name, login_password, high_end_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_redeem_page(high_end_product=high_end_product)
        self.main_page.verify_page_title(product_name=high_end_product)
        self.main_page.go_to_product_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_product_name(product_name=high_end_product, product_type='vip')

    # 基金撤单
    def cancel_fund_order(self, user_name, login_password, product_name, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_fund_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_specific_trade_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(product_name=product_name, status='已受理')
        self.main_page.cancel_order(trade_password=trade_password)
        self.main_page.user_operation_complete(return_page='AssetsFundDetailPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_specific_trade_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(product_name=product_name, status='已撤销')

    # 高端撤单
    def cancel_vipproduct_order(self, user_name, login_password, trade_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='买入', product_name=product_name, status='已受理')
        self.main_page.go_to_specific_trade_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(product_name=product_name, status='已受理')
        self.main_page.cancel_order(trade_password=trade_password)
        self.main_page.user_operation_complete(return_page='AssetsHighEndDetailPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='买入', product_name=product_name, status='已撤销')
        self.main_page.go_to_specific_trade_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(product_name=product_name, status='已撤销')

    # 用户绑定银行卡张数为0时绑定信用卡
    def add_credit_card_without_binding_bank_card(self, user_name, login_password, bank_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_page(index='4')
        self.main_page.verify_page_title()
        # self.main_page.go_to_set_trade_password_page()
        # self.main_page.verify_page_title()
        # self.main_page.set_trade_password(trade_password=trade_password)
        # self.main_page.verify_page_title()
        # self.main_page.confirm_trade_password(trade_password=trade_password)
        # self.main_page.verify_page_title()
        self.main_page.go_to_binding_bank_card_page(self.device_id)
        self.main_page.verify_page_title()
        self.main_page.certificated_user_binding_bank_card(bank_card_no=bank_card_no, mobile=user_name)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='CreditCardRepayPage')
        self.main_page.verify_page_title()
        self._db.delete_bank_card(mobile=user_name)

    # 热门页查看全部产品
    def view_all_products(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_page()
        self.main_page.go_to_all_products_page()
        self.main_page.verify_page_title()
        self.main_page.view_all_products()

    # 理财频道全部产品--筛选器
    def all_products_filter(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_page()
        self.main_page.go_to_all_products_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_filter_detail_page()
        self.main_page.verify_filter_details()
        self.main_page.products_filter()
        self.main_page.verify_page_title()
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(amount_type='1分-5万')
        self.main_page.verify_page_title()
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(amount_type='5-100万')
        self.main_page.verify_page_title()
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(amount_type='100万以上')
        self.main_page.verify_page_title()
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(product_type='定活宝')
        self.main_page.verify_page_title()
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(product_type='高端现金管理')
        self.main_page.verify_page_title()
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(product_type='高端固定收益')
        self.main_page.verify_page_title()
        self.main_page.go_to_filter_detail_page()
        self.main_page.products_filter(product_type='高端精选权益')
        self.main_page.verify_page_title()

    # 稳健型用户购买高风险产品(提示加验证码)
    def moderate_user_buy_high_risk_product(self, user_name, login_password, fund_product_name, fund_product_code,
                                            amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.verify_page_title()
        # self.main_page.search_fund_products_with_names(fund_product_name=fund_product_name)
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_purchase_page(risk='high', user_type='moderate'
                                                )
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, risk='high',
                                        user_type='moderate', phone_number=user_name)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='FundPageFundDetail')
        self.main_page.back_to_fund_product_search_page()
        self.main_page.back_to_fund_page()
        self.main_page.go_to_assets_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='买入', product_name=fund_product_name, status='已受理',
                                            amount=amount)

    # 激进型用户购买高风险产品(需输入验证码)
    def radical_user_buy_high_risk_product(self, user_name, login_password, fund_product_name, fund_product_code,
                                           amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.verify_page_title()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_purchase_page()
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, risk='high',
                                        user_type='radical', phone_number=user_name)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='FundPageFundDetail')
        self.main_page.back_to_fund_product_search_page()
        self.main_page.back_to_fund_page()
        self.main_page.go_to_assets_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='买入', product_name=fund_product_name, status='已受理',
                                            amount=amount)

    # 保守型用户购买高风险产品(风险提示且用户不能购买)
    def conservative_user_buy_high_risk_product(self, user_name, login_password, fund_product_name, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.verify_page_title()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_purchase_page(risk='high', user_type='conservative')
        # self.main_page.buy_fund_product(risk='high', user_type='conservative', amount=amount)
        self.main_page.verify_page_title()

    # 谨慎型用户购买中高风险产品(有提示,可以购买)
    def cautious_user_buy_middle_high_risk_product(self, user_name, login_password, fund_product_name,
                                                   fund_product_code, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.verify_page_title()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_purchase_page(user_type='cautious', risk='middle_high')
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, risk='middle_high',
                                        user_type='cautious')
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='FundPageFundDetail')
        self.main_page.back_to_fund_product_search_page()
        self.main_page.back_to_fund_page()
        self.main_page.go_to_assets_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='买入', product_name=fund_product_name, status='已受理',
                                            amount=amount)

    # 现金宝持有页面查看在途资产(资产分析页面进)
    def view_xjb_asset_in_transit(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_asset_in_transit_page()
        self.main_page.verify_page_title()
        self.main_page.verify_asset_in_transit_details()

    # 现金宝持有页面查看产品详情(资产分析页面进)
    def view_xjb_product_detail(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_xjb_product_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_xjb_product_details()

    # 现金宝持有页面查看七日年化收益率曲线(资产分析页面进)
    def view_xjb_seven_days_annual_rate_of_return_curve(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.view_xjb_seven_days_annual_rate_of_return(term='1个月')
        self.main_page.verify_page_title()
        self.main_page.view_xjb_seven_days_annual_rate_of_return(term='3个月')
        self.main_page.verify_page_title()

    # 查看基金资产(资产分析页面进)
    def view_fund_asset(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_fund_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_assets_structure_page()
        self.main_page.verify_page_title()
        self.main_page.verify_fund_assets_structure_details()
        self.main_page.go_to_fund_assets_page(fund_type='混合型')
        self.main_page.verify_page_title()
        self.main_page.verify_fund_assets_details(fund_type='混合型')
        self.main_page.back_to_fund_assets_structure_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_assets_page(fund_type='货币型')
        self.main_page.verify_page_title()
        self.main_page.verify_fund_assets_details(fund_type='货币型')

    # 高端追加购买(资产分析页面进)
    def vipproduct_supplementary_purchase(self, user_name, login_password, high_end_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_high_end_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_high_end_assets_details()
        self.main_page.go_to_high_end_redeem_page(high_end_product=high_end_product)
        self.main_page.verify_page_title(product_name=high_end_product)
        self.main_page.vipproduct_supplementary_purchase()
        self.main_page.verify_page_title()
        self.main_page.verify_product_purchase_page_details(product_name=high_end_product)

    # 定期追加购买(资产分析页面进)
    def dhb_supplementary_purchase(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_analysis_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_dhb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_dhb_assets_details()
        self.main_page.go_to_dqb_supplementary_purchase_page()
        self.main_page.verify_page_title(product_name=product_name)
        self.main_page.verify_dqb_supplementary_purchase_page_details(product_name=product_name)
        self.main_page.dqb_supplementary_purchase()
        self.main_page.verify_page_title()
        self.main_page.verify_product_purchase_page_details(product_name=product_name)

    # 基金追加购买(购买确认中)
    def fund_supplementary_purchase(self, user_name, login_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_supplementary_purchase_page(fund_product=fund_product_name)
        self.main_page.verify_page_title(fund_product=fund_product_name)
        self.main_page.verify_fund_supplementary_purchase_page_details(fund_product=fund_product_name)
        self.main_page.fund_supplementary_purchase()
        self.main_page.verify_page_title()
        self.main_page.verify_fund_purchase_page_details(fund_product=fund_product_name)

    # 未测评用户购买产品(提示先进行风险评测)
    def buy_fund_product_without_risk_evaluation(self, user_name, login_password, fund_product_name, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_fav_fund(mobile=user_name)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_purchase_page()
        self.main_page.verify_risk_indication_details()
        self.main_page.go_to_risk_evaluation_page()
        self.main_page.verify_page_title()

    # 短信验证码登录
    def login_use_verification_code(self, user_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.verify_login_button()
        self.main_page.login_use_verification_code(user_name=user_name, return_page='AssetsPage')
        self.main_page.verify_page_title()

    # 使用优惠券充值
    def recharge_use_coupon(self, user_name, login_password, nonsuperposed_coupon_code, recharge_amount,
                            nonsuperposed_coupon_quantity, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_xjb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.get_xjb_total_assets()
        self.main_page.go_to_recharge_page_from_assets_page()
        self.main_page.verify_page_title()
        self._cms.issue_coupon(code=nonsuperposed_coupon_code, mobile=user_name, quantity=nonsuperposed_coupon_quantity)
        self.main_page.recharge(recharge_amount=recharge_amount, trade_password=trade_password,
                                nonsuperposed_coupon='Y')
        if ASSERT_DICT['success_flag'] != '0':
            self.main_page.verify_page_title()
            self.main_page.user_operation_complete(return_page='AssetsXjbDetailPage')
            self.main_page.verify_xjb_total_assets(amount=recharge_amount)
            self.main_page.go_to_xjb_trade_detail_page()
            self.main_page.verify_trade_record_values(amount=recharge_amount)
        else:
            self.main_page.back_to_xjb_detail_page()
            self.main_page.verify_xjb_total_assets(amount='0')

    # 现金管理系列作为支付手段买基金
    def buy_fund_product_use_cash_management_product(self, user_name, login_password, fund_product_name, amount,
                                                     trade_password, fund_product_code, cash_management_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_purchase_page()
        self.main_page.verify_page_title()
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password,
                                        cash_management_product=cash_management_product)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='FundPageFundDetail')
        self.main_page.verify_page_title()
        self.main_page.back_to_fund_product_search_page()
        self.main_page.back_to_fund_page()
        self.main_page.go_to_assets_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.select_filter_type(filter_type='fund')
        self.main_page.verify_trade_details(trade_type='买入', product_name=fund_product_name, status='已受理',
                                            amount=amount)
        self.main_page.go_to_specific_trade_detail_page(product_name=fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(from_account=cash_management_product, product_name=fund_product_name,
                                            status='已受理')

    # 现金管理系列作为支付手段买定活宝
    def buy_dhb_product_use_cash_management_product(self, user_name, login_password, trade_password, product_name,
                                                    amount, cash_management_product):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_dqb_product_list_page_()
        self.main_page.verify_page_title()
        self.main_page.go_to_finance_product_search_page()
        self.main_page.go_to_product_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_product_name(product_name=product_name, product_type='dhb')
        self.main_page.go_to_product_purchase_page()
        self.main_page.verify_page_title()
        self.main_page.verify_product_purchase_page_details(product_name=product_name)
        self.main_page.buy_finance_product(amount=amount, trade_password=trade_password,
                                           cash_management_product=cash_management_product)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='FinanceDqbPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_trade_detail_page()
        self.main_page.verify_page_title()
        self.main_page.select_filter_type(filter_type='dhb')
        self.main_page.go_to_specific_trade_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(from_account=cash_management_product, product_name=product_name,
                                            status='已受理')

    # 信用卡还款使用优惠券
    def credit_card_repay_use_coupon(self, user_name, login_password, repay_amount, trade_password, last_card_no,
                                     superposed_coupon_code, superposed_coupon_quantity):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_detail_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.verify_credit_card_details(last_card_no=last_card_no)
        self._cms.issue_coupon(code=superposed_coupon_code, mobile=user_name, quantity=superposed_coupon_quantity)
        self.main_page.repay(repay_amount, trade_password, superposed_coupon='Y')
        self.main_page.user_operation_complete(return_page='CreditCardRepayPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_detail_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_record_page()
        self.main_page.verify_page_title(last_card_no=last_card_no)
        self.main_page.verify_credit_card_repay_record_details(last_card_no=last_card_no, amount=repay_amount)

    # 查看现金宝资产的说明
    def view_xjb_holding_assets_description(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_description_page()
        self.main_page.verify_page_title()
        self.main_page.verify_description(type='xjb')
        self.main_page.back_to_assets_xjb_detail_page(return_page='AssetsXjbDetailPage')
        self.main_page.verify_page_title()

    # 查看定活宝资产的说明
    def view_dhb_holding_assets_description(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_description_page()
        self.main_page.verify_page_title()
        self.main_page.verify_description(type='dhb')
        self.main_page.back_to_assets_xjb_detail_page(return_page='AssetsDqbDetailPage')
        self.main_page.verify_page_title()

    # 查看基金资产的说明
    def view_fund_holding_assets_description(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_assets_fund_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_description_page()
        self.main_page.verify_page_title()
        self.main_page.verify_description(type='fund')
        self.main_page.back_to_assets_xjb_detail_page(return_page='AssetsFundDetailPage')
        self.main_page.verify_page_title()

    # 查看高端资产的说明
    def view_vipproduct_holding_assets_description(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_description_page()
        self.main_page.verify_page_title()
        self.main_page.verify_description(type='vip')
        self.main_page.back_to_assets_xjb_detail_page(return_page='AssetsHighEndDetailPage')
        self.main_page.verify_page_title()

    # 定投排行
    def view_fund_plan_rankings(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_plan_ranking_page()
        self.main_page.verify_fund_plan_rankings_details()
        self.main_page.view_fund_plan_rankings(fund_type='股票型')

    # 信用卡预约还款使用优惠券(理财日历页面进)
    def credit_card_reserved_pay_use_nonsuperposed_coupon(self, user_name, login_password, reserved_pay_amount,
                                                          trade_password, last_card_no, nonsuperposed_coupon_code,
                                                          nonsuperposed_coupon_quantity):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        count = self._db.check_creditcard_reserve_repay_normal_order(mobile=user_name, state='N')
        if count > 0:
            self._db.delete_noc_builder_useless_data(user_name=user_name, type='reserve_pay')
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_financing_calendar_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_personal_matters_setting_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_credit_card_repay_detail_page(last_card_no=last_card_no)
        self.main_page.verify_page_title()
        self.main_page.go_to_reserved_pay_page()
        self.main_page.verify_page_title()
        self._cms.issue_coupon(code=nonsuperposed_coupon_code, mobile=user_name, quantity=nonsuperposed_coupon_quantity)
        self.main_page.verify_credit_card_details(last_card_no=last_card_no)
        self.main_page.reserved_pay(reserved_pay_amount, trade_password, coupon='nonsuperposed')
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='CreditCardRepayPage')
        self.main_page.verify_credit_card_repay_details(reserved_pay_amount=reserved_pay_amount)
        self.main_page.back_to_personal_matters_setting_page()
        self.main_page.verify_page_title()
        self.main_page.back_to_financing_calender_page()
        self.main_page.verify_page_title()
        self.main_page.back_to_home_page()
        self.main_page.verify_financing_calendar_items(item='信用卡预约还款', reserved_pay_amount=reserved_pay_amount,
                                                       last_card_no=last_card_no)

    # 滑动理财日历
    def swipe_financing_calender(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.click_more_go_to_financing_calendar_page()
        self.main_page.swipe_calendar(month='10', swipe_direction='L')
        self.main_page.verify_page_title()
        self.main_page.swipe_calendar(month='08', swipe_direction='R')
        self.main_page.verify_page_title()
        self.main_page.select_calendar_date()
        self.main_page.verify_calender_date()
        self.main_page.verify_page_title()

    # 定活宝收益计算器
    def dhb_income_calculator(self, user_name, login_password, product_name, amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_dqb_detail_page()
        self.main_page.go_to_dqb_supplementary_purchase_page_(product_name=product_name)
        self.main_page.go_to_product_detail_page()
        self.main_page.verify_page_title()
        self.main_page.income_calculator(amount=amount)
        if float(amount) >= ASSERT_DICT['min']:
            self.main_page.go_to_product_purchase_page_by_income_calculator()
            self.main_page.verify_page_title()
            self.main_page.verify_purchase_amount(amount=amount)

    # 高端收益计算器
    def high_end_income_calculator(self, user_name, login_password, product_name, amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_high_end_supplementary_purchase_page_(product_name=product_name)
        self.main_page.go_to_product_detail_page()
        self.main_page.verify_page_title()
        self.main_page.income_calculator(amount=amount, product_type='VIP')
        if float(amount) >= ASSERT_DICT['min']:
            self.main_page.go_to_product_purchase_page_by_income_calculator()
            self.main_page.verify_page_title()
            self.main_page.verify_purchase_amount(amount=amount)

    # 查看非货币性基金业绩及历史净值(基金频道页面进)
    def view_non_monetary_fund_performance(self, user_name, login_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products_with_names(fund_product_name=fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.check_fund_basic_information(fund_product_name=fund_product_name, fund_type='混合型')
        self.main_page.go_to_product_history_income_page()
        self.main_page.verify_page_title(fund_product_name=fund_product_name)
        self.main_page.view_product_history_income()
        self.main_page.back_to_product_detail_page()
        self.main_page.verify_page_title()
        self.main_page.view_non_monetary_fund_details(detail_type='业绩')

    # 查看非货币性基金公告
    def view_non_monetary_fund_notice(self, user_name, login_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products_with_names(fund_product_name=fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.view_non_monetary_fund_details(detail_type='公告')
        self.main_page.go_to_fund_notice_page()
        self.main_page.verify_page_title()
        self.main_page.back_to_product_detail_page()
        self.main_page.verify_page_title()
        self.main_page.view_monetary_fund_details(detail_type='概况')
        self.main_page.view_monetary_fund_details(detail_type='组合')
        self.main_page.view_monetary_fund_details(detail_type='费率')

    # 查看货币性基金业绩及历史收益(全部基金页面进)
    def view_monetary_fund_performance(self, user_name, login_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_page_all_fund_page()
        self.main_page.select_fund_type(fund_type='货币型')
        self.main_page.go_to_fund_detail_page(fund_product_name=fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.check_fund_basic_information(fund_product_name=fund_product_name, fund_type='货币型')
        self.main_page.go_to_product_history_income_page()
        self.main_page.verify_page_title(fund_product_name=fund_product_name)
        self.main_page.view_product_history_income(product_type='货币型')
        self.main_page.back_to_product_detail_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_product_history_income_page(type='TextView')
        self.main_page.verify_page_title(fund_product_name=fund_product_name)
        self.main_page.back_to_product_detail_page()
        self.main_page.view_monetary_fund_details(detail_type='业绩')

    # 查看货币性基金公告
    def view_monetary_fund_notice(self, user_name, login_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_page_all_fund_page()
        self.main_page.select_fund_type(fund_type='货币型')
        self.main_page.go_to_fund_detail_page(fund_product_name=fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.view_monetary_fund_details(detail_type='公告')
        self.main_page.go_to_fund_notice_page()
        self.main_page.verify_page_title()
        self.main_page.back_to_product_detail_page()
        self.main_page.verify_page_title()
        self.main_page.view_monetary_fund_details(detail_type='概况')
        self.main_page.view_monetary_fund_details(detail_type='组合')
        self.main_page.view_monetary_fund_details(detail_type='费率')

    # 查看高端精选系列产品基础信息
    def view_high_end_best_recommend_basic_information(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        self.main_page.go_to_best_recommend_series(series='精选系列')
        self.main_page.verify_at_best_recommend_series_page()
        self.main_page.go_to_product_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_product_basic_information(product_name=product_name)

    # 查看高端精选系列产品业绩等其他详情信息
    def view_high_end_best_recommend_performance(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        self.main_page.go_to_best_recommend_series(series='精选系列')
        self.main_page.verify_at_best_recommend_series_page()
        self.main_page.go_to_product_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_product_other_information(product_name=product_name, detail_type='业绩')
        self.main_page.verify_product_other_information(product_name=product_name, detail_type='投资经理')
        self.main_page.verify_product_other_information(product_name=product_name, detail_type='规则')
        self.main_page.verify_product_other_information(product_name=product_name, detail_type='合同公告')

    # 查看高端精选系列产品历史净值
    def view_high_end_best_recommend_history_nav(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_finance_product_search_page()
        self.main_page.go_to_product_detail_page(product_name=product_name)
        self.main_page.go_to_high_end_history_income_page()
        self.main_page.verify_page_title(product_type='vip')
        self.main_page.view_product_history_income(product_type='精选系列')
        self.main_page.back_to_product_detail_page(return_page='ProductDetailPage', product_type='vip')
        self.main_page.verify_page_title()

    # 查看高端现金管理系列产品基础信息
    def view_high_end_cash_management_basic_information(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        self.main_page.go_to_cash_management_series_page(series='现金管理系列')
        self.main_page.verify_at_cash_management_series_page()
        self.main_page.go_to_product_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_product_basic_information(product_name=product_name, product_type='现金管理系列')

    # 查看高端现金管理系列产品历史收益
    def view_high_end_cash_management_history_income(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        # self.main_page.go_to_high_end_product_introduction_page()
        # self.main_page.verify_page_title()
        # self.main_page.go_to_finance_high_end_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_cash_management_series_page(series='现金管理系列')
        self.main_page.verify_at_cash_management_series_page()
        self.main_page.go_to_product_detail_page(product_name=product_name)
        self.main_page.go_to_high_end_history_income_page()
        self.main_page.verify_page_title(product_type='现金管理系列')
        self.main_page.view_product_history_income(product_type='现金管理系列')
        self.main_page.back_to_product_detail_page(return_page='ProductDetailPage', product_type='vip')
        self.main_page.verify_page_title()

    # 查看固定收益系列产品详情
    def view_high_end_fixed_rate_product_details(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_fixed_rate_series(series='固定收益系列')
        self.main_page.verify_at_fixed_rate_series_page()
        self.main_page.go_to_product_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.verify_product_basic_information(product_name=product_name, product_type='固定收益系列')
        self.main_page.go_to_frequently_asked_question_page()
        self.main_page.verify_page_title()
        self.main_page.view_question_detail()
        self.main_page.back_to_product_detail_page()
        self.main_page.verify_page_title(product_name=product_name)

    # 未登录状态验证
    def check_not_login_status_details(self):
        self.main_page.go_to_home_page()
        self.main_page.go_to_assets_page()
        self.main_page.check_not_login_status_details()
        self.main_page.go_to_personal_setting_page()
        self.main_page.verify_page_title()
        self.main_page.back_to_assets_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_login_page()
        self.main_page.verify_login_button()

    # 查看基金历史持仓
    def view_fund_history_holding(self, user_name, login_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_history_holding_page()
        self.main_page.verify_fund_history_holding_detail(fund_product=fund_product_name)
        self.main_page.go_to_history_holding_page(fund_product=fund_product_name)
        self.main_page.verify_page_title(product_name=fund_product_name)
        self.main_page.verify_history_holding_page_details()
        self.main_page.verify_page_title(product_name=fund_product_name)

    # 查看定活宝历史持仓
    def view_dhb_history_holding(self, user_name, login_password, product_name, name, risk_type):
        self.main_page.go_to_home_page()
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_login_page()
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
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_dhb_history_holding_list_page()
        self.main_page.verify_vip_history_holding_detail(product_name=product_name)
        self.main_page.go_to_history_holding_page(product_name=product_name)
        self.main_page.verify_page_title(product_name=product_name)
        self.main_page.verify_history_holding_page_details(product_type='vip')
        self.main_page.back_to_high_end_holding_list_page()
        self.main_page.verify_page_title()
        self.main_page.back_to_assets_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_personal_setting_page()
        self.main_page.logout()
        self.main_page.go_to_assets_page()
        self.main_page.verify_page_title()
        self.main_page.check_not_login_status_details()

    # 基金分红方式切换
    def fund_dividend_type_switch(self, user_name, login_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_redeem_page(fund_product=fund_product_name)
        self.main_page.fund_dividend_type_switch(dividend_type='红利再投')
        self.main_page.fund_dividend_type_switch(dividend_type='现金分红')

    # 基金极速转换
    def fund_fast_convert(self, user_name, login_password, fund_convert_from, fund_convert_to, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_redeem_page(fund_product=fund_convert_from)
        self.main_page.go_to_select_convert_to_fund_page()
        self.main_page.verify_page_title()
        # self.main_page.go_to_fund_convert_page(fund_product=fund_convert_to)
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products_with_names(fund_product_name=fund_convert_to)
        self.main_page.verify_page_title(operation_type='fund_convert')
        self.main_page.verify_fund_convert_details(fund_convert_from=fund_convert_from, fund_convert_to=fund_convert_to)
        self.main_page.fund_convert(amount=amount, trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='FundRedeemPage')
        self.main_page.verify_page_title(fund_product=fund_convert_from)
        # self.main_page.back_to_fund_redeem_page()
        # self.main_page.verify_page_title()
        self.main_page.verify_available_amount()
        self.main_page.go_to_trade_records_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='极速转换', status='已受理', amount=amount,
                                            product_name=fund_convert_to)
        self.main_page.go_to_specific_trade_detail_page(product_name=fund_convert_to)
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(product_name=fund_convert_to, status='已受理', from_account=fund_convert_from)

    # 基金普通转换
    def fund_normal_convert(self, user_name, login_password, fund_convert_from, fund_convert_to, amount,
                            trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_redeem_page(fund_product=fund_convert_from)
        self.main_page.go_to_select_convert_to_fund_page()
        self.main_page.verify_page_title()
        # self.main_page.go_to_fund_convert_page(fund_product=fund_convert_to)
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products_with_names(fund_product_name=fund_convert_to)
        self.main_page.verify_page_title(operation_type='fund_convert')
        self.main_page.verify_fund_convert_details(fund_convert_from=fund_convert_from, fund_convert_to=fund_convert_to,
                                                   convert_type='normal')
        self.main_page.fund_convert(amount=amount, trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='FundRedeemPage')
        self.main_page.verify_page_title(fund_product=fund_convert_from)
        # self.main_page.back_to_fund_redeem_page()
        # self.main_page.verify_page_title()
        self.main_page.verify_available_amount()
        self.main_page.go_to_trade_records_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='普通转换', status='已受理', amount=amount,
                                            product_name=fund_convert_to)
        self.main_page.go_to_specific_trade_detail_page(product_name=fund_convert_to)
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(product_name=fund_convert_to, status='已受理', from_account=fund_convert_from)

    # 基金极速转换撤单
    def cancel_fund_fast_convert_order(self, user_name, login_password, fund_convert_from, fund_convert_to,
                                       trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_redeem_page(fund_product=fund_convert_from)
        self.main_page.go_to_trade_records_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='极速转换', status='已受理', product_name=fund_convert_to)
        self.main_page.go_to_specific_trade_detail_page(product_name=fund_convert_to)
        self.main_page.cancel_order(trade_password=trade_password)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='FundRedeemPage')
        self.main_page.verify_page_title(fund_product=fund_convert_from)
        self.main_page.go_to_trade_records_page()
        # self.main_page.verify_trade_details(trade_type='极速转换', status='已撤销',product_name=fund_product)
        self.main_page.go_to_specific_trade_detail_page(product_name=fund_convert_to)
        self.main_page.verify_trade_details(product_name=fund_convert_to, status='已撤销', to_detail='已撤单')

    # 基金普通转换撤单
    def cancel_fund_normal_convert_order(self, user_name, login_password, fund_convert_from, fund_convert_to,
                                         trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_redeem_page(fund_product=fund_convert_from)
        self.main_page.go_to_trade_records_page()
        self.main_page.verify_page_title()
        self.main_page.verify_trade_details(trade_type='普通转换', status='已受理', product_name=fund_convert_to)
        self.main_page.go_to_specific_trade_detail_page(product_name=fund_convert_to)
        self.main_page.cancel_order(trade_password=trade_password, trade_type='fund_normal_convert')
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='FundRedeemPage')
        self.main_page.verify_page_title(fund_product=fund_convert_from)
        self.main_page.verify_available_amount()
        self.main_page.go_to_trade_records_page()
        self.main_page.go_to_specific_trade_detail_page(product_name=fund_convert_to)
        self.main_page.verify_trade_details(product_name=fund_convert_to, status='已撤销', to_detail='已撤单')

    # 理财型基金到期处理方式切换(全部赎回至现金宝切换为部分赎回至现金宝)
    def financial_fund_expiry_processing_all_to_part(self, user_name, login_password, fund_product_name,
                                                     fund_product_code, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self._db.update_cts_prod_renew(user_name=user_name, fund_id=fund_product_code, value_date='20170908',
                                       due_process_type='AR', red_amt='1000000.00')
        self.main_page.go_to_fund_redeem_page(fund_product=fund_product_name)
        self.main_page.verify_expiry_processing_type_details(processing_type='全部赎回至现金宝', expiry_date='12月29日')
        self.main_page.go_to_expiry_processing_type_page(processing_type='全部赎回至现金宝')
        self.main_page.verify_page_title()
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='全部赎回至现金宝',
                                                        expiry_dispose_amount='1,000,000.00')
        self.main_page.product_expiry_processing_type_switch(switch_to='部分赎回至现金宝', expiry_redeem_amount='1000',
                                                             trade_password=trade_password)
        self.main_page.verify_page_title(fund_product=fund_product_name)
        self.main_page.verify_expiry_processing_type_details(processing_type='部分赎回至现金宝', expiry_date='12月29日')

    # 理财型基金到期处理方式切换(部分赎回至现金宝切换为自动续存)
    def financial_fund_expiry_processing_part_to_automatic(self, user_name, login_password, fund_product_name,
                                                           fund_product_code, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self._db.update_cts_prod_renew(user_name=user_name, fund_id=fund_product_code, value_date='20170908',
                                       due_process_type='AR', red_amt='1,000.00')
        self.main_page.go_to_fund_redeem_page(fund_product=fund_product_name)
        self.main_page.verify_expiry_processing_type_details(processing_type='部分赎回至现金宝', expiry_date='12月29日')
        self.main_page.go_to_expiry_processing_type_page(processing_type='部分赎回至现金宝')
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='部分赎回至现金宝',
                                                        expiry_dispose_amount='1,000.00')
        self.main_page.product_expiry_processing_type_switch(switch_to='自动续存', trade_password=trade_password)
        self.main_page.verify_expiry_processing_type_details(processing_type='自动续存', expiry_date='12月29日')

    # 理财型基金到期处理方式切换(自动续存转全部赎回至现金宝)
    def financial_fund_expiry_processing_automatic_to_all(self, user_name, login_password, fund_product_name,
                                                          fund_product_code, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_detail_page()
        self._db.update_cts_prod_renew(user_name=user_name, fund_id=fund_product_code, value_date='20170908',
                                       due_process_type='AO', red_amt='0.00')
        self.main_page.go_to_fund_redeem_page(fund_product=fund_product_name)
        self.main_page.verify_expiry_processing_type_details(processing_type='自动续存', expiry_date='12月29日')
        self.main_page.go_to_expiry_processing_type_page(processing_type='自动续存')
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='自动续存')
        self.main_page.product_expiry_processing_type_switch(switch_to='全部赎回至现金宝', trade_password=trade_password)
        self.main_page.verify_expiry_processing_type_details(processing_type='全部赎回至现金宝', expiry_date='12月29日')

    # 设置-修改个人信息
    def modify_personal_information(self, user_name, login_password, email, address):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_information_page(device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.modify_personal_photo()
        self.main_page.go_to_email_page()
        self.main_page.verify_page_title()
        self.main_page.modify_email_address(email=email)
        self.main_page.verify_page_title()
        self.main_page.go_to_address_page()
        self.main_page.verify_page_title()
        self.main_page.modify_residential_address(address=address)
        self.main_page.verify_page_title()
        self.main_page.verify_personal_information_details(email=email, address=u'北京市县密云县南京西路399号')

    # 用户使用通行证实名/修改用户信息
    def bank_card_manage_binding_card_use_laissez_passer(self, user_name, login_password, banding_card_user_name,
                                                         laissez_passer_no, trade_password, modified_name,
                                                         modified_id_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.verify_page_title()
        self.main_page.verify_bind_card_status()
        self.main_page.go_to_bank_card_management_page(device_id=self.device_id)
        self.main_page.go_to_set_trade_password_page()
        self.main_page.set_trade_password(trade_password=trade_password)
        self.main_page.confirm_trade_password(trade_password=trade_password)
        self.main_page.input_id_information_manually(device_id=self.device_id)
        self.main_page.binding_card_input_user_information(banding_card_user_name=banding_card_user_name,
                                                           id_no=laissez_passer_no, id_type='laissez_passer')
        self.main_page.verify_user_information(user_name=banding_card_user_name, id_no=laissez_passer_no,
                                               id_type='HK_laissez_passer')
        self.main_page.modify_user_information()
        self.main_page.binding_card_input_user_information(banding_card_user_name=modified_name, id_no=modified_id_no,
                                                           id_type='laissez_passer')
        self.main_page.verify_user_information(user_name=modified_name, id_no=modified_id_no,
                                               id_type='T_laissez_passer')

    # 基金热门主题
    def view_fund_hot_topics(self, fund_product_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_hot_topics_page()
        self.main_page.verify_page_title()
        self.main_page.verify_page_illustration()
        self.main_page.go_to_topic_detail_page()
        self.main_page.verify_page_illustration()
        self.main_page.go_to_fund_detail_page(fund_product=fund_product_name)
        self.main_page.verify_page_title()
        self.main_page.back_to_fund_topic_detail_page()
        self.main_page.verify_page_title()

    # 高端报价式产品修改到期处理方式(全部退出切换为部分退出)(产品处于续约日期前5个工作日,持有列表页面进)
    def high_end_quotation_product_expiry_processing_all_to_part(self, user_name, login_password, trade_password,
                                                                 product_code):
        date = self.get_today_date()
        new_work_date = self._db.judge_is_work_date(day=date)
        self._db.modify_expire_date(user_name=user_name, product_id=product_code, value_date='20170908',
                                    expired_date=str(new_work_date[0]['WORK_DATE']))
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_cts_prod_renew(user_name=user_name, fund_id=product_code, value_date='20170908',
                                       due_process_type='AR', red_amt='1000000.00')
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.verify_page_title()
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='到期退出', product_type='vip')
        self.main_page.product_expiry_processing_type_switch(switch_to='部分退出', trade_password=trade_password,
                                                             product_type='vip', expiry_redeem_amount='10,000.00',
                                                             return_page='AssetsHighEndDetailPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='到期退出', expiry_dispose_amount='10,000.00',
                                                        product_type='vip')

    # 高端报价式产品修改到期处理方式(部分退出切换为自动续存)(持有列表页面进)
    def high_end_quotation_product_expiry_processing_part_to_auto(self, user_name, login_password, trade_password,
                                                                  product_code):
        date = self.get_today_date()
        new_work_date = self._db.judge_is_work_date(day=date)
        self._db.modify_expire_date(user_name=user_name, product_id=product_code, value_date='20170908',
                                    expired_date=new_work_date)
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_cts_prod_renew(user_name=user_name, fund_id=product_code, value_date='20170908',
                                       due_process_type='AR', red_amt='10000.00')
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.product_expiry_processing_type_switch(switch_to='自动续存', trade_password=trade_password,
                                                             product_type='vip', return_page='AssetsHighEndDetailPage')
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='自动续存', product_type='vip')

    # 高端报价式产品修改到期处理方式(自动续存切换为全部退出)(持有列表页面进)
    def high_end_quotation_product_expiry_processing_auto_to_all(self, user_name, login_password, trade_password,
                                                                 product_code):
        date = self.get_today_date()
        new_work_date = self._db.judge_is_work_date(day=date)
        self._db.modify_expire_date(user_name=user_name, product_id=product_code, value_date='20170908',
                                    expired_date=new_work_date)
        self.old_user(user_name=user_name, login_password=login_password)
        self._db.update_cts_prod_renew(user_name=user_name, fund_id=product_code, value_date='20170908',
                                       due_process_type='AO', red_amt='0.00')
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.product_expiry_processing_type_switch(switch_to='全部退出', trade_password=trade_password,
                                                             expiry_redeem_amount='1,000,000.00',
                                                             product_type='vip', return_page='AssetsHighEndDetailPage')
        self.main_page.go_to_expiry_processing_type_page()
        self.main_page.verify_expiry_processing_details(expiry_dispose_type='到期退出',
                                                        expiry_dispose_amount='1,000,000.00',
                                                        product_type='vip')

    # 税收居民身份申明
    def tax_dweller_identity_declaration(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_user_account_information_page()
        self.main_page.verify_page_title()
        self.main_page.go_to_identity_declaration_page()
        self.main_page.verify_page_title()
        self.main_page.select_tax_dweller_identity(identity='既为中国税收居民又是其他国家（地区）税收居民')
        self.main_page.verify_tax_dweller_identity_result()
        self.main_page.select_tax_dweller_identity(identity='仅为非居民')
        self.main_page.verify_tax_dweller_identity_result()
        self.main_page.select_tax_dweller_identity(identity='仅为中国税收居民')

    # 现金宝充值银行通道重新签约
    def bank_channel_resign(self, user_name, login_password, recharge_amount, trade_password, card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_recharge_page_from_assets_page(return_page='WhatIsXjbPage')
        self.main_page.verify_page_title()
        self.main_page.go_to_recharge_page()
        self.main_page.verify_page_title()
        self.main_page.recharge(recharge_amount=recharge_amount, trade_password=trade_password, type='resign')
        self.main_page.verify_page_title(last_no=card_no[-4:])
        self.main_page.resign(mobile=user_name)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='RechargePage')
        self.main_page.verify_page_title()

    # 充值落地页查看博时详情
    def recharge_landing_page_view_fund_details(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_recharge_page_from_assets_page(return_page='WhatIsXjbPage')
        self.main_page.verify_page_title()
        self.main_page.verify_page_content_details()
        self.main_page.go_to_xjb_product_detail_page()
        self.main_page.verify_page_title()
        self.main_page.verify_xjb_product_details()

    # 首页全局搜索
    def home_page_global_search(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_home_page_from_assets_page()
        self.main_page.go_to_global_search_page()
        self.main_page.global_search(product=u'产品')
        self.main_page.search_view_more_result(product_type='高端理财', return_page='FinanceProductSearchPage')
        self.main_page.go_to_product_detail_page_default_first(product='高端理财')
        self.main_page.verify_page_title()
        self.main_page.back_to_finance_product_search_page()
        self.main_page.back_to_home_page()

        self.main_page.go_to_global_search_page()
        self.main_page.global_search(product=u'0')
        self.main_page.search_view_more_result(product_type='定活宝', return_page='FinanceProductSearchPage')
        self.main_page.go_to_product_detail_page_default_first(product='定活宝')
        self.main_page.verify_page_title()
        self.main_page.back_to_finance_product_search_page()
        self.main_page.back_to_home_page()

        self.main_page.go_to_global_search_page()
        self.main_page.global_search(product=u'B')
        self.main_page.verify_search_result()
        self.main_page.search_view_more_result(product_type='基金', return_page='FundProductSearchPage')
        self.main_page.go_to_fund_detail_page()
        self.main_page.verify_page_title()

    # 安全中心查看登录记录
    def security_center_view_login_record(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_security_center_page()
        self.main_page.go_to_login_record_page()
        self.main_page.verify_page_title()
        self.main_page.view_login_records(device_id=self.device_id)

    # 查看新发基金
    def view_newly_raised_funds(self, product_name):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.verify_newly_raised_fund_details()
        self.main_page.go_to_newly_raised_funds_page()
        self.main_page.verify_page_title()
        self.main_page.verify_newly_raised_fund_details(product_name=product_name)
        self.main_page.go_to_fund_detail_page(product_name=product_name)
        self.main_page.verify_page_title()
        self.main_page.view_newly_raised_fund_details()

    # 查看市场指数(基金频道底部进)
    def view_market_index(self, csi_index):
        self.main_page.go_to_home_page()
        self.main_page.go_to_fund_page()
        self.main_page.verify_index_name(index_name='上证指数')
        self.main_page.verify_index_name(index_name='深证成指')
        self.main_page.go_to_market_index_page(name='深证成指')
        self.main_page.verify_page_title()
        self.main_page.verify_index_type(index_type='综合指数', index_name='上证指数')
        self.main_page.verify_index_type(index_type='上证指数', index_name='上证50')
        self.main_page.verify_index_type(index_type='中证指数', index_name='中证100')
        self.main_page.verify_index_type(index_type='深证指数', index_name='深证综指')
        self.main_page.verify_index_type(index_type='Shibor', index_name='隔夜利率')
        self.main_page.fund_market_index(csi_index=csi_index)

    # 查看未实名用户账户信息,实名之后,再次查看
    def view_user_account_information(self, user_name, name, login_password, trade_password,
                                      id_no, band_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_user_account_information_page()
        self.main_page.view_user_account_information(title='姓名', content='未实名', type='uncertificated')
        self.main_page.view_user_account_information(title='证件类型', content='未实名', type='uncertificated')
        self.main_page.view_user_account_information(title='证件号码', content='未实名', type='uncertificated')
        self.main_page.view_user_account_information(title='资金账户', content='未绑定', type='uncertificated')
        self.main_page.view_user_account_information(title='风险测评', content='未测评', type='uncertificated')
        self.main_page.view_user_account_information(title='税收居民身份声明', content='待填写', type='uncertificated')
        self.main_page.back_to_personal_setting_page()
        self.main_page.verify_page_title()
        self.main_page.back_to_assets_page()
        self.main_page.go_to_setting_trade_password_page()
        self.main_page.verify_page_title()
        self.main_page.set_trade_password(trade_password=trade_password)
        self.main_page.confirm_trade_password(trade_password=trade_password)
        self.main_page.input_id_information_manually(device_id=self.device_id)
        self.main_page.binding_card_input_user_information(banding_card_user_name=name, id_no=id_no)
        self.main_page.binding_card_first_time(bank_card_no=band_card_no, mobile=user_name)
        self.main_page.binding_card_confirm()
        self.main_page.verify_page_title()
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_user_account_information_page()
        name_char = name[-1:]
        id_char = id_no[-4:]
        self.main_page.view_user_account_information(title='姓名', content=name_char, type='certificated')
        self.main_page.view_user_account_information(title='证件类型', content='身份证', type='certificated')
        self.main_page.view_user_account_information(title='证件号码', content=id_char, type='certificated')
        self.main_page.view_user_account_information(title='资金账户', content='未绑定', type='certificated')
        self.main_page.view_user_account_information(title='电子签名约定书', content='签署时间', type='certificated')
        self.main_page.view_user_account_information(title='风险测评', content='未测评', type='certificated')
        self.main_page.view_user_account_information(title='税收居民身份申明', content='待填写', type='certificated')

    # 开启短信验证码登录方式
    def lock_sms_login_mode(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_security_center_page()
        self.main_page.go_to_login_mode_page()
        self.main_page.verify_page_title()
        self.main_page.modify_login_mode(mode='off')
        self.main_page.back_to_security_center_page()
        self.main_page.verify_page_title()
        self.main_page.back_to_personal_setting_page()
        self.main_page.verify_page_title()
        self.main_page.logout()
        self.main_page.go_to_assets_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_login_page()
        self.main_page.login_use_verification_code(user_name=user_name, mode='off')
        self.main_page.verify_login_button()

    # 开启短信验证码登录方式
    def unlock_sms_login_mode(self, user_name, login_password, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_security_center_page()
        self.main_page.go_to_login_mode_page()
        self.main_page.modify_login_mode(mode='on', trade_password=trade_password)
        self.main_page.back_to_security_center_page()
        self.main_page.back_to_personal_setting_page()
        self.main_page.logout()
        self.main_page.go_to_assets_page()
        self.main_page.go_to_login_page()
        self.main_page.login_use_verification_code(mode='on', return_page='AssetsPage')
        self.main_page.verify_page_title()

    # 修改手机号码(不能接收短信)
    def modify_mobile_without_sms(self, user_name, login_password, mobile_new):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_setting_page()
        self.main_page.go_to_setting_modify_mobile_page(device_id=self.device_id)
        # self.main_page.verify_page_title(title='验证交易密码')
        # self.main_page.confirm_trade_password(trade_password=trade_password, return_page='SettingModifyMobilePage',
        #                                       device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.go_to_upload_materials_page(device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.upload_photo(return_page='SetPhoneNumberPage')
        self.main_page.verify_page_title()
        self.main_page.set_phone_number(mobile_new=mobile_new)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='PersonalSettingPage')
        self.main_page.verify_page_title()

    # 购买高端产品超过500万(,风险提示,短信验证码,可以购买)
    def buy_vip_product_exceed_five_million(self, user_name, login_password, product_name, amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        self.main_page.go_to_product_detail_page(product_name=product_name)
        self.main_page.go_to_product_purchase_page()
        self.main_page.buy_finance_product(amount=amount)

    # 购买高风险产品,金额超过500万,且年纪超过70岁(风险提示,短信验证码,可以购买)
    def buy_high_risk_product_exceed_five_million_and_over_seventy_years_old(self, user_name, login_password, fund_code,
                                                                             fund_product, amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_product_search_page()
        self.main_page.search_fund_products(fund_product_name=fund_product, fund_product_code=fund_code)
        self.main_page.go_to_fund_purchase_page()
        self.main_page.buy_fund_product(amount=amount, risk='high', user_type='radical', age='70')

    # 现金宝存入,使用新卡付款
    def recharge_use_new_bank_card(self, user_name, login_password, bank_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_xjb_detail_page()
        self.main_page.get_xjb_total_assets()
        self.main_page.go_to_recharge_page_from_assets_page()
        self.main_page.add_new_bank_card(device_id=self.device_id)
        self.main_page.verify_page_title()
        self.main_page.binding_card(bank_card_no=bank_card_no, mobile=user_name)
        self.main_page.verify_page_title()
        self.main_page.user_operation_complete(return_page='RechargePage')
        self.main_page.verify_page_title()
        self.main_page.verify_bank_card_info(last_card_no=bank_card_no[-4:])
        self._db.delete_bank_card(mobile=user_name, card_no=bank_card_no)


if __name__ == '__main__':
    # phone_number = Utility.GetData().mobile()
    # mobile_new = Utility.GetData().mobile()
    # user_name = Utility.GetData().english_name()
    # modified_user_name = Utility.GetData().english_name()
    # id_no = Utility.GetData().id_no()
    # modified_id_no = Utility.GetData().id_no()

    bank_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]
    # bank_card_no_nan_yue = Utility.GetData().bank_card_no(card_bin='623595').split('-')[0]

    # user_new, login_password = RestfulXjbTools().register(mobile=phone_number, login_password='a0000000')

    # user_new, login_password, trade_password, card_no = RestfulXjbTools().new_user(user_name=phone_number,
    #                                                                                login_password='a0000000',
    #                                                                                card_bin='622202',
    #                                                                                trade_password='135790')

    app_path = GlobalController.XJB_CONNECT
    platform_version = '6.0'
    # device_id = 'ae9b496c'  # vivo
    device_id = 'ac3997d9'  # 小米
    # device_id = '546703b0'  # DX小米
    # device_id = '3eb2fc1f'  # note3
    # device_id = 'PBV7N16924004496'  # 华为
    # device_id='141d7a62'   # 联想
    # device_id = '546703b0'  # vivo
    # device_id = '2895b262'  # 酷派
    # device_id = '3eb2fc1f'  # 红米
    # device_id = '7N2TDM1557021079'  # honor

    port = '4725'
    package_name = 'com.shhxzq.xjb'

    m = AndroidXjbTools30(app_path='', platform_version=platform_version, device_id=device_id, port=port,
                          package_name=package_name, app_status='N', os='Android')

    try:
        user = GlobalConfig.XjbAccountInfo.XJB_CI_USER_1  # 华为
        # user = GlobalConfig.XjbAccountInfo.XJB_CI_USER_2  # vivo
        # user = GlobalConfig.XjbAccountInfo.XJB_UAT_USER_2  # UAT
        # user = GlobalConfig.XjbAccountInfo.XJB_UAT_USER_1  # UAT

        # m.use_coupon_from_my_coupon_list(user_name=user['u1']['user_name'], login_password=user['u1']['login_password'])

        # m.history_coupon_list(user_name=user['u1']['user_name'], password=user['u1']['login_password'])

        # #
        # m.coupon_description(user_name=user['u1']['user_name'], password=user['u1']['login_password'])
        #
        # 现金宝存入--首页(金额符合)
        # m.home_page_recharge(user_name=user['u1']['user_name'],
        #                      login_password=user['u1']['login_password'],
        #                      recharge_amount='1.00',
        #                      trade_password=user['u1']['trade_password'])

        # # 现金宝存入--首页(金额小于最小限额)
        # m.home_page_recharge(user_name=user['u1']['user_name'],
        #                      login_password=user['u1']['login_password'],
        #                      recharge_amount='0',
        #                      trade_password=user['u1']['trade_password'])

        # # 现金宝存入--首页(金额大于最大限额)
        # m.home_page_recharge(user_name=user['u1']['user_name'],
        #                      login_password=user['u1']['login_password'],
        #                      recharge_amount='100000000000',
        #                      trade_password=user['u1']['trade_password'])

        # # 现金宝取出--首页(取出金额正常)
        # m.home_page_regular_withdraw(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              withdraw_amount='0.1',
        #                              trade_password=user['u1']['trade_password'])

        # # 现金宝取出--首页(取出金额小于最小值)
        # m.home_page_regular_withdraw(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              withdraw_amount='0',
        #                              trade_password=user['u1']['trade_password'])

        # # 现金宝取出--首页(取出金额大于最大值)
        # m.home_page_regular_withdraw(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              withdraw_amount='10000000000000000',
        #                              trade_password=user['u1']['trade_password'])

        # # 现金宝快取--首页(取出金额正常)
        # m.home_page_fast_withdraw(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           withdraw_amount='0.10',
        #                           trade_password=user['u1']['trade_password'])

        # # 现金宝快取--首页(取出金额小于最小)
        # m.home_page_fast_withdraw(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           withdraw_amount='0',
        #                           trade_password=user['u1']['trade_password'])

        # # 现金宝快取--首页(取出金额大于最大)
        # m.home_page_fast_withdraw(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           withdraw_amount='10000000000000000',
        #                           trade_password=user['u1']['trade_password'])

        # m.home_page_view_essence_recommend_list(user_name=user['u1']['user_name'],
        #                                         login_password=user['u1']['login_password'])

        # m.register(phone_number=phone_number, login_password='a0000000')

        # m.register_binding_card(phone_number=phone_number, login_password='a0000000', trade_password='135790',
        #                         user_name=user_name, id_no=id_no, band_card_no=str(bank_card_no))

        # m.bank_card_manage_binding_card(user_name=user_new,
        #                                 login_password=login_password,
        #                                 bank_card_no=bank_card_no)

        # 未绑卡用户绑南粤卡
        # m.bank_card_manage_binding_nan_yue_card(user_name=user_new,
        #                                         login_password=login_password,
        #                                         bank_card_no=bank_card_no_nan_yue,
        #                                         banding_card_user_name=user_name,
        #                                         trade_password='142536',
        #                                         id_no=id_no)

        # m.delete_bank_card(user_name=user_new,
        #                    login_password=login_password,
        #                    trade_password=trade_password,
        #                    last_card_no=card_no[-4:])

        # m.modify_mobile(user_name=user_new,
        #                 login_password=login_password,
        #                 trade_password='135790',
        #                 mobile_new=mobile_new)

        # m.security_center_modify_trade_password(user_name=user_new,
        #                                         login_password=login_password,
        #                                         trade_password_old=trade_password,
        #                                         trade_password_new='147258')

        # m.security_center_modify_login_password(user_name=user_new,
        #                                         login_password=login_password,
        #                                         login_password_new='a1111111')

        # 提交过找回交易密码申请
        # m.security_center_find_trade_password(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password'])

        # 购买高端产品(金额正常)
        # m.buy_high_end_product(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'],
        #                        trade_password=user['u1']['trade_password'],
        #                        product_name=user['u1']['high_end_product'],
        #                        amount=user['u1']['high_end_product_amount'])

        # 购买高端产品(金额小于最小值)
        # m.buy_high_end_product(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'],
        #                        trade_password=user['u1']['trade_password'],
        #                        product_name=user['u1']['high_end_product'],
        #                        #amount=user['u1']['high_end_product_amount'])
        #                        amount='0')
        #
        # # 购买高端产品(金额大于最大值)
        # m.buy_high_end_product(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'],
        #                        trade_password=user['u1']['trade_password'],
        #                        product_name=user['u1']['high_end_product'],
        #                        #amount=user['u1']['high_end_product_amount'])
        #                        amount=user['u1']['amount_max'])

        # 购买定活宝(金额正常)
        # m.buy_dqb_product(user_name=user['u1']['user_name'],
        #                   login_password=user['u1']['login_password'],
        #                   product_name=user['u1']['dqb_product'],
        #                   amount=user['u1']['dqb_product_amount'],
        #                   trade_password=user['u1']['trade_password'])

        # 购买定活宝(金额小于最小值)
        # m.buy_dqb_product(user_name=user['u1']['user_name'],
        #                   login_password=user['u1']['login_password'],
        #                   product_name=user['u1']['dqb_product'],
        #                   amount=user['u1']['amount_min'],
        #                   trade_password=user['u1']['trade_password'])

        # 购买定活宝(金额大于最大值)
        # m.buy_dqb_product(user_name=user['u1']['user_name'],
        #                   login_password=user['u1']['login_password'],
        #                   product_name=user['u1']['dqb_product'],
        #                   amount=user['u1']['amount_max'],
        #                   trade_password=user['u1']['trade_password'])

        # m.hot_switch_to_dqb_product_list_page(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password'])
        #
        # m.hot_switch_to_high_end_product_list_page(user_name=user['u1']['user_name'],
        #                                            login_password=user['u1']['login_password'])

        # m.finance_product_search_with_full_name(user_name=user['u1']['user_name'],
        #                                         login_password=user['u1']['login_password'],
        #                                         product_name=user['u1']['search_with_full_name'])

        # m.finance_product_search_with_short_name(user_name=user['u1']['user_name'],
        #                                          login_password=user['u1']['login_password'],
        #                                          product_name=user['u1']['search_with_short_name'])

        # # 资产页现金宝存入(存入金额正常)
        # m.assets_xjb_detail_page_recharge(user_name=user['u1']['user_name'],
        #                                   login_password=user['u1']['login_password'],
        #                                   recharge_amount='1.00',
        #                                   trade_password=user['u1']['trade_password'])

        # # 资产页现金宝存入(存入金额小于0.01)
        # m.assets_xjb_detail_page_recharge(user_name=user['u1']['user_name'],
        #                                   login_password=user['u1']['login_password'],
        #                                   recharge_amount='0',
        #                                   trade_password=user['u1']['trade_password'])

        # # 资产页现金宝存入(存入金额大于限额)
        # m.assets_xjb_detail_page_recharge(user_name=user['u1']['user_name'],
        #                                   login_password=user['u1']['login_password'],
        #                                   recharge_amount='10000000000',
        #                                   trade_password=user['u1']['trade_password'])

        # 资产页现金宝取出(取出金额正常)
        # m.assets_xjb_detail_page_regular_withdraw(user_name=user['u1']['user_name'],
        #                                           login_password=user['u1']['login_password'],
        #                                           withdraw_amount='0.1',
        #                                           trade_password=user['u1']['trade_password'])

        # 资产页现金宝取出(取出金额小于最小限额)
        # m.assets_xjb_detail_page_regular_withdraw(user_name=user['u1']['user_name'],
        #                                           login_password=user['u1']['login_password'],
        #                                           withdraw_amount='0',
        #                                           trade_password=user['u1']['trade_password'])

        # 资产页现金宝取出(取出金额大于最大额)
        # m.assets_xjb_detail_page_regular_withdraw(user_name=user['u1']['user_name'],
        #                                           login_password=user['u1']['login_password'],
        #                                           withdraw_amount='10000000000000000',
        #                                           trade_password=user['u1']['trade_password'])

        # 资产页现金宝快取(取出金额正常)
        # m.assets_xjb_detail_page_fast_withdraw(user_name=user['u1']['user_name'],
        #                                        login_password=user['u1']['login_password'],
        #                                        withdraw_amount='0.1',
        #                                        trade_password=user['u1']['trade_password'])

        # 资产页现金宝快取(取出金额小于最小值)
        # m.assets_xjb_detail_page_fast_withdraw(user_name=user['u1']['user_name'],
        #                                        login_password=user['u1']['login_password'],
        #                                        withdraw_amount='0',
        #                                        trade_password=user['u1']['trade_password'])

        # 资产页现金宝快取(取出金额大于最大值)
        # ##m.assets_xjb_detail_page_fast_withdraw(user_name=user['u1']['user_name'],
        #                                        login_password=user['u1']['login_password'],
        #                                        withdraw_amount='1000000000000000',
        #                                        trade_password=user['u1']['trade_password'])
        # 添加信用卡
        # m.add_credit_card(user_name=user['u1']['user_name'],
        #                   login_password=user['u1']['login_password'],
        #                   credit_card_no=user['u1']['credit_card_no'],
        #                   last_card_no=user['u1']['last_card_no'])

        # 删除信用卡
        # m.delete_credit_card(user_name=user['u1']['user_name'],
        #                      login_password=user['u1']['login_password'],
        #                      last_card_no=user['u1']['last_card_no'],
        #                      trade_password=user['u1']['trade_password'])

        # m.view_message(user_name=user['u1']['user_name'],
        #                login_password=user['u1']['login_password'])

        # m.view_xjb_trade_detail(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'])
        #
        # m.dqb_detail_page_view_trade_detail(user_name=user['u1']['user_name'],
        #                                     login_password=user['u1']['login_password'])
        #
        # m.view_dqb_more_product(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'])
        #
        # #m.fund_detail_page_view_trade_detail(user_name=user['u1']['user_name'],
        #                                      login_password=user['u1']['login_password'])
        #
        # m.view_fund_more_product(user_name=user['u1']['user_name'],
        #                          login_password=user['u1']['login_password'])
        #
        # m.high_end_detail_page_view_trade_detail(user_name=user['u1']['user_name'],
        #                                          login_password=user['u1']['login_password'])
        #
        # m.view_high_end_more_product(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'])

        # 高端没有历史产品
        # m.view_high_end_history_product(user_name=user['u1']['user_name'],
        #                                 login_password=user['u1']['login_password'])

        # 赎回高端(份额正常)
        # m.redeem_high_end_product(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           redeem_amount=user['u1']['high_end_product_amount'],
        #                           # redeem_amount=user['u1']['high_end_product_amount_for_redeem'],
        #                           trade_password=user['u1']['trade_password'],
        #                           high_end_product=user['u1']['high_end_product'])

        # 赎回高端(份额小于最小值)
        # m.redeem_high_end_product(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           # redeem_amount=user['u1']['high_end_product_amount'],
        #                           redeem_amount=user['u1']['amount_min'],
        #                           trade_password=user['u1']['trade_password'],
        #                           high_end_product=user['u1']['high_end_product'])

        # 赎回高端(份额大于最大值)
        # m.redeem_high_end_product(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           # redeem_amount=user['u1']['high_end_product_amount'],
        #                           redeem_amount=user['u1']['amount_max'],
        #                           trade_password=user['u1']['trade_password'],
        #                           high_end_product=user['u1']['high_end_product'])

        # 赎回定活宝(金额正常)
        # m.redeem_dqb_product(user_name=user['u1']['user_name'],
        #                      # user_name=user['u1']['user_name_for_dqb_redeem'],
        #                      login_password=user['u1']['login_password'],
        #                      # login_password=user['u1']['login_password_for_dqb_redeem'],
        #                      redeem_amount=user['u1']['dqb_product_amount_2'],
        #                      trade_password=user['u1']['trade_password'],
        #                      dqb_product=user['u1']['dqb_product_2'])

        # 赎回定活宝(金额小于最小值)
        # m.redeem_dqb_product(user_name=user['u1']['user_name'],
        #                      # user_name=user['u1']['user_name_for_dqb_redeem'],
        #                      login_password=user['u1']['login_password'],
        #                      # login_password=user['u1']['login_password_for_dqb_redeem'],
        #                      redeem_amount=user['u1']['amount_min'],
        #                      trade_password=user['u1']['trade_password'],
        #                      dqb_product=user['u1']['dqb_product_2'])
        #
        # # 赎回定活宝(金额大于最大值)
        # m.redeem_dqb_product(user_name=user['u1']['user_name'],
        #                      # user_name=user['u1']['user_name_for_dqb_redeem'],
        #                      login_password=user['u1']['login_password'],
        #                      # login_password=user['u1']['login_password_for_dqb_redeem'],
        #                      redeem_amount=user['u1']['amount_max'],
        #                      trade_password=user['u1']['trade_password'],
        #                      dqb_product=user['u1']['dqb_product_2'])

        # m.my_referee(user_name=user['u1']['user_name'],
        #              login_password=user['u1']['login_password'],
        #              phone_no=user['u1']['user_name'])

        # m.risk_evaluating_new_user(user_name=user_new,
        #                            login_password=login_password)

        # m.fund_product_search_with_name(user_name=user['u1']['user_name'],
        #                                 login_password=user['u1']['login_password'],
        #                                 fund_product_name=user['u1']['fund_product_name'])

        # m.fund_product_search_with_code(user_name=user['u1']['user_name'],
        #                                 login_password=user['u1']['login_password'],
        #                                 fund_product_code=user['u1']['fund_product_code'])

        # 购买基金(正常金额)
        # m.buy_fund_product(user_name=user['u1']['user_name'],
        #                    login_password=user['u1']['login_password'],
        #                    fund_product_name=user['u1']['fund_product_name'],
        #                    amount='15',
        #                    trade_password=user['u1']['trade_password'],
        #                    fund_product_code=user['u1']['fund_product_code']
        #                    )

        # 购买基金(购买金额小于最小值)
        # m.buy_fund_product(user_name=user['u1']['user_name'],
        #                    login_password=user['u1']['login_password'],
        #                    fund_product_name=user['u1']['fund_product_name'],
        #                    amount='0',
        #                    trade_password=user['u1']['trade_password'],
        #                    fund_product_code=user['u1']['fund_product_code']
        #                    )

        # 购买基金(购买金额大于最大值)
        # ##m.buy_fund_product(user_name=user['u1']['user_name'],
        #                    login_password=user['u1']['login_password'],
        #                    fund_product_name=user['u1']['fund_product_name'],
        #                    amount='1000000000',
        #                    trade_password=user['u1']['trade_password'],
        #                    fund_product_code=user['u1']['fund_product_code']
        #                    )

        # m.invite_friend(user_name=user['u1']['user_name'],
        #                 login_password=user['u1']['login_password'])

        # 预约码--使用其他预约码(有预约码)
        # m.use_other_reservation_code(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              trade_password=user['u1']['trade_password'],
        #                              buy_quota=user['u1']['reservation_code_buy_quota'],
        #                              buy_count=user['u1']['reservation_code_buy_count'],
        #                              reserve_quota=user['u1']['reservation_code_reserve_quota'],
        #                              reserve_count=user['u1']['reservation_code_reserve_count'],
        #                              reserve_code=user['u1']['reserve_code'],
        #                              product_id=user['u1']['product_id_for_reservation_code']
        #                              )

        # 预约码--使用其他预约码(无预约码)
        # m.use_other_reservation_code_without_reservation_code(user_name=user['u2']['user_name'],
        #                                                       login_password=user['u2']['login_password'],
        #                                                       trade_password=user['u2']['trade_password'],
        #                                                       buy_quota=user['u2']['reservation_code_buy_quota'],
        #                                                       buy_count=user['u2']['reservation_code_buy_count'],
        #                                                       reserve_quota=user['u2'][
        #                                                           'reservation_code_reserve_quota'],
        #                                                       reserve_count=user['u2'][
        #                                                           'reservation_code_reserve_count'],
        #                                                       reserve_code=user['u2']['reserve_code'],
        #                                                       product_id=user['u2']['product_id_for_reservation_code'],
        #                                                       mobile=user['u1']['user_name']
        #                                                       )

        # 赎回基金(金额正常)
        # m.redeem_fund_product(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       fund_product=user['u1']['fund_product_name'],
        #                       amount='1',
        #                       trade_password=user['u1']['trade_password'])

        # 赎回基金(金额小于最小值)
        # m.redeem_fund_product(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       fund_product=user['u1']['fund_product_name_for_redeem'],
        #                       amount=user['u1']['amount_min'],
        #                       trade_password=user['u1']['trade_password'])
        #
        # # 赎回基金(金额大于最大值)
        # m.redeem_fund_product(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       fund_product=user['u1']['fund_product_name_for_redeem'],
        #                       amount=user['u1']['amount_max'],
        #                       trade_password=user['u1']['trade_password'])

        # 预约码--使用自己的预约码
        # m.use_reservation_code(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'],
        #                        trade_password=user['u1']['trade_password'],
        #                        buy_quota=user['u1']['reservation_code_buy_quota'],
        #                        buy_count=user['u1']['reservation_code_buy_count'],
        #                        reserve_quota=user['u1']['reservation_code_reserve_quota'],
        #                        reserve_count=user['u1']['reservation_code_reserve_count'],
        #                        reserve_code=user['u1']['reserve_code'],
        #                        product_id=user['u1']['product_id_for_reservation_code']
        #                       )

        # m.earn_points(user_name=user['u1']['user_name'],
        #               login_password=user['u1']['login_password'],
        #               amount=user['u1']['fund_product_amount'],
        #               trade_password=user['u1']['trade_password'],
        #               fund_product_name=user['u1']['fund_product_name'],
        #               fund_product_code=user['u1']['fund_product_code'],
        #               )

        # # 信用卡还款
        # m.credit_card_repay(user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'],
        #                     repay_amount=user['u1']['credit_card_repay_amount'],
        #                     trade_password=user['u1']['trade_password'],
        #                     last_card_no=user['u1']['last_card_no_for_repay'])

        # 信用卡预约还款
        # m.credit_card_reserved_pay(user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           reserved_pay_amount=user['u1']['credit_card_reserved_pay_amount'],
        #                           trade_password=user['u1']['trade_password'],
        #                           last_card_no=user['u1']['last_card_no_for_repay'])

        # 取消预约还款
        # m.cancel_reserved_pay(user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       last_card_no=user['u1']['last_card_no_for_repay']
        #                       )

        # 赚积分--推荐用户注册绑卡
        # m.earn_points_by_recommend_user_register(user['u1']['user_name'],
        #                                          login_password=user['u1']['login_password'])

        # 花积分--买基金
        # m.spend_points_by_buy_fund(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            amount=user['u1']['fund_product_amount'],
        #                            trade_password=user['u1']['trade_password'],
        #                            fund_product_name=user['u1']['fund_product_name'],
        #                            fund_product_code=user['u1']['fund_product_code'],
        #                            )
        #
        # # 花积分--买高端产品
        # m.spend_points_by_buy_vipproduct_use_product_name(user_name=user['u1']['user_name'],
        #                                                   login_password=user['u1']['login_password'],
        #                                                   amount=user['u1']['high_end_product_amount'],
        #                                                   trade_password=user['u1']['trade_password'],
        #                                                   product_name=user['u1']['high_end_product_for_points'],
        #                                                   # product_name=user['u1']['high_end_product_for_points_offset'],
        #                                                   )

        # 花积分--买定期宝
        # m.spend_points_by_buy_dqb(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           dqb_product_amount=user['u1']['dqb_product_amount'],
        #                           trade_password=user['u1']['trade_password'],
        #                           dqb_product=user['u1']['dqb_product'])

        # 添加还款提醒
        # m.add_credit_card_repayment_warn(user_name=user['u1']['user_name'],
        #                                  login_password=user['u1']['login_password'],
        #                                  last_card_no=user['u1']['last_card_no_for_repay']
        #                                  )

        # 取消还款提醒
        # m.cancel_credit_card_repayment_warn(user_name=user['u1']['user_name'],
        #                                     login_password=user['u1']['login_password'],
        #                                     last_card_no=user['u1']['last_card_no_for_repay']
        #                                  )

        # 高端普通卖出
        # m.normal_redeem_vipproduct(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            redeem_amount=user['u1']['high_end_product_amount'],
        #                            trade_password=user['u1']['trade_password'],
        #                            high_end_product_for_fast_redeem=user['u1']['high_end_product_for_fast_redeem']
        #                            )

        # 高端极速卖出
        # m.fast_redeem_vipproduct(user_name=user['u1']['user_name'],
        #                          login_password=user['u1']['login_password'],
        #                          redeem_amount=user['u1']['high_end_product_amount'],
        #                          trade_password=user['u1']['trade_password'],
        #                          high_end_product_for_fast_redeem=user['u1']['high_end_product_for_fast_redeem']
        #                          )

        # 基金普通卖出
        # m.normal_redeem_fund_product(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              redeem_amount=user['u1']['fund_product_amount'],
        #                              trade_password=user['u1']['trade_password'],
        #                              fund_product_name_for_fast_redeem=user['u1']['fund_product_name']
        #                              )

        # 基金极速卖出
        # m.fast_redeem_fund_product(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            redeem_amount=user['u1']['fund_product_amount'],
        #                            trade_password=user['u1']['trade_password'],
        #                            fund_product_name_for_fast_redeem=user['u1']['fund_product_name']
        #                            )

        # 积分明细
        # #m.assets_my_points_details(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password']
        #                            )

        # 基金频道--研究报告
        # #m.fund_research_report(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password']
        #                        )

        # 基金频道--机构观点
        # #m.fund_institution_viewpoint(user_name=user['u1']['user_name'],
        #                             login_password=user['u1']['login_password']
        #                             )

        # 基金频道--达人论基
        # #m.fund_talent_fund_discussion(user_name=user['u1']['user_name'],
        #                               login_password=user['u1']['login_password']
        #                               )

        # 基金频道--市场指数
        # m.fund_market_index(user_name=user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'],
        #                     csi_index=user['u1']['csi_index'])

        # 基金频道--全部基金
        # m.fund_all_funds(user_name=user['u1']['user_name'],
        #                  login_password=user['u1']['login_password'])

        # 基金频道--评级排行
        # m.fund_rating_and_ranking(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'])

        # 基金频道--自选基金
        # m.fund_selected_funds(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       fund_product_name=user['u1']['fund_product_name'],
        #                       fund_product_code=user['u1']['fund_product_code']
        #                       )

        # m.fund_selected_funds(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       fund_product_name=user['u1']['fund_product_name'],
        #                       fund_product_name_2=user['u1']['fund_product_name_2'],
        #                       fund_product_code=user['u1']['fund_product_code'],
        #                       fund_product_code_2=user['u1']['fund_product_code_2'],
        #                       fund_company=user['u1']['fund_company']
        #                       )

        # 基金频道--对比分析
        # m.fund_comparasion_and_analysis(user_name=user['u1']['user_name'],
        #                                 login_password=user['u1']['login_password'],
        #                                 fund_product_code=user['u1']['fund_product_code'],
        #                                 fund_product_code_2=user['u1']['fund_product_code_2'],
        #                                 )
        #
        # # 购买定期宝使用优惠券(不可叠加)
        # m.buy_dqb_use_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                    login_password=user['u1']['login_password'],
        #                                    nonsuperposed_coupon_code =user['u1']['nonsuperposed_coupon_code'],
        #                                    nonsuperposed_coupon_quantity=user['u1']['nonsuperposed_coupon_quantity'],
        #                                    amount=user['u1']['dqb_product_amount'],
        #                                    trade_password=user['u1']['trade_password'],
        #                                    product_name=user['u1']['dqb_product_for_coupon']
        #                                    # product_name=user['u1']['dqb_product']
        #                                    )

        # 购买定期宝使用优惠券(可叠加)
        # m.buy_dqb_use_superposed_coupon(user_name=user['u1']['user_name'],
        #                                    login_password=user['u1']['login_password'],
        #                                    superposed_coupon_code =user['u1']['superposed_coupon_code'],
        #                                    superposed_coupon_quantity=user['u1']['superposed_coupon_quantity'],
        #                                    amount=user['u1']['dqb_product_amount'],
        #                                    trade_password=user['u1']['trade_password'],
        #                                    product_name=user['u1']['dqb_product']
        #                                    )

        # 购买高端使用优惠券(不可叠加)
        # m.buy_vipproduct_use_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                           login_password=user['u1']['login_password'],
        #                                           nonsuperposed_coupon_code=user['u1']['nonsuperposed_coupon_code'],
        #                                           nonsuperposed_coupon_quantity=user['u1'][
        #                                               'nonsuperposed_coupon_quantity'],
        #                                           # amount=user['u1']['high_end_product_amount'],
        #                                           amount='20',
        #                                           trade_password=user['u1']['trade_password'],
        #                                           # product_name=user['u1']['high_end_product_for_points']
        #                                           product_name=user['u1']['high_end_product']
        #                                           )

        # 购买高端使用优惠券(可叠加)
        # m.buy_vipproduct_use_superposed_coupon(user_name=user['u1']['user_name'],
        #                                        login_password=user['u1']['login_password'],
        #                                        superposed_coupon_code=user['u1']['superposed_coupon_code'],
        #                                        superposed_coupon_quantity=user['u1']['superposed_coupon_quantity'],
        #                                        amount=user['u1']['high_end_product_amount'],
        #                                        trade_password=user['u1']['trade_password'],
        #                                        # product_name=user['u1']['high_end_product_for_points']
        #                                        product_name=user['u1']['high_end_product']
        #                                        )

        # 购买基金使用优惠券(不可叠加)
        # m.buy_fund_use_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                     login_password=user['u1']['login_password'],
        #                                     nonsuperposed_coupon_code=user['u1']['nonsuperposed_coupon_code'],
        #                                     nonsuperposed_coupon_quantity=user['u1']['nonsuperposed_coupon_quantity'],
        #                                     fund_product_name=user['u1']['fund_product_name'],
        #                                     amount=user['u1']['fund_product_amount'],
        #                                     trade_password=user['u1']['trade_password'],
        #                                     fund_product_code=user['u1']['fund_product_code']
        #                                     )

        # 购买基金使用优惠券(可叠加)
        # m.buy_fund_use_superposed_coupon(user_name=user['u1']['user_name'],
        #                                  login_password=user['u1']['login_password'],
        #                                  superposed_coupon_code=user['u1']['superposed_coupon_code'],
        #                                  superposed_coupon_quantity=user['u1']['superposed_coupon_quantity'],
        #                                  fund_product_name=user['u1']['fund_product_name'],
        #                                  amount='10',
        #                                  trade_password=user['u1']['trade_password'],
        #                                  fund_product_code=user['u1']['fund_product_code']
        #                                  )


        # 购买定期宝使用积分+优惠券(不可叠加)
        # m.buy_dqb_use_points_and_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                    login_password=user['u1']['login_password'],
        #                                    nonsuperposed_coupon_code =user['u1']['nonsuperposed_coupon_code'],
        #                                    nonsuperposed_coupon_quantity=user['u1']['nonsuperposed_coupon_quantity'],
        #                                    amount=user['u1']['dqb_product_amount'],
        #                                    trade_password=user['u1']['trade_password'],
        #                                   # product_name=user['u1']['dqb_product_for_coupon']
        #                                    product_name=user['u1']['dqb_product']
        #                                    )

        # 购买定期宝使用积分+优惠券(可叠加)
        # m.buy_dqb_use_points_and_superposed_coupon(user_name=user['u1']['user_name'],
        #                                            login_password=user['u1']['login_password'],
        #                                            superposed_coupon_code=user['u1']['superposed_coupon_code'],
        #                                            superposed_coupon_quantity=user['u1']['superposed_coupon_quantity'],
        #                                            amount=user['u1']['dqb_product_amount'],
        #                                            trade_password=user['u1']['trade_password'],
        #                                            product_name=user['u1']['dqb_product_for_coupon']
        #                                            # product_name=user['u1']['dqb_product']
        #                                            )

        # 购买高端使用积分+优惠券(不可叠加)
        # m.buy_vipproduct_use_points_and_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                                      login_password=user['u1']['login_password'],
        #                                  nonsuperposed_coupon_code =user['u1']['nonsuperposed_coupon_code'],
        #                                  nonsuperposed_coupon_quantity=user['u1']['nonsuperposed_coupon_quantity'],
        #                                                      amount=user['u1']['high_end_product_amount'],
        #                                                      trade_password=user['u1']['trade_password'],
        #                                                      product_name=user['u1']['high_end_product_for_points']
        #                                                    )

        # 购买高端使用积分+优惠券(可叠加)
        # m.buy_vipproduct_use_points_and_superposed_coupon(user_name=user['u1']['user_name'],
        #                                                   login_password=user['u1']['login_password'],
        #                                                   superposed_coupon_code=user['u1']['superposed_coupon_code'],
        #                                                   superposed_coupon_quantity=user['u1'][
        #                                                       'superposed_coupon_quantity'],
        #                                                   amount=user['u1']['high_end_product_amount'],
        #                                                   trade_password=user['u1']['trade_password'],
        #                                                   # product_name=user['u1']['high_end_product_for_points']
        #                                                   product_name=user['u1']['high_end_product']
        #                                                   )

        # 购买基金使用积分+优惠券(不可叠加)
        # m.buy_fund_use_points_and_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                     login_password=user['u1']['login_password'],
        #                                     nonsuperposed_coupon_code =user['u1']['nonsuperposed_coupon_code'],
        #                                     nonsuperposed_coupon_quantity=user['u1']['nonsuperposed_coupon_quantity'],
        #                                     fund_product_name=user['u1']['fund_product_name'],
        #                                     amount=user['u1']['fund_product_amount'],
        #                                     trade_password=user['u1']['trade_password'],
        #                                     fund_product_code=user['u1']['fund_product_code']
        #                                     )

        # 购买基金使用积分+优惠券(可叠加)
        # m.buy_fund_use_points_and_superposed_coupon(user_name=user['u1']['user_name'],
        #                                     login_password=user['u1']['login_password'],
        #                                     superposed_coupon_code =user['u1']['superposed_coupon_code'],
        #                                     superposed_coupon_quantity=user['u1']['superposed_coupon_quantity'],
        #                                     fund_product_name=user['u1']['fund_product_name'],
        #                                     amount='100',
        #                                     trade_password=user['u1']['trade_password'],
        #                                     fund_product_code=user['u1']['fund_product_code']
        #                                     )

        # 基金定投
        # m.fund_plan(user_name=user['u1']['user_name'],
        #             login_password=user['u1']['login_password'],
        #             fund_product_name=user['u1']['fund_product_name'],
        #             amount=user['u1']['fund_product_amount'],
        #             trade_password=user['u1']['trade_password'],
        #             fund_product_code=user['u1']['fund_product_code']
        #             )

        # 随心借
        # m.vipproduct_pledge(user_name=user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'],
        #                     product_name=user['u1']['high_end_product'],
        #                     pledge_amount=user['u1']['pledge_amount'],
        #                     trade_password=user['u1']['trade_password'],
        #                     )

        # 随心还
        # m.vipproduct_pledge_repay(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           product_name=user['u1']['high_end_product'],
        #                           pledge_repay_amount=user['u1']['pledge_repay_amount'],
        #                           trade_password=user['u1']['trade_password'],
        #                           )


        # #会员中心——钻石会员验证
        # m.associator_level(user_name=user['u1']['user_name'],
        #                    login_password=user['u1']['login_password']
        #                    )

        # 会员中心——铂金会员验证
        # m.associator_rank(user_name=user['u1']['user_name_for_associator_level_4'],
        #                   login_password=user['u1']['login_password'])

        # 会员中心——黄金会员验证
        # m.associator_rank(user_name=user['u1']['user_name_for_associator_level_3'],
        #                   login_password=user['u1']['login_password'])

        # 会员中心——白银会员验证
        # m.associator_rank(user_name=user['u1']['user_name_for_associator_level_2'],
        #                   login_password=user['u1']['login_password'])

        # 会员中心——新手会员验证
        # m.associator_rank(user_name=user['u1']['user_name_for_associator_level_1'],
        #                   login_password=user['u1']['login_password']
        #

        # 查看定期宝历史产品
        # m.view_dqb_history_product(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password']
        #                            )

        # 员工理财--工资代发
        # m.salary_issuing(user_name=user['u1']['user_name'],
        #                  login_password=user['u1']['login_password'],
        #                  protocol_status='0',
        #                  employee_id='19')

        # 员工理财--终止工资代发
        # m.stop_salary_issuing(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       trade_password=user['u1']['trade_password'],
        #                       )

        # 工资理财——新增计划
        # m.add_financing_plan(user_name=user['u1']['user_name'],
        #                      login_password=user['u1']['login_password'],
        #                      last_no=user['u1']['pay_card_last_no'],
        #                      amount=user['u1']['financing_amount'],
        #                      trade_password=user['u1']['trade_password'])

        # 工资理财——暂停计划
        # m.pause_financing_plan(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'],
        #                        trade_password=user['u1']['trade_password'])

        # # 工资理财——启用计划
        # m.restart_financing_plan(user_name=user['u1']['user_name'],
        #                      login_password=user['u1']['login_password'],
        #                      trade_password=user['u1']['trade_password'])

        # 修改理财计划
        # m.modify_financing_plan(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'],
        #                         trade_password=user['u1']['trade_password'],
        #                         last_no=user['u1']['pay_card_last_no_for_modification'],
        #                         amount=user['u1']['financing_amount'])

        # 终止理财计划
        # m.stop_financing_plan(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       trade_password=user['u1']['trade_password'])

        # 还房贷
        # m.make_repay_housing_loan_plan(user_name=user['u1']['user_name'],
        #                                login_password=user['u1']['login_password'],
        #                                last_no=user['u1']['pay_card_last_no'],
        #                                repay_amount=user['u1']['repay_loan_amount'],
        #                                trade_password=user['u1']['trade_password']
        #                                )

        # 还车贷
        # m.make_repay_car_loan_plan(user_name=user['u1']['user_name'],
        #                                login_password=user['u1']['login_password'],
        #                                last_no=user['u1']['pay_card_last_no'],
        #                                repay_amount=user['u1']['repay_loan_amount'],
        #                                trade_password=user['u1']['trade_password']
        #                                )

        # 暂停还贷款计划
        # m.pause_repay_loan_plan(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'],
        #                         trade_password=user['u1']['trade_password'])

        # 开启工资理财计划
        # m.start_financing_plan(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'],
        #                        last_no=user['u1']['pay_card_last_no'],
        #                        amount=user['u1']['financing_amount'],
        #                        trade_password=user['u1']['trade_password']
        #                        )

        # 还车贷
        # m.make_repay_car_loan_plan(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            last_no=user['u1']['pay_card_last_no'],
        #                            trade_password=user['u1']['trade_password'],
        #                            repay_amount=user['u1']['repay_loan_amount']
        #                            )

        # 还其他贷款
        # m.make_repay_other_loan_plan(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              last_no=user['u1']['pay_card_last_no'],
        #                              trade_password=user['u1']['trade_password'],
        #                              repay_amount=user['u1']['repay_loan_amount'])

        # 修改还房贷为还车贷
        # m.modify_repay_housing_loan_to_repay_car_loan(user_name=user['u1']['user_name'],
        #                                               login_password=user['u1']['login_password'],
        #                                               trade_password=user['u1']['trade_password'],
        #                                               last_no=user['u1']['pay_card_last_no_for_modification'],
        #                                               repay_amount=user['u1']['repay_loan_amount'])

        # 修改还车贷为还其他贷款
        # m.modify_repay_car_loan_to_repay_other_loan(user_name=user['u1']['user_name'],
        #                                               login_password=user['u1']['login_password'],
        #                                               trade_password=user['u1']['trade_password'],
        #                                               last_no=user['u1']['pay_card_last_no_for_modification'],
        #                                               repay_amount=user['u1']['repay_loan_amount'])

        # 修改还其他贷款为还房贷
        # m.modify_repay_other_loan_to_repay_housing_loan(user_name=user['u1']['user_name'],
        #                                             login_password=user['u1']['login_password'],
        #                                             trade_password=user['u1']['trade_password'],
        #                                             last_no=user['u1']['pay_card_last_no_for_modification'],
        #                                             repay_amount=user['u1']['repay_loan_amount'])

        # 删除还贷款计划
        # m.delete_repay_loan_plan(user_name=user['u1']['user_name'],
        #                          login_password=user['u1']['login_password'],
        #                          trade_password=user['u1']['trade_password'])

        # 现金支付手段买高端(金额正常)
        # m.buy_vipproduct_use_cash_management_product(user_name=user['u1']['user_name'],
        #                                              login_password=user['u1']['login_password'],
        #                                              product_name=user['u1']['high_end_product_for_points'],
        #                                              trade_password=user['u1']['trade_password'],
        #                                              amount=user['u1']['high_end_product_amount'],
        #                                              cash_management_product=user['u1']['cash_management_product'])

        #
        # # 现金支付手段买高端(金额超过持有金额)
        # m.buy_vipproduct_use_cash_management_product(user_name=user['u1']['user_name'],
        #                                              login_password=user['u1']['login_password'],
        #                                              product_name=user['u1']['high_end_product_for_points'],
        #                                              trade_password=user['u1']['trade_password'],
        #                                              amount=user['u1']['high_end_product_amount'],
        #                                              cash_management_product=user['u1']['cash_management_product_for_excess'])
        #
        # #实名用户绑银行卡
        # m.certificated_user_binding_card(user_name=user['u1']['user_name_for_add_credit_card_without_binding_bank_card'],
        #                                  login_password=user['u1']['login_password'],
        #                                  # bank_card_no='6222026514970936462')
        #                                  bank_card_no=user['u1']['bank_card_no_for_certificated_user_binding_card'])

        # 查看历史定投(用户无历史定投)
        # m.check_empty_fund_history_plan(user_name=user['u2']['user_name'],
        #                                 login_password=user['u2']['login_password'])

        # 基金定投
        # m.fund_plan(user_name=user['u1']['user_name'],
        #             login_password=user['u1']['login_password'],
        #             fund_product_name=user['u1']['fund_product_name'],
        #             amount=user['u1']['fund_product_amount'],
        #             trade_password=user['u1']['trade_password'],
        #             fund_product_code=user['u1']['fund_product_code'])

        # 暂停定投
        # m.pause_fund_plan(user_name=user['u1']['user_name'],
        #                   login_password=user['u1']['login_password'],
        #                   trade_password=user['u1']['trade_password'],
        #                   fund_product_name=user['u1']['fund_product_name'])

        # 恢复定投
        # m.restart_fund_plan(user_name=user['u1']['user_name'],
        #                   login_password=user['u1']['login_password'],
        #                   trade_password=user['u1']['trade_password'],
        #                   fund_product_name=user['u1']['fund_product_name'])

        # 终止定投
        # m.stop_fund_plan(user_name=user['u1']['user_name'],
        #                  login_password=user['u1']['login_password'],
        #                  trade_password=user['u1']['trade_password'],
        #                  fund_product_name=user['u1']['fund_product_name'])

        # 修改基金定投计划
        # m.modify_fund_plan(user_name=user['u1']['user_name'],
        #                    login_password=user['u1']['login_password'],
        #                    fund_product_name=user['u1']['fund_product_name'],
        #                    amount='1.00',
        #                    trade_password=user['u1']['trade_password'])

        # 新增定投计划
        # m.add_fund_plan(user_name=user['u1']['user_name'],
        #                 login_password=user['u1']['login_password'],
        #                 fund_product_name=user['u1']['fund_product_name'],
        #                 fund_product_code=user['u1']['fund_product_code'],
        #                 trade_password=user['u1']['trade_password'],
        #                 amount=user['u1']['fund_product_amount'])

        # 查看现金宝万分收益
        # m.view_xjb_income_per_wan(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password']
        #                           )

        # 查看现金宝累计收益
        # m.view_xjb_income_accumulated(user_name=user['u1']['user_name'],
        #                               login_password=user['u1']['login_password']
        #                              )

        # 查看历史七日年化收益率
        # m.view_xjb_seven_days_annual_rate_of_return(user_name=user['u1']['user_name'],
        #                                             login_password=user['u1']['login_password']
        #                                             )

        # 查看现金管理系列
        # m.view_high_end_cash_management_series(user_name=user['u1']['user_name'],
        #                                        login_password=user['u1']['login_password']
        #                                        )

        # 查看固定收益系列
        # m.view_high_end_fixed_rate_series(user_name=user['u1']['user_name'],
        #                               login_password=user['u1']['login_password']
        #                              )

        # 查看精选系列
        # m.view_high_end_best_recommend_series(user_name=user['u1']['user_name'],
        #                               login_password=user['u1']['login_password']
        #                              )

        # 查看资产证明
        # m.view_assets_analysis(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'])

        # 下载资产证明
        # m.download_assets_certification(user_name=user['u1']['user_name'],
        #                                 login_password=user['u1']['login_password'],
        #                                 trade_password=user['u1']['trade_password'])

        # 持有页面查看产品详情
        # m.view_product_details(user_name=user['u1']['user_name'],
        #                        login_password=user['u1']['login_password'],
        #                        high_end_product=user['u1']['high_end_product'])

        # 基金撤单
        # m.cancel_fund_order(user_name=user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'],
        #                     product_name=user['u1']['fund_product_name'],
        #                     trade_password=user['u1']['trade_password'],
        #                     )

        # 高端撤单
        # m.cancel_vipproduct_order(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'],
        #                           product_name=user['u1']['high_end_product'],
        #                           trade_password=user['u1']['trade_password'],
        #                           # amount=user['u1']['high_end_product_amount']
        #                           )

        # 用户绑定银行卡张数为0时绑定信用卡
        # m.add_credit_card_without_binding_bank_card(
        #     user_name=user['u1']['user_name_for_add_credit_card_without_binding_bank_card'],
        #     login_password=user['u1']['login_password'],
        #     bank_card_no=bank_card_no)

        # 热门页查看全部产品
        # m.view_all_products(user_name=user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'])

        #  理财频道全部产品--筛选器
        # m.all_products_filter(user_name=user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'])

        # 删除自选基金
        # m.fund_selected_funds_deleted(user_name=user['u1']['user_name'],
        #                               login_password=user['u1']['login_password'],
        #                               fund_product_name=user['u1']['fund_product_name'],
        #                               fund_product_code=user['u1']['fund_product_code']
        #                               )

        # 基金筛选器
        # m.fund_filter(user_name=user['u1']['user_name'],
        #               login_password=user['u1']['login_password']
        #                               )

        # 稳健型用户购买高风险产品(提示加验证码)
        # m.moderate_user_buy_high_risk_product(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password'],
        #                                       fund_product_name=user['u1']['fund_product_name_for_fast_redeem'],
        #                                       amount=user['u1']['fund_product_amount'],
        #                                       trade_password=user['u1']['trade_password'],
        #                                       fund_product_code='050035'
        #                                       )

        # 激进型用户购买高风险产品(提示加需输入验证码)
        # m.radical_user_buy_high_risk_product(user_name=user['u1']['radical_user'],
        #                                      login_password=user['u1']['login_password'],
        #                                      fund_product_name=user['u1']['fund_product_name_for_fast_redeem'],
        #                                      amount=user['u1']['fund_product_amount'],
        #                                      trade_password=user['u1']['trade_password'],
        #                                      fund_product_code='050035'
        #                                      )

        # 保守型用户购买高风险产品(风险提示且用户不能购买)
        # m.conservative_user_buy_high_risk_product(user_name=user['u1']['conservative_user'],
        #                                           login_password=user['u1']['login_password'],
        #                                           fund_product_name=user['u1']['fund_product_name_for_fast_redeem'],
        #                                           # amount=user['u1']['fund_product_amount'],
        #                                           fund_product_code='050035'
        #                                           )

        # 谨慎型用户购买中高风险产品(有提示,可以购买)
        # m.cautious_user_buy_middle_high_risk_product(user_name=user['u1']['cautious_user'],
        #                                              login_password=user['u1']['login_password'],
        #                                              fund_product_name=user['u1']['fund_product_name_2'],
        #                                              amount=user['u1']['fund_product_amount'],
        #                                              trade_password=user['u1']['trade_password'],
        #                                              fund_product_code='A09201'
        #                                              )

        # 现金宝持有页面查看在途资产
        # m.view_xjb_asset_in_transit(user_name=user['u1']['user_name'],
        #                             login_password=user['u1']['login_password']
        #                             )

        # 现金宝持有页面查看产品详情
        # m.view_xjb_product_detail(user_name=user['u1']['user_name'],
        #                             login_password=user['u1']['login_password']
        #                             )

        #  现金宝持有页面查看七日年化收益率曲线
        # m.view_xjb_seven_days_annual_rate_of_return_curve(user_name=user['u1']['user_name'],
        #                             login_password=user['u1']['login_password']
        #                             )

        # 查看基金资产(资产分析页面进)
        # m.view_fund_asset(user_name=user['u1']['user_name'],
        #                   login_password=user['u1']['login_password']
        #                   )

        # 我的优惠券列表为空
        # m.my_coupon_empty_list(user_name=user['u1']['radical_user'],
        #                        login_password=user['u1']['login_password']
        #                        )

        # 基金频道--删除自选基金（从自选基金详情页面删除）
        # m.fund_selected_funds_deleted_at_fund_detail_page(user_name=user['u1']['user_name'],
        #                                                   login_password=user['u1']['login_password'],
        #                                                   fund_product_name=user['u1']['fund_product_name'],
        #                                                   fund_product_code=user['u1']['fund_product_code'])

        # 高端追加购买页面跳转(资产分析页面进)
        # m.vipproduct_supplementary_purchase(user_name=user['u1']['user_name'],
        #                                     login_password=user['u1']['login_password'],
        #                                     high_end_product=user['u1']['high_end_product_for_fast_redeem'])

        # 定期追加购买(资产分析页面进)
        # m.dhb_supplementary_purchase(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              product_name=user['u1']['dqb_product'])

        # 未测评用户购买产品(提示先进行风险评测)
        # m.buy_fund_product_without_risk_evaluation(user_name=user['u1']['unevaluated_user'],
        #                                            login_password=user['u1']['login_password'],
        #                                            fund_product_name=user['u1']['fund_product_name'],
        #                                            fund_product_code=user['u1']['fund_product_code']
        #                                            )

        # 短信验证码登录
        # m.login_use_verification_code(user_name=user['u1']['unevaluated_user'])
        #
        # 使用优惠券充值现金宝
        # m.recharge_use_coupon(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       recharge_amount='3.00',
        #                       trade_password=user['u1']['trade_password'],
        #                       nonsuperposed_coupon_code=user['u1']['nonsuperposed_coupon_code'],
        #                       nonsuperposed_coupon_quantity=user['u1']['nonsuperposed_coupon_quantity'])

        # 现金支付手段买基金(金额正常)
        # m.buy_fund_product_use_cash_management_product(user_name=user['u1']['user_name'],
        #                                                login_password=user['u1']['login_password'],
        #                                                fund_product_name=user['u1']['fund_product_name'],
        #                                                trade_password=user['u1']['trade_password'],
        #                                                amount=user['u1']['fund_product_amount'],
        #                                                fund_product_code=user['u1']['fund_product_code'],
        #                                                cash_management_product=user['u1']['cash_management_product'])

        # 现金管理系列作为支付手段买定活宝
        # m.buy_dhb_product_use_cash_management_product(user_name=user['u1']['user_name'],
        #                                               login_password=user['u1']['login_password'],
        #                                               product_name=user['u1']['dqb_product'],
        #                                               trade_password=user['u1']['trade_password'],
        #                                               amount=user['u1']['dqb_product_amount'],
        #                                               cash_management_product=user['u1']['cash_management_product'])

        # 信用卡还款使用优惠券
        # m.credit_card_repay_use_coupon(user_name=user['u1']['user_name'],
        #                                login_password=user['u1']['login_password'],
        #                                repay_amount=user['u1']['credit_card_repay_amount'],
        #                                trade_password=user['u1']['trade_password'],
        #                                # last_card_no=user['u1']['last_card_no_for_repay'],
        #                                last_card_no='2696',
        #                                superposed_coupon_code=user['u1']['credit_card_repay_coupon_code'],
        #                                superposed_coupon_quantity=user['u1']['superposed_coupon_quantity'])

        # 查看现金宝资产的说明
        # m.view_xjb_holding_assets_description(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password'])

        # 查看定活宝资产的说明
        # m.view_dhb_holding_assets_description(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password'])

        # 查看基金资产的说明
        # m.view_fund_holding_assets_description(user_name=user['u1']['user_name'],
        #                                        login_password=user['u1']['login_password'])

        # 查看高端资产的说明
        # m.view_vipproduct_holding_assets_description(user_name=user['u1']['user_name'],
        #                                              login_password=user['u1']['login_password'])

        # 定投排行
        # m.view_fund_plan_rankings(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password'])
        #
        # 信用卡预约还款使用优惠券
        # m.credit_card_reserved_pay_use_nonsuperposed_coupon(user_name=user['u1']['user_name'],
        #                                                     login_password=user['u1']['login_password'],
        #                                                     reserved_pay_amount=user['u1']['credit_card_repay_amount'],
        #                                                     trade_password=user['u1']['trade_password'],
        #                                                     nonsuperposed_coupon_code=user['u1'][
        #                                                         'credit_card_reserved_repay_coupon_code'],
        #                                                     nonsuperposed_coupon_quantity=user['u1'][
        #                                                         'nonsuperposed_coupon_quantity'],
        #                                                     last_card_no=user['u1']['last_card_no_for_repay'])

        # 滑动理财日历
        # m.swipe_financing_calender(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            )

        # 基金追加购买(购买确认中)
        # m.fund_supplementary_purchase(user_name=user['u1']['user_name'],
        #                               login_password=user['u1']['login_password'],
        #                               fund_product_name=user['u1']['fund_product_name'],
        #                               )

        # 定活宝收益计算器(金额正常)
        # m.dhb_income_calculator(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'],
        #                         product_name=user['u1']['dqb_product'],
        #                         amount=user['u1']['dqb_product_amount']
        #                         )

        # 定活宝收益计算器(金额小于最小值)
        # m.dhb_income_calculator(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'],
        #                         product_name=user['u1']['dqb_product'],
        #                         amount=user['u1']['amount_min']
        #                         )

        # 定活宝收益计算器(金额大于最大值)
        # m.dhb_income_calculator(user_name=user['u1']['user_name'],
        #                         login_password=user['u1']['login_password'],
        #                         product_name=user['u1']['dqb_product'],
        #                         amount=user['u1']['amount_max']
        #                         )

        # 高端收益计算器(金额正常)
        # m.high_end_income_calculator(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              product_name=user['u1']['high_end_product_for_fast_redeem'],
        #                              amount=user['u1']['high_end_product_amount'])

        # 高端收益计算器(金额小于最小值)
        # m.high_end_income_calculator(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              product_name=user['u1']['high_end_product_for_fast_redeem'],
        #                              amount=user['u1']['amount_min'])

        # 高端收益计算器(金额大于最大值)
        # m.high_end_income_calculator(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'],
        #                              product_name=user['u1']['high_end_product_for_fast_redeem'],
        #                              amount=user['u1']['amount_max'])

        # 查看非货币型基金业绩
        # m.view_non_monetary_fund_performance(user_name=user['u1']['user_name'],
        #                                      login_password=user['u1']['login_password'],
        #                                      fund_product_name=user['u1']['fund_product_name']
        #                                      )

        # 查看非货币型基金公告
        # m.view_non_monetary_fund_notice(user_name=user['u1']['user_name'],
        #                                 login_password=user['u1']['login_password'],
        #                                 fund_product_name=user['u1']['fund_product_name']
        #                                 )

        # 查看货币型基金业绩
        # m.view_monetary_fund_performance(user_name=user['u1']['user_name'],
        #                                  login_password=user['u1']['login_password'],
        #                                  fund_product_name='中海货币B'
        #                                  )

        # 查看货币型基金公告
        # m.view_monetary_fund_notice(user_name=user['u1']['user_name'],
        #                             login_password=user['u1']['login_password'],
        #                             fund_product_name='中海货币B'
        #                             )

        # 未登录状态验证
        # m.check_not_login_status_details()

        # 查看高端精选系列产品历史净值
        # m.view_high_end_best_recommend_history_nav(user_name=user['u1']['user_name'],
        #                                            login_password=user['u1']['login_password'],
        #                                            product_name=u'华信证券现金管理1号集合资产管理计划')

        # 查看高端精选系列产品基础信息
        # m.view_high_end_best_recommend_basic_information(user_name=user['u1']['user_name'],
        #                                                  login_password=user['u1']['login_password'],
        #                                                  product_name=u'华信证券现金管理1号集合资产管理计划')

        # 查看高端精选系列产品业绩等其他详情信息
        # m.view_high_end_best_recommend_performance(user_name=user['u1']['user_name'],
        #                                            login_password=user['u1']['login_password'],
        #                                            product_name=u'华信证券现金管理1号集合资产管理计划')

        # 查看高端现金管理系列产品基础信息
        # m.view_high_end_cash_management_basic_information(user_name=user['u1']['user_name'],
        #                                                   login_password=user['u1']['login_password'],
        #                                                   product_name=user['u1']['cash_management_product'])

        # 查看高端现金管理系列产品历史收益
        # m.view_high_end_cash_management_history_income(user_name=user['u1']['user_name'],
        #                                                login_password=user['u1']['login_password'],
        #                                                product_name=user['u1']['cash_management_product'])

        # 查看固定收益系列产品详情
        # m.view_high_end_fixed_rate_product_details(user_name=user['u1']['user_name'],
        #                                            login_password=user['u1']['login_password'],
        #                                            product_name=u'CI高端质押产品')

        # 删除历史定投
        # m.delete_fund_history_plan(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            fund_product_name=user['u1']['fund_product_name'])

        # 查看基金历史持仓
        # m.view_fund_history_holding(user_name=user['u1']['user_name'],
        #                             login_password=user['u1']['login_password'],
        #                             fund_product_name=user['u1']['fund_product_name'])

        # 查看定活宝历史持仓
        # m.view_dhb_history_holding(user_name=user['u1']['user_name'],
        #                            login_password=user['u1']['login_password'],
        #                            product_name=user['u1']['dqb_product_2'],
        #                            name=user['u1']['name'],
        #                            risk_type=user['u1']['risk_type'])

        # 查看高端历史持仓
        # m.view_high_end_history_holding(user_name=user['u1']['user_name'],
        #                                 login_password=user['u1']['login_password'],
        #                                 product_name=user['u1']['high_end_product'])

        # 基金分红方式切换
        # m.fund_dividend_type_switch(user_name=user['u1']['user_name'],
        #                             login_password=user['u1']['login_password'],
        #                             fund_product_name=user['u1']['fund_product_name'])

        # 基金极速转换
        # m.fund_fast_convert(user_name=user['u1']['user_name'],
        #                     login_password=user['u1']['login_password'],
        #                     fund_convert_from=user['u1']['fund_fast_convert_from'],
        #                     fund_convert_to=user['u1']['fund_fast_convert_to'],
        #                     amount='2.00',
        #                     trade_password=user['u1']['trade_password'])

        # 基金极速转换撤单
        # m.cancel_fund_fast_convert_order(user_name=user['u1']['user_name'],
        #                                  login_password=user['u1']['login_password'],
        #                                  fund_convert_from=user['u1']['fund_fast_convert_from'],
        #                                  fund_convert_to=user['u1']['fund_fast_convert_to'],
        #                                  trade_password=user['u1']['trade_password'])

        # 理财型基金到期处理方式切换(全部赎回至现金宝切换为部分赎回至现金宝)
        # m.financial_fund_expiry_processing_all_to_part(user_name=user['u1']['user_name'],
        #                                                login_password=user['u1']['login_password'],
        #                                                fund_product_name=user['u1']['financial_fund_product_name'],
        #                                                fund_product_code=user['u1']['financial_fund_product_code'],
        #                                                trade_password=user['u1']['trade_password'])

        # 理财型基金到期处理方式切换(部分赎回至现金宝切换为自动续存)
        # m.financial_fund_expiry_processing_part_to_automatic(user_name=user['u1']['user_name'],
        #                                                      login_password=user['u1']['login_password'],
        #                                                      fund_product_name=user['u1'][
        #                                                          'financial_fund_product_name'],
        #                                                      fund_product_code=user['u1'][
        #                                                          'financial_fund_product_code'],
        #                                                      trade_password=user['u1']['trade_password'])

        # 理财型基金到期处理方式切换(自动续存转全部赎回至现金宝)
        # m.financial_fund_expiry_processing_automatic_to_all(user_name=user['u1']['user_name'],
        #                                                     login_password=user['u1']['login_password'],
        #                                                     fund_product_name=user['u1'][
        #                                                         'financial_fund_product_name'],
        #                                                     fund_product_code=user['u1'][
        #                                                         'financial_fund_product_code'],
        #                                                     trade_password=user['u1']['trade_password'])

        # 设置-修改个人信息
        # phone_number = Utility.GetData().mobile()
        # user_new, login_password = RestfulXjbTools().register(mobile=phone_number, login_password='a0000000')
        # m.modify_personal_information(user_name=user_new,
        #                               login_password=login_password,
        #                               email=user['u1']['mail'],
        #                               address=user['u1']['address'])

        # 用户使用通行证实名/修改用户信息
        # m.bank_card_manage_binding_card_use_laissez_passer(user_name=user_new,
        #                                                    login_password=login_password,
        #                                                    # bank_card_no=bank_card_no_nan_yue,
        #                                                    banding_card_user_name=user_name,
        #                                                    modified_name=modified_user_name,
        #                                                    modified_id_no=modified_id_no,
        #                                                    trade_password='142536',
        #                                                    laissez_passer_no=id_no)

        # 基金普通转换
        # m.fund_normal_convert(user_name=user['u1']['user_name'],
        #                       login_password=user['u1']['login_password'],
        #                       fund_convert_from=user['u1']['fund_normal_convert_from'],
        #                       fund_convert_to=user['u1']['fund_normal_convert_to'],
        #                       amount='2.00',
        #                       trade_password=user['u1']['trade_password'])

        # 基金普通转换撤单
        # m.cancel_fund_normal_convert_order(user_name=user['u1']['user_name'],
        #                                    login_password=user['u1']['login_password'],
        #                                    fund_convert_from=user['u1']['fund_normal_convert_from'],
        #                                    fund_convert_to=user['u1']['fund_normal_convert_to'],
        #                                    trade_password=user['u1']['trade_password'])

        # 基金频道--最佳表现基金
        # m.fund_best_performance_fund(user_name=user['u1']['user_name'],
        #                              login_password=user['u1']['login_password'])

        # 基金热门主题
        # m.view_fund_hot_topics(fund_product_name=user['u1']['fund_product_for_hot_topic'])

        # 高端报价式产品修改到期处理方式(全部退出切换为部分退出)
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

        # 高端报价式产品修改到期处理方式(自动续存切换为全部退出)
        # m.high_end_quotation_product_expiry_processing_auto_to_all(user_name=user['u1']['user_name'],
        #                                                            login_password=user['u1']['login_password'],
        #                                                            trade_password=user['u1']['trade_password'],
        #                                                            product_code=user['u1'][
        #                                                                'high_end_quotation_product_code'])

        # 税收居民身份声明
        # m.tax_dweller_identity_declaration(
        #     user_name=user_new,
        #     login_password=login_password)

        # 重新测评
        # m.user_risk_reevaluating(user_name=user['u1']['user_name_for_reevaluating'],
        #                          login_password=user['u1']['login_password'])

        # 银行重新签约
        # m.bank_channel_resign(user_name=user['u1']['user_name_for_bank_card_resign'],
        #                       login_password=user['u1']['login_password'],
        #                       recharge_amount='1.00',
        #                       trade_password=user['u1']['trade_password'],
        #                       card_no=user['u1']['bank_card_no_for_resign'])

        # 充值落地页查看博时详情
        # m.recharge_landing_page_view_fund_details(user_name=user['u1']['user_name_for_bank_card_resign'],
        #                                           login_password=user['u1']['login_password'])

        # 首页全局搜索
        # m.home_page_global_search(user_name=user['u1']['user_name'],
        #                           login_password=user['u1']['login_password']
        #                           )

        # 安全中心查看登录记录
        # m.security_center_view_login_record(user_name=user['u1']['user_name'],
        #                                     login_password=user['u1']['login_password'])

        #  查看新发基金
        # m.view_newly_raised_funds(product_name=user['u1']['fund_product_name_for_newly_raised_fund'])

        #  查看市场指数(基金频道底部进)
        # m.view_market_index(csi_index=user['u1']['csi_index'])

        #  查看未实名用户账户信息,实名之后,再次查看
        # m.view_user_account_information(user_name=user_new,
        #                                 login_password=login_password,
        #                                 trade_password='142536',
        #                                 name=user_name,
        #                                 id_no=id_no,
        #                                 band_card_no=bank_card_no)

        #  关闭短信验证码登录方式
        # m.lock_sms_login_mode(user_name=user['u1']['user_name_for_modify_login_mode'],
        #                        login_password=user['u1']['login_password'])

        #  开启短信验证码登录方式
        # m.unlock_sms_login_mode(user_name=user['u1']['user_name_for_modify_login_mode'],
        #                         login_password=user['u1']['login_password'],
        #                         trade_password=user['u1']['trade_password'])

        # 修改手机号码(不能接收短信)
        # m.modify_mobile_without_sms(user_name=user['u1']['user_name_for_modify_mobile_without_sms'],
        #                             login_password=user['u1']['login_password'],
        #                             # trade_password=trade_password,
        #                             mobile_new=mobile_new)

        # 购买高端产品超过500万(短信验证码,可以购买)
        # m.buy_vip_product_exceed_five_million(user_name=user['u1']['user_name'],
        #                                       login_password=user['u1']['login_password'],
        #                                       product_name=user['u1']['high_end_product'],
        #                                       amount='5000000')

        # 购买高风险产品,金额超过500万,且年纪超过70岁(风险提示,短信验证码,可以购买)
        # m.buy_high_risk_product_exceed_five_million_and_over_seventy_years_old(
        #     user_name=user['u1']['user_name_for_over_seventy_years_old'],
        #     login_password=user['u1']['login_password'],
        #     fund_product=user['u1']['fund_product_name_for_fast_redeem'],
        #     fund_code='050035',
        #     amount='5000001')

        # 现金宝存入,使用新卡付款
        m.recharge_use_new_bank_card(user_name=user['u1']['user_name_for_recharge_use_new_card'],
                                     login_password=user['u1']['login_password'],
                                     bank_card_no=bank_card_no)



    finally:
        # m.web_driver.quit()
        pass
