# coding=utf-8
from _common.page_object import PageObject

import huaxin_ui.ui_ios_xjb_2_0.fund_page
import huaxin_ui.ui_ios_xjb_2_0.fund_plan_page
from _common.xjb_decorator import robot_log

BUY_FUND = "accId_UIAButton_购买"
BUY_AMOUNT = "accId_UIATextField_(buyCount)最低买入金额1.00元"
USE_POINTS = "axis_IOS_(integralSwitch)"
BUY_CONFIRM = "accId_UIAButton_(payButton)"
TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
BUY_DONE = "accId_UIAButton_确认"
CANCEL = "accId_UIAButton_取消"

USE_COUPON = "axis_IOS_优惠券_0.5,0"
COUPON_1 = "axis_IOS_满10元减1元"
COUPON_2 = "axis_IOS_满2000元减10元"
COUPON_CONFIRM = "axis_IOS_确定"

FUND_PLAN_BUTTON="axis_IOS_定投"
FUND_PLAN_BUTTON_START="accId_UIAButton_开启定投[POP]"

current_page = []


class FundPageFundDetail(PageObject):
    def __init__(self, web_driver):
        super(FundPageFundDetail, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def buy_fund_product(self, amount, trade_password, points='N', nonsuperposed_coupon='N',
                         superposed_coupon='N'):
        self.perform_actions(
            BUY_FUND,
            BUY_AMOUNT, amount,
        )

        if not points == 'N':
            self.perform_actions(
                USE_POINTS,
            )

        if not nonsuperposed_coupon == 'N':
            self.perform_actions(
                USE_COUPON,
                COUPON_2,
                COUPON_CONFIRM,
            )

        if not superposed_coupon == 'N':
            self.perform_actions(
                USE_COUPON,
                COUPON_1,
                COUPON_CONFIRM,
            )

        self.perform_actions(
            BUY_CONFIRM,
            TRADE_PASSWORD, trade_password,
            BUY_DONE,
            # CANCEL,
        )

        page = huaxin_ui.ui_ios_xjb_2_0.fund_page.FundPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_plan_page(self):
        self.perform_actions(FUND_PLAN_BUTTON,
                             FUND_PLAN_BUTTON_START,
                             )

        page = huaxin_ui.ui_ios_xjb_2_0.fund_plan_page.FundPlanPage(self.web_driver)

        return page
