# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.finance_product_search_page
import huaxin_ui.ui_android_xjb_3_0.fund_product_search_page

SWIPE_START = "swipe_xpath_//"
SEARCH_BAR = "xpath_//android.widget.EditText[@text='高端理财/定活宝/基金']"
SEARCH_STOP = "swipe_xpath_//android.widget.TextView[@text='基金']"
VIEW_MORE = "xpath_//android.widget.TextView[@text='%s']/following-sibling::android.widget.FrameLayout[1]/android.widget.TextView[@text='查看更多']"
VIEW_MORE_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']/following-sibling::android.widget.FrameLayout[1]/android.widget.TextView[@text='查看更多']"

class GlobalSearchPage(PageObject):
    def __init__(self, web_driver):
        super(GlobalSearchPage, self).__init__(web_driver)
        self._return_page = {
            'FinanceProductSearchPage': huaxin_ui.ui_android_xjb_3_0.finance_product_search_page.FinanceProductSearchPage(
                self.web_driver),
            'FundProductSearchPage': huaxin_ui.ui_android_xjb_3_0.fund_product_search_page.FundProductSearchPage(
                self.web_driver)}

    @robot_log
    def global_search(self, product):
        self.perform_actions(SEARCH_BAR, product)

        page = self
        return page

    @robot_log
    def verify_search_result(self):
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='高端理财']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='定活宝']"))
        self.perform_actions(SWIPE_START, SEARCH_STOP, 'U')
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='基金']"))

        page = self
        return page

    @robot_log
    def search_view_more_result(self, product_type, return_page):
        self.perform_actions(SWIPE_START, VIEW_MORE_STOP % product_type, 'U')
        self.perform_actions(VIEW_MORE % product_type)

        page = self._return_page[return_page]
        return page

