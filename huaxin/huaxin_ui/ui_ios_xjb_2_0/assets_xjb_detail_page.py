# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_2_0.recharge_page import RechargePage
from huaxin_ui.ui_ios_xjb_2_0.withdraw_page import WithdrawPage

from huaxin_ui.ui_ios_xjb_2_0.xjb_trade_detail_page import XjbTradeDetailPage

WITHDRAW = "accId_UIAButton_取出"
RECHARGE = "accId_UIAButton_存入"
XJB_TRADE_DETAIL = "accId_UIAButton_收支明细"

current_page = []


class AssetsXjbDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsXjbDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_recharge_page(self):
        self.perform_actions(RECHARGE)
        page = RechargePage(self.web_driver)
        return page

    @robot_log
    def go_to_withdraw_page(self):
        self.perform_actions(WITHDRAW)
        page = WithdrawPage(self.web_driver)
        return page

    @robot_log
    def go_to_xjb_trade_detail_page(self):
        self.perform_actions(XJB_TRADE_DETAIL)
        page = XjbTradeDetailPage(self.web_driver)
        return page
