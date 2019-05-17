# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_history_plan_page
import huaxin_ui.ui_android_xjb_3_0.fund_plan_detail_page
import huaxin_ui.ui_android_xjb_3_0.fund_page_all_fund_page
import time

FUND_HISTORY_PLAN_NOT_EMPTY = "xpath_//android.widget.TextView[@text='查看历史定投']"
FUND_HISTORY_PLAN = "xpath_//android.widget.TextView[@text='您暂无制定定投计划']/following-sibling::android.widget.RelativeLayout[1]/android.widget.TextView[@text='查看历史定投']"
SWIPE_BEGIN = "swipe_xpath_//"
FUND_HISTORY_PLAN_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='查看历史定投']"
FUND_PLAN_STOP = "swipe_xpath_//android.widget.TextView[contains(@text,'%s')]"
FUND_PLAN = "xpath_//android.widget.TextView[contains(@text,'%s')]"
ADD_FUND_PLAN = "xpath_//android.widget.TextView[@text='新增定投']"


class MyFundPlanPage(PageObject):
    def __init__(self, web_driver):
        super(MyFundPlanPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('我的定投计划', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_fund_history_plan_page(self, history_type='empty'):
        time.sleep(2)
        self.perform_actions(SWIPE_BEGIN, FUND_HISTORY_PLAN_SWIPE_STOP, 'U')
        if history_type == 'empty':
            self.perform_actions(FUND_HISTORY_PLAN)
        else:
            self.perform_actions(FUND_HISTORY_PLAN_NOT_EMPTY)

        page = huaxin_ui.ui_android_xjb_3_0.fund_history_plan_page.FundHistoryPlanPage(self.web_driver)

        return page

    @robot_log
    def view_my_fund_plan(self):
        if self.element_exist("//android.widget.TextView[@text='您暂无制定定投计划']"):
            self.assert_values('查看历史定投',
                               self.get_text('com.shhxzq.xjb:id/tv_fund_plan_empty_history', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_fund_plan_detail_page(self, fund_product_name):
        self.perform_actions(SWIPE_BEGIN, FUND_PLAN_STOP % fund_product_name, 'U')
        self.perform_actions(FUND_PLAN % fund_product_name)

        page = huaxin_ui.ui_android_xjb_3_0.fund_plan_detail_page.FundPlanDetailPage(self.web_driver)

        return page

    def add_fund_plan(self):
        self.perform_actions(ADD_FUND_PLAN)

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_all_fund_page.FundPageAllFundPage(self.web_driver)

        return page
