# coding=utf-8
import time
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

import huaxin_ui.ui_ios_xjb_2_0.credit_card_repay_page

TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
RESERVED_PAY_AMOUNT = "accId_UIATextField_(textField)请输入还款金额"
RESERVED_PAY_DATE = "accId_UIAStaticText_请选择信用卡还款日"
# DEDUCTION_DATE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_cr_deduction_date']"
# RESERVED_PAY_DATE_MONTH="xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/month']"
# RESERVED_PAY_DATE_DAY="xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/day']"
RESERVED_PAY_DATE_COMPELETED = "accId_UIAButton_(UIButton_完成)"
RESERVED_PAY_COMFIRM = "accId_UIAButton_确认还款"
RESERVED_PAY_DONE = "accId_UIAButton_确认"

current_page = []


class ReservedPayPage(PageObject):
    def __init__(self, web_driver):
        super(ReservedPayPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    # 信用卡预约还款
    @robot_log
    def reserved_pay(self, reserved_pay_amount, trade_password):
        self.perform_actions(RESERVED_PAY_AMOUNT, reserved_pay_amount,
                             RESERVED_PAY_DATE,
                             # RESERVED_PAY_DATE_MONTH,
                             # RESERVED_PAY_DATE_DAY,
                             RESERVED_PAY_DATE_COMPELETED,
                             RESERVED_PAY_COMFIRM,
                             TRADE_PASSWORD, trade_password,
                             RESERVED_PAY_DONE
                             )

        page = huaxin_ui.ui_ios_xjb_2_0.credit_card_repay_page.CreditCardRepayPage(self.web_driver)
        return page
