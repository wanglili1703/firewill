# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_2_0.assets_dqb_detail_page import AssetsDqbDetailPage
from huaxin_ui.ui_ios_xjb_2_0.assets_fund_detail_page import AssetsFundDetailPage
from huaxin_ui.ui_ios_xjb_2_0.assets_high_end_detail_page import AssetsHighEndDetailPage
from huaxin_ui.ui_ios_xjb_2_0.assets_xjb_detail_page import AssetsXjbDetailPage
from huaxin_ui.ui_ios_xjb_2_0.bank_card_management_page import BankCardManagementPage
from huaxin_ui.ui_ios_xjb_2_0.credit_card_repay_page import CreditCardRepayPage
import huaxin_ui.ui_ios_xjb_2_0.assets_my_points_detail_page
import huaxin_ui.ui_ios_xjb_2_0.pledge_detail_page

XJB_DETAIL = "accId_UIAStaticText_现金宝"
DQB_DETAIL = "accId_UIAStaticText_定期宝"
FUND_DETAIL = "accId_UIAStaticText_基金"
HIGH_END_DETAIL = "accId_UIAStaticText_高端理财"

CARD_MANAGEMENT = "accId_UIAStaticText_银行卡管理"
CREDIT_CARD_REPAY = "accId_UIAStaticText_信用卡还款"
MY_POINTS_STOP = "swipe_accId_我的积分"
MY_POINTS = "accId_UIAStaticText_我的积分"

HOME = "accId_UIAButton_(UITabBarButton_)"
FINANCE = "accId_UIAButton_(UITabBarButton_item_1)"
FUND = "accId_UIAButton_(UITabBarButton_item_2)"

SWIPE_START = "swipe_accId_//"
SWIPE_STOP = "swipe_accId_银行卡管理"

SWIPE_BEGAIN = "swipe_accId_//"
PLEDGE_STOP = "swipe_accId_随心借"
PLEDGE_REPAY_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
PLEDGE_REPAY_BUTTON_STOP="swipe_xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/bottom_bt']"
ASSETS_PLEDGE="accId_UIAStaticText_随心借"
PLEDGE_BUTTON="axis_IOS_我要借款"
PLEDGE_SWIPE_STOP = "swipe_accId_%s"
SELECT_PLEDGE_PRODUCT="accId_UIAStaticText_%s"
PLEDGE_REPAY="xpath_//android.widget.TextView[@text='%s']"
PLEDGE_REPAY_BUTTON="xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/bottom_bt']"

TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
PLEDGE_REPAY_DONE="accId_UIAButton_确认"

current_page = []


class AssetsPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_xjb_detail_page(self):
        self.perform_actions(
            XJB_DETAIL,
        )

        page = AssetsXjbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_dqb_detail_page(self):
        self.perform_actions(
            DQB_DETAIL,
        )

        page = AssetsDqbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_detail_page(self):
        self.perform_actions(
            FUND_DETAIL,
        )

        page = AssetsFundDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_high_end_detail_page(self):
        self.perform_actions(
            HIGH_END_DETAIL,
        )

        page = AssetsHighEndDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_bank_card_management_page(self):
        self.perform_actions(
            SWIPE_START, SWIPE_STOP, 'U',
            CARD_MANAGEMENT, )
        page = BankCardManagementPage(self.web_driver)

        return page

    @robot_log
    def go_to_credit_card_repay_page(self):
        self.perform_actions(
            CREDIT_CARD_REPAY,
        )

        page = CreditCardRepayPage(self.web_driver)

        return page

    @robot_log
    def go_to_my_points_page(self):
        self.perform_actions(
            "swipe_xpath_//", MY_POINTS_STOP, 'U',
            MY_POINTS,
        )

        page = huaxin_ui.ui_ios_xjb_2_0.assets_my_points_detail_page.AssetsMyPointsDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_pledge_detail_page(self, product_name):
        self.perform_actions(SWIPE_BEGAIN, PLEDGE_STOP, 'U',
                             ASSETS_PLEDGE,
                             PLEDGE_BUTTON,
                             SWIPE_BEGAIN, PLEDGE_SWIPE_STOP % product_name, 'U',
                             SELECT_PLEDGE_PRODUCT % product_name
                             )

        page = huaxin_ui.ui_ios_xjb_2_0.pledge_detail_page.PledgeDetailPage(self.web_driver)

        return page

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
