# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

ONE_WEEK = "accId_UIAButton_近1周"
ONE_MONTH = "accId_UIAButton_近1月"
THREE_MONTHS = "accId_UIAButton_近3月"
SIX_MONTHS = "accId_UIAButton_近6月"
ONE_YEAR = "accId_UIAButton_近1年"
THREE_YEARS = "accId_UIAButton_近3年"
FINISH = "accId_UIAButton_完成"


# 最佳表现基金
class FundBestPerformancePage(PageObject):
    def __init__(self, web_driver):
        super(FundBestPerformancePage, self).__init__(web_driver)

    @robot_log
    def verify_at_fund_best_performance_page(self, title):
        self.assert_values(title, self.get_text("(UIButton_最佳表现基金icon_arrowfold)", "find_element_by_accessibility_id"))

        page = self
        return page

    @robot_log
    def view_best_performance_funds(self):
        self.perform_actions(ONE_WEEK)
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[contains(@label, '+')]"))

        self.perform_actions(ONE_MONTH)
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[contains(@label, '+')]"))

        self.perform_actions(THREE_MONTHS)
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[contains(@label, '+')]"))

        self.perform_actions(SIX_MONTHS)
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[contains(@label, '+')]"))

        self.perform_actions(ONE_YEAR)
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[contains(@label, '+')]"))

        self.perform_actions(THREE_YEARS)
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[contains(@label, '+')]"))

        self.verify_at_fund_best_performance_page('最佳表现基金')

        page = self
        return page

    @robot_log
    def view_highest_turnovers(self):
        self.perform_actions("accId_UIAButton_(UIButton_最佳表现基金icon_arrowfold)",
                             "swipe_accId_//", "swipe_accId_scroll_1", "U",
                             FINISH)
        self.perform_actions(ONE_WEEK)
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[contains(@label, '+')]"))

        self.perform_actions(ONE_MONTH)
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[contains(@label, '+')]"))

        self.assert_values(False,
                           self.element_exist("近3月", "find_element_by_accessibility_id"))

        self.verify_at_fund_best_performance_page('最高成交量')

        page = self
        return page
