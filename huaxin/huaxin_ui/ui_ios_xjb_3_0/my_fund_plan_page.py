# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_history_plan_page
import huaxin_ui.ui_ios_xjb_3_0.fund_plan_detail_page
import huaxin_ui.ui_ios_xjb_3_0.fund_page_all_fund_page

FUND_HISTORY_PLAN = "accId_UIAButton_查看历史定投"
ADD_FUND_PLAN = "accId_UIAButton_新增定投"
# SWIPE_BEGIN = "swipe_xpath_//"
# FUND_PLAN_STOP = "swipe_xpath_//android.widget.TextView[contains(@text,'%s')]"
FUND_PLAN = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@label,'%s')]"


class MyFundPlanPage(PageObject):
    def __init__(self, web_driver):
        super(MyFundPlanPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('我的定投计划', self.get_text("//UIAStaticText[@label='我的定投计划']"))

        page = self

        return page

    @robot_log
    def go_to_fund_history_plan_page(self):
        self.perform_actions(FUND_HISTORY_PLAN)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_history_plan_page.FundHistoryPlanPage(self.web_driver)

        return page

    @robot_log
    def view_my_fund_plan(self):
        if self.element_exist("您暂无制定定投计划", "find_element_by_accessibility_id"):
            self.assert_values('查看历史定投',
                               self.get_text('查看历史定投', "find_element_by_accessibility_id"))

        page = self

        return page

    @robot_log
    def go_to_fund_plan_detail_page(self, fund_product_name):
        # self.perform_actions(SWIPE_BEGIN, FUND_PLAN_STOP % fund_product_name, 'U')
        self.perform_actions(FUND_PLAN % fund_product_name)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_plan_detail_page.FundPlanDetailPage(self.web_driver)

        return page

    def add_fund_plan(self):
        self.perform_actions(ADD_FUND_PLAN)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_all_fund_page.FundPageAllFundPage(self.web_driver)

        return page
