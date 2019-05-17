# coding: utf-8
import time
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

HIGH_END_START = "swipe_xpath_//"
HIGH_END_PRODUCT_STOP = "swipe_accId_%s"
HIGH_END_PRODUCT = "accId_UIAStaticText_%s"

BUY_NOW = "accId_UIAButton_立即购买"
# AMOUNT = "accId_UIATextField_(textField)请输入购买金额"
AMOUNT = "accId_UIATextField_(textMoney)"
USE_POINTS = "axis_IOS_(integralSwitch)"
BUY_CONFIRM = "accId_UIAButton_(btnNext)"
BUY_CONTINUE = "accId_UIAButton_继续买入[POP]"

TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
# TRADE_PASSWORD = "accId_UIATextField_(tradePwdBoxView)"

BUY_DONE = "accId_UIAButton_确认"

USE_COUPON = "axis_IOS_优惠券_0.5,0"
COUPON_1 = "axis_IOS_满10元减1元"
COUPON_2 = "axis_IOS_满2000元减10元"
COUPON_CONFIRM = "axis_IOS_确定"

current_page = []

class FinanceHighEndPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceHighEndPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def buy_high_end_product(self, product_name, amount, trade_password, points='N', nonsuperposed_coupon='N',
                             superposed_coupon='N'):
        self.perform_actions(
            HIGH_END_START, HIGH_END_PRODUCT_STOP % product_name, 'U',
                            HIGH_END_PRODUCT % product_name,
            BUY_NOW,
            AMOUNT, amount,
        )

        if not points == 'N':
            self.perform_actions(
                USE_POINTS,
            )

        if not nonsuperposed_coupon == 'N':
            self.perform_actions(
                USE_COUPON,
                COUPON_1,
                COUPON_CONFIRM,
            )

        if not superposed_coupon == 'N':
            self.perform_actions(
                USE_COUPON,
                COUPON_2,
                COUPON_CONFIRM,
            )

            return self

        self.perform_actions(
            BUY_CONFIRM,
            BUY_CONTINUE,
            BUY_CONFIRM,
            TRADE_PASSWORD, trade_password,
            BUY_DONE,
        )

        page = self

        return page
