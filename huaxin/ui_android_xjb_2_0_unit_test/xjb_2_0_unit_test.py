# coding=utf-8
import time
from robot.api.deco import keyword

from _common.global_config import GlobalConfig
from _common.utility import Utility
from _tools.restful_xjb_tools import RestfulXjbTools
from _tools.ui_android_xjb_tools_2_0 import AndroidXjbTools20


class UiAndroidXjb20UnitTest:
    @keyword('Set Environemt Args')
    def set_environemt_args(self, app_path, platform_version, device_id, port, package_name, account, app_status):
        self.xjb = AndroidXjbTools20(app_path, platform_version, device_id, port, package_name, app_status, os='Android')
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
                                    trade_password=self._account['u1']['trade_password'])

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
        band_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]

        self.xjb.register_binding_card(phone_number=phone_number,
                                       login_password='a0000000',
                                       trade_password='135790',
                                       user_name=user_name,
                                       id_no=id_no,
                                       band_card_no=band_card_no)

    @keyword('test_bank_card_manage_binding_card')
    def bank_card_manage_binding_card(self):
        band_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password = RestfulXjbTools().new_user(user_name=phone_number,
                                                                              login_password='a0000000',
                                                                              card_bin='622202',
                                                                              trade_password='135790',
                                                                              recharge_amount='10000')

        self.xjb.bank_card_manage_binding_card(user_name=user_new,
                                               login_password=login_password,
                                               band_card_no=band_card_no,
                                               phone_number=user_new)

    @keyword('test_bank_card_manage_binding_nan_yue_card')
    def bank_card_manage_binding_nan_yue_card(self):
        band_card_no = Utility.GetData().bank_card_no(card_bin='623595').split('-')[0]
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password = RestfulXjbTools().new_user(user_name=phone_number,
                                                                              login_password='a0000000',
                                                                              card_bin='623595',
                                                                              trade_password='135790',
                                                                              recharge_amount='10000')

        self.xjb.bank_card_manage_binding_nan_yue_card(user_name=user_new,
                                                       login_password=login_password,
                                                       band_card_no=band_card_no,
                                                       phone_number=user_new)

    @keyword('test_delete_bank_card')
    def delete_bank_card(self):
        band_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password = RestfulXjbTools().new_user(user_name=phone_number,
                                                                              login_password='a0000000',
                                                                              card_bin='622202',
                                                                              trade_password='135790',
                                                                              recharge_amount='10000')
        self.xjb.delete_bank_card(user_name=user_new,
                                  login_password=login_password,
                                  trade_password=trade_password,
                                  last_card_no=band_card_no[-4:])

    @keyword('test_security_center_modify_mobile')
    def security_center_modify_mobile(self):
        phone_number = Utility.GetData().mobile()
        mobile_new = Utility.GetData().mobile()
        user_new, login_password, trade_password = RestfulXjbTools().new_user(user_name=phone_number,
                                                                              login_password='a0000000',
                                                                              card_bin='622202',
                                                                              trade_password='135790',
                                                                              recharge_amount='10000')

        self.xjb.security_center_modify_mobile(user_name=user_new,
                                               login_password=login_password,
                                               trade_password=trade_password,
                                               mobile_new=mobile_new)

    @keyword('test_security_center_modify_trade_password')
    def security_center_modify_trade_password(self):
        phone_number = Utility.GetData().mobile()
        user_new, login_password, trade_password = RestfulXjbTools().new_user(user_name=phone_number,
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
        user_new, login_password, trade_password = RestfulXjbTools().new_user(user_name=phone_number,
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

    @keyword('test_buy_high_end_product')
    def buy_high_end_product(self):
        self.xjb.buy_high_end_product(user_name=self._account['u1']['user_name'],
                                      login_password=self._account['u1']['login_password'],
                                      trade_password=self._account['u1']['trade_password'],
                                      product_name=self._account['u1']['high_end_product'],
                                      amount=self._account['u1']['high_end_product_amount'])

    @keyword('test_buy_dqb_product')
    def buy_dqb_product(self):
        self.xjb.buy_dqb_product(user_name=self._account['u1']['user_name'],
                                 login_password=self._account['u1']['login_password'],
                                 product_name=self._account['u1']['dqb_product'],
                                 amount=self._account['u1']['dqb_product_amount'],
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

    @keyword('test_view_high_end_history_product')
    def view_high_end_history_product(self):
        self.xjb.view_high_end_history_product(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'])

    @keyword('test_redeem_high_end_product')
    def redeem_high_end_product(self):
        self.xjb.redeem_high_end_product(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         redeem_amount=self._account['u1']['high_end_product_amount'],
                                         trade_password=self._account['u1']['trade_password'],
                                         high_end_product=self._account['u1']['high_end_product'])

    @keyword('test_redeem_dqb_product')
    def redeem_dqb_product(self):
        self.xjb.redeem_dqb_product(user_name=self._account['u1']['user_name'],
                                    login_password=self._account['u1']['login_password'],
                                    redeem_amount=self._account['u1']['dqb_product_amount_2'],
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
        user_new, login_password, trade_password = RestfulXjbTools().new_user(user_name=phone_number,
                                                                              login_password='a0000000',
                                                                              card_bin='622202',
                                                                              trade_password='135790',
                                                                              recharge_amount='10000')
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

    @keyword('test_buy_fund_product')
    def buy_fund_product(self):
        self.xjb.buy_fund_product(user_name=self._account['u1']['user_name'],
                                  login_password=self._account['u1']['login_password'],
                                  fund_product_name=self._account['u1']['fund_product_name'],
                                  amount=self._account['u1']['fund_product_amount'],
                                  trade_password=self._account['u1']['trade_password'],
                                  fund_product_code=self._account['u1']['fund_product_code'],
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
                                       buy_count= self._account['u1']['reservation_code_buy_count'],
                                       reserve_quota=self._account['u1']['reservation_code_reserve_quota'],
                                       reserve_count= self._account['u1']['reservation_code_reserve_count'],
                                       reserve_code=self._account['u1']['reserve_code'],
                                       product_id= self._account['u1']['product_id_for_reservation_code']
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

    @keyword('test_redeem_fund_product')
    def redeem_fund_product(self):
        self.xjb.redeem_fund_product(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'],
                                     fund_product=self._account['u1']['fund_product_name'],
                                     amount=self._account['u1']['fund_product_amount'],
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
                                   trade_password=self._account['u1']['trade_password'])

    # 信用卡预约还款
    @keyword('test_credit_card_reserved_pay')
    def credit_card_reserved_pay(self):
        self.xjb.credit_card_reserved_pay(user_name=self._account['u1']['user_name'],
                                          login_password=self._account['u1']['login_password'],
                                          reserved_pay_amount=self._account['u1']['credit_card_reserved_pay_amount'],
                                          trade_password=self._account['u1']['trade_password'])

    # 取消预约还款
    @keyword('test_cancel_reserved_pay')
    def cancel_reserved_pay(self):
        self.xjb.cancel_reserved_pay(user_name=self._account['u1']['user_name'],
                                     login_password=self._account['u1']['login_password'])

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
                                                                 product_name=self._account['u1']['high_end_product_for_points'],
                                                                 amount=self._account['u1']['high_end_product_amount'])

    # 花积分--买定期产品
    @keyword('test_spend_points_by_buy_dqb')
    def spend_points_by_buy_dqb(self):
        self.xjb.spend_points_by_buy_dqb(user_name=self._account['u1']['user_name'],
                                         login_password=self._account['u1']['login_password'],
                                         trade_password=self._account['u1']['trade_password'],
                                         dqb_product=self._account['u1']['dqb_product_3'],
                                         dqb_product_amount=self._account['u1']['dqb_product_amount'])

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
                                          high_end_product_for_fast_redeem=self._account['u1']['high_end_product_for_fast_redeem'])

    # 高端极速卖出
    @keyword('test_fast_redeem_vipproduct')
    def fast_redeem_vipproduct(self):
        self.xjb.fast_redeem_vipproduct(user_name=self._account['u1']['user_name'],
                                        login_password=self._account['u1']['login_password'],
                                        redeem_amount=self._account['u1']['high_end_product_amount'],
                                        trade_password=self._account['u1']['trade_password'],
                                        high_end_product_for_fast_redeem=self._account['u1']['high_end_product_for_fast_redeem'])

    # 基金普通卖出
    @keyword('test_normal_redeem_fund_product')
    def normal_redeem_fund_product(self):
        self.xjb.normal_redeem_fund_product(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            redeem_amount=self._account['u1']['fund_product_amount'],
                                            trade_password=self._account['u1']['trade_password'],
                                            fund_product_name_for_fast_redeem=self._account['u1']['fund_product_name_for_fast_redeem'])

    # 基金极速卖出
    @keyword('test_fast_redeem_fund_product')
    def fast_redeem_fund_product(self):
        self.xjb.fast_redeem_fund_product(user_name=self._account['u1']['user_name'],
                                            login_password=self._account['u1']['login_password'],
                                            redeem_amount=self._account['u1']['fund_product_amount'],
                                            trade_password=self._account['u1']['trade_password'],
                                            fund_product_name_for_fast_redeem=self._account['u1']['fund_product_name_for_fast_redeem']
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
                                               amount=self._account['u1']['dqb_product_amount'],
                                               trade_password=self._account['u1']['trade_password'],
                                               product_name=self._account['u1']['dqb_product_for_coupon']
                                               )

    # 购买定期宝使用优惠券(可叠加)
    @keyword('test_buy_dqb_use_superposed_coupon')
    def buy_dqb_use_superposed_coupon(self):
        self.xjb.buy_dqb_use_superposed_coupon(user_name=self._account['u1']['user_name'],
                                                  login_password=self._account['u1']['login_password'],
                                                  amount=self._account['u1']['dqb_product_amount'],
                                                  trade_password=self._account['u1']['trade_password'],
                                                  product_name=self._account['u1']['dqb_product_for_coupon']
                                                  )

    # 购买高端使用优惠券(不可叠加)
    @keyword('test_buy_vipproduct_use_nonsuperposed_coupon')
    def buy_vipproduct_use_nonsuperposed_coupon(self):
        self.xjb.buy_vipproduct_use_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                               login_password=self._account['u1']['login_password'],
                                               amount=self._account['u1']['high_end_product_amount'],
                                               trade_password=self._account['u1']['trade_password'],
                                               product_name=self._account['u1']['high_end_product_for_points']
                                               )

    # 购买高端使用优惠券(可叠加)
    @keyword('test_buy_vipproduct_use_superposed_coupon')
    def buy_vipproduct_use_superposed_coupon(self):
        self.xjb.buy_vipproduct_use_superposed_coupon(user_name=self._account['u1']['user_name'],
                                                         login_password=self._account['u1']['login_password'],
                                                         amount=self._account['u1']['high_end_product_amount'],
                                                         trade_password=self._account['u1']['trade_password'],
                                                         product_name=self._account['u1']['high_end_product_for_points']
                                                         )

    # 购买基金使用优惠券(不可叠加)
    @keyword('test_buy_fund_use_nonsuperposed_coupon')
    def buy_fund_use_nonsuperposed_coupon(self):
        self.xjb.buy_fund_use_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                  login_password=self._account['u1']['login_password'],
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
                                                  amount=self._account['u1']['dqb_product_amount'],
                                                  trade_password=self._account['u1']['trade_password'],
                                                  product_name=self._account['u1']['dqb_product_for_coupon']
                                                  )

    # 购买定期宝使用积分+优惠券(可叠加)
    @keyword('test_buy_dqb_use_points_and_superposed_coupon')
    def buy_dqb_use_points_and_superposed_coupon(self):
        self.xjb.buy_dqb_use_points_and_superposed_coupon(user_name=self._account['u1']['user_name'],
                                                             login_password=self._account['u1']['login_password'],
                                                             amount=self._account['u1']['dqb_product_amount'],
                                                             trade_password=self._account['u1']['trade_password'],
                                                             product_name=self._account['u1']['dqb_product_for_coupon']
                                                             )

    # 购买高端使用积分+优惠券(不可叠加)
    @keyword('test_buy_vipproduct_use_points_and_nonsuperposed_coupon')
    def buy_vipproduct_use_points_and_nonsuperposed_coupon(self):
        self.xjb.buy_vipproduct_use_points_and_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                         login_password=self._account['u1']['login_password'],
                                                         amount=self._account['u1']['high_end_product_amount'],
                                                         trade_password=self._account['u1']['trade_password'],
                                                         product_name=self._account['u1']['high_end_product_for_points']
                                                         )

    # 购买高端使用积分+优惠券(可叠加)
    @keyword('test_buy_vipproduct_use_points_and_superposed_coupon')
    def buy_vipproduct_use_points_and_superposed_coupon(self):
        self.xjb.buy_vipproduct_use_points_and_superposed_coupon(user_name=self._account['u1']['user_name'],
                                                         login_password=self._account['u1']['login_password'],
                                                         amount=self._account['u1']['high_end_product_amount'],
                                                         trade_password=self._account['u1']['trade_password'],
                                                         product_name=self._account['u1']['high_end_product_for_points']
                                                         )

    # 购买基金使用积分+优惠券(不可叠加)
    @keyword('test_buy_fund_use_points_and_nonsuperposed_coupon')
    def buy_fund_use_points_and_nonsuperposed_coupon(self):
        self.xjb.buy_fund_use_points_and_nonsuperposed_coupon(user_name=self._account['u1']['user_name'],
                                                      login_password=self._account['u1']['login_password'],
                                                      fund_product_name=self._account['u1']['fund_product_name'],
                                                      amount=self._account['u1']['fund_product_amount'],
                                                      trade_password=self._account['u1']['trade_password'],
                                                      fund_product_code=self._account['u1']['fund_product_code']
                                                      )

    # 购买基金使用积分+优惠券(可叠加)
    @keyword('test_buy_fund_use_points_and_superposed_coupon')
    def buy_fund_use_points_and_superposed_coupon(self):
        self.xjb.buy_fund_use_points_and_superposed_coupon(user_name=self._account['u1']['user_name'],
                                                           login_password=self._account['u1']['login_password'],
                                                           fund_product_name=self._account['u1']['fund_product_name'],
                                                           amount=self._account['u1']['fund_product_amount'],
                                                           trade_password=self._account['u1']['trade_password'],
                                                           fund_product_code=self._account['u1']['fund_product_code']
                                                           )



