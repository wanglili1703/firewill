# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

current_page = []


class FinanceHighEndCashManagementPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceHighEndCashManagementPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_cash_management_series_page(self):
        self.assert_values("现金管理系列", self.get_text("//UIAStaticText[@label='现金管理系列']"))
        self.assert_values("现金管理系列", self.get_text("//UIATableCell/UIAStaticText[@label='现金管理系列']"))
        self.assert_values(True, self.element_exist("//UIAStaticText[@label='七日年化收益率']"))
