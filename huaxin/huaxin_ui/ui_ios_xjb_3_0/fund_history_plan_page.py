# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_plan_detail_page

FUND_PLAN = "accId_UIAStaticText_%s(%s)"


class FundHistoryPlanPage(PageObject):
    def __init__(self, web_driver):
        super(FundHistoryPlanPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('历史定投', self.get_text("//UIAStaticText[@label='历史定投']"))
        page = self

        return page

    @robot_log
    def verify_page_elements(self):
        self.assert_values('暂无历史定投', self.get_text('(暂无历史定投)', 'find_element_by_accessibility_id'))
        page = self

        return page

    @robot_log
    def verify_fund_history_details(self, fund_product_name):
        fund_plan_name_content = self.get_text("//UIAStaticText[contains(@label,'%s')]" % fund_product_name)
        fund_plan_name = fund_plan_name_content.split('(')[0]
        # fund_plan_amount_content = self.get_text('com.shhxzq.xjb:id/tv_fund_plan_amount', 'find_element_by_id')
        # amount = filter(lambda ch: ch in '0123456789.', fund_plan_amount_content)

        self.assert_values(fund_product_name, fund_plan_name)
        # self.assert_values(ASSERT_DICT['amount'], amount)
        # self.assert_values('已终止', self.get_text('com.shhxzq.xjb:id/tv_fund_plan_day', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_fund_plan_detail_page(self, fund_product_name, fund_product_code):
        self.perform_actions(FUND_PLAN % (fund_product_name, fund_product_code))

        page = huaxin_ui.ui_ios_xjb_3_0.fund_plan_detail_page.FundPlanDetailPage(self.web_driver)
        return page
