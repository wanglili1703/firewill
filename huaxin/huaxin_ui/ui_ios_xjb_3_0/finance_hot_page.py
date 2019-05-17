# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_3_0.finance_dqb_page import FinanceDqbPage
import huaxin_ui.ui_ios_xjb_3_0.finance_high_end_page

CATEGORY_TITLE_DQB = "accId_UIAStaticText_(定活宝)"
CATEGORY_TITLE_HIGH_END = "accId_UIAStaticText_(高端)"

CATEGORY_TITLE_HIGH_END_START = "swipe_accId_UIAStaticText_(热门)"
CATEGORY_TITLE_HIGH_END_STOP = "swipe_accId_UIAStaticText_(高端理财)"

current_page = []


class FinanceHotPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceHotPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def hot_switch_to_dqb_product_list_page(self):
        self.perform_actions(
            CATEGORY_TITLE_DQB,
        )

        page = FinanceDqbPage(self.web_driver)
        page.verify_at_dhb_page()

        return page

    @robot_log
    def hot_switch_to_high_end_product_list_page(self):
        self.perform_actions(
            # CATEGORY_TITLE_HIGH_END_START, CATEGORY_TITLE_HIGH_END_STOP, 'U',
            CATEGORY_TITLE_HIGH_END
        )

        page = huaxin_ui.ui_ios_xjb_3_0.finance_high_end_page.FinanceHighEndPage(self.web_driver)
        page.verify_at_high_end_page()

        return page
