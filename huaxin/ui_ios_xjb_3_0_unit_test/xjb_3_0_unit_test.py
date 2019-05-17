# coding=utf-8
import time
from robot.api.deco import keyword

from _common.global_config import GlobalConfig
from _common.utility import Utility
from _tools.restful_xjb_tools import RestfulXjbTools
from _tools.ui_ios_xjb_tools_3_0 import IOSXjbTools30


class UiIosXjb30UnitTest:
    @keyword('Set Environment Args')
    def set_environment_args(self, app_path, platform_version, device_id, port, package_name, account, app_status):
        self.xjb = IOSXjbTools30('', platform_version, device_id, port, package_name, app_status, os='IOS')
        self.xjb.main_page.screen_shot()
        self._account = getattr(GlobalConfig.XjbAccountInfo, account)

    @keyword('Case Tear Down')
    def tear_down(self):
        time.sleep(1)
        self.xjb.main_page.screen_shot()
        self.xjb.web_driver.quit()
        return

    @keyword('test_home_page_recharge')
    def home_page_recharge(self):
        self.xjb.home_page_recharge(user_name=self._account['u1']['user_name'],
                                    login_password=self._account['u1']['login_password'],
                                    recharge_amount='100',
                                    trade_password=self._account['u1']['trade_password'],
                                    non_superposed_coupon_quantity=self._account['u1'][
                                        'non_superposed_coupon_quantity'],
                                    non_superposed_coupon=self._account['u1']['non_superposed_coupon_code']
                                    )

    @keyword('test_home_page_regular_withdraw')
    def home_page_regular_withdraw(self):
        self.xjb.home_page_regular_withdraw(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            withdraw_amount='0.1',
                                            trade_password=self._account['u1']['trade_password'])

    @keyword('test_home_page_fast_withdraw')
    def home_page_fast_withdraw(self):
        self.xjb.home_page_fast_withdraw(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         withdraw_amount='0.1',
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
        bank_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]

        self.xjb.register_binding_card(phone_number=phone_number,
                                       login_password='a0000000',
                                       trade_password='135790',
                                       user_name=user_name,
                                       id_no=id_no,
                                       bank_card_no=bank_card_no)

    @keyword('test_bank_card_manage_binding_card')
    def bank_card_manage_binding_card(self):
        bank_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password, bank_card_no_1 = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                              login_password='a0000000',
                                                                                              card_bin='456351',
                                                                                              trade_password='135790',
                                                                                              recharge_amount='10000')

        self.xjb.bank_card_manage_binding_card(user_name=user_new,
                                               login_password=login_password,
                                               bank_card_no=bank_card_no,
                                               phone_number=user_new)

    @keyword('test_bank_card_manage_binding_nan_yue_card')
    def bank_card_manage_binding_nan_yue_card(self):
        phone_number = Utility.GetData().mobile()
        bank_card_no = Utility.GetData().bank_card_no(card_bin='623595').split('-')[0]
        user_new, login_password, trade_password, bank_card_no_1 = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                              login_password='a0000000',
                                                                                              card_bin='456351',
                                                                                              trade_password='135790',
                                                                                              recharge_amount='10000')

        self.xjb.bank_card_manage_binding_nan_yue_card(user_name=user_new,
                                                       login_password=login_password,
                                                       bank_card_no=bank_card_no,
                                                       phone_number=user_new)

    @keyword('test_delete_bank_card')
    def delete_bank_card(self):
        # bank_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password, bank_card_no = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                            login_password='a0000000',
                                                                                            card_bin='456351',
                                                                                            trade_password='135790',
                                                                                            recharge_amount='10000')
        self.xjb.delete_bank_card(user_name=user_new,
                                  login_password=login_password,
                                  trade_password=trade_password)

    @keyword('test_security_center_modify_mobile')
    def security_center_modify_mobile(self):
        phone_number = Utility.GetData().mobile()
        mobile_new = Utility.GetData().mobile()
        user_new, login_password, trade_password, bank_card_no = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                            login_password='a0000000',
                                                                                            card_bin='456351',
                                                                                            trade_password='135790',
                                                                                            recharge_amount='10000')

        self.xjb.security_center_modify_mobile(user_name=user_new,
                                               login_password=login_password,
                                               trade_password=trade_password,
                                               mobile_new=mobile_new)

    @keyword('test_security_center_modify_trade_password')
    def security_center_modify_trade_password(self):
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password, bank_card_no = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                            login_password='a0000000',
                                                                                            card_bin='456351',
                                                                                            trade_password='135790',
                                                                                            recharge_amount='10000')

        self.xjb.security_center_modify_trade_password(user_name=user_new,
                                                       login_password=login_password,
                                                       trade_password_old=trade_password,
                                                       trade_password_new='147258')

    @keyword('test_security_center_modify_login_password')
    def security_center_modify_login_password(self):
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password, bank_card_no = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                            login_password='a0000000',
                                                                                            card_bin='456351',
                                                                                            trade_password='135790',
                                                                                            recharge_amount='10000')

        self.xjb.security_center_modify_login_password(user_name=user_new,
                                                       login_password=login_password,
                                                       login_password_new='a1111111')

    @keyword('test_security_center_find_trade_password')
    def security_center_find_trade_password(self):
        self.xjb.security_center_find_trade_password(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'])

    @keyword('test_buy_high_end_product')
    def buy_high_end_product(self):
        self.xjb.buy_high_end_product(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      trade_password=self._account['u1']['trade_password'],
                                      product_name=self._account['u1']['high_end_product'],
                                      amount=self._account['u1']['high_end_product_amount'], )

    @keyword('test_buy_dqb_product')
    def buy_dqb_product(self):
        self.xjb.buy_dqb_product(user_name=self._account['u1']['user_name'],
                                 login_password=self._account['u1']['login_password'],
                                 product_name=self._account['u1']['dqb_product'],
                                 amount=self._account['u1']['dqb_product_amount'],
                                 trade_password=self._account['u1']['trade_password'], )

    @keyword('test_hot_switch_to_dqb_product_list_page')
    def hot_switch_to_regular_product_list_page(self):
        self.xjb.hot_switch_to_dqb_product_list_page(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'])

    @keyword('test_hot_switch_to_high_end_product_list_page')
    def hot_switch_to_high_end_product_list_page(self):
        self.xjb.hot_switch_to_high_end_product_list_page(user_name=self._account['u1']['user_name'],
                                                          login_password=self._account['u1']['login_password'])

    @keyword('test_finance_product_search_with_full_name_at_home_page')
    def finance_product_search_with_full_name_at_home_page(self):
        self.xjb.finance_product_search_with_full_name_at_home_page(user_name=self._account['u1']['user_name'],
                                                                    login_password=self._account['u1'][
                                                                        'login_password'],
                                                                    product_name=self._account['u1'][
                                                                        'search_with_full_name'])

    @keyword('test_finance_product_search_with_short_name_at_home_page')
    def finance_product_search_with_short_name_at_home_page(self):
        self.xjb.finance_product_search_with_short_name_at_home_page(user_name=self._account['u1']['user_name'],
                                                                     login_password=self._account['u1'][
                                                                         'login_password'],
                                                                     product_name=self._account['u1'][
                                                                         'search_with_short_name'])

    @keyword('test_assets_xjb_detail_page_recharge')
    def assets_xjb_detail_page_recharge(self):
        self.xjb.assets_xjb_detail_page_recharge(user_name=self._account['u1']['user_name'],
                                                 login_password=self._account['u1']['login_password'],
                                                 recharge_amount='100',
                                                 trade_password=self._account['u1']['trade_password'])

    @keyword('test_assets_xjb_detail_page_regular_withdraw')
    def assets_xjb_detail_page_regular_withdraw(self):
        self.xjb.assets_xjb_detail_page_regular_withdraw(user_name=self._account['u1']['user_name'],
                                                         login_password=self._account['u1']['login_password'],
                                                         withdraw_amount='0.1',
                                                         trade_password=self._account['u1']['trade_password'])

    @keyword('test_assets_xjb_detail_page_fast_withdraw')
    def assets_xjb_detail_page_fast_withdraw(self):
        self.xjb.assets_xjb_detail_page_fast_withdraw(user_name=self._account['u1']['user_name'],
                                                      login_password=self._account['u1']['login_password'],
                                                      withdraw_amount='0.1',
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
                                 credit_card_no=self._account['u1']['credit_card_no'])

    @keyword('test_view_message')
    def view_message(self):
        self.xjb.view_message(user_name=self._account['u1']['user_name'],
                              login_password=self._account['u1']['login_password'])

    @keyword('test_view_xjb_trade_detail')
    def view_xjb_trade_detail(self):
        self.xjb.view_xjb_trade_detail(user_name=self._account['u1']['user_name'],
                                       login_password=self._account['u1']['login_password'])

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

    # 现金管理系列页面
    @keyword('test_view_high_end_cash_management_series')
    def view_high_end_cash_management_series(self):
        self.xjb.view_high_end_cash_management_series(user_name=self._account['u1']['user_name'],
                                                      login_password=self._account['u1']['login_password'])

    # 精选系列页面
    @keyword('test_view_high_end_best_recommend_series')
    def view_high_end_best_recommend_series(self):
        self.xjb.view_high_end_best_recommend_series(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'])

    # 固定收益系列页面
    @keyword('test_view_high_end_fixed_rate_series')
    def view_high_end_fixed_rate_series(self):
        self.xjb.view_high_end_fixed_rate_series(user_name=self._account['u1']['user_name'],
                                                 login_password=self._account['u1']['login_password'])

    @keyword('test_redeem_high_end_product')
    def redeem_high_end_product(self):
        self.xjb.redeem_high_end_product(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         redeem_amount=self._account['u1']['high_end_product_amount'],
                                         trade_password=self._account['u1']['trade_password'],
                                         high_end_product=self._account['u1']['high_end_product'])

    @keyword('test_redeem_high_end_product_max')
    def redeem_high_end_product_max(self):
        self.xjb.redeem_high_end_product_max(user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password'],
                                             redeem_amount='999999999999',
                                             trade_password=self._account['u1']['trade_password'],
                                             high_end_product=self._account['u1']['high_end_product'])

    @keyword('test_redeem_high_end_product_min')
    def redeem_high_end_product_min(self):
        self.xjb.redeem_high_end_product_min(user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password'],
                                             redeem_amount='0',
                                             trade_password=self._account['u1']['trade_password'],
                                             high_end_product=self._account['u1']['high_end_product'])

    @keyword('test_redeem_dqb_product')
    def redeem_dqb_product(self):
        self.xjb.redeem_dqb_product(user_name=self._account['u1']['user_for_redeem_dqb'],
                                    login_password='qq789123',
                                    redeem_amount=self._account['u1']['dqb_product_amount_2'],
                                    trade_password='121212',
                                    dqb_product=self._account['u1']['dqb_product_2'])

    @keyword('test_redeem_dqb_product_max')
    def redeem_dqb_product_max(self):
        self.xjb.redeem_dqb_product_max(user_name=self._account['u1']['user_for_redeem_dqb'],
                                        login_password='qq789123',
                                        redeem_amount='999999999999',
                                        trade_password='121212',
                                        dqb_product=self._account['u1']['dqb_product_2'])

    @keyword('test_redeem_dqb_product_min')
    def redeem_dqb_product_min(self):
        self.xjb.redeem_dqb_product_min(user_name=self._account['u1']['user_for_redeem_dqb'],
                                        login_password='qq789123',
                                        redeem_amount='0',
                                        trade_password='121212',
                                        dqb_product=self._account['u1']['dqb_product_2'])

    @keyword('test_my_referee')
    def my_referee(self):
        self.xjb.my_referee(user_name=self._account['u1']['user_name'],
                            login_password=self._account['u1']['login_password'],
                            phone_no=self._account['u2']['user_name'])

    @keyword('test_risk_evaluating_new_user')
    def risk_evaluating_new_user(self):
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password, bank_card_no = RestfulXjbTools().new_user(user_name=phone_number,
                                                                                            login_password='a0000000',
                                                                                            card_bin='456351',
                                                                                            trade_password='135790',
                                                                                            recharge_amount='10000')
        self.xjb.risk_evaluating_new_user(user_name=user_new,
                                          login_password=login_password)

    @keyword('test_fund_non_money_product_search_with_name')
    def fund_product_search_with_name(self):
        self.xjb.fund_non_money_product_search_with_name(user_name=self._account['u1']['user_name'],
                                                         login_password=self._account['u1']['login_password'],
                                                         product_name=self._account['u1']['fund_product_name'])

    @keyword('test_fund_money_product_search_with_code')
    def fund_product_search_with_code(self):
        self.xjb.fund_money_product_search_with_code(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'],
                                                     product_name=self._account['u1']['fund_product_code'])

    @keyword('test_buy_fund_product')
    def buy_fund_product(self):
        self.xjb.buy_fund_product(user_name=self._account['u1']['user_name'],
                                  login_password=self._account['u1']['login_password'],
                                  fund_product_name=self._account['u1']['fund_product_name'],
                                  amount=self._account['u1']['fund_product_amount'],
                                  trade_password=self._account['u1']['trade_password'],
                                  fund_product_code=self._account['u1']['non_money_fund_product_code'], )

    @keyword('test_invite_friend')
    def invite_friend(self):
        self.xjb.invite_friend(user_name=self._account['u1']['user_name'],
                               login_password=self._account['u1']['login_password'])

    @keyword('test_use_other_reservation_code')
    def use_other_reservation_code(self):
        self.xjb.use_other_reservation_code(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            reservation_code=self._account['u1']['reserve_code'],
                                            trade_password=self._account['u1']['trade_password'],
                                            buy_quota=self._account['u1']['reservation_code_buy_quota'],
                                            buy_count=self._account['u1']['reservation_code_buy_count'],
                                            reserve_quota=self._account['u1']['reservation_code_reserve_quota'],
                                            reserve_count=self._account['u1']['reservation_code_reserve_count'],
                                            product_id=self._account['u1']['product_id_for_reservation_code']
                                            )

    @keyword('test_use_other_reservation_code_without_reservation_code')
    def use_other_reservation_code_without_reservation_code(self):
        self.xjb.use_other_reservation_code_without_reservation_code(
            user_name=self._account['u1']['user_name_for_reservation_code'],
            login_password=self._account['u1']['login_password_for_reservation_code'],
            reservation_code=self._account['u1']['reserve_code'],
            trade_password=self._account['u1']['trade_password_for_reservation_code'],
            buy_quota=self._account['u1']['reservation_code_buy_quota'],
            buy_count=self._account['u1']['reservation_code_buy_count'],
            reserve_quota=self._account['u1']['reservation_code_reserve_quota'],
            reserve_count=self._account['u1']['reservation_code_reserve_count'],
            product_id=self._account['u1']['product_id_for_reservation_code'],
            user_name_have_reservation_code=self._account['u1']['user_name'],
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
                                      reservation_code=self._account['u1']['reserve_code'],
                                      product_id=self._account['u1']['product_id_for_reservation_code']
                                      )

    @keyword('test_redeem_fund_product')
    def redeem_fund_product(self):
        self.xjb.redeem_fund_product(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     amount=self._account['u1']['fund_product_amount'],
                                     trade_password=self._account['u1']['trade_password'],
                                     fund_product_name_for_redeem=self._account['u1']['fund_product_name_for_redeem'], )

    @keyword('test_redeem_fund_product_max')
    def redeem_fund_product_max(self):
        self.xjb.redeem_fund_product_max(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         amount='999999999999',
                                         trade_password=self._account['u1']['trade_password'],
                                         fund_product_name_for_redeem=self._account['u1'][
                                             'fund_product_name_for_redeem'], )

    @keyword('test_redeem_fund_product_min')
    def redeem_fund_product_min(self):
        self.xjb.redeem_fund_product_min(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         amount='0',
                                         trade_password=self._account['u1']['trade_password'],
                                         fund_product_name_for_redeem=self._account['u1'][
                                             'fund_product_name_for_redeem'], )

    @keyword('test_earn_points')
    def earn_points(self):
        self.xjb.earn_points(user_name=self._account['u1']['user_name'],
                             login_password=self._account['u1']['login_password'],
                             amount=self._account['u1']['fund_product_amount'],
                             trade_password=self._account['u1']['trade_password'],
                             fund_product_name=self._account['u1']['fund_product_name'],
                             fund_product_code=self._account['u1']['non_money_fund_product_code'],
                             )

    # 信用卡还款
    @keyword('test_credit_card_repay')
    def credit_card_repay(self):
        self.xjb.credit_card_repay(user_name=self._account['u1']['user_name'],
                                   login_password=self._account['u1']['login_password'],
                                   repay_amount=self._account['u1']['credit_card_repay_amount'],
                                   trade_password=self._account['u1']['trade_password'])

    # 信用卡预约还款
    @keyword('test_credit_card_reserved_pay')
    def credit_card_reserved_pay(self):
        self.xjb.credit_card_reserved_pay(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          reserved_pay_amount=self._account['u1']['credit_card_reserved_pay_amount'],
                                          trade_password=self._account['u1']['trade_password'],
                                          user_credit_card_id=self._account['u1']['user_credit_card_id'])

    # 取消预约还款
    @keyword('test_cancel_reserved_pay')
    def cancel_reserved_pay(self):
        self.xjb.cancel_reserved_pay(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     user_credit_card_id=self._account['u1']['user_credit_card_id'])

    # 赚积分--推荐用户注册绑卡
    @keyword('test_earn_points_by_recommend_user_register')
    def earn_points_by_recommend_user_register(self):
        self.xjb.earn_points_by_recommend_user_register(user_name=self._account['u1']['user_name'],
                                                        login_password=self._account['u1']['login_password'])

    # 花积分--买定期宝
    @keyword('test_spend_points_by_buy_dqb')
    def spend_points_by_buy_dqb(self):
        self.xjb.spend_points_by_buy_dqb(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         amount=self._account['u1']['dqb_product_amount'],
                                         trade_password=self._account['u1']['trade_password'],
                                         dqb_product_name=self._account['u1']['dqb_product'],
                                         )

    # 花积分--买基金
    @keyword('test_spend_points_by_buy_fund')
    def spend_points_by_buy_fund(self):
        self.xjb.spend_points_by_buy_fund(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          amount=self._account['u1']['fund_product_amount'],
                                          trade_password=self._account['u1']['trade_password'],
                                          fund_product_name=self._account['u1']['fund_product_name'],
                                          fund_product_code=self._account['u1']['non_money_fund_product_code']
                                          )

    # 花积分--买高端产品
    @keyword('test_spend_points_by_buy_vipproduct_use_product_name')
    def spend_points_by_buy_vipproduct_use_product_name(self):
        self.xjb.spend_points_by_buy_vipproduct_use_product_name(user_name=self._account['u1']['user_name'],
                                                                 login_password=self._account['u1']['login_password'],
                                                                 trade_password=self._account['u1']['trade_password'],
                                                                 product_name=self._account['u1'][
                                                                     'high_end_product_for_points_offset'],
                                                                 amount=self._account['u1']['high_end_product_amount'])

    # 设置还款提醒
    @keyword('test_add_credit_card_repayment_warn')
    def add_credit_card_repayment_warn(self):
        self.xjb.add_credit_card_repayment_warn(user_name=self._account['u1']['user_name'],
                                                login_password=self._account['u1']['login_password'])

    # 取消还款提醒
    @keyword('test_cancel_credit_card_repayment_warn')
    def cancel_credit_card_repayment_warn(self):
        self.xjb.cancel_credit_card_repayment_warn(user_name=self._account['u1']['user_name'],
                                                   login_password=self._account['u1']['login_password'])

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
    @keyword('test_fund_info_report')
    def fund_info_report(self):
        self.xjb.fund_info_report(user_name=self._account['u1']['user_name'],
                                  login_password=self._account['u1']['login_password']
                                  )

    # 基金频道--机构观点
    @keyword('test_fund_institution_viewpoint')
    def fund_institution_viewpoint(self):
        self.xjb.fund_institution_viewpoint()

    # 基金频道--达人论基
    @keyword('test_fund_talent_fund_discussion')
    def fund_talent_fund_discussion(self):
        self.xjb.fund_talent_fund_discussion()

    # 基金频道--市场指数
    @keyword('test_fund_market_index')
    def fund_market_index(self):
        self.xjb.fund_market_index(csi_index=self._account['u1']['csi_index'])

    # 基金频道--全部基金
    @keyword('test_fund_all_funds')
    def fund_all_funds(self):
        self.xjb.fund_all_funds()

    # 基金频道--评级排行
    @keyword('test_fund_rating_and_ranking')
    def fund_rating_and_ranking(self):
        self.xjb.fund_rating_and_ranking()

    # 基金频道--自选基金
    @keyword('test_fund_selected_funds')
    def fund_selected_funds(self):
        self.xjb.fund_selected_funds(fund_product_name=self._account['u1']['fund_product_name'],
                                     user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     fund_company=self._account['u1']['fund_company']
                                     )

    # 基金频道--对比分析
    @keyword('test_fund_comparison_and_analysis')
    def fund_comparison_and_analysis(self):
        self.xjb.fund_comparison_and_analysis(fund_product_code=self._account['u1']['non_money_fund_product_code'],
                                              fund_product_code_2=self._account['u1']['fund_product_code_2'],
                                              )

    # 购买定期宝使用优惠券(不可叠加)
    @keyword('test_buy_dqb_use_nonsuperposed_coupon')
    def buy_dqb_use_nonsuperposed_coupon(self):
        self.xjb.buy_dqb_use_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                  login_password=self._account['u1']['login_password'],
                                                  non_superposed_coupon_code=self._account['u1'][
                                                      'non_superposed_coupon_code'],
                                                  non_superposed_coupon_quantity=self._account['u1'][
                                                      'non_superposed_coupon_quantity'],
                                                  amount=self._account['u1']['dqb_product_amount'],
                                                  trade_password=self._account['u1']['trade_password'],
                                                  product_name=self._account['u1']['dqb_product']
                                                  )

    # 购买定期宝使用优惠券(可叠加)
    @keyword('test_buy_dqb_use_superposed_coupon')
    def buy_dqb_use_superposed_coupon(self):
        self.xjb.buy_dqb_use_superposed_coupon(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'],
                                               superposed_coupon_code=self._account['u1'][
                                                   'superposed_coupon_code'],
                                               superposed_coupon_quantity=self._account['u1'][
                                                   'superposed_coupon_quantity'],
                                               amount=self._account['u1']['dqb_product_amount'],
                                               trade_password=self._account['u1']['trade_password'],
                                               product_name=self._account['u1']['dqb_product']
                                               )

    # 购买高端使用优惠券(不可叠加)
    @keyword('test_buy_vipproduct_use_nonsuperposed_coupon')
    def buy_vipproduct_use_nonsuperposed_coupon(self):
        self.xjb.buy_vipproduct_use_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                         login_password=self._account['u1']['login_password'],
                                                         non_superposed_coupon_code=self._account['u1'][
                                                             'non_superposed_coupon_code'],
                                                         non_superposed_coupon_quantity=self._account['u1'][
                                                             'non_superposed_coupon_quantity'],
                                                         amount=self._account['u1']['high_end_product_amount'],
                                                         trade_password=self._account['u1']['trade_password'],
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
                                                      amount=self._account['u1'][
                                                          'high_end_amount_for_superposed_coupon'],
                                                      trade_password=self._account['u1']['trade_password'],
                                                      product_name=self._account['u1']['high_end_product']
                                                      )

    # 购买基金使用优惠券(不可叠加)
    @keyword('test_buy_fund_use_nonsuperposed_coupon')
    def buy_fund_use_nonsuperposed_coupon(self):
        self.xjb.buy_fund_use_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                   login_password=self._account['u1']['login_password'],
                                                   non_superposed_coupon_code=self._account['u1'][
                                                       'non_superposed_coupon_code'],
                                                   non_superposed_coupon_quantity=self._account['u1'][
                                                       'non_superposed_coupon_quantity'],
                                                   product_name=self._account['u1']['fund_product_name'],
                                                   amount=self._account['u1'][
                                                       'fund_product_amount_for_nonsuperposed_coupon'],
                                                   trade_password=self._account['u1']['trade_password'],
                                                   fund_product_code=self._account['u1']['non_money_fund_product_code']
                                                   )

    # 购买基金使用优惠券(可叠加)
    @keyword('test_buy_fund_use_superposed_coupon')
    def buy_fund_use_superposed_coupon(self):
        self.xjb.buy_fund_use_superposed_coupon(user_name=self._account['u1']['user_name'],
                                                login_password=self._account['u1']['login_password'],
                                                superposed_coupon_code=self._account['u1'][
                                                    'superposed_coupon_code'],
                                                superposed_coupon_quantity=self._account['u1'][
                                                    'superposed_coupon_quantity'],
                                                product_name=self._account['u1']['fund_product_name'],
                                                amount=self._account['u1']['fund_product_amount'],
                                                trade_password=self._account['u1']['trade_password'],
                                                fund_product_code=self._account['u1']['non_money_fund_product_code']
                                                )

    # 购买定期宝使用积分+优惠券(不可叠加)
    @keyword('test_buy_dqb_use_points_and_nonsuperposed_coupon')
    def buy_dqb_use_points_and_nonsuperposed_coupon(self):
        self.xjb.buy_dqb_use_points_and_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                             login_password=self._account['u1']['login_password'],
                                                             non_superposed_coupon_code=self._account['u1'][
                                                                 'non_superposed_coupon_code'],
                                                             non_superposed_coupon_quantity=self._account['u1'][
                                                                 'non_superposed_coupon_quantity'],
                                                             amount=self._account['u1'][
                                                                 'dqb_product_amount_for_superposed_coupon'],
                                                             trade_password=self._account['u1']['trade_password'],
                                                             product_name=self._account['u1']['dqb_product']
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
                                                          product_name=self._account['u1']['dqb_product']
                                                          )

    # 购买高端使用积分+优惠券(不可叠加)
    @keyword('test_buy_vipproduct_use_points_and_nonsuperposed_coupon')
    def buy_vipproduct_use_points_and_nonsuperposed_coupon(self):
        self.xjb.buy_vipproduct_use_points_and_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                                    login_password=self._account['u1'][
                                                                        'login_password'],
                                                                    non_superposed_coupon_code=self._account['u1'][
                                                                        'non_superposed_coupon_code'],
                                                                    non_superposed_coupon_quantity=self._account['u1'][
                                                                        'non_superposed_coupon_quantity'],
                                                                    amount=self._account['u1'][
                                                                        'high_end_product_amount'],
                                                                    trade_password=self._account['u1'][
                                                                        'trade_password'],
                                                                    product_name=self._account['u1']['high_end_product']
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
                                                                 product_name=self._account['u1']['high_end_product']
                                                                 )

    # 购买基金使用积分+优惠券(不可叠加)
    @keyword('test_buy_fund_use_points_and_nonsuperposed_coupon')
    def buy_fund_use_points_and_nonsuperposed_coupon(self):
        self.xjb.buy_fund_use_points_and_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                              login_password=self._account['u1']['login_password'],
                                                              non_superposed_coupon_code=self._account['u1'][
                                                                  'non_superposed_coupon_code'],
                                                              non_superposed_coupon_quantity=self._account['u1'][
                                                                  'non_superposed_coupon_quantity'],
                                                              fund_product_name=self._account['u1'][
                                                                  'fund_product_name'],
                                                              amount=self._account['u1']['fund_product_amount'],
                                                              trade_password=self._account['u1']['trade_password'],
                                                              fund_product_code=self._account['u1'][
                                                                  'non_money_fund_product_code']
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
                                                           fund_product_code=self._account['u1'][
                                                               'non_money_fund_product_code']
                                                           )

    # 基金定投
    @keyword('test_fund_plan')
    def fund_plan(self):
        self.xjb.fund_plan(user_name=self._account['u1']['user_name'],
                           login_password=self._account['u1']['login_password'],
                           fund_product_name=self._account['u1']['fund_product_name'],
                           amount=self._account['u1']['fund_product_amount'],
                           trade_password=self._account['u1']['trade_password'],
                           )

    # 查看历史定投(用户没有历史定投)
    @keyword('test_check_empty_fund_history_plan')
    def check_empty_fund_history_plan(self):
        self.xjb.check_empty_fund_history_plan(user_name=self._account['u2']['user_name'],
                                               login_password=self._account['u2']['login_password'])

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
                                  amount='2.00')

    # 新增定投计划
    @keyword('test_add_fund_plan')
    def add_fund_plan(self):
        self.xjb.add_fund_plan(user_name=self._account['u1']['user_name'],
                               login_password=self._account['u1']['login_password'],
                               trade_password=self._account['u1']['trade_password'],
                               fund_product_name=self._account['u1']['fund_product_name'],
                               fund_product_code=self._account['u1']['fund_product_code'],
                               amount=self._account['u1']['fund_product_amount'])

    # 随心借
    @keyword('test_vip_product_pledge')
    def vip_product_pledge(self):
        self.xjb.vip_product_pledge(user_name=self._account['u1']['user_name'],
                                    login_password=self._account['u1']['login_password'],
                                    product_name=self._account['u1']['product_name_for_vipproduct_pledge'],
                                    pledge_amount=self._account['u1']['pledge_amount'],
                                    trade_password=self._account['u1']['trade_password'],
                                    )

    # 随心还(一次还完)
    @keyword('test_vip_product_pledge_repay')
    def vip_product_pledge_repay(self):
        self.xjb.vip_product_pledge_repay(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          product_name=self._account['u1']['product_name_for_vipproduct_pledge'],
                                          pledge_repay_amount=self._account['u1']['pledge_repay_amount'],
                                          trade_password=self._account['u1']['trade_password'],
                                          )

    # 现金宝页面查看七日年化收益率
    @keyword('test_view_xjb_seven_days_annual_rate_of_return')
    def view_xjb_seven_days_annual_rate_of_return(self):
        self.xjb.view_xjb_seven_days_annual_rate_of_return(user_name=self._account['u1']['user_name'],
                                                           login_password=self._account['u1']['login_password'])

    # 现金宝页面点击累计收益,进入累计收益页面
    @keyword('test_view_xjb_income_accumulated')
    def view_xjb_income_accumulated(self):
        self.xjb.view_xjb_income_accumulated(user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password'])

    # 现金宝页面点击万份收益, 进入万份收益页面
    @keyword('test_view_xjb_income_per_wan')
    def view_xjb_income_per_wan(self):
        self.xjb.view_xjb_income_per_wan(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'])

    # 基金频道--删除自选基金
    @keyword('test_fund_selected_funds_deleted')
    def fund_selected_funds_deleted(self):
        self.xjb.fund_selected_funds_deleted(fund_product_name=self._account['u1']['fund_product_name'],
                                             user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password'])

    # 我的优惠券列表-立即使用-购买页面
    @keyword('test_my_coupon_list_to_buy_page')
    def my_coupon_list_to_buy_page(self):
        self.xjb.use_coupon_from_my_coupon_list(user_name=self._account['u1']['user_name'],
                                                login_password=self._account['u1']['login_password'])

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

    # 优惠券说明
    @keyword('test_my_coupon_empty_list')
    def my_coupon_empty_list(self):
        self.xjb.my_coupon_empty_list(user_name=self._account['u2']['user_name'],
                                      password=self._account['u2']['login_password'])

    # 开启工资代发
    @keyword('test_salary_issuing')
    def salary_issuing(self):
        self.xjb.salary_issuing(user_name=self._account['u1']['user_name'],
                                login_password=self._account['u1']['login_password'])

    # 终止工资代发
    @keyword('test_stop_salary_issuing')
    def stop_salary_issuing(self):
        self.xjb.stop_salary_issuing(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     trade_password=self._account['u1']['trade_password'])

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
                                                           last_no=self._account['u1'][
                                                               'pay_card_last_no_for_modification'],
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

    # 下载资产证明
    @keyword('test_download_assets_certification')
    def download_assets_certification(self):
        self.xjb.download_assets_certification(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'],
                                               trade_password=self._account['u1']['trade_password'])

    # 现金宝持有页面查看在途资产(从资产分析页面进)
    @keyword('test_view_xjb_asset_in_transit')
    def view_xjb_asset_in_transit(self):
        self.xjb.view_xjb_asset_in_transit(user_name=self._account['u1']['user_name'],
                                           login_password=self._account['u1']['login_password'])

    # 现金宝持有页面查看产品详情(资产分析页面进)
    @keyword('test_view_xjb_product_detail')
    def view_xjb_product_detail(self):
        self.xjb.view_xjb_product_detail(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'])

    # 现金宝持有页面查看七日年化收益率曲线
    @keyword('test_view_xjb_seven_days_annual_rate_of_return_curve')
    def view_xjb_seven_days_annual_rate_of_return_curve(self):
        self.xjb.view_xjb_seven_days_annual_rate_of_return_curve(user_name=self._account['u1']['user_name'],
                                                                 login_password=self._account['u1']['login_password'])

    # 查看基金资产, 资产结构配置页面(资产分析页面进)
    @keyword('test_view_holding_fund_asset_structure')
    def view_holding_fund_asset_structure(self):
        self.xjb.view_holding_fund_asset_structure(user_name=self._account['u1']['user_name'],
                                                   login_password=self._account['u1']['login_password'])

    # 查看高端资产（资产分析页面进）的说明
    @keyword('test_view_high_end_holding_assets_description')
    def view_high_end_holding_assets_description(self):
        self.xjb.view_high_end_holding_assets_description(user_name=self._account['u1']['user_name'],
                                                          login_password=self._account['u1']['login_password'])

    # 查看定活宝资产（资产分析页面进）的说明
    @keyword('test_view_dhb_holding_assets_description')
    def view_dhb_holding_assets_description(self):
        self.xjb.view_dhb_holding_assets_description(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'])

    # 查看现金宝资产（我的页面进）的说明
    @keyword('test_view_xjb_holding_assets_description')
    def view_xjb_holding_assets_description(self):
        self.xjb.view_xjb_holding_assets_description(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'])

    # 查看基金资产（我的页面进）的说明
    @keyword('test_view_fund_holding_assets_description')
    def view_fund_holding_assets_description(self):
        self.xjb.view_fund_holding_assets_description(user_name=self._account['u1']['user_name'],
                                                      login_password=self._account['u1']['login_password'])

    # 工资理财——开启计划
    @keyword('test_start_financing_plan')
    def start_financing_plan(self):
        self.xjb.start_financing_plan(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      last_no=self._account['u1']['pay_card_last_no'],
                                      amount=self._account['u1']['financing_amount'],
                                      trade_password=self._account['u1']['trade_password'],
                                      )

    # 持有高端产品追加购买(包含购买确认中和确认后)
    @keyword('test_high_end_continue_purchase')
    def high_end_continue_purchase(self):
        self.xjb.high_end_continue_purchase(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            product_name=self._account['u1']['high_end_product']
                                            )

    # 持有定活宝产品追加购买
    @keyword('test_dhb_continue_purchase')
    def dhb_continue_purchase(self):
        self.xjb.dhb_continue_purchase(user_name=self._account['u1']['user_name'],
                                       login_password=self._account['u1']['login_password'],
                                       product_name=self._account['u1']['dqb_product']
                                       )

    # 持有基金产品追加购买(包含购买确认中和确认后)
    @keyword('test_fund_continue_purchase')
    def fund_continue_purchase(self):
        self.xjb.fund_continue_purchase(user_name=self._account['u1']['user_name'],
                                        login_password=self._account['u1']['login_password'],
                                        product_name=self._account['u1']['fund_product_name'],
                                        product_code=self._account['u1']['non_money_fund_product_code'],
                                        product_name_confirmed=self._account['u1']['fund_product_name_for_fast_redeem']
                                        )

    # 短信验证码登录
    @keyword('test_login_use_verification_code')
    def login_use_verification_code(self):
        self.xjb.login_use_verification_code(user_name=self._account['u2']['user_name'])

    # 信用卡还款使用优惠券
    @keyword('test_credit_card_repay_use_coupon')
    def credit_card_repay_use_coupon(self):
        self.xjb.credit_card_repay_use_coupon(user_name=self._account['u1']['user_name'],
                                              login_password=self._account['u1']['login_password'],
                                              repay_amount=self._account['u1']['credit_card_repay_amount'],
                                              trade_password=self._account['u1']['trade_password'],
                                              last_card_no=self._account['u1']['last_card_no_for_repay'],
                                              non_superposed_coupon_code=self._account['u1'][
                                                  'non_superposed_coupon_code'],
                                              non_superposed_coupon_quantity=self._account['u1'][
                                                  'non_superposed_coupon_quantity'])

    # 信用卡预约还款使用优惠券
    @keyword('test_credit_card_reserve_repay_use_coupon')
    def credit_card_reserve_repay_use_coupon(self):
        self.xjb.credit_card_reserve_repay_use_coupon(user_name=self._account['u1']['user_name'],
                                                      login_password=self._account['u1']['login_password'],
                                                      repay_amount=self._account['u1']['credit_card_repay_amount'],
                                                      trade_password=self._account['u1']['trade_password'],
                                                      last_card_no=self._account['u1']['last_card_no_for_repay'],
                                                      superposed_coupon_code=self._account['u1'][
                                                          'superposed_coupon_code'],
                                                      superposed_coupon_quantity=self._account['u1'][
                                                          'non_superposed_coupon_quantity'],
                                                      user_credit_card_id=self._account['u1']['user_credit_card_id'])

    # 基金撤单
    @keyword('test_cancel_fund_order')
    def cancel_fund_order(self):
        self.xjb.cancel_fund_order(user_name=self._account['u1']['user_name'],
                                   login_password=self._account['u1']['login_password'],
                                   product_name=self._account['u1']['fund_product_name'],
                                   trade_password=self._account['u1']['trade_password'],
                                   )

    # 高端撤单
    @keyword('test_cancel_vip_product_order')
    def cancel_vip_product_order(self):
        self.xjb.cancel_vip_product_order(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          product_name=self._account['u1']['high_end_product'],
                                          trade_password=self._account['u1']['trade_password'],
                                          amount=self._account['u1']['high_end_product_amount']
                                          )

    # 首页现金宝取出(存入金额小于最小值)
    @keyword('test_home_page_recharge_min')
    def home_page_recharge_min(self):
        self.xjb.home_page_recharge_negative(user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password'],
                                             recharge_amount='0',
                                             trade_password=self._account['u1']['trade_password'])

    # 首页现金宝取出(存入金额大于最大值)
    @keyword('test_home_page_recharge_max')
    def home_page_recharge_max(self):
        self.xjb.home_page_recharge_negative(user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password'],
                                             recharge_amount='999999999',
                                             trade_password=self._account['u1']['trade_password'])

    # 理财日历查看提醒事项
    @keyword('test_check_event_reminder_in_calendar')
    def check_event_reminder_in_calendar(self):
        self.xjb.check_event_reminder_in_calendar(user_name=self._account['u1']['user_name'],
                                                  password=self._account['u1']['login_password'])

    # 定活宝收益计算器
    @keyword('test_dhb_income_calculator')
    def dhb_income_calculator(self):
        self.xjb.dhb_income_calculator(user_name=self._account['u1']['user_name'],
                                       password=self._account['u1']['login_password'],
                                       product_name=self._account['u1']['dqb_product'], amount='600')

    # 定活宝收益计算器小于起投金额
    @keyword('test_dhb_income_calculator_less_than_start_money')
    def dhb_income_calculator_less_than_start_amount(self):
        self.xjb.dhb_income_calculator_less_than_start_amount(user_name=self._account['u1']['user_name'],
                                                              password=self._account['u1']['login_password'],
                                                              product_name=self._account['u1']['dqb_product'],
                                                              amount='400')

    # 定活宝收益计算器大于最大金额
    @keyword('test_dhb_income_calculator_greater_than_max_amount')
    def dhb_income_calculator_greater_than_max_amount(self):
        self.xjb.dhb_income_calculator_greater_than_max_amount(user_name=self._account['u1']['user_name'],
                                                               password=self._account['u1']['login_password'],
                                                               product_name=self._account['u1']['dqb_product'],
                                                               amount='9999999')

    # 高端收益计算器
    @keyword('test_vip_income_calculator')
    def vip_income_calculator(self):
        self.xjb.vip_income_calculator(user_name=self._account['u1']['user_name'],
                                       password=self._account['u1']['login_password'],
                                       product_name=self._account['u1'][
                                           'high_end_product_for_income_calculator'], amount='25000')

    # 高端收益计算器少于起投金额
    @keyword('test_vip_income_calculator_less_than_start_amount')
    def vip_income_calculator_less_than_start_amount(self):
        self.xjb.vip_income_calculator_less_than_start_amount(user_name=self._account['u1']['user_name'],
                                                              password=self._account['u1']['login_password'],
                                                              product_name=self._account['u1'][
                                                                  'high_end_product_for_income_calculator'], amount='0')

    # 高端收益计算器大于最大购买金额
    @keyword('test_vip_income_calculator_greater_than_max_amount')
    def vip_income_calculator_greater_than_max_amount(self):
        self.xjb.vip_income_calculator_greater_than_max_amount(user_name=self._account['u1']['user_name'],
                                                               password=self._account['u1']['login_password'],
                                                               product_name=self._account['u1'][
                                                                   'high_end_product_for_income_calculator'],
                                                               amount='9999999999999')

    # 定投排行
    @keyword('test_view_fund_plan_rankings')
    def view_fund_plan_rankings(self):
        self.xjb.view_fund_plan_rankings()

    # 现金管理系列购买高端
    @keyword('test_buy_vip_product_use_cash_management_product')
    def buy_vip_product_use_cash_management_product(self):
        self.xjb.buy_vip_product_use_cash_management_product(user_name=self._account['u1']['user_name'],
                                                             login_password=self._account['u1']['login_password'],
                                                             product_name=self._account['u1']['high_end_product'],
                                                             trade_password=self._account['u1']['trade_password'],
                                                             amount=self._account['u1']['high_end_product_amount'],
                                                             cash_management_product=self._account['u1'][
                                                                 'cash_management_product'])

    # 现金管理系列购买基金
    @keyword('test_buy_fund_product_use_cash_management_product')
    def buy_fund_product_use_cash_management_product(self):
        self.xjb.buy_fund_product_use_cash_management_product(user_name=self._account['u1']['user_name'],
                                                              login_password=self._account['u1']['login_password'],
                                                              fund_product_name=self._account['u1'][
                                                                  'fund_product_name'],
                                                              trade_password=self._account['u1']['trade_password'],
                                                              amount=self._account['u1']['fund_product_amount'],
                                                              cash_management_product=self._account['u1'][
                                                                  'cash_management_product'])

    # 现金管理系列购买定活宝
    @keyword('test_buy_dhb_product_use_cash_management_product')
    def buy_dhb_product_use_cash_management_product(self):
        self.xjb.buy_dhb_product_use_cash_management_product(user_name=self._account['u1']['user_name'],
                                                             login_password=self._account['u1']['login_password'],
                                                             product_name=self._account['u1']['dqb_product'],
                                                             trade_password=self._account['u1']['trade_password'],
                                                             amount=self._account['u1']['dqb_product_amount'],
                                                             cash_management_product=self._account['u1'][
                                                                 'cash_management_product'])

    # 查看非货币性基金详情信息
    @keyword('test_view_non_monetary_fund_info')
    def view_non_monetary_fund_info(self):
        self.xjb.view_non_monetary_fund_info(fund_product_name=self._account['u1']['fund_product_name'])

    # 查看货币性基金详情信息
    @keyword('test_view_monetary_fund_info')
    def view_monetary_fund_info(self):
        self.xjb.view_monetary_fund_info(fund_product_name=self._account['u1']['fund_product_name_for_redeem'])

    # 查看货币型基金的7日年化收益和万份收益(从查看历史和查看更多进入)
    @keyword('test_view_monetary_fund_annual_rate')
    def view_monetary_fund_annual_rate(self):
        self.xjb.view_monetary_fund_annual_rate(fund_product_name=self._account['u1']['fund_product_name_for_redeem'])

    # 查看现金管理系列产品详情
    @keyword('test_view_cash_management_high_end_info')
    def view_cash_management_high_end_info(self):
        self.xjb.view_cash_management_high_end_info(
            product_name=self._account['u1']['high_end_product_for_income_calculator'])

    # 查看固定收益系列产品详情
    @keyword('test_view_fixed_rated_high_end_info')
    def view_fixed_rated_high_end_info(self):
        self.xjb.view_fixed_rated_high_end_info(product_name=self._account['u1']['high_end_product'])

    # 查看精选收益系列产品详情
    @keyword('test_view_best_recommend_high_end_info')
    def view_best_recommend_high_end_info(self):
        self.xjb.view_best_recommend_high_end_info(product_name=self._account['u1']['best_recommend_high_end_product'])

    # 查看精选收益产品的历史净值
    @keyword('test_view_high_end_history_nav')
    def view_high_end_history_nav(self):
        self.xjb.view_high_end_history_nav(product_name=self._account['u1']['best_recommend_high_end_product'])

    # 查看现金管理系列产品的历史收益
    @keyword('test_view_cash_management_high_end_annual_rate')
    def view_cash_management_high_end_annual_rate(self):
        self.xjb.view_cash_management_high_end_annual_rate(
            product_name=self._account['u1']['high_end_product_for_income_calculator'])

    # 福利中心去推荐
    @keyword('test_welfare_center_invite_friend')
    def welfare_center_invite_friend(self):
        self.xjb.welfare_center_invite_friend(user_name=self._account['u1']['user_name'],
                                              password=self._account['u1']['login_password'])

    # 福利中心去分享
    @keyword('test_welfare_center_go_to_share')
    def welfare_center_go_to_share(self):
        self.xjb.welfare_center_go_to_share(user_name=self._account['u1']['user_name'],
                                            password=self._account['u1']['login_password'])

    # 福利中心去关注
    @keyword('test_welfare_center_go_to_focus')
    def welfare_center_go_to_focus(self):
        self.xjb.welfare_center_go_to_focus(user_name=self._account['u1']['user_name'],
                                            password=self._account['u1']['login_password'])

    # 福利中心去点赞
    @keyword('test_welfare_center_go_to_good')
    def welfare_center_go_to_good(self):
        self.xjb.welfare_center_go_to_good(user_name=self._account['u1']['user_name'],
                                           password=self._account['u1']['login_password'])

    # 福利中心查看积分明细
    @keyword('test_welfare_center_points_details')
    def welfare_center_points_details(self):
        self.xjb.welfare_center_points_details(user_name=self._account['u1']['user_name'],
                                               password=self._account['u1']['login_password'])

    # 福利中心查看元宝明细
    @keyword('test_welfare_center_yb_details')
    def welfare_center_yb_details(self):
        self.xjb.welfare_center_yb_details(user_name=self._account['u1']['user_name'],
                                           password=self._account['u1']['login_password'])

    # 福利中心签到
    @keyword('test_welfare_center_check_in')
    def welfare_center_check_in(self):
        self.xjb.welfare_center_check_in(user_name=self._account['u3']['user_name'],
                                         password=self._account['u3']['login_password'])

    # 福利中心限时特惠
    @keyword('test_welfare_center_timed_discount')
    def welfare_center_timed_discount(self):
        self.xjb.welfare_center_timed_discount(user_name=self._account['u1']['user_name'],
                                               password=self._account['u1']['login_password'])

    # 福利中心边逛边兑-优惠券
    @keyword('test_welfare_center_exchange_coupon')
    def welfare_center_exchange_coupon(self):
        self.xjb.welfare_center_exchange_coupon(user_name=self._account['u1']['user_name'],
                                                password=self._account['u1']['login_password'])

    # 查看货币基金历史持仓
    @keyword('test_view_fund_history_holding')
    def view_fund_history_holding(self):
        self.xjb.view_fund_history_holding(user_name=self._account['u1']['user_name'],
                                           password=self._account['u1']['login_password'],
                                           fund_product_name='华夏现金增利货币B')

    # 查看高端现金管理历史持仓
    @keyword('test_view_high_end_history_holding')
    def view_high_end_history_holding(self):
        self.xjb.view_high_end_history_holding(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'],
                                               product_name='现金管理3号')

    # 基金快速转换
    @keyword('test_fund_fast_convert')
    def fund_fast_convert(self):
        self.xjb.fund_fast_convert(user_name=self._account['u1']['user_name'],
                                   login_password=self._account['u1']['login_password'],
                                   fund_convert_from=self._account['u1']['fund_product_name_for_redeem'],
                                   fund_convert_to=self._account['u1']['fund_product_name_for_fast_convert'],
                                   amount='100',
                                   trade_password=self._account['u1']['trade_password'])

    # 基金快速转换撤单
    @keyword('test_cancel_fund_fast_convert_order')
    def cancel_fund_fast_convert_order(self):
        self.xjb.cancel_fund_fast_convert_order(user_name=self._account['u1']['user_name'],
                                                login_password=self._account['u1']['login_password'],
                                                fund_convert_from=self._account['u1']['fund_product_name_for_redeem'],
                                                fund_convert_to=self._account['u1'][
                                                    'fund_product_name_for_fast_convert'],
                                                trade_password=self._account['u1']['trade_password'])

    # 基金分红方式切换
    @keyword('test_fund_dividend_type_switch')
    def fund_dividend_type_switch(self):
        self.xjb.fund_dividend_type_switch(user_name=self._account['u1']['user_name'],
                                           login_password=self._account['u1']['login_password'],
                                           fund_product_name=self._account['u1']['fund_product_name_for_redeem'])

    # 个人信息修改
    @keyword('test_modify_personal_information')
    def modify_personal_information(self):
        self.xjb.modify_personal_information(user_name=self._account['u1']['user_name'],
                                             login_password=self._account['u1']['login_password'],
                                             email='test@shhxzq.com', address='test')

    # 首次绑卡上传已有身份证图片，显示用户已注册。
    @keyword('test_bind_card_upload_id_info_negative')
    def bind_card_upload_id_info_negative(self):
        self.xjb.bind_card_upload_id_info_negative(login_password='a0000000', trade_password='135790',
                                                   user_name=self._account['u3']['user_name'])

    # 删除历史定投
    @keyword('test_delete_fund_history_plan')
    def delete_fund_history_plan(self):
        self.xjb.delete_fund_history_plan(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          fund_product_name=self._account['u1']['fund_product_name'],
                                          fund_product_code=self._account['u1']['non_money_fund_product_code'])

    # 实名用户重绑删除的卡（只有一张卡）
    @keyword('test_certificated_user_rebind_deleted_card')
    def certificated_user_rebind_deleted_card(self):
        self.xjb.certificated_user_rebind_deleted_card(user_name=self._account['u2']['user_name'],
                                                       login_password=self._account['u2']['login_password'],
                                                       bank_card_no='45635178090586794')

    # 实名用户没有绑定的储蓄卡，点击进入信用卡页面。
    @keyword('test_click_credit_card_without_bank_card_certificated_user')
    def click_credit_card_without_bank_card_certificated_user(self):
        self.xjb.click_credit_card_without_bank_card_certificated_user(user_name=self._account['u2']['user_name'],
                                                                       login_password=self._account['u2'][
                                                                           'login_password'])

    # 热门页查看全部产品
    @keyword('test_view_all_products')
    def view_all_products(self):
        self.xjb.view_all_products(user_name=self._account['u1']['user_name'],
                                   login_password=self._account['u1']['login_password'])

    # 热门全部产品页面筛选
    @keyword('test_all_products_filter')
    def all_products_filter(self):
        self.xjb.all_products_filter(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'])

    # 基金主题
    @keyword('test_view_fund_topics')
    def view_fund_topics(self):
        self.xjb.view_fund_topics()

    # 基金估值排行
    @keyword('test_view_fund_estimated_value_ranking')
    def view_fund_estimated_value_ranking(self):
        self.xjb.view_fund_estimated_value_ranking()

    # 基金估值排行
    @keyword('test_tax_dweller_identity_declaration')
    def tax_dweller_identity_declaration(self):
        self.xjb.tax_dweller_identity_declaration(user_name=self._account['u1']['user_name'],
                                                  login_password=self._account['u1']['login_password'])

    # 最佳表现基金和最高成交量
    @keyword('test_best_performance_highest_turnovers_fund')
    def best_performance_highest_turnovers_fund(self):
        self.xjb.best_performance_highest_turnovers_fund()

    # 更改登陆方式
    @keyword('test_change_sms_login_method')
    def change_sms_login_method(self):
        self.xjb.change_sms_login_method(user_name=self._account['u2']['user_name'],
                                         login_password=self._account['u2']['login_password'],
                                         trade_password=self._account['u2']['trade_password'])

    # 查看会员中心
    @keyword('test_view_member_center')
    def view_member_center(self):
        self.xjb.view_member_center(user_name=self._account['u1']['user_name'],
                                    login_password=self._account['u1']['login_password'])

    # 查看新发基金
    @keyword('test_view_newly_raised_funds')
    def view_newly_raised_funds(self):
        self.xjb.view_newly_raised_funds(product_name=self._account['u1']['fund_product_name_for_newly_raised_fund'])

    # 安全中心查看登录记录
    @keyword('test_security_center_view_login_record')
    def security_center_view_login_record(self):
        self.xjb.security_center_view_login_record(user_name=self._account['u1']['user_name'],
                                                   login_password=self._account['u1']['login_password'], )

    # 查看未实名用户账户信息
    @keyword('test_view_user_account_information')
    def view_user_account_information(self):
        self.xjb.view_user_account_information(user_name=self._account['u3']['user_name'],
                                               login_password=self._account['u3']['login_password'], )

    # 修改手机号码(不能接收短信)
    @keyword('test_modify_mobile_without_sms')
    def modify_mobile_without_sms(self):
        mobile_new = Utility.GetData().mobile()
        self.xjb.modify_mobile_without_sms(user_name=self._account['u1']['user_name_for_modify_mobile_without_sms'],
                                           login_password='a0000000', trade_password='135790', mobile_new=mobile_new)

    # 现金宝首页快取(金额小于最小值)
    @keyword('test_home_page_fast_withdraw_min')
    def home_page_fast_withdraw_min(self):
        self.xjb.home_page_fast_withdraw_negative(user_name=self._account['u1']['user_name'],
                                                  login_password=self._account['u1']['login_password'],
                                                  withdraw_amount='0',
                                                  trade_password=self._account['u1']['trade_password'])

    # 现金宝首页快取(金额大于最大值)
    @keyword('test_home_page_fast_withdraw_max')
    def home_page_fast_withdraw_max(self):
        self.xjb.home_page_fast_withdraw_negative(user_name=self._account['u1']['user_name'],
                                                  login_password=self._account['u1']['login_password'],
                                                  withdraw_amount='100000000000000000',
                                                  trade_password=self._account['u1']['trade_password'])

    # 首页现金宝普取(金额大于最大值)
    @keyword('test_home_page_regular_withdraw_max')
    def home_page_regular_withdraw_max(self):
        self.xjb.home_page_regular_withdraw_negative(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'],
                                                     withdraw_amount='100000000000000000',
                                                     trade_password=self._account['u1']['trade_password'])

    # 首页现金宝普取(金额小于最小值)
    @keyword('test_home_page_regular_withdraw_min')
    def home_page_regular_withdraw_min(self):
        self.xjb.home_page_regular_withdraw_negative(user_name=self._account['u1']['user_name'],
                                                     login_password=self._account['u1']['login_password'],
                                                     withdraw_amount='0',
                                                     trade_password=self._account['u1']['trade_password'])
