# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.pledge_repay_history_detail_page

PLEDGE_PRODUCT_NAME = "//android.widget.TextView[contains(@text,'%s')]/following-sibling::android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_title_name_sub']"
PLEDGE_PRODUCT = "xpath_//android.widget.TextView[contains(@text,'%s')]"


class PledgeHistoryPage(PageObject):
    def __init__(self, web_driver):
        super(PledgeHistoryPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('历史记录', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_pledge_repay_status(self, product_name):
        self.assert_values('已还款', self.get_text(PLEDGE_PRODUCT_NAME % product_name))

        page = self
        return page

    @robot_log
    def go_to_pledge_repay_history_detail_page(self, product_name):
        self.perform_actions(PLEDGE_PRODUCT % product_name)

        page = huaxin_ui.ui_android_xjb_3_0.pledge_repay_history_detail_page.PledgeRepayHistoryDetailPage(
            self.web_driver)
        return page
