# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_3_0.assets_dqb_detail_page import AssetsDqbDetailPage
from huaxin_ui.ui_android_xjb_3_0.assets_fund_detail_page import AssetsFundDetailPage
from huaxin_ui.ui_android_xjb_3_0.assets_high_end_detail_page import AssetsHighEndDetailPage
from huaxin_ui.ui_android_xjb_3_0.assets_xjb_detail_page import AssetsXjbDetailPage
from huaxin_ui.ui_android_xjb_3_0.bank_card_management_page import BankCardManagementPage
from huaxin_ui.ui_android_xjb_3_0.credit_card_repay_page import CreditCardRepayPage
import huaxin_ui.ui_android_xjb_3_0.assets_my_points_detail_page
import huaxin_ui.ui_android_xjb_3_0.pledge_detail_page
import huaxin_ui.ui_android_xjb_3_0.personal_setting_page
import huaxin_ui.ui_android_xjb_3_0.invite_friend_page

import huaxin_ui.ui_android_xjb_3_0.my_coupons_list_page
from huaxin_ui.ui_android_xjb_3_0.reservation_code_page import ReservationCodePage
import huaxin_ui.ui_android_xjb_3_0.fund_page
from huaxin_ui.ui_android_xjb_3_0.finance_page import FinancePage
import huaxin_ui.ui_android_xjb_3_0.home_page
import huaxin_ui.ui_android_xjb_3_0.assets_associator_center_page
import huaxin_ui.ui_android_xjb_3_0.repay_loan_page
import huaxin_ui.ui_android_xjb_3_0.assets_analysis_page
import huaxin_ui.ui_android_xjb_3_0.pledge_page
import huaxin_ui.ui_android_xjb_3_0.trade_detail_page
import huaxin_ui.ui_android_xjb_3_0.login_page
import huaxin_ui.ui_android_xjb_3_0.personal_information_page
import huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page
import time
from _common.global_config import ASSERT_DICT
from decimal import *

XJB_DETAIL = "xpath_//android.widget.TextView[@text='现金宝']"
DQB_DETAIL = "xpath_//android.widget.TextView[@text='定活宝']"
FUND_DETAIL = "xpath_//android.widget.TextView[@text='基金']"
HIGH_END_DETAIL = "xpath_//android.widget.TextView[@text='高端']"

CARD_MANAGEMENT = "xpath_//android.widget.TextView[@text='银行卡']"
CREDIT_CARD_REPAY_SWIPE_BEGIN = "swipe_xpath_//"
CREDIT_CARD_REPAY_STOP = "swipe_xpath_//android.widget.TextView[@text='还信用卡']"
# CREDIT_CARD_REPAY = "xpath_//android.widget.TextView[@text='还信用卡']"
# CREDIT_CARD_REPAY = "xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/container']/android.widget.TextView[@text='follow your heart']"  # 还信用卡

CREDIT_CARD_REPAY = "xpath_//android.widget.RelativeLayout[@index='%s']"  # 还信用卡

# MY_COUPONS_SWIPE = "swipe_xpath_//android.widget.TextView[@text='我的优惠券']"
MY_COUPONS_SWIPE = "swipe_xpath_//android.widget.TextView[@text='我的优惠券']"
# MY_COUPONS = "xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/container']/android.widget.TextView[@text='我的优惠券说明']"
MY_COUPONS = "xpath_//android.widget.RelativeLayout[@index='%s']"

MY_POINTS_STOP = "swipe_xpath_//android.widget.TextView[@text='我的积分']"
MY_POINTS = "xpath_//android.widget.RelativeLayout[@index='8']"
# MY_POINTS = "xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/container']/android.widget.TextView[@text='我的积分']"

REPAY_LOAN_SWIPE_BEGIN = "swipe_xpath_//"
REPAY_LOAN_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='还贷款']"
REPAY_LOAN = "xpath_//android.widget.RelativeLayout[@index='6']"
# REPAY_LOAN = "xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/container']/android.widget.TextView[@text='走到哪还到哪']"

HOME = "xpath_//android.widget.RelativeLayout[1]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
FINANCE = "xpath_//android.widget.RelativeLayout[2]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
FUND = "xpath_//android.widget.RelativeLayout[3]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"

SWIPE_START = "swipe_xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/title_actionbar']"
SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/realcontent']"

SWIPE_BEGAIN = "swipe_xpath_//"
PLEDGE_STOP = "swipe_xpath_//android.widget.TextView[@text='随心借']"
PLEDGE_REPAY_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
PLEDGE_REPAY_BUTTON_STOP = "swipe_xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/bottom_bt']"
ASSETS_PLEDGE = "xpath_//android.widget.TextView[@text='随心借']"
PLEDGE_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
PLEDGE_REPAY = "xpath_//android.widget.TextView[@text='%s']"
PLEDGE_REPAY_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/bottom_bt']"

TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
PLEDGE_REPAY_DONE = "xpath_//android.widget.Button[@text='确认']"
HOME_PAGE = "xpath_//android.widget.TabWidget/android.widget.RelativeLayout[1]"
POP_DIALOG_CLOSE = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_dialog_close'][POP]"
MESSAGE_CENTER = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_home_actionbar_right']"

SETTINGS_BUTTON = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"
INVITE_FRIEND = "xpath_//android.widget.TextView[@text='邀请好友']"
RESERVATION_CODE = "xpath_//android.widget.TextView[@text='预约码']"
MASK_KNOW = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_mask_know'][POP]"
TOTAL_ASSETS = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/total_assets']"
TOTAL_ASSETS_ID = "com.shhxzq.xjb:id/total_assets"
XJB_ASSETS = "//android.widget.TextView[@text=\'现金宝\']/./following-sibling::android.widget.TextView[1]"
ASSOCIATOR_CENTER = "xpath_//android.widget.TextView[@text='会员中心']"
TOTAL_ACCOUNT_NAME = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/total_account_name']"
TRADE_RECORDS = "xpath_//android.widget.TextView[@text='交易记录']"
LOGIN = "xpath_//android.widget.Button[@text='登录']"
SETTING = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"
USER_ICON = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/user_icon']"
BIND_CARD_TIP = "xpath_//android.widget.TextView[@text='您尚未绑卡，请去绑卡']"

current_page = []

associator_rank_1 = 1000.00
associator_rank_2 = 50000.00
associator_rank_3 = 1000000.00
associator_rank_4 = 5000000.00
associator_assets = 0.00
user_level_1 = "新手会员"
user_level_2 = "白银会员"
user_level_3 = "黄金会员"
user_level_4 = "铂金会员"
user_level_5 = "钻石会员"


class AssetsPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('我的', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_bind_card_status(self):
        self.assert_values('您尚未绑卡，请去绑卡',
                           self.get_text('com.shhxzq.xjb:id/tv_header_tips_content', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def get_total_assets(self):
        return str(self.get_text(TOTAL_ASSETS_ID, 'find_element_by_id')).replace(',', '')

    @robot_log
    def get_xjb_assets(self):
        return str(self.get_text(XJB_ASSETS)).replace(',', '')

    @robot_log
    def go_to_xjb_detail_page(self):
        self.perform_actions(
            XJB_DETAIL,
        )

        page = AssetsXjbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_dqb_detail_page(self):
        self.perform_actions(DQB_DETAIL)

        time.sleep(5)

        page = AssetsDqbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_detail_page(self):
        self.perform_actions(FUND_DETAIL)

        time.sleep(5)

        page = AssetsFundDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_high_end_detail_page(self):
        self.perform_actions(
            HIGH_END_DETAIL)

        time.sleep(5)

        page = AssetsHighEndDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_bank_card_management_page(self, device_id=None):
        self.perform_actions(
            # SWIPE_START, SWIPE_STOP, 'U',
            # CARD_MANAGEMENT,
            CARD_MANAGEMENT)
        page = BankCardManagementPage(self.web_driver, device_id)

        return page

    @robot_log
    def go_to_credit_card_repay_page(self, device_id=None, index='5'):

        self.perform_actions(CREDIT_CARD_REPAY_SWIPE_BEGIN, CREDIT_CARD_REPAY_STOP, 'U')

        self.perform_actions(CREDIT_CARD_REPAY % index)

        page = CreditCardRepayPage(self.web_driver, device_id)
        return page

    @robot_log
    def go_to_my_points_page(self):
        self.perform_actions(
            CREDIT_CARD_REPAY_SWIPE_BEGIN, MY_POINTS_STOP, 'U')

        time.sleep(10)

        self.perform_actions(MY_POINTS)

        page = huaxin_ui.ui_android_xjb_3_0.assets_my_points_detail_page.AssetsMyPointsDetailPage(self.web_driver)

        return page

    # @robot_log
    # def go_to_pledge_detail_page(self, product_name):
    #     self.perform_actions(SWIPE_BEGAIN, PLEDGE_STOP, 'U',
    #                          ASSETS_PLEDGE,
    #                          PLEDGE_BUTTON,
    #                          SWIPE_BEGAIN, PLEDGE_SWIPE_STOP % product_name, 'U',
    #                          SELECT_PLEDGE_PRODUCT % product_name
    #                          )
    #
    #     page = huaxin_ui.ui_android_xjb_3_0.pledge_detail_page.PledgeDetailPage(self.web_driver)
    #
    #     return page

    @robot_log
    def pledge_repay(self, product_name, trade_password):
        self.perform_actions(SWIPE_BEGAIN, PLEDGE_STOP, 'U',
                             ASSETS_PLEDGE,
                             SWIPE_BEGAIN, PLEDGE_REPAY_STOP % product_name, 'U',
                             PLEDGE_REPAY % product_name,
                             SWIPE_BEGAIN, PLEDGE_REPAY_BUTTON_STOP, 'U',
                             PLEDGE_REPAY_BUTTON,
                             TRADE_PASSWORD, trade_password,
                             PLEDGE_REPAY_DONE
                             )

    @robot_log
    def go_to_pledge_page(self):
        self.perform_actions(SWIPE_BEGAIN, PLEDGE_STOP, 'U')
        self.perform_actions(ASSETS_PLEDGE)

        page = huaxin_ui.ui_android_xjb_3_0.pledge_page.PledgePage(self.web_driver)
        return page

    @robot_log
    def go_to_personal_setting_page(self):
        self.perform_actions(SETTINGS_BUTTON)
        page = huaxin_ui.ui_android_xjb_3_0.personal_setting_page.PersonalSettingPage(self.web_driver)

        return page

    @robot_log
    def go_to_invite_friend_page(self):
        self.perform_actions(INVITE_FRIEND)
        page = huaxin_ui.ui_android_xjb_3_0.invite_friend_page.InviteFriendPage(self.web_driver)

        return page

    @robot_log
    def go_to_reservation_code_page(self):
        self.perform_actions(RESERVATION_CODE)

        page = ReservationCodePage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_page(self):
        self.perform_actions(FUND)
        page = huaxin_ui.ui_android_xjb_3_0.fund_page.FundPage(self.web_driver)

        return page

    @robot_log
    def go_to_finance_page(self):
        self.perform_actions(FINANCE,
                             MASK_KNOW)
        page = FinancePage(self.web_driver)

        return page

    @robot_log
    def go_to_home_page_from_assets_page(self):
        self.perform_actions(HOME,
                             POP_DIALOG_CLOSE)
        page = huaxin_ui.ui_android_xjb_3_0.home_page.HomePage(self.web_driver)

        return page

    @robot_log
    def associator_rank_verify(self):
        associator_assets = str(self.get_text('com.shhxzq.xjb:id/total_assets', 'find_element_by_id'))
        level = self.get_text('com.shhxzq.xjb:id/user_level', 'find_element_by_id')
        if associator_assets < associator_rank_1:
            self.assert_values(user_level_1, level)
        elif (associator_assets >= associator_rank_1) and (associator_assets < associator_rank_2):
            self.assert_values(user_level_2, level)
        elif (associator_assets >= associator_rank_2) and (associator_assets < associator_rank_3):
            self.assert_values(user_level_3, level)
        elif (associator_assets >= associator_rank_3) and (associator_assets < associator_rank_4):
            self.assert_values(user_level_4, level)
        elif associator_assets >= associator_rank_4:
            self.assert_values(user_level_5, level)

    @robot_log
    def go_to_associator_center(self):
        self.perform_actions(ASSOCIATOR_CENTER)

        page = huaxin_ui.ui_android_xjb_3_0.assets_associator_center_page.AssetsAssociatorCenterPage(self.web_driver)

        return page

    @robot_log
    def go_to_repay_loan_page(self):

        self.perform_actions(REPAY_LOAN_SWIPE_BEGIN, REPAY_LOAN_SWIPE_STOP, 'U')

        self.perform_actions(REPAY_LOAN)

        page = huaxin_ui.ui_android_xjb_3_0.repay_loan_page.RepayLoanPage(self.web_driver)

        time.sleep(5)

        return page

    @robot_log
    def go_to_my_coupon_list(self, index='4'):
        self.perform_actions(CREDIT_CARD_REPAY_SWIPE_BEGIN, MY_COUPONS_SWIPE, 'U',
                             MY_COUPONS % index)

        page = huaxin_ui.ui_android_xjb_3_0.my_coupons_list_page.MyCouponsListPage(self.web_driver)
        return page

    @robot_log
    def go_to_my_empty_coupon_list(self, index='4'):
        self.perform_actions(CREDIT_CARD_REPAY_SWIPE_BEGIN, REPAY_LOAN_SWIPE_STOP, 'U',
                             MY_COUPONS % index)

        page = huaxin_ui.ui_android_xjb_3_0.my_coupons_list_page.MyCouponsListPage(self.web_driver)
        return page

    @robot_log
    def go_to_assets_fund_detail_page(self):
        self.perform_actions(FUND_DETAIL)

        time.sleep(5)

        page = AssetsFundDetailPage(self.web_driver)

        return page

    @robot_log
    def verify_xjb_total_assets(self, amount, operate_type=None):
        xjb_total_assets = str(self.get_text(
            '//android.widget.TextView[@text=\'现金宝\']/./following-sibling::android.widget.TextView[1]')).replace(',',
                                                                                                                 '')
        xjb_total_assets_actual = Decimal(float(xjb_total_assets)).quantize(Decimal('0.00'))

        if operate_type is None:
            xjb_total_assets_expected = float(
                Decimal(float(str(ASSERT_DICT['xjb_total_assets_login']).replace(',', ''))).quantize(
                    Decimal('0.00'))) + float(amount)
        else:
            xjb_total_assets_expected = float(
                Decimal(float(str(ASSERT_DICT['xjb_total_assets_login']).replace(',', ''))).quantize(
                    Decimal('0.00'))) - float(amount)
        ASSERT_DICT.update({'xjb_total_assets': xjb_total_assets_expected})
        self.assert_values('%.2f' % xjb_total_assets_expected, str(xjb_total_assets_actual), '==')

        page = self
        return page

    @robot_log
    def go_to_assets_analysis_page(self):
        self.perform_actions(TOTAL_ACCOUNT_NAME)

        time.sleep(5)

        page = huaxin_ui.ui_android_xjb_3_0.assets_analysis_page.AssetsAnalysisPage(self.web_driver)

        return page

    @robot_log
    def verify_total_assets(self, operate_type=None):
        total_assets = str(self.get_text('com.shhxzq.xjb:id/total_assets', 'find_element_by_id')).replace(',', '')
        if operate_type is None:
            self.assert_values('0.00', total_assets, '==')

        page = self
        return page

    @robot_log
    def go_to_trade_detail_page(self):
        self.perform_actions(TRADE_RECORDS)

        page = huaxin_ui.ui_android_xjb_3_0.trade_detail_page.TradeDetailPage(self.web_driver)
        return page

    @robot_log
    def go_to_login_page(self):
        self.perform_actions(LOGIN)

        page = huaxin_ui.ui_android_xjb_3_0.login_page.LoginPage(self.web_driver)
        return page

    @robot_log
    def check_not_login_status_details(self):
        self.assert_values('未登录', self.get_text('com.shhxzq.xjb:id/not_login_txt', 'find_element_by_id'))
        self.assert_values(False, self.element_exist("//android.widget.TextView[@text='您尚未绑卡，请去绑卡']"))
        # self.assert_values('0.00', self.get_text('com.shhxzq.xjb:id/total_assets', 'find_element_by_id'))
        # yesterday_income_text = self.get_text('com.shhxzq.xjb:id/yesterday_income', 'find_element_by_id')
        # total_income_text = self.get_text('com.shhxzq.xjb:id/total_income', 'find_element_by_id')
        # yesterday_income = filter(lambda ch: ch in '0123456789.', yesterday_income_text)
        # total_income = filter(lambda ch: ch in '0123456789.', total_income_text)
        # self.assert_values('0.00', yesterday_income)
        # self.assert_values('0.00', total_income)
        self.assert_values(False, self.element_exist(
            "//android.widget.TextView[@text='现金宝']/following-sibling::android.widget.TextView[1]"))
        self.assert_values(False, self.element_exist(
            "//android.widget.TextView[@text='定活宝']/following-sibling::android.widget.TextView[1]"))
        self.assert_values(False, self.element_exist(
            "//android.widget.TextView[@text='基金']/following-sibling::android.widget.TextView[1]"))
        self.assert_values(False, self.element_exist(
            "//android.widget.TextView[@text='高端']/following-sibling::android.widget.TextView[1]"))
        # self.assert_values('1分起存', self.get_text(
        #     "//android.widget.TextView[@text='现金宝']/following-sibling::android.widget.TextView[1]"))
        # self.assert_values('定期理财，活期存取', self.get_text(
        #     "//android.widget.TextView[@text='定活宝']/following-sibling::android.widget.TextView[1]"))
        # self.assert_values('1折费率 全市场最低', self.get_text(
        #     "//android.widget.TextView[@text='基金']/following-sibling::android.widget.TextView[1]"))
        # self.assert_values('百万起购 超高收益', self.get_text(
        #     "//android.widget.TextView[@text='高端']/following-sibling::android.widget.TextView[1]"))

        page = self
        return page

    @robot_log
    def go_to_personal_information_page(self, device_id):
        self.perform_actions(USER_ICON)

        page = huaxin_ui.ui_android_xjb_3_0.personal_information_page.PersonalInformationPage(self.web_driver,
                                                                                              device_id)
        return page

    @robot_log
    def go_to_setting_trade_password_page(self):
        self.perform_actions(BIND_CARD_TIP)

        page = huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page.SettingTradePasswordPage(self.web_driver)
        return page
