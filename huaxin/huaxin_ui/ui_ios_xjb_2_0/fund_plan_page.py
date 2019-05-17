# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

AMOUNT="accId_UIATextField_(textField)最低买入金额1.00元"
PURCHASE_CYCLE_WEEK_LIST="accId_UIAElement_(viewPeriod)"
PURCHASE_CYCLE_WEEK="accId_UIAButton_完成"
PURCHASE_CYCLE_DAY_LIST="accId_UIAElement_(viewDate)"
PURCHASE_CYCLE_DAY="accId_UIAButton_完成"
PURCHASE_COMFIRM="accId_UIAButton_确认"
TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
PURCHASE_DONE = "accId_UIAButton_确认"



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