# coding=utf-8
import decimal

from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

import huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_page
import huaxin_ui.ui_ios_xjb_3_0.credit_card_add_finish_page

TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
RESERVED_PAY_AMOUNT = "xpathIOS_UIATextField_//UIATextField[@value='请输入还款金额']"
RESERVED_PAY_DATE = "accId_UIAStaticText_请选择信用卡还款日"
RESERVED_PAY_DATE_COMPLETED = "accId_UIAButton_(UIButton_完成)"
RESERVED_PAY_CONFIRM = "accId_UIAButton_确认还款"
RESERVED_PAY_DONE = "accId_UIAButton_确认"

USE_COUPON = "axis_IOS_优惠券_0.5,0"
COUPON = "accId_UIAStaticText_满10减1所有产品可叠加"
SUPER_COMPOSED_COUPON_SWIPE_STOP = "swipe_accId_满10减1所有产品可叠加"
COUPON_CONFIRM = "accId_UIAButton_(UIButton_确定)"
CREDIT_SELECT = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@name, '**** **** **** %s')]"
RECORD = "accId_UIAButton_还款记录"
BANK_NAME = "/AppiumAUT/UIAApplication/UIAWindow/UIAStaticText[1]"

current_page = []


class ReservedPayPage(PageObject):
    def __init__(self, web_driver):
        super(ReservedPayPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    # 信用卡预约还款
    @robot_log
    def reserved_pay(self, reserved_pay_amount, trade_password, use_coupon=None):
        bank = self.get_text(BANK_NAME)
        ASSERT_DICT.update({
            "bank": bank
        })
        actual_pay_amount = decimal.Decimal(reserved_pay_amount)

        self.perform_actions(RESERVED_PAY_AMOUNT, reserved_pay_amount,
                             RESERVED_PAY_DATE,
                             RESERVED_PAY_DATE_COMPLETED,
                             )

        if use_coupon is not None:
            self.perform_actions(USE_COUPON)
            coupon_amount = 1

            self.perform_actions("swipe_accId_//", SUPER_COMPOSED_COUPON_SWIPE_STOP, 'U',
                                 COUPON,
                                 COUPON_CONFIRM)
            actual_pay_amount = (decimal.Decimal(reserved_pay_amount) - decimal.Decimal(coupon_amount)).quantize(
                decimal.Decimal('0.00'))

        self.perform_actions(RESERVED_PAY_CONFIRM)

        if use_coupon is not None:
            self.assert_values(str(actual_pay_amount),
                               self.get_text("//UIAStaticText[@label='请输入交易密码']/following-sibling::UIAStaticText[1]"),
                               "==")

        self.perform_actions(TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_ios_xjb_3_0.credit_card_add_finish_page.CreditCardAddFinishPage(self.web_driver)
        return page
