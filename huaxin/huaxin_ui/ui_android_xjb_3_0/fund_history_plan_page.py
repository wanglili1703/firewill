# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.fund_plan_detail_page
FUND_PLAN = "xpath_//android.widget.TextView[contains(@text,'%s')]"


class FundHistoryPlanPage(PageObject):
    def __init__(self, web_driver):
        super(FundHistoryPlanPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('历史定投', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def verify_page_elements(self):
        self.assert_values('暂无历史定投', self.get_text('com.shhxzq.xjb:id/tv_empty_plan', 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def verify_fund_history_details(self, fund_product_name):
        fund_plan_name_content = self.get_text('com.shhxzq.xjb:id/tv_fund_plan_name', 'find_element_by_id')
        fund_plan_name = fund_plan_name_content.split('(')[0]
        fund_plan_amount_content = self.get_text('com.shhxzq.xjb:id/tv_fund_plan_amount', 'find_element_by_id')
        amount = filter(lambda ch: ch in '0123456789.', fund_plan_amount_content)

        self.assert_values(fund_product_name, fund_plan_name)
        self.assert_values(ASSERT_DICT['amount'], amount)
        self.assert_values('已终止', self.get_text('com.shhxzq.xjb:id/tv_fund_plan_day', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_fund_plan_detail_page(self, fund_product_name):
        self.perform_actions(FUND_PLAN % fund_product_name)

        page = huaxin_ui.ui_android_xjb_3_0.fund_plan_detail_page.FundPlanDetailPage(self.web_driver)
        return page
