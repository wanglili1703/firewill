# coding: utf-8

from _common.page_object import PageObject
from  _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_page_all_fund_page
import time

START_FUND_PLAN = "xpathIOS_UIAImage_//UIAScrollView/UIAWebView/UIAImage[2]"
I_KNOW = "accId_UIAButton_(UIButton_)"


class StartFundPlanPage(PageObject):
    def __init__(self, web_driver):
        super(StartFundPlanPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('基金定投开启须知', self.get_text("//UIAStaticText[@label='基金定投开启须知']"))

        page = self

        return page

    @robot_log
    def go_to_fund_page_all_fund_page(self):
        self.perform_actions(START_FUND_PLAN)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_all_fund_page.FundPageAllFundPage(self.web_driver)

        return page
