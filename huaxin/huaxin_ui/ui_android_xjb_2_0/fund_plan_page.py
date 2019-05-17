# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

AMOUNT="xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/product_purchase_amt']"
PURCHASE_CYCLE_WEEK_LIST="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_purchase_cycle_weak']"
PURCHASE_CYCLE_WEEK="xpath_//android.widget.ListView/android.widget.CheckedTextView[2]"
PURCHASE_CYCLE_DAY_LIST="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_purchase_cycle_day']"
PURCHASE_CYCLE_DAY="xpath_//android.widget.ListView/android.widget.CheckedTextView[2]"
PURCHASE_COMFIRM="xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
PURCHASE_DONE = "xpath_//android.widget.Button[@text='确认']"



current_page = []

class FundPlanPage(PageObject):
    def __init__(self, web_driver):
        super(FundPlanPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def fund_plan_detail(self,amount,trade_password):
        self.perform_actions(AMOUNT,amount,
                             PURCHASE_CYCLE_WEEK_LIST,
                             PURCHASE_CYCLE_WEEK,
                             PURCHASE_CYCLE_DAY_LIST,
                             PURCHASE_CYCLE_DAY,
                             PURCHASE_COMFIRM,
                             TRADE_PASSWORD,trade_password,
                             PURCHASE_DONE)