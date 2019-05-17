# coding=utf-8
from selenium.common.exceptions import NoSuchElementException

from _common.app_compatibility_install import AppCompatibilityInstall
from _common.global_config import GlobalConfig
from _common.global_controller import GlobalController
from _common.ios_deploy import IosDeploy
from _common.utility import Utility
from _common.web_driver import WebDriver
from _tools.mysql_xjb_tools import MysqlXjbTools
from _tools.restful_xjb_tools import RestfulXjbTools
from huaxin_ui.ui_ios_xjb_2_0.main_page import MainPage
from _common.data_base import DataBase


class IOSXjbTools20(object):
    def __init__(self, app_path, platform_version, device_id, port, package_name, app_status, os):
        self._db = MysqlXjbTools()
        self._rt = RestfulXjbTools()
        self.app_status = app_status

        AppCompatibilityInstall().app_install_handle(device_id=device_id, app_path=app_path, package_name=package_name,
                                                     app_status=app_status, os=os)

        self.web_driver = WebDriver.Appium().open_ios_app(app_path, platform_version, device_id, port, package_name)
        self.main_page = MainPage(self.web_driver)

        AppCompatibilityInstall().after_launch_handle(device_id=device_id, os=os, web_driver=self.web_driver)

    def old_user(self, user_name, login_password):
        if self.app_status == 'Y':
            self.main_page.go_to_home_page_()
            self.main_page.go_to_login_page()
            self.main_page.login(user_name, login_password, 'HomePage')
        else:
            self.main_page.go_to_home_page()
            self.main_page.go_to_login_page()
            self.main_page.login(user_name, login_password, 'HomePage')

    def home_page_recharge(self, user_name, login_password, recharge_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_recharge_page()
        self.main_page.recharge(recharge_amount=recharge_amount, trade_password=trade_password)

    def home_page_regular_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_withdraw_page()
        self.main_page.regular_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password)

    def home_page_fast_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_withdraw_page()
        self.main_page.fast_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password)

    def home_page_view_essence_recommend_list(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_essence_recommend_page()
        self.main_page.view_essence_recommend_list()

    def register(self, phone_number, login_password):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.go_to_register_page()
        self.main_page.register(phone_number=phone_number, login_password=login_password)

    def register_binding_card(self, phone_number, login_password, trade_password, user_name, id_no, band_card_no):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.go_to_register_page()
        self.main_page.register_binding_card(phone_number=phone_number, login_password=login_password,
                                             trade_password=trade_password)
        self.main_page.binding_card(user_name=user_name, id_no=id_no,
                                    band_card_no=band_card_no,
                                    phone_number=phone_number)

    def bank_card_manage_binding_card(self, user_name, login_password, band_card_no, phone_number):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_bank_card_management_page()
        self.main_page.binding_card(band_card_no=band_card_no, phone_number=phone_number)

    def bank_card_manage_binding_nan_yue_card(self, user_name, login_password, band_card_no, phone_number):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_bank_card_management_page()
        self.main_page.binding_card(band_card_no=band_card_no, phone_number=phone_number)

    def delete_bank_card(self, user_name, login_password, trade_password, last_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_bank_card_management_page()
        self.main_page.delete_band_card(trade_password=trade_password, last_card_no=last_card_no)

    def security_center_modify_mobile(self, user_name, login_password, trade_password, mobile_new):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_center_page()
        self.main_page.go_to_security_center_page()
        self.main_page.go_to_setting_modify_mobile_page()
        self.main_page.modify_mobile(mobile_old=user_name, trade_password=trade_password, mobile_new=mobile_new)

    def security_center_modify_trade_password(self, user_name, login_password, trade_password_old, trade_password_new):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_center_page()
        self.main_page.go_to_security_center_page()
        self.main_page.go_to_setting_trade_password_page()
        self.main_page.modify_trade_password(trade_password_old=trade_password_old,
                                             trade_password_new=trade_password_new)

    def security_center_modify_login_password(self, user_name, login_password, login_password_new):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_center_page()
        self.main_page.go_to_security_center_page()
        self.main_page.go_to_setting_login_password_page()
        self.main_page.modify_login_password(login_password_old=login_password, login_password_new=login_password_new)

    def security_center_find_trade_password(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_center_page()
        self.main_page.go_to_security_center_page()
        self.main_page.go_to_setting_trade_password_page()
        self.main_page.find_trade_password()

    def buy_high_end_product(self, user_name, login_password, trade_password, product_name, amount):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password)

    def buy_dqb_product(self, user_name, login_password, product_name, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_dqb_product_list_page()
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       mobile=user_name)

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

    def finance_product_search_with_full_name(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name)

    def finance_product_search_with_short_name(self, user_name, login_password, product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.finance_product_search(product_name=product_name)

    def assets_xjb_detail_page_recharge(self, user_name, login_password, recharge_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_recharge_page()
        self.main_page.recharge(recharge_amount=recharge_amount, trade_password=trade_password,
                                return_page='AssetsXjbDetailPage')

    def assets_xjb_detail_page_regular_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_withdraw_page()
        self.main_page.regular_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password,
                                        return_page='AssetsPage')

    def assets_xjb_detail_page_fast_withdraw(self, user_name, login_password, withdraw_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_xjb_detail_page()
        self.main_page.go_to_withdraw_page()
        self.main_page.fast_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password,
                                     return_page='AssetsPage')

    def delete_credit_card(self, user_name, login_password, last_card_no, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.delete_credit_card(last_card_no=last_card_no, trade_password=trade_password)

    def add_credit_card(self, user_name, login_password, credit_card_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.add_credit_card(credit_card_no=credit_card_no, phone_no=user_name)

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
        self.main_page.view_trade_detail()

    def view_dqb_more_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.view_dqb_more_product()

    def view_dqb_history_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_dqb_detail_page()
        self.main_page.view_dqb_history_product()

    def fund_detail_page_view_trade_detail(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.view_trade_detail()

    def view_fund_more_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.go_to_fund_more_product_page()
        self.main_page.view_fund_more_product()

    def high_end_detail_page_view_trade_detail(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.go_to_trade_detail_page()
        self.main_page.view_trade_detail()

    def view_high_end_more_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_more_product()

    def view_high_end_history_product(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.view_high_end_history_product()

    def redeem_high_end_product(self, user_name, login_password, redeem_amount, trade_password, high_end_product):
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

    def my_referee(self, user_name, login_password, phone_no):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_center_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.my_referee(phone_no=phone_no)

    def risk_evaluating_new_user(self, user_name, login_password):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.login(user_name, login_password, 'HomePage')
        self.main_page.go_to_personal_center_page()
        self.main_page.go_to_personal_setting_page()
        self.main_page.risk_evaluating()

    def fund_product_search_with_name(self, user_name, login_password, fund_product_name):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_product_search_with_name(fund_product_name=fund_product_name)

    def fund_product_search_with_code(self, user_name, login_password, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_product_search_with_code(fund_product_code=fund_product_code)

    def buy_fund_product(self, user_name, login_password, fund_product_name, amount, trade_password, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_detail_page(fund_product_name=fund_product_name, fund_product_code=fund_product_code)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password)

    def invite_friend(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_center_page()
        self.main_page.go_to_invite_friend_page()

    # 使用其他预约码
    def use_other_reservation_code(self, user_name, login_password, reservation_code, trade_password, buy_quota,
                                   buy_count, reserve_quota, reserve_count, product_id):
        self._db.reservation_code_status_modify(buy_quota=buy_quota, buy_count=buy_count,
                                                reserve_quota=reserve_quota,
                                                reserve_count=reserve_count, mobile=user_name,
                                                reserve_code=reservation_code,
                                                product_id=product_id)

        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_center_page()
        self.main_page.go_to_reservation_code_page()
        self.main_page.use_other_reservation_code(reserve_code=reservation_code, trade_password=trade_password,
                                                  amount=reserve_quota, mobile=user_name)

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
        self.main_page.go_to_personal_center_page()
        self.main_page.go_to_reservation_code_page()
        self.main_page.use_other_reservation_code(reserve_code=reservation_code, trade_password=trade_password,
                                                  amount=reserve_quota, mobile=user_name)

    # 预约码--使用自己的预约码
    def use_reservation_code(self, user_name, login_password, trade_password, buy_quota, buy_count, reserve_quota,
                             reserve_count, reservation_code, product_id):
        self._db.reservation_code_status_modify(buy_quota=buy_quota, buy_count=buy_count,
                                                reserve_quota=reserve_quota,
                                                reserve_count=reserve_count, mobile=user_name,
                                                reserve_code=reservation_code,
                                                product_id=product_id)

        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_personal_center_page()
        self.main_page.go_to_reservation_code_page()
        self.main_page.use_reservation_code(trade_password=trade_password, amount=reserve_quota, mobile=user_name)

    def redeem_fund_product(self, user_name, login_password, amount, trade_password, fund_product_name_for_redeem):
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
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password)

    # 赚积分--推荐用户注册绑卡
    def earn_points_by_recommend_user_register(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.earn_points_by_recommend_user_register()

    # 信用卡还款
    def credit_card_repay(self, user_name, login_password, repay_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.repay(repay_amount, trade_password)

    # 信用卡预约还款
    def credit_card_reserved_pay(self, user_name, login_password, reserved_pay_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_credit_card_repay_page()
        self.main_page.go_to_reserved_pay_page()
        self.main_page.reserved_pay(reserved_pay_amount, trade_password)

    # 取消预约还款
    def cancel_reserved_pay(self, user_name, login_password):
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

    # 花积分--买基金
    def spend_points_by_buy_fund(self, user_name, login_password, amount, trade_password, fund_product_name,
                                 fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.spend_points_by_buy_fund(fund_product_name=fund_product_name,
                                                fund_product_code=fund_product_code)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, points='Y')

    # 花积分--买高端产品
    def spend_points_by_buy_vipproduct_use_product_name(self, user_name, login_password, product_name, amount,
                                                        trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_my_points_page()
        self.main_page.spend_points_by_buy_vipproduct_use_product_name()
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            points='Y')

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

    # 高端急速卖出
    def fast_redeem_vipproduct(self, user_name, login_password, redeem_amount, trade_password,
                               high_end_product_for_fast_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_high_end_detail_page()
        self.main_page.fast_redeem_vipproduct(redeem_amount=redeem_amount, trade_password=trade_password,
                                              high_end_product_for_fast_redeem=high_end_product_for_fast_redeem)

    # 基金普通卖出
    def normal_redeem_fund_product(self, user_name, login_password, redeem_amount, trade_password,
                                   fund_product_name_for_fast_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.normal_redeem_fund_product(fund_product_name_for_fast_redeem=fund_product_name_for_fast_redeem,
                                                  redeem_amount=redeem_amount, trade_password=trade_password)

    # 基金极速卖出
    def fast_redeem_fund_product(self, user_name, login_password, redeem_amount, trade_password,
                                 fund_product_name_for_fast_redeem):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_fund_detail_page()
        self.main_page.fast_redeem_fund_product(fund_product_name_for_fast_redeem=fund_product_name_for_fast_redeem,
                                                redeem_amount=redeem_amount, trade_password=trade_password)

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
        self.main_page.fund_market_index(csi_index=csi_index)

    # 基金频道--全部基金
    def fund_all_funds(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_all_funds()

    # 基金频道--评级排行
    def fund_rating_and_ranking(self, user_name, login_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_rating_and_ranking()

    # 基金频道--自选基金
    def fund_selected_funds(self, user_name, login_password, fund_product_name, fund_product_code, fund_product_name_2,
                            fund_company):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_selected_funds(fund_product_name=fund_product_name, fund_product_code=fund_product_code,
                                           fund_product_name_2=fund_product_name_2,
                                           fund_company=fund_company)

    # 基金频道--对比分析
    def fund_comparasion_and_analysis(self, user_name, login_password, fund_product_code, fund_product_code_2):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.fund_comparasion_and_analysis(fund_product_code=fund_product_code,
                                                     fund_product_code_2=fund_product_code_2)

    # 购买定期宝使用优惠券(不可叠加)
    def buy_dqb_use_nonsuperposed_coupon(self, user_name, login_password, product_name, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_dqb_product_list_page()
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       mobile=user_name, nonsuperposed_coupon='Y')

    # 购买定期宝使用优惠券(可叠加)
    def buy_dqb_use_superposed_coupon(self, user_name, login_password, product_name, amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_dqb_product_list_page()
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       mobile=user_name, superposed_coupon='Y')

    # 购买高端使用优惠券(不可叠加)
    def buy_vipproduct_use_nonsuperposed_coupon(self, user_name, login_password, product_name, amount,
                                                trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            nonsuperposed_coupon='Y')

    # 购买高端使用优惠券(可叠加)
    def buy_vipproduct_use_superposed_coupon(self, user_name, login_password, product_name, amount,
                                             trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_high_end_product_list_page()
        self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                            superposed_coupon='Y')

    # 购买基金使用优惠券(不可叠加)
    def buy_fund_use_nonsuperposed_coupon(self, user_name, login_password, fund_product_name, amount,
                                          trade_password, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_detail_page(fund_product_name=fund_product_name,
                                              fund_product_code=fund_product_code)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, nonsuperposed_coupon='Y')

    # 购买基金使用优惠券(可叠加)
    def buy_fund_use_superposed_coupon(self, user_name, login_password, fund_product_name, amount, trade_password,
                                       fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_detail_page(fund_product_name=fund_product_name,
                                              fund_product_code=fund_product_code)
        self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, superposed_coupon='Y')

    # 购买定期宝使用积分+优惠券(不可叠加)
    def buy_dqb_use_points_and_nonsuperposed_coupon(self, user_name, login_password, product_name, amount,
                                                    trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_finance_page()
        self.main_page.go_to_dqb_product_list_page()
        self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
                                       mobile=user_name, points='Y', nonsuperposed_coupon='Y')
    #
    # # 购买定期宝使用积分+优惠券(可叠加)
    # def buy_dqb_use_points_and_superposed_coupon(self, user_name, login_password, product_name, amount,
    #                                              trade_password):
    #     self.old_user(user_name=user_name, login_password=login_password)
    #     self.main_page.go_to_finance_page()
    #     self.main_page.go_to_dqb_product_list_page()
    #     self.main_page.buy_dqb_product(product_name=product_name, amount=amount, trade_password=trade_password,
    #                                    points='Y', superposed_coupon='Y')
    #
    # # 购买高端使用积分+优惠券(不可叠加)
    # def buy_vipproduct_use_points_and_nonsuperposed_coupon(self, user_name, login_password, product_name, amount,
    #                                                        trade_password):
    #     self.old_user(user_name=user_name, login_password=login_password)
    #     selfmain_page.go_to_finance_page()
    #     self.main_page.go_to_high_end_product_list_page()
    #     self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
    #                                         points='Y', nonsuperposed_coupon='Y')
    #
    # # 购买高端使用积分+优惠券(可叠加)
    # def buy_vipproduct_use_points_and_superposed_coupon(self, user_name, login_password, product_name, amount,
    #                                                     trade_password):
    #     self.old_user(user_name=user_name, login_password=login_password)
    #     self.main_page.go_to_finance_page()
    #     self.main_page.go_to_high_end_product_list_page()
    #     self.main_page.buy_high_end_product(product_name=product_name, amount=amount, trade_password=trade_password,
    #                                         points='Y', superposed_coupon='Y')
    #
    # # 购买基金使用积分+优惠券(不可叠加)
    # def buy_fund_use_points_and_nonsuperposed_coupon(self, user_name, login_password, fund_product_name, amount,
    #                                                  trade_password, fund_product_code):
    #     self.old_user(user_name=user_name, login_password=login_password)
    #     self.main_page.go_to_fund_page()
    #     self.main_page.go_to_fund_detail_page(fund_product_name=fund_product_name,
    #                                           fund_product_code=fund_product_code)
    #     self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, points='Y',
    #                                     nonsuperposed_coupon='Y')
    #
    # # 购买基金使用积分+优惠券(可叠加)
    # def buy_fund_use_points_and_superposed_coupon(self, user_name, login_password, fund_product_name, amount,
    #                                               trade_password,
    #                                               fund_product_code):
    #     self.old_user(user_name=user_name, login_password=login_password)
    #     self.main_page.go_to_fund_page()
    #     self.main_page.go_to_fund_detail_page(fund_product_name=fund_product_name,
    #                                           fund_product_code=fund_product_code)
    #     self.main_page.buy_fund_product(amount=amount, trade_password=trade_password, points='Y',
    #                                     superposed_coupon='Y')

    # 基金定投
    def fund_plan(self, user_name, login_password, fund_product_name, amount, trade_password, fund_product_code):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_fund_page()
        self.main_page.go_to_fund_detail_page(fund_product_name=fund_product_name,
                                              fund_product_code=fund_product_code)
        self.main_page.go_to_fund_plan_page()
        self.main_page.fund_plan_detail(amount=amount, trade_password=trade_password)

    # 随心借
    def vipproduct_pledge(self, user_name, login_password, product_name, pledge_amount, trade_password):
        self.old_user(user_name=user_name, login_password=login_password)
        self.main_page.go_to_assets_page()
        self.main_page.go_to_pledge_detail_page(product_name=product_name)
        self.main_page.pledge_detail(pledge_amount=pledge_amount, trade_password=trade_password)


if __name__ == '__main__':
    phone_number = Utility.GetData().mobile()
    mobile_new = Utility.GetData().mobile()
    user_name = Utility.GetData().english_name()
    id_no = Utility.GetData().id_no()
    band_card_no = Utility.GetData().bank_card_no(card_bin='622202').split('-')[0]
    band_card_no_nan_yue = Utility.GetData().bank_card_no(card_bin='623595').split('-')[0]
    # user_new, login_password, trade_password = RestfulXjbTools().new_user(user_name=phone_number,
    #                                                                       login_password='a0000000',
    #                                                                       card_bin='622202',
    #                                                                       trade_password='135790',
    #                                                                       recharge_amount='10000')
    # app_path = GlobalController.XJB_CONNECT
    # app_path = GlobalConfig.XjbApp.Xjb_App_2_0_IOS_UAT
    app_path = '/Users/linkinpark/xjb/build/DerivedData/Build/Products/Debug-iphoneos/HXXjb.app'
    platform_version = '9.3'
    device_id = '56a36d750ab8d2c6e5b73365099bdbf7bc05d9d2'
    # device_id = 'd90b21dc9cc8a80ddc28c40f8eae5efb9500a2bd'
    # package_name = 'com.shhxzq.xjb'
    port = '4723'
    package_name = 'com.shhxzq.xjbDev'
    m = IOSXjbTools20(app_path=app_path, platform_version=platform_version, device_id=device_id, port=port,
                      package_name=package_name, app_status='Y', os='IOS')
    # user = GlobalConfig.XjbAccountInfo.XJB_CI_USER_1
    user = GlobalConfig.XjbAccountInfo.XJB_UAT_USER_1

    m.home_page_recharge(user_name=user['u1']['user_name'],
                         login_password=user['u1']['login_password'],
                         recharge_amount='100',
                         trade_password=user['u1']['trade_password'])
    # m.home_page_regular_withdraw(user_name=user['u1']['user_name'],
    #                              login_password=user['u1']['login_password'],
    #                              withdraw_amount='0.1',
    #                              trade_password=user['u1']['trade_password'])
    # m.home_page_fast_withdraw(user_name=user['u1']['user_name'],
    #                           login_password=user['u1']['login_password'],
    #                           withdraw_amount='0.1',
    #                           trade_password=user['u1']['trade_password'])
    # m.home_page_view_essence_recommend_list(user_name=user['u1']['user_name'],
    #                                         login_password=user['u1']['login_password'])
    # m.register(phone_number=phone_number, login_password='a0000000')
    # m.register_binding_card(phone_number=phone_number, login_password='a0000000', trade_password='135790',
    #                         user_name=user_name, id_no=id_no, band_card_no=str(band_card_no))
    # m.bank_card_manage_binding_card(user_name=user_new,
    #                                 login_password=login_password,
    #                                 band_card_no=band_card_no,
    #                                 phone_number=user_new)
    # m.bank_card_manage_binding_nan_yue_card(user_name=user_new,
    #                                         login_password=login_password,
    #                                         band_card_no=band_card_no_nan_yue,
    #                                         phone_number=user_new)
    # m.delete_bank_card(user_name=user_new,
    #                    login_password=login_password,
    #                    trade_password=trade_password, last_card_no=band_card_no[-4:])
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
    # m.buy_high_end_product(user_name=user['u1']['user_name'],
    #                        login_password=user['u1']['login_password'],
    #                        trade_password=user['u1']['trade_password'],
    #                        product_name=user['u1']['high_end_product'],
    #                        amount=user['u1']['high_end_product_amount'])
    # m.buy_dqb_product(user_name=user['u1']['user_name'],
    #                   login_password=user['u1']['login_password'],
    #                   product_name=user['u1']['dqb_product'],
    #                   amount=user['u1']['dqb_product_amount'],
    #                   trade_password=user['u1']['trade_password'])

    # m.hot_switch_to_dqb_product_list_page(user_name=user['u1']['user_name'],
    #                                       login_password=user['u1']['login_password'])
    # m.hot_switch_to_high_end_product_list_page(user_name=user['u1']['user_name'],
    #                                            login_password=user['u1']['login_password'])
    # m.finance_product_search_with_full_name(user_name=user['u1']['user_name'],
    #                                         login_password=user['u1']['login_password'],
    #                                         product_name=user['u1']['search_with_full_name'])
    # m.finance_product_search_with_short_name(user_name=user['u1']['user_name'],
    #                                          login_password=user['u1']['login_password'],
    #                                          product_name=user['u1']['search_with_short_name'])
    # m.assets_xjb_detail_page_recharge(user_name=user['u1']['user_name'],
    #                                   login_password=user['u1']['login_password'],
    #                                   recharge_amount='100',
    #                                   trade_password=user['u1']['trade_password'])
    # m.assets_xjb_detail_page_regular_withdraw(user_name=user['u1']['user_name'],
    #                                           login_password=user['u1']['login_password'],
    #                                           withdraw_amount='0.1',
    #                                           trade_password=user['u1']['trade_password'])
    # m.assets_xjb_detail_page_fast_withdraw(user_name=user['u1']['user_name'],
    #                                        login_password=user['u1']['login_password'],
    #                                        withdraw_amount='0.1',
    #                                        trade_password=user['u1']['trade_password'])

    # m.add_credit_card(user_name=user['u1']['user_name'],
    #                   login_password=user['u1']['login_password'],
    #                   credit_card_no=user['u1']['credit_card_no'])
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
    # m.fund_detail_page_view_trade_detail(user_name=user['u1']['user_name'],
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
    # m.view_high_end_history_product(user_name=user['u1']['user_name'],
    #                                 login_password=user['u1']['login_password'])
    # m.redeem_high_end_product(user_name=user['u1']['user_name'],
    #                           login_password=user['u1']['login_password'],
    #                           redeem_amount=user['u1']['high_end_product_amount'],
    #                           trade_password=user['u1']['trade_password'],
    #                           high_end_product=user['u1']['high_end_product'])
    # m.redeem_dqb_product(user_name=user['u1']['user_name'],
    #                      login_password=user['u1']['login_password'],
    #                      redeem_amount=user['u1']['dqb_product_amount_2'],
    #                      trade_password=user['u1']['trade_password'],
    #                      dqb_product=user['u1']['dqb_product_2'])
    # m.my_referee(user_name=user['u1']['user_name'],
    #              login_password=user['u1']['login_password'],
    #              phone_no=user['u2']['user_name'])
    # m.risk_evaluating_new_user(user_name=user_new,
    #                            login_password=login_password)
    # m.fund_product_search_with_name(user_name=user['u1']['user_name'],
    #                                 login_password=user['u1']['login_password'],
    #                                 fund_product_name=user['u1']['fund_product_name'])
    # m.fund_product_search_with_code(user_name=user['u1']['user_name'],
    #                                 login_password=user['u1']['login_password'],
    #                                 fund_product_code=user['u1']['fund_product_code'])
    # m.buy_fund_product(user_name=user['u1']['user_name'],
    #                    login_password=user['u1']['login_password'],
    #                    fund_product_name=user['u1']['fund_product_name'],
    #                    amount=user['u1']['fund_product_amount'],
    #                    trade_password=user['u1']['trade_password'],
    #                    fund_product_code=user['u1']['fund_product_code'])
    # m.invite_friend(user_name=user['u1']['user_name'],
    #                 login_password=user['u1']['login_password'])

    # 预约码--使用其他预约码
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

    # 预约码--用户未绑定预约码, 使用其他预约码
    # m.use_other_reservation_code_without_reservation_code(user_name=user['u1']['user_name_for_reservation_code'],
    #                                                       login_password=user['u1'][
    #                                                           'login_password_for_reservation_code'],
    #                                                       reservation_code=user['u1']['reserve_code'],
    #                                                       trade_password=user['u1'][
    #                                                           'trade_password_for_reservation_code'],
    #                                                       buy_quota=user['u1']['reservation_code_buy_quota'],
    #                                                       buy_count=user['u1']['reservation_code_buy_count'],
    #                                                       reserve_quota=user['u1']['reservation_code_reserve_quota'],
    #                                                       reserve_count=user['u1']['reservation_code_reserve_count'],
    #                                                       product_id=user['u1']['product_id_for_reservation_code'],
    #                                                       user_name_have_reservation_code=user['u1']['user_name'],
    #                                                       )


    # m.redeem_fund_product(user_name=user['u1']['user_name'],
    #                       login_password=user['u1']['login_password'],
    #                       amount=user['u1']['fund_product_amount'],
    #                       trade_password=user['u1']['trade_password'],
    #                       fund_product_name_for_redeem=user['u1']['fund_product_name_for_redeem'],)

    # 预约码--使用自己的预约码
    # m.use_reservation_code(user_name=user['u1']['user_name'],
    #                        login_password=user['u1']['login_password'],
    #                        trade_password=user['u1']['trade_password'],
    #                        buy_quota=user['u1']['reservation_code_buy_quota'],
    #                        buy_count=user['u1']['reservation_code_buy_count'],
    #                        reserve_quota=user['u1']['reservation_code_reserve_quota'],
    #                        reserve_count=user['u1']['reservation_code_reserve_count'],
    #                        reservation_code=user['u1']['reserve_code'],
    #                        product_id=user['u1']['product_id_for_reservation_code']
    #                       )

    # m.earn_points(user_name=user['u1']['user_name'],
    #               login_password=user['u1']['login_password'],
    #               amount=user['u1']['fund_product_amount'],
    #               trade_password=user['u1']['trade_password'],
    #               fund_product_name=user['u1']['fund_product_name'],
    #               fund_product_code=user['u1']['fund_product_code'],
    #               )

    # 信用卡还款
    # m.credit_card_repay(user['u1']['user_name'],
    #                     login_password=user['u1']['login_password'],
    #                     repay_amount=user['u1']['credit_card_repay_amount'],
    #                     trade_password=user['u1']['trade_password'])

    # 信用卡预约还款
    # m.credit_card_reserved_pay(user['u1']['user_name'],
    #                           login_password=user['u1']['login_password'],
    #                           reserved_pay_amount=user['u1']['credit_card_reserved_pay_amount'],
    #                           trade_password=user['u1']['trade_password'])

    # 取消预约还款
    # m.cancel_reserved_pay(user['u1']['user_name'],
    #                       login_password=user['u1']['login_password'])

    # 赚积分--推荐用户注册绑卡
    # m.earn_points_by_recommend_user_register(user['u1']['user_name'],
    #                                          login_password=user['u1']['login_password'])

    # 花积分--买定期宝
    # m.spend_points_by_buy_dqb(user_name=user['u1']['user_name'],
    #                           login_password=user['u1']['login_password'],
    #                           amount=user['u1']['dqb_product_amount'],
    #                           trade_password=user['u1']['trade_password'],
    #                           dqb_product_name=user['u1']['dqb_product'], )

    # 花积分--买基金
    # m.spend_points_by_buy_fund(user_name=user['u1']['user_name'],
    #                            login_password=user['u1']['login_password'],
    #                            amount=user['u1']['fund_product_amount'],
    #                            trade_password=user['u1']['trade_password'],
    #                            fund_product_name=user['u1']['fund_product_name'],
    #                            fund_product_code=user['u1']['fund_product_code'],
    #                            )

    # 花积分--买高端产品
    # m.spend_points_by_buy_vipproduct_use_product_name(user_name=user['u1']['user_name'],
    #                                                   login_password=user['u1']['login_password'],
    #                                                   amount=user['u1']['high_end_product_amount'],
    #                                                   trade_password=user['u1']['trade_password'],
    #                                                   product_name=user['u1']['high_end_product_for_points_offset'],
    #                                                   )

    # 添加还款提醒
    # m.add_credit_card_repayment_warn(user_name=user['u1']['user_name'],
    #                                  login_password=user['u1']['login_password']
    #                                  )

    # 取消还款提醒
    # m.cancel_credit_card_repayment_warn(user_name=user['u1']['user_name'],
    #                                  login_password=user['u1']['login_password']
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
    #                              fund_product_name_for_fast_redeem=user['u1']['fund_product_name_for_fast_redeem']
    #                              )


    # 基金极速卖出
    # m.fast_redeem_fund_product(user_name=user['u1']['user_name'],
    #                            login_password=user['u1']['login_password'],
    #                            redeem_amount=user['u1']['fund_product_amount'],
    #                            trade_password=user['u1']['trade_password'],
    #                            fund_product_name_for_fast_redeem=user['u1']['fund_product_name_for_fast_redeem']
    #                            )

    # 积分明细
    # m.assets_my_points_details(user_name=user['u1']['user_name'],
    #                            login_password=user['u1']['login_password']
    #                            )

    # 新基金频道--研究报告
    # m.fund_research_report(user_name=user['u1']['user_name'],
    #                        login_password=user['u1']['login_password']
    #                        )

    # 基金频道--机构观点
    # m.fund_institution_viewpoint(user_name=user['u1']['user_name'],
    #                             login_password=user['u1']['login_password']
    #                             )

    # 基金频道--达人论基
    # m.fund_talent_fund_discussion(user_name=user['u1']['user_name'],
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
    #                       fund_product_name_2=user['u1']['fund_product_name_2'],
    #                       fund_product_code=user['u1']['fund_product_code'],
    #                       fund_company=user['u1']['fund_company']
    #                       )

    # 基金频道--对比分析
    # m.fund_comparasion_and_analysis(user_name=user['u1']['user_name'],
    #                                 login_password=user['u1']['login_password'],
    #                                 fund_product_code=user['u1']['fund_product_code'],
    #                                 fund_product_code_2=user['u1']['fund_product_code_2'],
    #                                 )

    # 购买定期宝使用优惠券(不可叠加)
    # m.buy_dqb_use_nonsuperposed_coupon(user_name=user['u1']['user_name'],
    #                                    login_password=user['u1']['login_password'],
    #                                    amount=user['u1']['dqb_product_amount'],
    #                                    trade_password=user['u1']['trade_password'],
    #                                    product_name=user['u1']['dqb_product']
    #                                    )

    # 购买定期宝使用优惠券(可叠加)
    # m.buy_dqb_use_superposed_coupon(user_name=user['u1']['user_name'],
    #                                    login_password=user['u1']['login_password'],
    #                                    amount=user['u1']['dqb_product_amount_for_superposed_coupon'],
    #                                    trade_password=user['u1']['trade_password'],
    #                                    product_name=user['u1']['dqb_product']
    #                                    )

    # 购买高端使用优惠券(不可叠加)
    # m.buy_vipproduct_use_nonsuperposed_coupon(user_name=user['u1']['user_name'],
    #                                    login_password=user['u1']['login_password'],
    #                                    amount=user['u1']['high_end_product_amount'],
    #                                    trade_password=user['u1']['trade_password'],
    #                                    product_name=user['u1']['high_end_product']
    #                                    )

    # 购买高端使用优惠券(可叠加)
    # m.buy_vipproduct_use_superposed_coupon(user_name=user['u1']['user_name'],
    #                                       login_password=user['u1']['login_password'],
    #                                       amount=user['u1']['high_end_amount_for_superposed_coupon'],
    #                                       trade_password=user['u1']['trade_password'],
    #                                       product_name=user['u1']['high_end_product']
    #                                       )

    # 购买基金使用优惠券(不可叠加)
    # m.buy_fund_use_nonsuperposed_coupon(user_name=user['u1']['user_name'],
    #                                     login_password=user['u1']['login_password'],
    #                                     fund_product_name=user['u1']['fund_product_name'],
    #                                     amount=user['u1']['fund_product_amount_for_nonsuperposed_coupon'],
    #                                     trade_password=user['u1']['trade_password'],
    #                                     fund_product_code=user['u1']['fund_product_code']
    #                                     )

    # 购买基金使用优惠券(可叠加)
    # m.buy_fund_use_superposed_coupon(user_name=user['u1']['user_name'],
    #                                     login_password=user['u1']['login_password'],
    #                                     fund_product_name=user['u1']['fund_product_name'],
    #                                     amount=user['u1']['fund_product_amount'],
    #                                     trade_password=user['u1']['trade_password'],
    #                                     fund_product_code=user['u1']['fund_product_code']
    #                                     )

    # 购买定期宝使用积分+优惠券(不可叠加)
    # m.buy_dqb_use_points_and_nonsuperposed_coupon(user_name=user['u1']['user_name'],
    #                                    login_password=user['u1']['login_password'],
    #                                    amount=user['u1']['dqb_product_amount_for_superposed_coupon'],
    #                                    trade_password=user['u1']['trade_password'],
    #                                    product_name=user['u1']['dqb_product']
    #                                    )

    # 购买定期宝使用积分+优惠券(可叠加)
    # m.buy_dqb_use_points_and_superposed_coupon(user_name=user['u1']['user_name'],
    #                                    login_password=user['u1']['login_password'],
    #                                    amount=user['u1']['dqb_product_amount'],
    #                                    trade_password=user['u1']['trade_password'],
    #                                    product_name=user['u1']['dqb_product']
    #                                    )

    # 购买高端使用积分+优惠券(不可叠加)
    # m.buy_vipproduct_use_points_and_nonsuperposed_coupon(user_name=user['u1']['user_name'],
    #                                    login_password=user['u1']['login_password'],
    #                                    amount=user['u1']['high_end_product_amount'],
    #                                    trade_password=user['u1']['trade_password'],
    #                                    product_name=user['u1']['high_end_product_for_points']
    #                                    )

    # 购买高端使用积分+优惠券(可叠加)
    # m.buy_vipproduct_use_points_and_superposed_coupon(user_name=user['u1']['user_name'],
    #                                           login_password=user['u1']['login_password'],
    #                                           amount=user['u1']['high_end_product_amount'],
    #                                           trade_password=user['u1']['trade_password'],
    #                                           product_name=user['u1']['high_end_product_for_points']
    #                                           )

    # 购买基金使用积分+优惠券(不可叠加)
    # m.buy_fund_use_points_and_nonsuperposed_coupon(user_name=user['u1']['user_name'],
    #                                     login_password=user['u1']['login_password'],
    #                                     fund_product_name=user['u1']['fund_product_name'],
    #                                     amount=user['u1']['fund_product_amount'],
    #                                     trade_password=user['u1']['trade_password'],
    #                                     fund_product_code=user['u1']['fund_product_code']
    #                                     )

    # 购买基金使用积分+优惠券(可叠加)
    # m.buy_fund_use_points_and_superposed_coupon(user_name=user['u1']['user_name'],
    #                                     login_password=user['u1']['login_password'],
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
    #                     product_name=user['u1']['product_name_for_vipproduct_pledge'],
    #                     pledge_amount=user['u1']['pledge_amount'],
    #                     trade_password=user['u1']['trade_password'],
    #                     )
