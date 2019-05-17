# coding: utf-8
import time

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_3_0.finance_dqb_page import FinanceDqbPage
from huaxin_ui.ui_ios_xjb_3_0.finance_high_end_page import FinanceHighEndPage
from huaxin_ui.ui_ios_xjb_3_0.finance_hot_page import FinanceHotPage
import huaxin_ui.ui_ios_xjb_3_0.product_detail_page
import huaxin_ui.ui_ios_xjb_3_0.all_products_page

HOT = "accId_UIAStaticText_(热门)"
DQB = "accId_UIAStaticText_(定活宝)"
HIGH_END = "accId_UIAStaticText_高端"

HOME = "accId_UIAButton_(UITabBarButton_)"
FUND = "accId_UIAButton_(UITabBarButton_item_2)"
ASSETS = "accId_UIAButton_(UITabBarButton_item_3)"

SEARCH_PRODUCT = "accId_UIAButton_UIBarButtonItemLocationRight"
SEARCH_INPUT = "accId_UIASearchBar_产品名称/简拼"
PRODUCT_NAME = "accId_UIAStaticText_%s"
ALL_PRODUCTS = "accId_UIAButton_查看全部产品"

current_page = []


class FinancePage(PageObject):
    def __init__(self, web_driver):
        super(FinancePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

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
            DQB
        )

        page = FinanceDqbPage(self.web_driver)

        return page

    @robot_log
    def go_to_high_end_product_list_page(self):
        self.perform_actions(
            HIGH_END
        )

        page = FinanceHighEndPage(self.web_driver)

        return page

    @robot_log
    # 高端理财/定活宝/产品详情 prd_tag=0,1,2
    def finance_product_search(self, product_name, prd_tag):
        page = None

        self.perform_actions(
            SEARCH_PRODUCT,
            SEARCH_INPUT, product_name,
            PRODUCT_NAME % product_name,
        )

        if prd_tag == 0:
            page = FinanceHighEndPage(self.web_driver)

        elif prd_tag == 1:
            page = FinanceDqbPage(self.web_driver)
        elif prd_tag == 2:
            page = huaxin_ui.ui_ios_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_all_products_page(self):
        self.perform_actions(ALL_PRODUCTS)

        page = huaxin_ui.ui_ios_xjb_3_0.all_products_page.AllProductsPage(self.web_driver)
        return page
