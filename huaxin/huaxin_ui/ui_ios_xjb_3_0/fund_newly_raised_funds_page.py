# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail

FUND = "accId_UIAStaticText_%s"


class FundNewlyRaisedFundsPage(PageObject):
    def __init__(self, web_driver):
        super(FundNewlyRaisedFundsPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values(True, self.element_exist('新发基金', 'find_element_by_accessibility_id'))

        page = self
        return page

    @robot_log
    def verify_newly_raised_fund_details(self, product_name):
        self.assert_values(True, self.element_exist(product_name, 'find_element_by_accessibility_id'))

        page = self
        return page

    @robot_log
    def go_to_fund_detail_page(self, product_name):
        self.perform_actions(FUND % product_name)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)
        return page
