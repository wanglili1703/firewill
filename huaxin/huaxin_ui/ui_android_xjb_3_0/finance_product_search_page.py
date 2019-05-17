# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.product_detail_page
import huaxin_ui.ui_android_xjb_3_0.home_page

INPUT_FUND_PRODUCT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cet_search_tile']"
DQB_PRODUCT_NAME = "xpath_//android.widget.TextView[contains(@text,'%s')]"
SEARCH_TITLE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_item_fin_search_title']"
PRODUCT = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_item_fin_search_title']"
CANCEL = "xpath_//android.widget.TextView[@text='取消']"


class FinanceProductSearchPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceProductSearchPage, self).__init__(web_driver)

    @robot_log
    def go_to_product_detail_page(self, product_name):
        self.perform_actions(INPUT_FUND_PRODUCT, product_name,
                             DQB_PRODUCT_NAME % product_name)

        page = huaxin_ui.ui_android_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)

        return page

    @robot_log
    def finance_product_search(self, product_name):
        self.perform_actions(
            INPUT_FUND_PRODUCT, product_name,
        )

        page = self

        return page

    @robot_log
    def verify_product_name_search_result(self, product_name, name_type=None):
        if name_type == 'full':
            self.assert_values(product_name,
                               self.get_text('com.shhxzq.xjb:id/tv_item_fin_search_title', 'find_element_by_id'))
        else:
            self.assert_values(True,
                               self.element_exist("//android.widget.TextView[contains(@text,'%s')]" % product_name))

        page = self
        return page

    @robot_log
    def go_to_product_detail_page_default_first(self, product):
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='%s']" % product))
        self.perform_actions(PRODUCT)

        page = huaxin_ui.ui_android_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)
        return page

    @robot_log
    def back_to_home_page(self):
        self.perform_actions(CANCEL)

        page = huaxin_ui.ui_android_xjb_3_0.home_page.HomePage(self.web_driver)
        return page
