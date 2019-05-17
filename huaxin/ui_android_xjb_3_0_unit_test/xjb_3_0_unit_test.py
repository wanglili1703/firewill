# coding=utf-8
import time
from robot.api.deco import keyword

from _common.global_config import GlobalConfig
from _common.utility import Utility
from _tools.restful_xjb_tools import RestfulXjbTools
from _tools.ui_android_xjb_tools_3_0 import AndroidXjbTools30


class UiAndroidXjb30UnitTest:
    @keyword('Set Environemt Args')
    def set_environemt_args(self, app_path, platform_version, device_id, port, package_name, account, app_status):
        self.xjb = AndroidXjbTools30('', platform_version, device_id, port, package_name, app_status, os='Android')
        self.xjb.main_page.screen_shot()
        self._account = getattr(GlobalConfig.XjbAccountInfo, account)

    @keyword('Case Tear Down')
    def tear_down(self):
        time.sleep(1)
        self.xjb.main_page.screen_shot()
        self.xjb.web_driver.quit()
        return

    # 首页现金宝取出(正常值)
    @keyword('test_home_page_recharge_normal')
    def home_page_recharge_normal(self):
        self.xjb.home_page_recharge(user_name=self._account['u1']['user_name'],
                                    login_password=self._account['u1']['login_password'],
                                    recharge_amount='100',
                                    trade_password=self._account['u1']['trade_password'])

    # 首页现金宝取出(存入金额小于最小值)
    @keyword('test_home_page_recharge_min')
    def home_page_recharge_min(self):
        self.xjb.home_page_recharge(user_name=self._account['u1']['user_name'],
                                    login_password=self._account['u1']['login_password'],
                                    recharge_amount='0',
                                    trade_password=self._account['u1']['trade_password'])

    @keyword('test_home_page_recharge_max')
    def home_page_recharge_max(self):
        self.xjb.home_page_recharge(user_name=self._account['u1']['user_name'],
                                    login_password=self._account['u1']['login_password'],
                                    recharge_amount='1000000000000',
                                    trade_password=self._account['u1']['trade_password'])

    # 首页现金宝普取(金额正常)
    @keyword('test_home_page_regular_withdraw_normal')
    def home_page_regular_withdraw_normal(self):
        self.xjb.home_page_regular_withdraw(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            withdraw_amount='0.1',
                                            trade_password=self._account['u1']['trade_password'])

    # 首页现金宝普取(金额小于最小值)
    @keyword('test_home_page_regular_withdraw_min')
    def home_page_regular_withdraw_min(self):
        self.xjb.home_page_regular_withdraw(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            withdraw_amount='0',
                                            trade_password=self._account['u1']['trade_password'])

    # 首页现金宝普取(金额大于最大值)
    @keyword('test_home_page_regular_withdraw_max')
    def home_page_regular_withdraw_max(self):
        self.xjb.home_page_regular_withdraw(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            withdraw_amount='100000000000000000',
                                            trade_password=self._account['u1']['trade_password'])

    # 现金宝首页快取(金额正常)
    @keyword('test_home_page_fast_withdraw_normal')
    def home_page_fast_withdraw_normal(self):
        self.xjb.home_page_fast_withdraw(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         withdraw_amount='0.1',
                                         trade_password=self._account['u1']['trade_password'])

    # 现金宝首页快取(金额小于最小值)
    @keyword('test_home_page_fast_withdraw_min')
    def home_page_fast_withdraw_min(self):
        self.xjb.home_page_fast_withdraw(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         withdraw_amount='0',
                                         trade_password=self._account['u1']['trade_password'])

    # 现金宝首页快取(金额大于最大值)
    @keyword('test_home_page_fast_withdraw_max')
    def home_page_fast_withdraw_max(self):
        self.xjb.home_page_fast_withdraw(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         withdraw_amount='100000000000000000',
                                         trade_password=self._account['u1']['trade_password'])

    @keyword('test_home_page_view_essence_recommend_list')
    def home_page_view_essence_recommend_list(self):
        self.xjb.home_page_view_essence_recommend_list(user_name=self._account['u1']['user_name'],
                                                       login_password=self._account['u1']['login_password'])

    @keyword('test_register')
    def register(self):
        phone_number = Utility.GetData().mobile()
        self.xjb.register(phone_number=phone_number,
                          login_password='a0000000')

    @keyword('test_register_binding_card')
    def register_binding_card(self):
        phone_number = Utility.GetData().mobile()
        user_name = Utility.GetData().english_name()
        id_no = Utility.GetData().id_no()
        band_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]

        self.xjb.register_binding_card(phone_number=phone_number,
                                       login_password='a0000000',
                                       trade_password='135790',
                                       user_name=user_name,
                                       id_no=id_no,
                                       band_card_no=band_card_no)

    @keyword('test_bank_card_manage_binding_card')
    def bank_card_manage_binding_card(self):
        bank_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password, card_no = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                       login_password='a0000000',
                                                                                       card_bin='622202',
                                                                                       trade_password='135790',
                                                                                       recharge_amount='10000')

        self.xjb.bank_card_manage_binding_card(user_name=user_new,
                                               login_password=login_password,
                                               bank_card_no=bank_card_no)

    @keyword('test_bank_card_manage_binding_nan_yue_card')
    def bank_card_manage_binding_nan_yue_card(self):
        bank_card_no = Utility.GetData().bank_card_no(card_bin='623595').split('-')[0]
        phone_number = Utility.GetData().mobile()
        user_name = Utility.GetData().english_name()
        id_no = Utility.GetData().id_no()

        user_new, login_password = RestfulXjbTools().register(mobile=phone_number,
                                                              login_password='a0000000')

        self.xjb.bank_card_manage_binding_nan_yue_card(user_name=user_new,
                                                       login_password=login_password,
                                                       bank_card_no=bank_card_no,
                                                       banding_card_user_name=user_name,
                                                       trade_password='142536',
                                                       id_no=id_no)

    @keyword('test_delete_bank_card')
    def delete_bank_card(self):
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password, card_no = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                       login_password='a0000000',
                                                                                       card_bin='622202',
                                                                                       trade_password='135790')
        self.xjb.delete_bank_card(user_name=user_new,
                                  login_password=login_password,
                                  trade_password=trade_password,
                                  last_card_no=card_no[-4:])

    @keyword('test_modify_mobile')
    def modify_mobile(self):
        phone_number = Utility.GetData().mobile()
        mobile_new = Utility.GetData().mobile()
        user_new, login_password, trade_password, card_no = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                       login_password='a0000000',
                                                                                       card_bin='622202',
                                                                                       trade_password='135790',
                                                                                       recharge_amount='10000')

        self.xjb.modify_mobile(user_name=user_new,
                               login_password=login_password,
                               trade_password=trade_password,
                               mobile_new=mobile_new)

    @keyword('test_security_center_modify_trade_password')
    def security_center_modify_trade_password(self):
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password, card_no = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                       login_password='a0000000',
                                                                                       card_bin='622202',
                                                                                       trade_password='135790',
                                                                                       recharge_amount='10000')

        self.xjb.security_center_modify_trade_password(user_name=user_new,
                                                       login_password=login_password,
                                                       trade_password_old=trade_password,
                                                       trade_password_new='147258')

    @keyword('test_security_center_modify_login_password')
    def security_center_modify_login_password(self):
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password, card_no = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                       login_password='a0000000',
                                                                                       card_bin='622202',
                                                                                       trade_password='135790',
                                                                                       recharge_amount='10000')

        self.xjb.security_center_modify_login_password(user_name=user_new,
                                                       login_password=login_password,
                                                       login_password_new='a1111111')

    @keyword('test_security_center_find_trade_password')
    def security_center_find_trade_password(self):
        self.xjb.security_center_find_trade_password(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'])

    # 购买高端(金额正常)
    @keyword('test_buy_high_end_product_normal')
    def buy_high_end_product_normal(self):
        self.xjb.buy_high_end_product(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      trade_password=self._account['u1']['trade_password'],
                                      product_name=self._account['u1']['high_end_product'],
                                      amount=self._account['u1']['high_end_product_amount'])

    # 购买高端(金额小于最小值)
    @keyword('test_buy_high_end_product_min')
    def buy_high_end_product(self):
        self.xjb.buy_high_end_product(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      trade_password=self._account['u1']['trade_password'],
                                      product_name=self._account['u1']['high_end_product'],
                                      amount=self._account['u1']['amount_min'])

    # 购买高端(金额大于最大值)
    @keyword('test_buy_high_end_product_max')
    def buy_high_end_product_max(self):
        self.xjb.buy_high_end_product(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      trade_password=self._account['u1']['trade_password'],
                                      product_name=self._account['u1']['high_end_product'],
                                      amount=self._account['u1']['amount_max'])

    # 购买定活宝(金额正常)
    @keyword('test_buy_dqb_product_normal')
    def buy_dqb_product_normal(self):
        self.xjb.buy_dqb_product(user_name=self._account['u1']['user_name'],
                                 login_password=self._account['u1']['login_password'],
                                 product_name=self._account['u1']['dqb_product'],
                                 amount=self._account['u1']['dqb_product_amount'],
                                 trade_password=self._account['u1']['trade_password'])

    # 购买定活宝(金额小于最小值)
    @keyword('test_buy_dqb_product_min')
    def buy_dqb_product_min(self):
        self.xjb.buy_dqb_product(user_name=self._account['u1']['user_name'],
                                 login_password=self._account['u1']['login_password'],
                                 product_name=self._account['u1']['dqb_product'],
                                 amount=self._account['u1']['amount_min'],
                                 trade_password=self._account['u1']['trade_password'])

    # 购买定活宝(金额大于最大值)
    @keyword('test_buy_dqb_product_max')
    def buy_dqb_product_max(self):
        self.xjb.buy_dqb_product(user_name=self._account['u1']['user_name'],
                                 login_password=self._account['u1']['login_password'],
                                 product_name=self._account['u1']['dqb_product'],
                                 amount=self._account['u1']['amount_max'],
                                 trade_password=self._account['u1']['trade_password'])

    @keyword('test_hot_switch_to_dqb_product_list_page')
    def hot_switch_to_regular_product_list_page(self):
        self.xjb.hot_switch_to_dqb_product_list_page(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'])

    @keyword('test_hot_switch_to_high_end_product_list_page')
    def hot_switch_to_high_end_product_list_page(self):
        self.xjb.hot_switch_to_high_end_product_list_page(user_name=self._account['u1']['user_name'],
                                                          login_password=self._account['u1']['login_password'])

    @keyword('test_finance_product_search_with_full_name')
    def finance_product_search_with_full_name(self):
        self.xjb.finance_product_search_with_full_name(user_name=self._account['u1']['user_name'],
                                                       login_password=self._account['u1']['login_password'],
                                                       product_name=self._account['u1']['search_with_full_name'])

    @keyword('test_finance_product_search_with_short_name')
    def finance_product_search_with_short_name(self):
        self.xjb.finance_product_search_with_short_name(user_name=self._account['u1']['user_name'],
                                                        login_password=self._account['u1']['login_password'],
                                                        product_name=self._account['u1']['search_with_short_name'])

    # 资产页现金宝存入(存入金额大于等于0.01)
    @keyword('test_assets_xjb_detail_page_recharge_normal')
    def assets_xjb_detail_page_recharge_normal(self):
        self.xjb.assets_xjb_detail_page_recharge(user_name=self._account['u1']['user_name'],
                                                 login_password=self._account['u1']['login_password'],
                                                 recharge_amount='100',
                                                 trade_password=self._account['u1']['trade_password'])

    # 资产页现金宝存入(存入金额小于0.01)
    @keyword('test_assets_xjb_detail_page_recharge_min')
    def test_assets_xjb_detail_page_recharge_min(self):
        self.xjb.assets_xjb_detail_page_recharge(user_name=self._account['u1']['user_name'],
                                                 login_password=self._account['u1']['login_password'],
                                                 recharge_amount='0',
                                                 trade_password=self._account['u1']['trade_password'])

    # 资产页现金宝存入(存入金额大于限额)
    @keyword('test_assets_xjb_detail_page_recharge_max')
    def assets_xjb_detail_page_recharge_max(self):
        self.xjb.assets_xjb_detail_page_recharge(user_name=self._account['u1']['user_name'],
                                                 login_password=self._account['u1']['login_password'],
                                                 recharge_amount='10000000000000',
                                                 trade_password=self._account['u1']['trade_password'])

    # 资产页现金宝取出(取出金额正常)
    @keyword('test_assets_xjb_detail_page_regular_withdraw_normal')
    def assets_xjb_detail_page_regular_withdraw_normal(self):
        self.xjb.assets_xjb_detail_page_regular_withdraw(user_name=self._account['u1']['user_name'],
                                                         login_password=self._account['u1']['login_password'],
                                                         withdraw_amount='0.1',
                                                         trade_password=self._account['u1']['trade_password'])

    # 资产页现金宝取出(取出金额小于最小限额)
    @keyword('test_assets_xjb_detail_page_regular_withdraw_min')
    def assets_xjb_detail_page_regular_withdraw_min(self):
        self.xjb.assets_xjb_detail_page_regular_withdraw(user_name=self._account['u1']['user_name'],
                                                         login_password=self._account['u1']['login_password'],
                                                         withdraw_amount='0',
                                                         trade_password=self._account['u1']['trade_password'])

    # 资产页现金宝取出(取出金额大于最大限额)
    @keyword('test_assets_xjb_detail_page_regular_withdraw_max')
    def assets_xjb_detail_page_regular_withdraw_max(self):
        self.xjb.assets_xjb_detail_page_regular_withdraw(user_name=self._account['u1']['user_name'],
                                                         login_password=self._account['u1']['login_password'],
                                                         withdraw_amount='100000000000000000',
                                                         trade_password=self._account['u1']['trade_password'])

    # 资产页现金宝快取(取出金额正常)
    @keyword('test_assets_xjb_detail_page_fast_withdraw_normal')
    def assets_xjb_detail_page_fast_withdraw_normal(self):
        self.xjb.assets_xjb_detail_page_fast_withdraw(user_name=self._account['u1']['user_name'],
                                                      login_password=self._account['u1']['login_password'],
                                                      withdraw_amount='0.01',
                                                      trade_password=self._account['u1']['trade_password'])

    # 资产页现金宝快取(取出金额小于最小值)
    @keyword('test_assets_xjb_detail_page_fast_withdraw_min')
    def assets_xjb_detail_page_fast_withdraw_min(self):
        self.xjb.assets_xjb_detail_page_fast_withdraw(user_name=self._account['u1']['user_name'],
                                                      login_password=self._account['u1']['login_password'],
                                                      withdraw_amount='0',
                                                      trade_password=self._account['u1']['trade_password'])

    # 资产页现金宝快取(取出金额正常)
    @keyword('test_assets_xjb_detail_page_fast_withdraw_max')
    def assets_xjb_detail_page_fast_withdraw_max(self):
        self.xjb.assets_xjb_detail_page_fast_withdraw(user_name=self._account['u1']['user_name'],
                                                      login_password=self._account['u1']['login_password'],
                                                      withdraw_amount='10000000000000000',
                                                      trade_password=self._account['u1']['trade_password'])

    @keyword('test_delete_credit_card')
    def delete_credit_card(self):
        self.xjb.delete_credit_card(user_name=self._account['u1']['user_name'],
                                    login_password=self._account['u1']['login_password'],
                                    last_card_no=self._account['u1']['last_card_no'],
                                    trade_password=self._account['u1']['trade_password'])

    @keyword('test_add_credit_card')
    def add_credit_card(self):
        self.xjb.add_credit_card(user_name=self._account['u1']['user_name'],
                                 login_password=self._account['u1']['login_password'],
                                 credit_card_no=self._account['u1']['credit_card_no'],
                                 last_card_no=self._account['u1']['last_card_no'])

    @keyword('test_view_message')
    def view_message(self):
        self.xjb.view_message(user_name=self._account['u1']['user_name'],
                              login_password=self._account['u1']['login_password'])

    # @keyword('test_view_xjb_trade_detail')
    # def view_xjb_trade_detail(self):
    #     self.xjb.view_xjb_trade_detail(user_name=self._account['u1']['user_name'],
    #                                    login_password=self._account['u1']['login_password'])

    @keyword('test_dqb_detail_page_view_trade_detail')
    def view_dqb_trade_detail(self):
        self.xjb.dqb_detail_page_view_trade_detail(user_name=self._account['u1']['user_name'],
                                                   login_password=self._account['u1']['login_password'])

    @keyword('test_view_dqb_more_product')
    def view_dqb_more_product(self):
        self.xjb.view_dqb_more_product(user_name=self._account['u1']['user_name'],
                                       login_password=self._account['u1']['login_password'])

    @keyword('test_view_dqb_history_product')
    def view_dqb_history_product(self):
        self.xjb.view_dqb_history_product(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'])

    @keyword('test_fund_detail_page_view_trade_detail')
    def fund_detail_page_view_trade_detail(self):
        self.xjb.fund_detail_page_view_trade_detail(user_name=self._account['u1']['user_name'],
                                                    login_password=self._account['u1']['login_password'])

    @keyword('test_view_fund_more_product')
    def view_fund_more_product(self):
        self.xjb.view_fund_more_product(user_name=self._account['u1']['user_name'],
                                        login_password=self._account['u1']['login_password'])

    @keyword('test_high_end_detail_page_view_trade_detail')
    def high_end_detail_page_view_trade_detail(self):
        self.xjb.high_end_detail_page_view_trade_detail(user_name=self._account['u1']['user_name'],
                                                        login_password=self._account['u1']['login_password'])

    @keyword('test_view_high_end_more_product')
    def view_high_end_more_product(self):
        self.xjb.view_high_end_more_product(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'])

    @keyword('test_view_high_end_history_product')
    def view_high_end_history_product(self):
        self.xjb.view_high_end_history_product(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'])

    # 赎回高端(份额正常)
    @keyword('test_redeem_high_end_product_normal')
    def redeem_high_end_product_normal(self):
        self.xjb.redeem_high_end_product(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         redeem_amount=self._account['u1']['high_end_product_amount'],
                                         # redeem_amount=self._account['u1']['high_end_product_amount_for_redeem'],
                                         trade_password=self._account['u1']['trade_password'],
                                         high_end_product=self._account['u1']['high_end_product'])

    # 赎回高端(份额小于最小值)
    @keyword('test_redeem_high_end_product_min')
    def redeem_high_end_product_min(self):
        self.xjb.redeem_high_end_product(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         redeem_amount=self._account['u1']['amount_min'],
                                         # redeem_amount=self._account['u1']['high_end_product_amount_for_redeem'],
                                         trade_password=self._account['u1']['trade_password'],
                                         high_end_product=self._account['u1']['high_end_product'])

    # 赎回高端(份额大于最大值)
    @keyword('test_redeem_high_end_product_max')
    def redeem_high_end_product_max(self):
        self.xjb.redeem_high_end_product(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         redeem_amount=self._account['u1']['amount_max'],
                                         # redeem_amount=self._account['u1']['high_end_product_amount_for_redeem'],
                                         trade_password=self._account['u1']['trade_password'],
                                         high_end_product=self._account['u1']['high_end_product'])

    # 赎回定期宝(金额正常)
    @keyword('test_redeem_dqb_product_normal')
    def redeem_dqb_product_normal(self):
        self.xjb.redeem_dqb_product(
            user_name=self._account['u1']['user_name'],
            # user_name=self._account['u1']['user_name_for_dqb_redeem'],
            # login_password=self._account['u1']['login_password_for_dqb_redeem'],
            login_password=self._account['u1']['login_password'],
            redeem_amount=self._account['u1']['dqb_product_amount_2'],
            trade_password=self._account['u1']['trade_password'],
            dqb_product=self._account['u1']['dqb_product_2'])

    # 赎回定期宝(金额小于最小值)
    @keyword('test_redeem_dqb_product_min')
    def redeem_dqb_product_min(self):
        self.xjb.redeem_dqb_product(
            user_name=self._account['u1']['user_name'],
            # user_name=self._account['u1']['user_name_for_dqb_redeem'],
            # login_password=self._account['u1']['login_password_for_dqb_redeem'],
            login_password=self._account['u1']['login_password'],
            redeem_amount=self._account['u1']['amount_min'],
            trade_password=self._account['u1']['trade_password'],
            dqb_product=self._account['u1']['dqb_product_2'])

    # 赎回定期宝(金额大于最大值)
    @keyword('test_redeem_dqb_product_max')
    def redeem_dqb_product_max(self):
        self.xjb.redeem_dqb_product(
            user_name=self._account['u1']['user_name'],
            # user_name=self._account['u1']['user_name_for_dqb_redeem'],
            # login_password=self._account['u1']['login_password_for_dqb_redeem'],
            login_password=self._account['u1']['login_password'],
            redeem_amount=self._account['u1']['amount_max'],
            trade_password=self._account['u1']['trade_password'],
            dqb_product=self._account['u1']['dqb_product_2'])

    @keyword('test_my_referee')
    def my_referee(self):
        self.xjb.my_referee(user_name=self._account['u1']['user_name'],
                            login_password=self._account['u1']['login_password'],
                            phone_no=self._account['u2']['user_name'])

    @keyword('test_risk_evaluating_new_user')
    def risk_evaluating_new_user(self):
        phone_number = Utility.GetData().mobile()
        user_new, login_password = RestfulXjbTools().register(mobile=phone_number, login_password='a0000000')

        self.xjb.risk_evaluating_new_user(user_name=user_new,
                                          login_password=login_password)

    @keyword('test_fund_product_search_with_name')
    def fund_product_search_with_name(self):
        self.xjb.fund_product_search_with_name(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'],
                                               fund_product_name=self._account['u1']['fund_product_name'])

    @keyword('test_fund_product_search_with_code')
    def fund_product_search_with_code(self):
        self.xjb.fund_product_search_with_code(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'],
                                               fund_product_code=self._account['u1']['fund_product_code'])

    # 购买基金(金额正常)
    @keyword('test_buy_fund_product_normal')
    def buy_fund_product_normal(self):
        self.xjb.buy_fund_product(user_name=self._account['u1']['user_name'],
                                  login_password=self._account['u1']['login_password'],
                                  fund_product_name=self._account['u1']['fund_product_name'],
                                  amount=self._account['u1']['fund_product_amount'],
                                  trade_password=self._account['u1']['trade_password'],
                                  fund_product_code=self._account['u1']['fund_product_code'],
                                  )

    # 购买基金(金额小于最小值)
    @keyword('test_buy_fund_product_min')
    def buy_fund_product_min(self):
        self.xjb.buy_fund_product(user_name=self._account['u1']['user_name'],
                                  login_password=self._account['u1']['login_password'],
                                  fund_product_name=self._account['u1']['fund_product_name'],
                                  amount=self._account['u1']['amount_min'],
                                  trade_password=self._account['u1']['trade_password'],
                                  fund_product_code=self._account['u1']['fund_product_code'],
                                  )

    # 购买基金(金额大于最大值)
    @keyword('test_buy_fund_product_max')
    def buy_fund_product_max(self):
        self.xjb.buy_fund_product(user_name=self._account['u1']['user_name'],
                                  login_password=self._account['u1']['login_password'],
                                  fund_product_name=self._account['u1']['fund_product_name'],
                                  amount=self._account['u1']['amount_max'],
                                  trade_password=self._account['u1']['trade_password'],
                                  fund_product_code=self._account['u1']['fund_product_code'],
                                  )

    # 基金追加购买(购买确认中)
    @keyword('test_fund_supplementary_purchase')
    def fund_supplementary_purchase(self):
        self.xjb.fund_supplementary_purchase(user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password'],
                                             fund_product_name=self._account['u1']['fund_product_name']
                                             )

    @keyword('test_invite_friend')
    def invite_friend(self):
        self.xjb.invite_friend(user_name=self._account['u1']['user_name'],
                               login_password=self._account['u1']['login_password'])

    @keyword('test_use_other_reservation_code')
    def use_other_reservation_code(self):
        self.xjb.use_other_reservation_code(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            trade_password=self._account['u1']['trade_password'],
                                            buy_quota=self._account['u1']['reservation_code_buy_quota'],
                                            buy_count=self._account['u1']['reservation_code_buy_count'],
                                            reserve_quota=self._account['u1']['reservation_code_reserve_quota'],
                                            reserve_count=self._account['u1']['reservation_code_reserve_count'],
                                            reserve_code=self._account['u1']['reserve_code'],
                                            product_id=self._account['u1']['product_id_for_reservation_code']
                                            )

    @keyword('test_use_reservation_code')
    def use_reservation_code(self):
        self.xjb.use_reservation_code(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      trade_password=self._account['u1']['trade_password'],
                                      buy_quota=self._account['u1']['reservation_code_buy_quota'],
                                      buy_count=self._account['u1']['reservation_code_buy_count'],
                                      reserve_quota=self._account['u1']['reservation_code_reserve_quota'],
                                      reserve_count=self._account['u1']['reservation_code_reserve_count'],
                                      reserve_code=self._account['u1']['reserve_code'],
                                      product_id=self._account['u1']['product_id_for_reservation_code']
                                      )

    # 赎回基金(份额正常)
    @keyword('test_redeem_fund_product_normal')
    def redeem_fund_product_normal(self):
        self.xjb.redeem_fund_product(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     fund_product=self._account['u1']['fund_product_name'],
                                     amount=self._account['u1']['fund_product_amount'],
                                     trade_password=self._account['u1']['trade_password'])

    # 赎回基金(份额小于最小值)
    @keyword('test_redeem_fund_product_min')
    def redeem_fund_product_min(self):
        self.xjb.redeem_fund_product(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     fund_product=self._account['u1']['fund_product_name'],
                                     amount=self._account['u1']['amount_min'],
                                     trade_password=self._account['u1']['trade_password'])

    # 赎回基金(份额大于最大值)
    @keyword('test_redeem_fund_product_max')
    def redeem_fund_product_max(self):
        self.xjb.redeem_fund_product(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     fund_product=self._account['u1']['fund_product_name'],
                                     amount=self._account['u1']['amount_max'],
                                     trade_password=self._account['u1']['trade_password'])

    @keyword('test_earn_points')
    def earn_points(self):
        self.xjb.earn_points(user_name=self._account['u1']['user_name'],
                             login_password=self._account['u1']['login_password'],
                             amount=self._account['u1']['fund_product_amount'],
                             trade_password=self._account['u1']['trade_password'],
                             fund_product_name=self._account['u1']['fund_product_name'],
                             fund_product_code=self._account['u1']['fund_product_code'],
                             )

    # 信用卡还款
    @keyword('test_credit_card_repay')
    def credit_card_repay(self):
        self.xjb.credit_card_repay(user_name=self._account['u1']['user_name'],
                                   login_password=self._account['u1']['login_password'],
                                   repay_amount=self._account['u1']['credit_card_repay_amount'],
                                   trade_password=self._account['u1']['trade_password'],
                                   last_card_no=self._account['u1']['last_card_no_for_repay'])

    # 信用卡预约还款
    @keyword('test_credit_card_reserved_pay')
    def credit_card_reserved_pay(self):
        self.xjb.credit_card_reserved_pay(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          reserved_pay_amount=self._account['u1']['credit_card_reserved_pay_amount'],
                                          trade_password=self._account['u1']['trade_password'],
                                          last_card_no=self._account['u1']['last_card_no_for_repay'])

    # 取消预约还款
    @keyword('test_cancel_reserved_pay')
    def cancel_reserved_pay(self):
        self.xjb.cancel_reserved_pay(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     last_card_no=self._account['u1']['last_card_no_for_repay'])

    # 赚积分--推荐用户注册绑卡
    @keyword('test_earn_points_by_recommend_user_register')
    def earn_points_by_recommend_user_register(self):
        self.xjb.earn_points_by_recommend_user_register(user_name=self._account['u1']['user_name'],
                                                        login_password=self._account['u1']['login_password'])

    # 花积分--买基金
    @keyword('test_spend_points_by_buy_fund')
    def spend_points_by_buy_fund(self):
        self.xjb.spend_points_by_buy_fund(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          amount=self._account['u1']['fund_product_amount'],
                                          trade_password=self._account['u1']['trade_password'],
                                          fund_product_name=self._account['u1']['fund_product_name'],
                                          fund_product_code=self._account['u1']['fund_product_code']
                                          )

    # 花积分--买高端产品
    @keyword('test_spend_points_by_buy_vipproduct_use_product_name')
    def spend_points_by_buy_vipproduct_use_product_name(self):
        self.xjb.spend_points_by_buy_vipproduct_use_product_name(user_name=self._account['u1']['user_name'],
                                                                 login_password=self._account['u1']['login_password'],
                                                                 trade_password=self._account['u1']['trade_password'],
                                                                 product_name=self._account['u1'][
                                                                     'high_end_product_for_points'],
                                                                 # product_name=self._account['u1']['high_end_product_for_points_offset'],
                                                                 amount=self._account['u1']['high_end_product_amount'])

    # 花积分--买定期产品
    @keyword('test_spend_points_by_buy_dqb')
    def spend_points_by_buy_dqb(self):
        self.xjb.spend_points_by_buy_dqb(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         trade_password=self._account['u1']['trade_password'],
                                         # dqb_product=self._account['u1']['dqb_product'],
                                         dqb_product=self._account['u1']['dqb_product_3'],
                                         dqb_product_amount=self._account['u1']['dqb_product_amount'])

    # 设置还款提醒
    @keyword('test_add_credit_card_repayment_warn')
    def add_credit_card_repayment_warn(self):
        self.xjb.add_credit_card_repayment_warn(user_name=self._account['u1']['user_name'],
                                                login_password=self._account['u1']['login_password'],
                                                last_card_no=self._account['u1']['last_card_no_for_repay'])

    # 取消还款提醒
    @keyword('test_cancel_credit_card_repayment_warn')
    def cancel_credit_card_repayment_warn(self):
        self.xjb.cancel_credit_card_repayment_warn(user_name=self._account['u1']['user_name'],
                                                   login_password=self._account['u1']['login_password'],
                                                   last_card_no=self._account['u1']['last_card_no_for_repay'])

    # 高端普通卖出
    @keyword('test_normal_redeem_vipproduct')
    def normal_redeem_vipproduct(self):
        self.xjb.normal_redeem_vipproduct(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          redeem_amount=self._account['u1']['high_end_product_amount'],
                                          trade_password=self._account['u1']['trade_password'],
                                          high_end_product_for_fast_redeem=self._account['u1'][
                                              'high_end_product_for_fast_redeem'])

    # 高端极速卖出
    @keyword('test_fast_redeem_vipproduct')
    def fast_redeem_vipproduct(self):
        self.xjb.fast_redeem_vipproduct(user_name=self._account['u1']['user_name'],
                                        login_password=self._account['u1']['login_password'],
                                        redeem_amount=self._account['u1']['high_end_product_amount'],
                                        trade_password=self._account['u1']['trade_password'],
                                        high_end_product_for_fast_redeem=self._account['u1'][
                                            'high_end_product_for_fast_redeem'])

    # 基金普通卖出
    @keyword('test_normal_redeem_fund_product')
    def normal_redeem_fund_product(self):
        self.xjb.normal_redeem_fund_product(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            redeem_amount=self._account['u1']['fund_product_amount'],
                                            trade_password=self._account['u1']['trade_password'],
                                            fund_product_name_for_fast_redeem=self._account['u1'][
                                                'fund_product_name_for_fast_redeem'])

    # 基金极速卖出
    @keyword('test_fast_redeem_fund_product')
    def fast_redeem_fund_product(self):
        self.xjb.fast_redeem_fund_product(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          redeem_amount=self._account['u1']['fund_product_amount'],
                                          trade_password=self._account['u1']['trade_password'],
                                          fund_product_name_for_fast_redeem=self._account['u1'][
                                              'fund_product_name_for_fast_redeem']
                                          )

    # 积分明细
    @keyword('test_assets_my_points_details')
    def assets_my_points_details(self):
        self.xjb.assets_my_points_details(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password']
                                          )

    # 基金频道--研究报告
    @keyword('test_fund_research_report')
    def fund_research_report(self):
        self.xjb.fund_research_report(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password']
                                      )

    # 基金频道--机构观点
    @keyword('test_fund_institution_viewpoint')
    def fund_institution_viewpoint(self):
        self.xjb.fund_institution_viewpoint(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password']
                                            )

    # 基金频道--达人论基
    @keyword('test_fund_talent_fund_discussion')
    def fund_talent_fund_discussion(self):
        self.xjb.fund_talent_fund_discussion(user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password']
                                             )

    # 基金频道--市场指数
    @keyword('test_fund_market_index')
    def fund_market_index(self):
        self.xjb.fund_market_index(user_name=self._account['u1']['user_name'],
                                   login_password=self._account['u1']['login_password'],
                                   csi_index=self._account['u1']['csi_index']
                                   )

    # 基金频道--全部基金
    @keyword('test_fund_all_funds')
    def fund_all_funds(self):
        self.xjb.fund_all_funds(user_name=self._account['u1']['user_name'],
                                login_password=self._account['u1']['login_password']
                                )

    # 基金频道--评级排行
    @keyword('test_fund_all_funds')
    def fund_all_funds(self):
        self.xjb.fund_all_funds(user_name=self._account['u1']['user_name'],
                                login_password=self._account['u1']['login_password']
                                )

    # 基金频道--自选基金
    @keyword('test_fund_selected_funds')
    def fund_selected_funds(self):
        self.xjb.fund_selected_funds(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     fund_product_name=self._account['u1']['fund_product_name'],
                                     fund_product_code=self._account['u1']['fund_product_code']
                                     )

    # 基金频道--删除自选基金
    @keyword('test_fund_selected_funds_deleted')
    def fund_selected_funds_deleted(self):
        self.xjb.fund_selected_funds_deleted(user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password'],
                                             fund_product_name=self._account['u1']['fund_product_name'],
                                             fund_product_code=self._account['u1']['fund_product_code']
                                             )

    # 基金频道--对比分析
    @keyword('test_fund_comparasion_and_analysis')
    def fund_comparasion_and_analysis(self):
        self.xjb.fund_comparasion_and_analysis(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'],
                                               fund_product_code=self._account['u1']['fund_product_code'],
                                               fund_product_code_2=self._account['u1']['fund_product_code_2'],
                                               )

    # 购买定期宝使用优惠券(不可叠加)
    @keyword('test_buy_dqb_use_nonsuperposed_coupon')
    def buy_dqb_use_nonsuperposed_coupon(self):
        self.xjb.buy_dqb_use_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                  login_password=self._account['u1']['login_password'],
                                                  nonsuperposed_coupon_code=self._account['u1'][
                                                      'nonsuperposed_coupon_code'],
                                                  nonsuperposed_coupon_quantity=self._account['u1'][
                                                      'nonsuperposed_coupon_quantity'],
                                                  amount=self._account['u1']['dqb_product_amount'],
                                                  trade_password=self._account['u1']['trade_password'],
                                                  product_name=self._account['u1']['dqb_product_for_coupon']
                                                  # product_name=self._account['u1']['dqb_product']
                                                  )

    # 购买定期宝使用优惠券(可叠加)
    @keyword('test_buy_dqb_use_superposed_coupon')
    def buy_dqb_use_superposed_coupon(self):
        self.xjb.buy_dqb_use_superposed_coupon(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'],
                                               superposed_coupon_code=self._account['u1']['superposed_coupon_code'],
                                               superposed_coupon_quantity=self._account['u1'][
                                                   'superposed_coupon_quantity'],
                                               amount=self._account['u1']['dqb_product_amount'],
                                               trade_password=self._account['u1']['trade_password'],
                                               product_name=self._account['u1']['dqb_product_for_coupon']
                                               # product_name=self._account['u1']['dqb_product']
                                               )

    # 购买高端使用优惠券(不可叠加)
    @keyword('test_buy_vipproduct_use_nonsuperposed_coupon')
    def buy_vipproduct_use_nonsuperposed_coupon(self):
        self.xjb.buy_vipproduct_use_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                         login_password=self._account['u1']['login_password'],
                                                         nonsuperposed_coupon_code=self._account['u1'][
                                                             'nonsuperposed_coupon_code'],
                                                         nonsuperposed_coupon_quantity=self._account['u1'][
                                                             'nonsuperposed_coupon_quantity'],
                                                         amount=self._account['u1']['high_end_product_amount'],
                                                         trade_password=self._account['u1']['trade_password'],
                                                         # product_name=self._account['u1']['high_end_product_for_points']
                                                         product_name=self._account['u1']['high_end_product']
                                                         )

    # 购买高端使用优惠券(可叠加)
    @keyword('test_buy_vipproduct_use_superposed_coupon')
    def buy_vipproduct_use_superposed_coupon(self):
        self.xjb.buy_vipproduct_use_superposed_coupon(user_name=self._account['u1']['user_name'],
                                                      login_password=self._account['u1']['login_password'],
                                                      superposed_coupon_code=self._account['u1'][
                                                          'superposed_coupon_code'],
                                                      superposed_coupon_quantity=self._account['u1'][
                                                          'superposed_coupon_quantity'],
                                                      amount=self._account['u1']['high_end_product_amount'],
                                                      trade_password=self._account['u1']['trade_password'],
                                                      # product_name=self._account['u1']['high_end_product_for_points']
                                                      product_name=self._account['u1']['high_end_product']
                                                      )

    # 购买基金使用优惠券(不可叠加)
    @keyword('test_buy_fund_use_nonsuperposed_coupon')
    def buy_fund_use_nonsuperposed_coupon(self):
        self.xjb.buy_fund_use_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                   login_password=self._account['u1']['login_password'],
                                                   nonsuperposed_coupon_code=self._account['u1'][
                                                       'nonsuperposed_coupon_code'],
                                                   nonsuperposed_coupon_quantity=self._account['u1'][
                                                       'nonsuperposed_coupon_quantity'],
                                                   fund_product_name=self._account['u1']['fund_product_name'],
                                                   amount=self._account['u1']['fund_product_amount'],
                                                   trade_password=self._account['u1']['trade_password'],
                                                   fund_product_code=self._account['u1']['fund_product_code']
                                                   )

    # 购买基金使用优惠券(可叠加)
    @keyword('test_buy_fund_use_superposed_coupon')
    def buy_fund_use_superposed_coupon(self):
        self.xjb.buy_fund_use_superposed_coupon(user_name=self._account['u1']['user_name'],
                                                login_password=self._account['u1']['login_password'],
                                                superposed_coupon_code=self._account['u1']['superposed_coupon_code'],
                                                superposed_coupon_quantity=self._account['u1'][
                                                    'superposed_coupon_quantity'],
                                                fund_product_name=self._account['u1']['fund_product_name'],
                                                amount=self._account['u1']['fund_product_amount'],
                                                trade_password=self._account['u1']['trade_password'],
                                                fund_product_code=self._account['u1']['fund_product_code']
                                                )

    # 购买定期宝使用积分+优惠券(不可叠加)
    @keyword('test_buy_dqb_use_points_and_nonsuperposed_coupon')
    def buy_dqb_use_points_and_nonsuperposed_coupon(self):
        self.xjb.buy_dqb_use_points_and_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                             login_password=self._account['u1']['login_password'],
                                                             nonsuperposed_coupon_code=self._account['u1'][
                                                                 'nonsuperposed_coupon_code'],
                                                             nonsuperposed_coupon_quantity=self._account['u1'][
                                                                 'nonsuperposed_coupon_quantity'],
                                                             amount=self._account['u1']['dqb_product_amount'],
                                                             # amount=self._account['u1']['dqb_product_amount_for_superposed_coupon'],
                                                             trade_password=self._account['u1']['trade_password'],
                                                             product_name=self._account['u1']['dqb_product_for_coupon']
                                                             # product_name=self._account['u1']['dqb_product']
                                                             )

    # 购买定期宝使用积分+优惠券(可叠加)
    @keyword('test_buy_dqb_use_points_and_superposed_coupon')
    def buy_dqb_use_points_and_superposed_coupon(self):
        self.xjb.buy_dqb_use_points_and_superposed_coupon(user_name=self._account['u1']['user_name'],
                                                          login_password=self._account['u1']['login_password'],
                                                          superposed_coupon_code=self._account['u1'][
                                                              'superposed_coupon_code'],
                                                          superposed_coupon_quantity=self._account['u1'][
                                                              'superposed_coupon_quantity'],
                                                          amount=self._account['u1']['dqb_product_amount'],
                                                          trade_password=self._account['u1']['trade_password'],
                                                          # product_name=self._account['u1']['dqb_product']
                                                          product_name=self._account['u1']['dqb_product_for_coupon']
                                                          )

    # 购买高端使用积分+优惠券(不可叠加)
    @keyword('test_buy_vipproduct_use_points_and_nonsuperposed_coupon')
    def buy_vipproduct_use_points_and_nonsuperposed_coupon(self):
        self.xjb.buy_vipproduct_use_points_and_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                                    login_password=self._account['u1'][
                                                                        'login_password'],
                                                                    nonsuperposed_coupon_code=self._account['u1'][
                                                                        'nonsuperposed_coupon_code'],
                                                                    nonsuperposed_coupon_quantity=self._account['u1'][
                                                                        'nonsuperposed_coupon_quantity'],
                                                                    amount=self._account['u1'][
                                                                        'high_end_product_amount'],
                                                                    trade_password=self._account['u1'][
                                                                        'trade_password'],
                                                                    # product_name=self._account['u1']['high_end_product_for_points_offset']
                                                                    product_name=self._account['u1'][
                                                                        'high_end_product_for_points']
                                                                    )

    # 购买高端使用积分+优惠券(可叠加)
    @keyword('test_buy_vipproduct_use_points_and_superposed_coupon')
    def buy_vipproduct_use_points_and_superposed_coupon(self):
        self.xjb.buy_vipproduct_use_points_and_superposed_coupon(user_name=self._account['u1']['user_name'],
                                                                 login_password=self._account['u1']['login_password'],
                                                                 superposed_coupon_code=self._account['u1'][
                                                                     'superposed_coupon_code'],
                                                                 superposed_coupon_quantity=self._account['u1'][
                                                                     'superposed_coupon_quantity'],
                                                                 amount=self._account['u1']['high_end_product_amount'],
                                                                 trade_password=self._account['u1']['trade_password'],
                                                                 # product_name=self._account['u1']['high_end_product_for_points_offset']
                                                                 product_name=self._account['u1'][
                                                                     'high_end_product_for_points']
                                                                 )

    # 购买基金使用积分+优惠券(不可叠加)
    @keyword('test_buy_fund_use_points_and_nonsuperposed_coupon')
    def buy_fund_use_points_and_nonsuperposed_coupon(self):
        self.xjb.buy_fund_use_points_and_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                              login_password=self._account['u1']['login_password'],
                                                              nonsuperposed_coupon_code=self._account['u1'][
                                                                  'nonsuperposed_coupon_code'],
                                                              nonsuperposed_coupon_quantity=self._account['u1'][
                                                                  'nonsuperposed_coupon_quantity'],
                                                              fund_product_name=self._account['u1'][
                                                                  'fund_product_name'],
                                                              amount=self._account['u1']['fund_product_amount'],
                                                              trade_password=self._account['u1']['trade_password'],
                                                              fund_product_code=self._account['u1']['fund_product_code']
                                                              )

    # 购买基金使用积分+优惠券(可叠加)
    @keyword('test_buy_fund_use_points_and_superposed_coupon')
    def buy_fund_use_points_and_superposed_coupon(self):
        self.xjb.buy_fund_use_points_and_superposed_coupon(user_name=self._account['u1']['user_name'],
                                                           login_password=self._account['u1']['login_password'],
                                                           superposed_coupon_code=self._account['u1'][
                                                               'superposed_coupon_code'],
                                                           superposed_coupon_quantity=self._account['u1'][
                                                               'superposed_coupon_quantity'],
                                                           fund_product_name=self._account['u1']['fund_product_name'],
                                                           amount=self._account['u1']['fund_product_amount'],
                                                           trade_password=self._account['u1']['trade_password'],
                                                           fund_product_code=self._account['u1']['fund_product_code']
                                                           )

    # 我的优惠券列表-立即使用-购买页面
    @keyword('test_my_coupon_list_to_buy_page')
    def my_coupon_list_to_buy_page(self):
        self.xjb.use_coupon_from_my_coupon_list(user_name=self._account['u1']['user_name'],
                                                login_password=self._account['u1']['login_password'])

    # 在无预约码情况下使用其他人的预约码
    @keyword('test_use_other_reservation_code_without_reservation_code')
    def use_other_reservation_code_without_reservation_code(self):
        self.xjb.use_other_reservation_code_without_reservation_code(user_name=self._account['u2']['user_name'],
                                                                     login_password=self._account['u2'][
                                                                         'login_password'],
                                                                     trade_password=self._account['u2'][
                                                                         'trade_password'],
                                                                     buy_quota=self._account['u2'][
                                                                         'reservation_code_buy_quota'],
                                                                     buy_count=self._account['u2'][
                                                                         'reservation_code_buy_count'],
                                                                     reserve_quota=self._account['u2'][
                                                                         'reservation_code_reserve_quota'],
                                                                     reserve_count=self._account['u2'][
                                                                         'reservation_code_reserve_count'],
                                                                     reserve_code=self._account['u2']['reserve_code'],
                                                                     product_id=self._account['u2'][
                                                                         'product_id_for_reservation_code'],
                                                                     mobile=self._account['u1']['user_name'])

    # 我的历史优惠券列表
    @keyword('test_history_coupon_list')
    def history_coupon_list(self):
        self.xjb.history_coupon_list(user_name=self._account['u1']['user_name'],
                                     password=self._account['u1']['login_password'])

    # 优惠券说明
    @keyword('test_coupon_description')
    def coupon_description(self):
        self.xjb.coupon_description(user_name=self._account['u1']['user_name'],
                                    password=self._account['u1']['login_password'])

    # 员工理财--开启工资代发
    @keyword('test_salary_issuing')
    def salary_issuing(self):
        self.xjb.salary_issuing(user_name=self._account['u1']['user_name'],
                                login_password=self._account['u1']['login_password'])

    # 员工理财--终止工资代发
    @keyword('test_stop_salary_issuing')
    def stop_salary_issuing(self):
        self.xjb.stop_salary_issuing(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     trade_password=self._account['u1']['trade_password'],
                                     )

    # 工资理财——开启计划
    @keyword('test_start_financing_plan')
    def start_financing_plan(self):
        self.xjb.start_financing_plan(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      last_no=self._account['u1']['pay_card_last_no'],
                                      amount=self._account['u1']['financing_amount'],
                                      trade_password=self._account['u1']['trade_password'],
                                      )

    # 工资理财——新增计划
    @keyword('test_add_financing_plan')
    def add_financing_plan(self):
        self.xjb.add_financing_plan(user_name=self._account['u1']['user_name'],
                                    login_password=self._account['u1']['login_password'],
                                    last_no=self._account['u1']['pay_card_last_no'],
                                    amount=self._account['u1']['financing_amount'],
                                    trade_password=self._account['u1']['trade_password'],
                                    )

    # 工资理财——暂停计划
    @keyword('test_pause_financing_plan')
    def pause_financing_plan(self):
        self.xjb.pause_financing_plan(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      trade_password=self._account['u1']['trade_password'],
                                      )

    # 工资理财——启用计划
    @keyword('test_restart_financing_plan')
    def restart_financing_plan(self):
        self.xjb.restart_financing_plan(user_name=self._account['u1']['user_name'],
                                        login_password=self._account['u1']['login_password'],
                                        trade_password=self._account['u1']['trade_password'],
                                        )

    # 工资理财--修改理财计划
    @keyword('test_modify_financing_plan')
    def modify_financing_plan(self):
        self.xjb.modify_financing_plan(user_name=self._account['u1']['user_name'],
                                       login_password=self._account['u1']['login_password'],
                                       last_no=self._account['u1']['pay_card_last_no_for_modification'],
                                       amount=self._account['u1']['financing_amount'],
                                       trade_password=self._account['u1']['trade_password'],
                                       )

    # 工资理财——终止理财计划
    @keyword('test_stop_financing_plan')
    def stop_financing_plan(self):
        self.xjb.stop_financing_plan(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     trade_password=self._account['u1']['trade_password'])

    # 还房贷
    @keyword('test_make_repay_housing_loan_plan')
    def make_repay_housing_loan_plan(self):
        self.xjb.make_repay_housing_loan_plan(user_name=self._account['u1']['user_name'],
                                              login_password=self._account['u1']['login_password'],
                                              last_no=self._account['u1']['pay_card_last_no'],
                                              repay_amount=self._account['u1']['repay_loan_amount'],
                                              trade_password=self._account['u1']['trade_password'])

    # 还车贷
    @keyword('test_make_repay_car_loan_plan')
    def make_repay_car_loan_plan(self):
        self.xjb.make_repay_car_loan_plan(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          last_no=self._account['u1']['pay_card_last_no'],
                                          repay_amount=self._account['u1']['repay_loan_amount'],
                                          trade_password=self._account['u1']['trade_password'])

    # 还其他贷款
    @keyword('test_make_repay_other_loan_plan')
    def make_repay_other_loan_plan(self):
        self.xjb.make_repay_other_loan_plan(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            last_no=self._account['u1']['pay_card_last_no'],
                                            repay_amount=self._account['u1']['repay_loan_amount'],
                                            trade_password=self._account['u1']['trade_password'])

    # 暂停还贷款计划
    @keyword('test_pause_repay_loan_plan')
    def pause_repay_loan_plan(self):
        self.xjb.pause_repay_loan_plan(user_name=self._account['u1']['user_name'],
                                       login_password=self._account['u1']['login_password'],
                                       trade_password=self._account['u1']['trade_password'])

    # 启用还贷款计划
    @keyword('test_restart_repay_loan_plan')
    def restart_repay_loan_plan(self):
        self.xjb.restart_repay_loan_plan(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         trade_password=self._account['u1']['trade_password'])

    # 修改还房贷为还车贷
    @keyword('test_modify_repay_housing_loan_to_repay_car_loan')
    def modify_repay_housing_loan_to_repay_car_loan(self):
        self.xjb.modify_repay_housing_loan_to_repay_car_loan(user_name=self._account['u1']['user_name'],
                                                             login_password=self._account['u1']['login_password'],
                                                             last_no=self._account['u1'][
                                                                 'pay_card_last_no_for_modification'],
                                                             repay_amount=self._account['u1']['repay_loan_amount'],
                                                             trade_password=self._account['u1']['trade_password'])

    # 修改还车贷为还其他贷款
    @keyword('test_modify_repay_car_loan_to_repay_other_loan')
    def modify_repay_car_loan_to_repay_other_loan(self):
        self.xjb.modify_repay_car_loan_to_repay_other_loan(user_name=self._account['u1']['user_name'],
                                                           login_password=self._account['u1']['login_password'],
                                                           last_no=self._account['u1']['pay_card_last_no'],
                                                           repay_amount=self._account['u1']['repay_loan_amount'],
                                                           trade_password=self._account['u1']['trade_password'])

    # 修改还其他贷款为还房贷
    @keyword('test_modify_repay_other_loan_to_repay_housing_loan')
    def modify_repay_other_loan_to_repay_housing_loan(self):
        self.xjb.modify_repay_other_loan_to_repay_housing_loan(user_name=self._account['u1']['user_name'],
                                                               login_password=self._account['u1']['login_password'],
                                                               last_no=self._account['u1'][
                                                                   'pay_card_last_no_for_modification'],
                                                               repay_amount=self._account['u1']['repay_loan_amount'],
                                                               trade_password=self._account['u1']['trade_password'])

    # 删除还贷款计划
    @keyword('test_delete_repay_loan_plan')
    def delete_repay_loan_plan(self):
        self.xjb.delete_repay_loan_plan(user_name=self._account['u1']['user_name'],
                                        login_password=self._account['u1']['login_password'],
                                        trade_password=self._account['u1']['trade_password'])

    # 现金支付手段买高端(金额正常)
    @keyword('test_buy_vipproduct_use_cash_management_product')
    def buy_vipproduct_use_cash_management_product(self):
        self.xjb.buy_vipproduct_use_cash_management_product(user_name=self._account['u1']['user_name'],
                                                            login_password=self._account['u1']['login_password'],
                                                            product_name=self._account['u1'][
                                                                'high_end_product_for_points'],
                                                            trade_password=self._account['u1']['trade_password'],
                                                            amount=self._account['u1']['high_end_product_amount'],
                                                            cash_management_product=self._account['u1'][
                                                                'cash_management_product']
                                                            )

    # 现金支付手段买高端(金额超过持有金额)
    @keyword('test_buy_vipproduct_use_cash_management_product_for_excess')
    def buy_vipproduct_use_cash_management_product_for_excess(self):
        self.xjb.buy_vipproduct_use_cash_management_product(user_name=self._account['u1']['user_name'],
                                                            login_password=self._account['u1']['login_password'],
                                                            product_name=self._account['u1'][
                                                                'high_end_product_for_points'],
                                                            trade_password=self._account['u1']['trade_password'],
                                                            amount=self._account['u1']['high_end_product_amount'],
                                                            cash_management_product=self._account['u1'][
                                                                'cash_management_product_for_excess']
                                                            )

    # 登陆绑卡
    @keyword('test_certificated_user_binding_card')
    def certificated_user_binding_card(self):
        self.xjb.certificated_user_binding_card(
            user_name=self._account['u1']['user_name_for_add_credit_card_without_binding_bank_card'],
            login_password=self._account['u1']['login_password'],
            bank_card_no=self._account['u1']['bank_card_no_for_certificated_user_binding_card']
            # Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]
        )

    # 随心借
    @keyword('test_vipproduct_pledge')
    def vipproduct_pledge(self):
        self.xjb.vipproduct_pledge(user_name=self._account['u1']['user_name'],
                                   login_password=self._account['u1']['login_password'],
                                   product_name=self._account['u1']['high_end_product'],
                                   pledge_amount=self._account['u1']['pledge_amount'],
                                   trade_password=self._account['u1']['trade_password'],
                                   )

    # 随心还
    @keyword('test_vipproduct_pledge_repay')
    def vipproduct_pledge_repay(self):
        self.xjb.vipproduct_pledge_repay(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         product_name=self._account['u1']['high_end_product'],
                                         pledge_repay_amount=self._account['u1']['pledge_amount'],
                                         trade_password=self._account['u1']['trade_password'],
                                         )

    # 基金定投
    @keyword('test_fund_plan')
    def fund_plan(self):
        self.xjb.fund_plan(user_name=self._account['u1']['user_name'],
                           login_password=self._account['u1']['login_password'],
                           fund_product_name=self._account['u1']['fund_product_name'],
                           amount=self._account['u1']['fund_product_amount'],
                           trade_password=self._account['u1']['trade_password'],
                           fund_product_code=self._account['u1']['fund_product_code']
                           )

    # 查看历史定投(用户无历史定投)
    @keyword('test_check_empty_fund_history_plan')
    def check_empty_fund_history_plan(self):
        self.xjb.check_empty_fund_history_plan(user_name=self._account['u2']['user_name'],
                                               login_password=self._account['u2']['login_password']
                                               )

    # 删除历史定投
    @keyword('test_delete_fund_history_plan')
    def delete_fund_history_plan(self):
        self.xjb.delete_fund_history_plan(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          fund_product_name=self._account['u1']['fund_product_name']
                                          )

    # 暂停定投
    @keyword('test_pause_fund_plan')
    def pause_fund_plan(self):
        self.xjb.pause_fund_plan(user_name=self._account['u1']['user_name'],
                                 login_password=self._account['u1']['login_password'],
                                 trade_password=self._account['u1']['trade_password'],
                                 fund_product_name=self._account['u1']['fund_product_name'])

    # 恢复定投
    @keyword('test_restart_fund_plan')
    def restart_fund_plan(self):
        self.xjb.restart_fund_plan(user_name=self._account['u1']['user_name'],
                                   login_password=self._account['u1']['login_password'],
                                   trade_password=self._account['u1']['trade_password'],
                                   fund_product_name=self._account['u1']['fund_product_name'])

    # 终止定投
    @keyword('test_stop_fund_plan')
    def stop_fund_plan(self):
        self.xjb.stop_fund_plan(user_name=self._account['u1']['user_name'],
                                login_password=self._account['u1']['login_password'],
                                trade_password=self._account['u1']['trade_password'],
                                fund_product_name=self._account['u1']['fund_product_name'])

    # 修改基金定投计划
    @keyword('test_modify_fund_plan')
    def modify_fund_plan(self):
        self.xjb.modify_fund_plan(user_name=self._account['u1']['user_name'],
                                  login_password=self._account['u1']['login_password'],
                                  trade_password=self._account['u1']['trade_password'],
                                  fund_product_name=self._account['u1']['fund_product_name'],
                                  amount='1.00')

    # 新增定投计划
    @keyword('test_add_fund_plan')
    def add_fund_plan(self):
        self.xjb.add_fund_plan(user_name=self._account['u1']['user_name'],
                               login_password=self._account['u1']['login_password'],
                               trade_password=self._account['u1']['trade_password'],
                               fund_product_name=self._account['u1']['fund_product_name'],
                               fund_product_code=self._account['u1']['fund_product_code'],
                               amount=self._account['u1']['fund_product_amount'])

    # 查看现金宝万分收益
    @keyword('test_view_xjb_income_per_wan')
    def view_xjb_income_per_wan(self):
        self.xjb.view_xjb_income_per_wan(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         )

    # 查看现金宝累计收益
    @keyword('test_view_xjb_income_accumulated')
    def view_xjb_income_accumulated(self):
        self.xjb.view_xjb_income_accumulated(user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password'],
                                             )

    # 查看历史七日年化收益率
    @keyword('test_view_xjb_seven_days_annual_rate_of_return')
    def view_xjb_seven_days_annual_rate_of_return(self):
        self.xjb.view_xjb_seven_days_annual_rate_of_return(user_name=self._account['u1']['user_name'],
                                                           login_password=self._account['u1']['login_password'],
                                                           )

    # 查看现金管理系列
    @keyword('test_view_high_end_cash_management_series')
    def view_high_end_cash_management_series(self):
        self.xjb.view_high_end_cash_management_series(user_name=self._account['u1']['user_name'],
                                                      login_password=self._account['u1']['login_password'],
                                                      )

    #  查看固定收益系列
    @keyword('test_view_high_end_fixed_rate_series')
    def view_high_end_fixed_rate_series(self):
        self.xjb.view_high_end_fixed_rate_series(user_name=self._account['u1']['user_name'],
                                                 login_password=self._account['u1']['login_password'],
                                                 )

    #  查看精选系列
    @keyword('test_view_high_end_best_recommend_series')
    def view_high_end_best_recommend_series(self):
        self.xjb.view_high_end_best_recommend_series(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'],
                                                     )

    #  基金频道--评级排行
    @keyword('test_fund_rating_and_ranking')
    def fund_rating_and_ranking(self):
        self.xjb.fund_rating_and_ranking(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         )

    #  查看资产证明
    @keyword('test_view_assets_analysis')
    def view_assets_analysis(self):
        self.xjb.view_assets_analysis(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      )

    #  下载资产证明
    @keyword('test_download_assets_certification')
    def download_assets_certification(self):
        self.xjb.download_assets_certification(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'],
                                               trade_password=self._account['u1']['trade_password'])

    #  查看资产证明
    @keyword('test_view_assets_analysis')
    def view_assets_analysis(self):
        self.xjb.view_assets_analysis(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      )

    #  持有页面查看产品详情
    @keyword('test_view_product_details')
    def view_product_details(self):
        self.xjb.view_product_details(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      high_end_product=self._account['u1']['high_end_product']
                                      )

    #  基金撤单
    @keyword('test_cancel_fund_order')
    def cancel_fund_order(self):
        self.xjb.cancel_fund_order(user_name=self._account['u1']['user_name'],
                                   login_password=self._account['u1']['login_password'],
                                   trade_password=self._account['u1']['trade_password'],
                                   product_name=self._account['u1']['fund_product_name']
                                   )

    #  高端撤单
    @keyword('test_cancel_vipproduct_order')
    def cancel_vipproduct_order(self):
        self.xjb.cancel_vipproduct_order(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         trade_password=self._account['u1']['trade_password'],
                                         product_name=self._account['u1']['high_end_product'],
                                         # amount=self._account['u1']['high_end_product_amount']
                                         )

    #  用户绑定银行卡张数为0时绑定信用卡
    @keyword('test_add_credit_card_without_binding_bank_card')
    def add_credit_card_without_binding_bank_card(self):
        bank_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]
        self.xjb.add_credit_card_without_binding_bank_card(
            user_name=self._account['u1']['user_name_for_add_credit_card_without_binding_bank_card'],
            login_password=self._account['u1']['login_password'],
            bank_card_no=bank_card_no
        )

    #  热门页查看全部产品
    @keyword('test_view_all_products')
    def view_all_products(self):
        self.xjb.view_all_products(user_name=self._account['u1']['user_name'],
                                   login_password=self._account['u1']['login_password'])

    #  理财频道全部产品--筛选器
    @keyword('test_all_products_filter')
    def all_products_filter(self):
        self.xjb.all_products_filter(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'])

    #  删除自选(从自选基金管理页面删除)
    @keyword('test_fund_selected_funds_deleted')
    def fund_selected_funds_deleted(self):
        self.xjb.fund_selected_funds_deleted(user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password'],
                                             fund_product_name=self._account['u1']['fund_product_name'],
                                             fund_product_code=self._account['u1']['fund_product_code']
                                             )

    #  基金筛选器
    @keyword('test_fund_filter')
    def fund_filter(self):
        self.xjb.fund_filter(user_name=self._account['u1']['user_name'],
                             login_password=self._account['u1']['login_password'])

    #  稳健型用户购买高风险产品(提示加验证码)
    @keyword('test_moderate_user_buy_high_risk_product')
    def moderate_user_buy_high_risk_product(self):
        self.xjb.moderate_user_buy_high_risk_product(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'],
                                                     fund_product_name=self._account['u1'][
                                                         'fund_product_name_for_fast_redeem'],
                                                     amount=self._account['u1']['fund_product_amount'],
                                                     trade_password=self._account['u1']['trade_password'],
                                                     fund_product_code='050035')

    #  激进型用户购买高风险产品(需输入验证码)
    @keyword('test_radical_user_buy_high_risk_product')
    def radical_user_buy_high_risk_product(self):
        self.xjb.radical_user_buy_high_risk_product(user_name=self._account['u1']['radical_user'],
                                                    login_password=self._account['u1']['login_password'],
                                                    fund_product_name=self._account['u1'][
                                                        'fund_product_name_for_fast_redeem'],
                                                    amount=self._account['u1']['fund_product_amount'],
                                                    trade_password=self._account['u1']['trade_password'],
                                                    fund_product_code='050035')

    #  保守型用户购买高风险产品(风险提示且用户不能购买)
    @keyword('test_conservative_user_buy_high_risk_product')
    def conservative_user_buy_high_risk_product(self):
        self.xjb.conservative_user_buy_high_risk_product(user_name=self._account['u1']['conservative_user'],
                                                         login_password=self._account['u1']['login_password'],
                                                         fund_product_name=self._account['u1'][
                                                             'fund_product_name_for_fast_redeem'],
                                                         # amount=self._account['u1']['fund_product_amount'],
                                                         fund_product_code='050035')

    #  谨慎型用户购买中高风险产品(有提示,可以购买)
    @keyword('test_cautious_user_buy_middle_high_risk_product')
    def cautious_user_buy_middle_high_risk_product(self):
        self.xjb.cautious_user_buy_middle_high_risk_product(user_name=self._account['u1']['cautious_user'],
                                                            login_password=self._account['u1']['login_password'],
                                                            fund_product_name=self._account['u1'][
                                                                'fund_product_name_2'],
                                                            amount=self._account['u1']['fund_product_amount'],
                                                            trade_password=self._account['u1']['trade_password'],
                                                            fund_product_code='A09201')

    #  现金宝持有页面查看在途资产
    @keyword('test_view_xjb_asset_in_transit')
    def view_xjb_asset_in_transit(self):
        self.xjb.view_xjb_asset_in_transit(user_name=self._account['u1']['user_name'],
                                           login_password=self._account['u1']['login_password'])

    #  现金宝持有页面查看产品详情
    @keyword('test_view_xjb_product_detail')
    def view_xjb_product_detail(self):
        self.xjb.view_xjb_product_detail(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'])

    #  现金宝持有页面查看七日年化收益率曲线
    @keyword('test_view_xjb_seven_days_annual_rate_of_return_curve')
    def view_xjb_seven_days_annual_rate_of_return_curve(self):
        self.xjb.view_xjb_seven_days_annual_rate_of_return_curve(user_name=self._account['u1']['user_name'],
                                                                 login_password=self._account['u1']['login_password'])

    # 查看基金资产(资产分析页面进)
    @keyword('test_view_fund_asset')
    def view_fund_asset(self):
        self.xjb.view_fund_asset(user_name=self._account['u1']['user_name'],
                                 login_password=self._account['u1']['login_password'])

    # 我的优惠券列表为空
    @keyword('test_my_coupon_empty_list')
    def my_coupon_empty_list(self):
        self.xjb.my_coupon_empty_list(user_name=self._account['u1']['radical_user'],
                                      login_password=self._account['u1']['login_password'])

    # 基金频道--删除自选基金（从自选基金详情页面删除）
    @keyword('test_fund_selected_funds_deleted_at_fund_detail_page')
    def fund_selected_funds_deleted_at_fund_detail_page(self):
        self.xjb.fund_selected_funds_deleted_at_fund_detail_page(user_name=self._account['u1']['user_name'],
                                                                 login_password=self._account['u1']['login_password'],
                                                                 fund_product_name=self._account['u1'][
                                                                     'fund_product_name'],
                                                                 fund_product_code=self._account['u1'][
                                                                     'fund_product_code'])

    # 高端追加购买页面跳转(资产分析页面进)
    @keyword('test_vipproduct_supplementary_purchase')
    def vipproduct_supplementary_purchase(self):
        self.xjb.vipproduct_supplementary_purchase(user_name=self._account['u1']['user_name'],
                                                   login_password=self._account['u1']['login_password'],
                                                   high_end_product=self._account['u1'][
                                                       'high_end_product_for_fast_redeem'])

    # 定期追加购买(资产分析页面进)
    @keyword('test_dhb_supplementary_purchase')
    def dhb_supplementary_purchase(self):
        self.xjb.dhb_supplementary_purchase(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            product_name=self._account['u1']['dqb_product'])

    # 未测评用户购买产品(提示先进行风险评测)
    @keyword('test_buy_fund_product_without_risk_evaluation')
    def buy_fund_product_without_risk_evaluation(self):
        self.xjb.buy_fund_product_without_risk_evaluation(user_name=self._account['u1']['unevaluated_user'],
                                                          login_password=self._account['u1']['login_password'],
                                                          fund_product_name=self._account['u1']['fund_product_name'],
                                                          fund_product_code=self._account['u1']['fund_product_code']
                                                          )

    # 短信验证码登录
    @keyword('test_login_use_verification_code')
    def login_use_verification_code(self):
        self.xjb.login_use_verification_code(user_name=self._account['u1']['user_name'])

    # 使用优惠券充值现金宝
    @keyword('test_recharge_use_coupon')
    def recharge_use_coupon(self):
        self.xjb.recharge_use_coupon(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     recharge_amount='3.00',
                                     trade_password=self._account['u1']['trade_password'],
                                     nonsuperposed_coupon_code=self._account['u1'][
                                         'nonsuperposed_coupon_code'],
                                     nonsuperposed_coupon_quantity=self._account['u1'][
                                         'nonsuperposed_coupon_quantity']
                                     )

    # 现金支付手段买基金(金额正常)
    @keyword('test_buy_fund_product_use_cash_management_product')
    def buy_fund_product_use_cash_management_product(self):
        self.xjb.buy_fund_product_use_cash_management_product(user_name=self._account['u1']['user_name'],
                                                              login_password=self._account['u1']['login_password'],
                                                              fund_product_name=self._account['u1'][
                                                                  'fund_product_name'],
                                                              amount=self._account['u1']['fund_product_amount'],
                                                              trade_password=self._account['u1']['trade_password'],
                                                              fund_product_code=self._account['u1'][
                                                                  'fund_product_code'],
                                                              cash_management_product=self._account['u1'][
                                                                  'cash_management_product']
                                                              )

    # 现金支付手段买定活宝
    @keyword('test_buy_dhb_product_use_cash_management_product')
    def buy_dhb_product_use_cash_management_product(self):
        self.xjb.buy_dhb_product_use_cash_management_product(user_name=self._account['u1']['user_name'],
                                                             login_password=self._account['u1']['login_password'],
                                                             product_name=self._account['u1']['dqb_product'],
                                                             amount=self._account['u1']['dqb_product_amount'],
                                                             trade_password=self._account['u1']['trade_password'],
                                                             cash_management_product=self._account['u1'][
                                                                 'cash_management_product']
                                                             )

    # 信用卡还款使用优惠券
    @keyword('test_credit_card_repay_use_coupon')
    def credit_card_repay_use_coupon(self):
        self.xjb.credit_card_repay_use_coupon(user_name=self._account['u1']['user_name'],
                                              login_password=self._account['u1']['login_password'],
                                              repay_amount=self._account['u1'][
                                                  'credit_card_repay_amount'],
                                              trade_password=self._account['u1']['trade_password'],
                                              last_card_no=self._account['u1'][
                                                  'last_card_no_for_repay'],
                                              superposed_coupon_code=self._account['u1'][
                                                  'credit_card_repay_coupon_code'],
                                              superposed_coupon_quantity=self._account['u1'][
                                                  'superposed_coupon_quantity']
                                              )

    # 查看现金宝资产的说明
    @keyword('test_view_xjb_holding_assets_description')
    def view_xjb_holding_assets_description(self):
        self.xjb.view_xjb_holding_assets_description(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password']
                                                     )

    # 查看定活宝资产的说明
    @keyword('test_view_dhb_holding_assets_description')
    def view_dhb_holding_assets_description(self):
        self.xjb.view_dhb_holding_assets_description(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password']
                                                     )

    # 查看基金资产的说明
    @keyword('test_view_fund_holding_assets_description')
    def view_fund_holding_assets_description(self):
        self.xjb.view_fund_holding_assets_description(user_name=self._account['u1']['user_name'],
                                                      login_password=self._account['u1']['login_password']
                                                      )

    # 查看高端资产的说明
    @keyword('test_view_vipproduct_holding_assets_description')
    def view_vipproduct_holding_assets_description(self):
        self.xjb.view_vipproduct_holding_assets_description(user_name=self._account['u1']['user_name'],
                                                            login_password=self._account['u1']['login_password']
                                                            )

    # 定投排行
    @keyword('test_view_fund_plan_rankings')
    def view_fund_plan_rankings(self):
        self.xjb.view_fund_plan_rankings(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password']
                                         )

    # 使用优惠券信用卡预约还款
    @keyword('test_credit_card_reserved_pay_use_nonsuperposed_coupon')
    def credit_card_reserved_pay_use_nonsuperposed_coupon(self):
        self.xjb.credit_card_reserved_pay_use_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                                   login_password=self._account['u1']['login_password'],
                                                                   reserved_pay_amount='3.00',
                                                                   trade_password=self._account['u1']['trade_password'],
                                                                   nonsuperposed_coupon_code=self._account['u1'][
                                                                       'credit_card_reserved_repay_coupon_code'],
                                                                   nonsuperposed_coupon_quantity=self._account['u1'][
                                                                       'nonsuperposed_coupon_quantity'],
                                                                   last_card_no=self._account['u1'][
                                                                       'last_card_no_for_repay']

                                                                   )

    # 会员中心
    @keyword('test_associator_level')
    def associator_level(self):
        self.xjb.associator_level(user_name=self._account['u1']['user_name'],
                                  login_password=self._account['u1']['login_password']
                                  )

    # 理财日历月份切换
    @keyword('test_swipe_financing_calender')
    def swipe_financing_calender(self):
        self.xjb.swipe_financing_calender(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password']
                                          )

    # 定活宝收益计算器(金额正常)
    @keyword('test_dhb_income_calculator_normal')
    def dhb_income_calculator_normal(self):
        self.xjb.dhb_income_calculator(user_name=self._account['u1']['user_name'],
                                       login_password=self._account['u1']['login_password'],
                                       product_name=self._account['u1']['dqb_product'],
                                       amount=self._account['u1']['dqb_product_amount']
                                       )

    # 定活宝收益计算器(金额小于起投金额)
    @keyword('test_dhb_income_calculator_min')
    def dhb_income_calculator_min(self):
        self.xjb.dhb_income_calculator(user_name=self._account['u1']['user_name'],
                                       login_password=self._account['u1']['login_password'],
                                       product_name=self._account['u1']['dqb_product'],
                                       amount=self._account['u1']['amount_min']
                                       )

    # 定活宝收益计算器(金额大于最大金额)
    @keyword('test_dhb_income_calculator_max')
    def dhb_income_calculator_max(self):
        self.xjb.dhb_income_calculator(user_name=self._account['u1']['user_name'],
                                       login_password=self._account['u1']['login_password'],
                                       product_name=self._account['u1']['dqb_product'],
                                       amount=self._account['u1']['amount_max']
                                       )

    # 高端收益计算器(金额正常)
    @keyword('test_high_end_income_calculator_normal')
    def high_end_income_calculator_normal(self):
        self.xjb.high_end_income_calculator(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            product_name=self._account['u1']['high_end_product_for_fast_redeem'],
                                            amount=self._account['u1']['high_end_product_amount']
                                            )

    # 高端收益计算器(金额小于起投金额)
    @keyword('test_high_end_income_calculator_min')
    def high_end_income_calculator_min(self):
        self.xjb.high_end_income_calculator(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            product_name=self._account['u1']['high_end_product_for_fast_redeem'],
                                            amount=self._account['u1']['amount_min']
                                            )

    # 高端收益计算器(金额大于最大金额)
    @keyword('test_high_end_income_calculator_max')
    def high_end_income_calculator_max(self):
        self.xjb.high_end_income_calculator(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            product_name=self._account['u1']['high_end_product_for_fast_redeem'],
                                            amount=self._account['u1']['amount_max']
                                            )

    # 查看非货币型基金业绩
    @keyword('test_view_non_monetary_fund_performance')
    def view_non_monetary_fund_performance(self):
        self.xjb.view_non_monetary_fund_performance(user_name=self._account['u1']['user_name'],
                                                    login_password=self._account['u1']['login_password'],
                                                    fund_product_name=self._account['u1']['fund_product_name'],
                                                    )

    # 查看非货币型基金公告
    @keyword('test_view_non_monetary_fund_notice')
    def view_non_monetary_fund_notice(self):
        self.xjb.view_non_monetary_fund_notice(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'],
                                               fund_product_name=self._account['u1']['fund_product_name'],
                                               )

    # 查看货币型基金业绩
    @keyword('test_view_monetary_fund_performance')
    def view_monetary_fund_performance(self):
        self.xjb.view_monetary_fund_performance(user_name=self._account['u1']['user_name'],
                                                login_password=self._account['u1']['login_password'],
                                                fund_product_name='中海货币B',
                                                )

    # 查看货币型基金公告
    @keyword('test_view_monetary_fund_notice')
    def view_monetary_fund_notice(self):
        self.xjb.view_monetary_fund_notice(user_name=self._account['u1']['user_name'],
                                           login_password=self._account['u1']['login_password'],
                                           fund_product_name='中海货币B',
                                           )

    # 未登录状态验证
    @keyword('test_check_not_login_status_details')
    def check_not_login_status_details(self):
        self.xjb.check_not_login_status_details()

    # 查看高端精选系列产品历史净值
    @keyword('test_view_high_end_best_recommend_history_nav')
    def view_high_end_best_recommend_history_nav(self):
        self.xjb.view_high_end_best_recommend_history_nav(user_name=self._account['u1']['user_name'],
                                                          login_password=self._account['u1']['login_password'],
                                                          product_name=u'华信证券现金管理1号集合资产管理计划')

    # 查看高端精选系列产品基础信息
    @keyword('test_view_high_end_best_recommend_basic_information')
    def view_high_end_best_recommend_basic_information(self):
        self.xjb.view_high_end_best_recommend_basic_information(user_name=self._account['u1']['user_name'],
                                                                login_password=self._account['u1']['login_password'],
                                                                product_name=u'华信证券现金管理1号集合资产管理计划')

    # 查看高端精选系列产品业绩等其他详情信息
    @keyword('test_view_high_end_best_recommend_performance')
    def view_high_end_best_recommend_performance(self):
        self.xjb.view_high_end_best_recommend_performance(user_name=self._account['u1']['user_name'],
                                                          login_password=self._account['u1']['login_password'],
                                                          product_name=u'华信证券现金管理1号集合资产管理计划')

    # 查看高端现金管理系列产品基础信息
    @keyword('test_view_high_end_cash_management_basic_information')
    def view_high_end_cash_management_basic_information(self):
        self.xjb.view_high_end_cash_management_basic_information(user_name=self._account['u1']['user_name'],
                                                                 login_password=self._account['u1']['login_password'],
                                                                 product_name=self._account['u1'][
                                                                     'cash_management_product'])

    # 查看高端现金管理系列产品历史收益
    @keyword('test_view_high_end_cash_management_history_income')
    def view_high_end_cash_management_history_income(self):
        self.xjb.view_high_end_cash_management_history_income(user_name=self._account['u1']['user_name'],
                                                              login_password=self._account['u1']['login_password'],
                                                              product_name=self._account['u1'][
                                                                  'cash_management_product'])

    # 查看固定收益系列产品详情
    @keyword('test_view_high_end_fixed_rate_product_details')
    def view_high_end_fixed_rate_product_details(self):
        self.xjb.view_high_end_fixed_rate_product_details(user_name=self._account['u1']['user_name'],
                                                          login_password=self._account['u1']['login_password'],
                                                          product_name=u'CI高端质押产品')

    # 删除历史定投
    @keyword('test_delete_fund_history_plan')
    def delete_fund_history_plan(self):
        self.xjb.delete_fund_history_plan(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          fund_product_name=self._account['u1']['fund_product_name'])

    # 查看基金历史持仓
    @keyword('test_view_fund_history_holding')
    def view_fund_history_holding(self):
        self.xjb.view_fund_history_holding(user_name=self._account['u1']['user_name'],
                                           login_password=self._account['u1']['login_password'],
                                           fund_product_name=self._account['u1']['fund_product_name'])

    # 查看定活宝历史持仓
    @keyword('test_view_dhb_history_holding')
    def view_dhb_history_holding(self):
        self.xjb.view_dhb_history_holding(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          product_name=self._account['u1']['dqb_product_2'],
                                          name=self._account['u1']['name'],
                                          risk_type=self._account['u1']['risk_type'])

    # 查看高端历史持仓
    @keyword('test_view_high_end_history_holding')
    def view_high_end_history_holding(self):
        self.xjb.view_high_end_history_holding(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'],
                                               product_name=self._account['u1']['high_end_product'])

    # 基金分红方式切换
    @keyword('test_fund_dividend_type_switch')
    def fund_dividend_type_switch(self):
        self.xjb.fund_dividend_type_switch(user_name=self._account['u1']['user_name'],
                                           login_password=self._account['u1']['login_password'],
                                           fund_product_name=self._account['u1']['fund_product_name'])

    # 基金极速转换
    @keyword('test_fund_fast_convert')
    def fund_fast_convert(self):
        self.xjb.fund_fast_convert(user_name=self._account['u1']['user_name'],
                                   login_password=self._account['u1']['login_password'],
                                   fund_convert_from=self._account['u1']['fund_fast_convert_from'],
                                   fund_convert_to=self._account['u1']['fund_fast_convert_to'],
                                   amount='2.00',
                                   trade_password=self._account['u1']['trade_password'],
                                   )

    # 基金极速转换撤单
    @keyword('test_cancel_fund_fast_convert_order')
    def cancel_fund_fast_convert_order(self):
        self.xjb.cancel_fund_fast_convert_order(user_name=self._account['u1']['user_name'],
                                                login_password=self._account['u1']['login_password'],
                                                fund_convert_from=self._account['u1']['fund_fast_convert_from'],
                                                fund_convert_to=self._account['u1']['fund_fast_convert_to'],
                                                trade_password=self._account['u1']['trade_password'])

    # 理财型基金到期处理方式切换(全部赎回至现金宝切换为部分赎回至现金宝)
    @keyword('test_financial_fund_expiry_processing_all_to_part')
    def financial_fund_expiry_processing_all_to_part(self):
        self.xjb.financial_fund_expiry_processing_all_to_part(user_name=self._account['u1']['user_name'],
                                                              login_password=self._account['u1']['login_password'],
                                                              fund_product_name=self._account['u1'][
                                                                  'financial_fund_product_name'],
                                                              fund_product_code=self._account['u1'][
                                                                  'financial_fund_product_code'],
                                                              trade_password=self._account['u1']['trade_password'])

    # 理财型基金到期处理方式切换(部分赎回至现金宝切换为自动续存)
    @keyword('test_financial_fund_expiry_processing_part_to_automatic')
    def financial_fund_expiry_processing_part_to_automatic(self):
        self.xjb.financial_fund_expiry_processing_part_to_automatic(user_name=self._account['u1']['user_name'],
                                                                    login_password=self._account['u1'][
                                                                        'login_password'],
                                                                    fund_product_name=self._account['u1'][
                                                                        'financial_fund_product_name'],
                                                                    fund_product_code=self._account['u1'][
                                                                        'financial_fund_product_code'],
                                                                    trade_password=self._account['u1'][
                                                                        'trade_password'])

    # 理财型基金到期处理方式切换(自动续存转全部赎回至现金宝)
    @keyword('test_financial_fund_expiry_processing_automatic_to_all')
    def financial_fund_expiry_processing_automatic_to_all(self):
        self.xjb.financial_fund_expiry_processing_automatic_to_all(user_name=self._account['u1']['user_name'],
                                                                   login_password=self._account['u1'][
                                                                       'login_password'],
                                                                   fund_product_name=self._account['u1'][
                                                                       'financial_fund_product_name'],
                                                                   fund_product_code=self._account['u1'][
                                                                       'financial_fund_product_code'],
                                                                   trade_password=self._account['u1'][
                                                                       'trade_password'])

    # 设置-修改个人信息
    @keyword('test_modify_personal_information')
    def modify_personal_information(self):
        phone_number = Utility.GetData().mobile()
        user_new, login_password = RestfulXjbTools().register(mobile=phone_number,
                                                              login_password='a0000000')
        self.xjb.modify_personal_information(user_name=user_new,
                                             login_password=login_password,
                                             email=self._account['u1']['mail'],
                                             address=self._account['u1']['address'])

    # 用户使用通行证实名/修改用户信息
    @keyword('test_bank_card_manage_binding_card_use_laissez_passer')
    def bank_card_manage_binding_card_use_laissez_passer(self):
        phone_number = Utility.GetData().mobile()
        user_new, login_password = RestfulXjbTools().register(mobile=phone_number,
                                                              login_password='a0000000')
        user_name = Utility.GetData().english_name()
        modified_user_name = Utility.GetData().english_name()

        id_no = Utility.GetData().id_no()
        modified_id_no = Utility.GetData().id_no()
        self.xjb.bank_card_manage_binding_card_use_laissez_passer(user_name=user_new,
                                                                  login_password=login_password,
                                                                  banding_card_user_name=user_name,
                                                                  modified_name=modified_user_name,
                                                                  modified_id_no=modified_id_no,
                                                                  trade_password='142536',
                                                                  laissez_passer_no=id_no,
                                                                  )

    # 基金普通转换
    @keyword('test_fund_normal_convert')
    def fund_normal_convert(self):
        self.xjb.fund_normal_convert(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     fund_convert_from=self._account['u1']['fund_normal_convert_from'],
                                     fund_convert_to=self._account['u1']['fund_normal_convert_to'],
                                     amount='2.00',
                                     trade_password=self._account['u1']['trade_password'],
                                     )

    # 基金普通转换撤单
    @keyword('test_cancel_fund_normal_convert_order')
    def cancel_fund_normal_convert_order(self):
        self.xjb.cancel_fund_normal_convert_order(user_name=self._account['u1']['user_name'],
                                                  login_password=self._account['u1']['login_password'],
                                                  fund_convert_from=self._account['u1']['fund_normal_convert_from'],
                                                  fund_convert_to=self._account['u1']['fund_normal_convert_to'],
                                                  trade_password=self._account['u1']['trade_password'],
                                                  )

    # 基金频道--最佳表现基金
    @keyword('test_fund_best_performance_fund')
    def fund_best_performance_fund(self):
        self.xjb.fund_best_performance_fund(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'])

    # 基金热门主题
    @keyword('test_view_fund_hot_topics')
    def view_fund_hot_topics(self):
        self.xjb.view_fund_hot_topics(fund_product_name=self._account['u1']['fund_product_for_hot_topic'])

    #  高端报价式产品修改到期处理方式(全部退出切换为部分退出)
    @keyword('test_high_end_quotation_product_expiry_processing_all_to_part')
    def high_end_quotation_product_expiry_processing_all_to_part(self):
        self.xjb.high_end_quotation_product_expiry_processing_all_to_part(user_name=self._account['u1']['user_name'],
                                                                          login_password=self._account['u1'][
                                                                              'login_password'],
                                                                          trade_password=self._account['u1'][
                                                                              'trade_password'],
                                                                          product_code=self._account['u1'][
                                                                              'high_end_quotation_product_code'])

    # 高端报价式产品修改到期处理方式(部分退出切换为自动续存)
    @keyword('test_high_end_quotation_product_expiry_processing_part_to_auto')
    def high_end_quotation_product_expiry_processing_part_to_auto(self):
        self.xjb.high_end_quotation_product_expiry_processing_part_to_auto(user_name=self._account['u1']['user_name'],
                                                                           login_password=self._account['u1'][
                                                                               'login_password'],
                                                                           trade_password=self._account['u1'][
                                                                               'trade_password'],
                                                                           product_code=self._account['u1'][
                                                                               'high_end_quotation_product_code'])

    # 高端报价式产品修改到期处理方式(自动续存切换为全部退出)
    @keyword('test_high_end_quotation_product_expiry_processing_auto_to_all')
    def high_end_quotation_product_expiry_processing_auto_to_all(self):
        self.xjb.high_end_quotation_product_expiry_processing_auto_to_all(user_name=self._account['u1']['user_name'],
                                                                          login_password=self._account['u1'][
                                                                              'login_password'],
                                                                          trade_password=self._account['u1'][
                                                                              'trade_password'],
                                                                          product_code=self._account['u1'][
                                                                              'high_end_quotation_product_code'])

    # 税收居民身份申明
    @keyword('test_tax_dweller_identity_declaration')
    def tax_dweller_identity_declaration(self):
        phone_number = Utility.GetData().mobile()
        user_new, login_password = RestfulXjbTools().register(mobile=phone_number, login_password='a0000000')
        self.xjb.tax_dweller_identity_declaration(user_name=user_new,
                                                  login_password=login_password)

    # 充值银行重新签约
    @keyword('test_bank_channel_resign')
    def bank_channel_resign(self):
        self.xjb.bank_channel_resign(user_name=self._account['u1']['user_name_for_bank_card_resign'],
                                     login_password=self._account['u1']['login_password'],
                                     recharge_amount='1.00',
                                     trade_password=self._account['u1']['trade_password'],
                                     card_no=self._account['u1']['bank_card_no_for_resign'])

    #  充值落地页查看博时详情
    @keyword('test_recharge_landing_page_view_fund_details')
    def recharge_landing_page_view_fund_details(self):
        self.xjb.recharge_landing_page_view_fund_details(
            user_name=self._account['u1']['user_name_for_bank_card_resign'],
            login_password=self._account['u1']['login_password'])

    #  首页全局搜索
    @keyword('test_home_page_global_search')
    def home_page_global_search(self):
        self.xjb.home_page_global_search(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password']
                                         )

    #  安全中心查看登录记录
    @keyword('test_security_center_view_login_record')
    def security_center_view_login_record(self):
        self.xjb.security_center_view_login_record(user_name=self._account['u1']['user_name'],
                                                   login_password=self._account['u1']['login_password']
                                                   )

    #  查看新发基金
    @keyword('test_view_newly_raised_funds')
    def view_newly_raised_funds(self):
        self.xjb.view_newly_raised_funds(product_name=self._account['u1']['fund_product_name_for_newly_raised_fund'])

    #  查看市场指数(基金频道底部进)
    @keyword('test_view_market_index')
    def view_market_index(self):
        self.xjb.view_market_index(csi_index=self._account['u1']['csi_index'])

    #  查看未实名用户账户信息,实名之后,再次查看
    @keyword('test_view_user_account_information')
    def view_user_account_information(self):
        bank_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]
        phone_number = Utility.GetData().mobile()
        user_name = Utility.GetData().english_name()
        id_no = Utility.GetData().id_no()

        user_new, login_password = RestfulXjbTools().register(mobile=phone_number, login_password='a0000000')

        self.xjb.view_user_account_information(user_name=user_new,
                                               login_password=login_password,
                                               trade_password='142536',
                                               name=user_name,
                                               id_no=id_no,
                                               band_card_no=bank_card_no)

    #  关闭短信验证码登录方式
    @keyword('test_lock_sms_login_mode')
    def lock_sms_login_mode(self):
        self.xjb.lock_sms_login_mode(user_name=self._account['u1']['user_name_for_modify_login_mode'],
                                     login_password=self._account['u1']['login_password'])

    #  开启短信验证码登录方式
    @keyword('test_unlock_sms_login_mode')
    def unlock_sms_login_mode(self):
        self.xjb.unlock_sms_login_mode(user_name=self._account['u1']['user_name_for_modify_login_mode'],
                                       login_password=self._account['u1']['login_password'],
                                       trade_password=self._account['u1']['trade_password']
                                       )

    # 修改手机号码(不能接收短信)
    @keyword('test_modify_mobile_without_sms')
    def modify_mobile_without_sms(self):
        mobile_new = Utility.GetData().mobile()

        self.xjb.modify_mobile_without_sms(user_name=self._account['u1']['user_name_for_modify_mobile_without_sms'],
                                           login_password=self._account['u1']['login_password'],
                                           mobile_new=mobile_new
                                           )

    # 重新测评
    @keyword('test_user_risk_reevaluating')
    def user_risk_reevaluating(self):
        self.xjb.user_risk_reevaluating(user_name=self._account['u1']['user_name_for_reevaluating'],
                                        login_password=self._account['u1']['login_password'])


