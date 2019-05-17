# coding: utf-8
import time

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_2_0.finance_dqb_page import FinanceDqbPage
from huaxin_ui.ui_ios_xjb_2_0.finance_high_end_page import FinanceHighEndPage
from huaxin_ui.ui_ios_xjb_2_0.finance_hot_page import FinanceHotPage

HOT = "accId_UIAStaticText_热门"
DQB = "accId_UIAStaticText_定期"
HIGH_END = "accId_UIAStaticText_高端"

HOME = "accId_UIAButton_(UITabBarButton_)"
FUND = "accId_UIAButton_(UITabBarButton_item_2)"
ASSETS = "accId_UIAButton_(UITabBarButton_item_3)"

SEARCH_PRODUCT = "accId_UIAButton_UIBarButtonItemLocationRight"
SEARCH_INPUT = "accId_UIASearchBar_(searchField)产品名称/简拼"

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
    def finance_product_search(self, product_name):
        self.perform_actions(
            SEARCH_PRODUCT,
            SEARCH_INPUT, product_name,
        )
