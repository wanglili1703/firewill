# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools

REGULAR_START = "swipe_accId_定期"
REGULAR_PRODUCT_STOP = "swipe_accId_%s"
REGULAR_PRODUCT = "accId_UIAStaticText_%s"

BUY_NOW = "accId_UIAButton_(btnBuy)"
# AMOUNT = "accId_UIATextField_(textField)请输入购买金额"
AMOUNT = "accId_UIATextField_(textMoney)"
USE_POINTS = "axis_IOS_(integralSwitch)"
BUY_CONFIRM = "accId_UIAButton_(btnNext)"
VIERY_CODE_CONFIRM = "axis_IOS_(textField)_0,0.05"
BUY_CONTINUE = "accId_UIAButton_继续买入"
FIRST_BUY_INFO = "accId_UIAButton_(UIButton_确定)[POP]"

MOBILE_CODE = "accId_UIATextField_(textField)"
TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
# TRADE_PASSWORD = "accId_UIATextField_(tradePwdBoxView)"

BUY_DONE = "accId_UIAButton_(confirmButton)[POP]"

USE_COUPON = "axis_IOS_优惠券_0.5,0"
COUPON_1 = "axis_IOS_满10元减1元"
COUPON_2 = "axis_IOS_满2000元减10元"
COUPON_CONFIRM = "axis_IOS_确定"

current_page = []


class FinanceDqbPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceDqbPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def buy_dqb_product(self, product_name, amount, trade_password, mobile, points='N', nonsuperposed_coupon='N',
                        superposed_coupon='N'):
        if not product_name is None:
            self.perform_actions(
                REGULAR_START, REGULAR_PRODUCT_STOP % product_name, 'U',
                               REGULAR_PRODUCT % product_name,
            )

        self.perform_actions(
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

        self.perform_actions(
            BUY_CONFIRM,
        )

        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(
                BUY_CONTINUE,
            )

            verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile, template_id='as_risk_level')

            self.perform_actions(
                MOBILE_CODE, verify_code,
                VIERY_CODE_CONFIRM,
                TRADE_PASSWORD, trade_password,
                BUY_DONE,
            )

        else:
            self.perform_actions(
                TRADE_PASSWORD, trade_password,
                BUY_DONE,
            )

            if self.element_exist(u'UIButton_确定', 'find_element_by_accessibility_id'):
                self.perform_actions(
                    FIRST_BUY_INFO,
                )

        page = self

        return page
