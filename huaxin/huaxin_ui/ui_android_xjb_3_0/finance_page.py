# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_3_0.finance_dqb_page import FinanceDqbPage
from huaxin_ui.ui_android_xjb_3_0.finance_high_end_page import FinanceHighEndPage
from huaxin_ui.ui_android_xjb_3_0.finance_hot_page import FinanceHotPage
import huaxin_ui.ui_android_xjb_3_0.all_products_page
import huaxin_ui.ui_android_xjb_3_0.finance_product_search_page

HOT = "xpath_//android.widget.TextView[@text='热门']"
DQB = "xpath_//android.widget.TextView[@text='定活宝']"
HIGH_END = "xpath_//android.widget.TextView[@text='高端']"

HOME = "xpath_//android.widget.RelativeLayout[1]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
FUND = "xpath_//android.widget.RelativeLayout[3]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
ASSETS = "xpath_//android.widget.RelativeLayout[5]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"

SEARCH_PRODUCT = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/iv_to_finproduct_search']"
SEARCH_INPUT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cet_search_tile']"
VIP_QUALIFIED = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_vip_qualified'][POP]"
SWIPE_BEGIN = "swipe_xpath_//"
ALL_PRODUCTS_BUTTON_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='查看全部产品']"
ALL_PRODUCTS = "xpath_//android.widget.TextView[@text='查看全部产品']"
SEARCH = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/iv_to_finproduct_search']"

current_page = []


class FinancePage(PageObject):
    def __init__(self, web_driver):
        super(FinancePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='热门']")))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='定活宝']")))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='高端']")))

        page = self
        return page

    @robot_log
    def go_to_hot_product_list_page(self):
        self.perform_actions(
            HOT
        )

        page = FinanceHotPage(self.web_driver)

        return page

    @robot_log
    def go_to_dqb_product_list_page(self):
        self.perform_actions(
            DQB,
            SEARCH_PRODUCT,
        )

        page = FinanceDqbPage(self.web_driver)

        return page

    @robot_log
    def go_to_dqb_product_list_page_(self):
        self.perform_actions(DQB)

        page = FinanceDqbPage(self.web_driver)

        return page

    @robot_log
    def go_to_high_end_product_list_page(self):
        self.perform_actions(
            HIGH_END,
            VIP_QUALIFIED
        )

        page = FinanceHighEndPage(self.web_driver)

        return page

    @robot_log
    def go_to_finance_product_search_page(self):
        self.perform_actions(SEARCH)

        page = huaxin_ui.ui_android_xjb_3_0.finance_product_search_page.FinanceProductSearchPage(
            self.web_driver)

        return page

    @robot_log
    def go_to_all_products_page(self):
        self.perform_actions(
            SWIPE_BEGIN, ALL_PRODUCTS_BUTTON_SWIPE_STOP, 'U',
            ALL_PRODUCTS
        )

        page = huaxin_ui.ui_android_xjb_3_0.all_products_page.AllProductsPage(self.web_driver)
        return page

    @robot_log
    def go_to_finance_product_search_page(self):
        self.perform_actions(SEARCH)

        page = huaxin_ui.ui_android_xjb_3_0.finance_product_search_page.FinanceProductSearchPage(
            self.web_driver)

        return page

