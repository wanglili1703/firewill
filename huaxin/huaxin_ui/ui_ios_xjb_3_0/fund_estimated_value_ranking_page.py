# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

STOCK = "accId_UIAButton_股票型"
MIXED = "accId_UIAButton_混合型"
INDEX = "accId_UIAButton_指数型"
ALL = "accId_UIAButton_全部"


class FundEstimatedValueRankingPage(PageObject):
    def __init__(self, web_driver):
        super(FundEstimatedValueRankingPage, self).__init__(web_driver)

    @robot_log
    def verify_at_fund_estimated_value_ranking_page(self):
        self.assert_values('估值排行', self.get_text("//UIAStaticText[@label='估值排行']"))

        page = self
        return page

    @robot_log
    def switch_tabs(self):
        self.perform_actions(STOCK)
        self.assert_values(True,
                           self.element_exist("(UIButton_估算净值order_type_none.png)", "find_element_by_accessibility_id"))
        self.assert_values(True,
                           self.element_exist("(UIButton_估算涨幅order_type_desc.png)", "find_element_by_accessibility_id"))

        self.perform_actions(ALL)
        self.assert_values(True,
                           self.element_exist("(UIButton_估算净值order_type_none.png)", "find_element_by_accessibility_id"))
        self.assert_values(True,
                           self.element_exist("(UIButton_估算涨幅order_type_desc.png)", "find_element_by_accessibility_id"))

        self.perform_actions(MIXED)
        self.assert_values(True,
                           self.element_exist("(UIButton_估算净值order_type_none.png)", "find_element_by_accessibility_id"))
        self.assert_values(True,
                           self.element_exist("(UIButton_估算涨幅order_type_desc.png)", "find_element_by_accessibility_id"))

        self.perform_actions(INDEX)
        self.assert_values(True,
                           self.element_exist("(UIButton_估算净值order_type_none.png)", "find_element_by_accessibility_id"))
        self.assert_values(True,
                           self.element_exist("(UIButton_估算涨幅order_type_desc.png)", "find_element_by_accessibility_id"))

        page = self
        return page
