# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

current_page = []

PLEDGE_AMOUNT="accId_UIATextField_(textField)不可超过最高借款金额"
PLEDGE_SUBMIT="accId_UIAButton_提交申请"
TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
PLEDGE_DONE="accId_UIAButton_确认"


class PledgeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(PledgeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def pledge_detail(self, pledge_amount, trade_password):
        self.perform_actions(PLEDGE_AMOUNT, pledge_amount,
                             PLEDGE_SUBMIT,
                             TRADE_PASSWORD, trade_password,
                             PLEDGE_DONE
                             )

