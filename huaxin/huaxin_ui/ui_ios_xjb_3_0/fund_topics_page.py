# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

ONE_MONTH = "accId_UIAButton_近1月"
ONE_WEEK = "accId_UIAButton_近1周"
THREE_MONTH = "accId_UIAButton_近3月"
SIX_MONTH = "accId_UIAButton_近6月"


class FundTopicPage(PageObject):
    def __init__(self, web_driver):
        super(FundTopicPage, self).__init__(web_driver)

    @robot_log
    def verify_at_fund_topic_page(self):
        self.assert_values('热门主题', self.get_text("//UIAStaticText[@label='热门主题']"))

        page = self
        return page

    @robot_log
    def switch_tabs(self):
        self.perform_actions(ONE_WEEK)
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, '%')]"))

        self.perform_actions(ONE_MONTH)
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, '%')]"))

        self.perform_actions(THREE_MONTH)
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, '%')]"))

        self.perform_actions(SIX_MONTH)
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, '%')]"))

        page = self
        return page
