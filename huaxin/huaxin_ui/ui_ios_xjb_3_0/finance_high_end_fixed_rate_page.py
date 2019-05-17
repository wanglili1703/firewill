# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

current_page = []


class FinanceHighEndFixedRatePage(PageObject):
    def __init__(self, web_driver):
        super(FinanceHighEndFixedRatePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_fixed_rate_series_page(self):
        self.assert_values("固定收益系列", self.get_text("//UIAStaticText[@label='固定收益系列']"))
        self.assert_values("固定收益系列", self.get_text("//UIATableCell/UIAStaticText[@label='固定收益系列']"))
        self.assert_values(True, self.element_exist("//UIAStaticText[@label='年化业绩比较基准']"))
