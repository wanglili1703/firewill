# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.pledge_repay_history_detail_page

PLEDGE_PRODUCT_NAME = "accId_UIAStaticText_%s"


class PledgeHistoryPage(PageObject):
    def __init__(self, web_driver):
        super(PledgeHistoryPage, self).__init__(web_driver)

    @robot_log
    def verify_at_pledge_repay_history_page(self):
        self.assert_values(True, self.element_exist("随心借", "find_element_by_accessibility_id"))

        page = self
        return page

    @robot_log
    def verify_pledge_repay_status(self, product_name):
        self.assert_values('已还款', self.get_text("已还款", "find_element_by_accessibility_id"))

        page = self
        return page

    @robot_log
    def go_to_pledge_repay_history_detail_page(self, product_name):
        self.perform_actions(PLEDGE_PRODUCT_NAME % product_name)

        page = huaxin_ui.ui_ios_xjb_3_0.pledge_repay_history_detail_page.PledgeRepayHistoryDetailPage(self.web_driver)
        return page
