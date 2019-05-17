# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.product_detail_page

SWIPE_BEGIN = "swipe_xpath_//"
HIGH_END_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
HIGH_END_PRODUCT = "xpath_//android.widget.TextView[@text='%s']"
current_page = []


class FinanceHighEndCashManagementPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceHighEndCashManagementPage, self).__init__(web_driver)

    @robot_log
    def verify_at_cash_management_series_page(self):
        self.assert_values("现金管理系列", self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
        self.assert_values(True,
                           self.element_exist('com.shhxzq.xjb:id/financial_item_income_type', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def go_to_product_detail_page(self, product_name):
        self.perform_actions(SWIPE_BEGIN, HIGH_END_PRODUCT_STOP % product_name, 'U',
                             HIGH_END_PRODUCT % product_name, )

        page = huaxin_ui.ui_android_xjb_3_0.product_detail_page.ProductDetailPage(
            self.web_driver)

        return page
