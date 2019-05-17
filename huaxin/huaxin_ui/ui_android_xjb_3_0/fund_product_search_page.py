# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_android_xjb_3_0.fund_selected_page
import huaxin_ui.ui_android_xjb_3_0.fund_page
import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail
import time

FUND_PRODUCT_INPUT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cet_search_tile']"
FUND_PRODUCT = "xpath_//android.widget.TextView[contains(@text,'%s')]"
FUND_PRODUCT_NAME = "xpath_//android.widget.TextView[@text='%s%s']"
BACK = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
CANCEL = "xpath_//android.widget.TextView[@text='取消']"
FUND = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_fund_name']"


class FundProductSearchPage(PageObject):
    def __init__(self, web_driver):
        super(FundProductSearchPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('基金代码/简拼/重仓资产', self.get_text('com.shhxzq.xjb:id/cet_search_tile', 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def search_fund_products(self, fund_product_name, fund_product_code=None):
        self.perform_actions(FUND_PRODUCT_INPUT, fund_product_name,
                             FUND_PRODUCT_NAME % (fund_product_name, fund_product_code))

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page

    @robot_log
    def back_to_fund_selected_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.fund_selected_page.FundSelectedPage(self.web_driver)

        return page

    @robot_log
    def search_fund_products_with_names(self, fund_product_name):
        fund_product_name = fund_product_name.upper()
        self.perform_actions(FUND_PRODUCT_INPUT, fund_product_name)
        time.sleep(2)
        self.perform_actions(FUND_PRODUCT % fund_product_name)

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)
        return page

    @robot_log
    def fund_product_search_with_code(self, fund_product_code):
        self.perform_actions(FUND_PRODUCT_INPUT, fund_product_code)
        time.sleep(2)
        self.perform_actions(FUND_PRODUCT % fund_product_code)

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)
        return page

    @robot_log
    def back_to_fund_page(self):
        self.perform_actions(CANCEL)

        page = huaxin_ui.ui_android_xjb_3_0.fund_page.FundPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_detail_page(self):
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='基金']"))
        self.perform_actions(FUND)

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)
        return page
