# coding=utf-8
import time
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

import huaxin_ui.ui_android_xjb_2_0.credit_card_repay_page


RESERVED_PAY="xpath_//android.widget.TextView[@text='信用卡还款']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
CREDIT_CARD_SELECTED="xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/rl_credit_item']"
RESERVED_PAY_AMOUNT="xpath_//android.widget.EditText[@text='请输入预约还款金额']"
RESERVED_PAY_DATE="xpath_//android.widget.TextView[@text='请选择信用卡还款日']"
DEDUCTION_DATE="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_cr_deduction_date']"
RESERVED_PAY_DATE_MONTH="xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/month']"
RESERVED_PAY_DATE_DAY="xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/day']"
RESERVED_PAY_DATE_COMPELETED="xpath_//android.widget.TextView[@text='完成']"
RESERVED_PAY_COMFIRM="xpath_//android.widget.Button[@text='确认还款']"
RESERVED_PAY_DONE="xpath_//android.widget.Button[@text='确认']"

current_page=[]

class ReservedPayPage(PageObject):
    def __init__(self, web_driver):
        super(ReservedPayPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

# 信用卡预约还款
    @robot_log
    def reserved_pay(self,reserved_pay_amount,trade_password):

        self.perform_actions(RESERVED_PAY_AMOUNT,reserved_pay_amount,
                             RESERVED_PAY_DATE,
                             RESERVED_PAY_DATE_MONTH,
                             RESERVED_PAY_DATE_DAY,
                             RESERVED_PAY_DATE_COMPELETED,
                             RESERVED_PAY_COMFIRM,
                             TRADE_PASSWORD,trade_password,
                             RESERVED_PAY_DONE
                             )

        page=huaxin_ui.ui_android_xjb_2_0.credit_card_repay_page.CreditCardRepayPage(self.web_driver)
        return page

