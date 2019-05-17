# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_3_0.finance_dqb_page import FinanceDqbPage
from huaxin_ui.ui_android_xjb_3_0.finance_high_end_page import FinanceHighEndPage

CATEGORY_TITLE_DQB = "xpath_//android.widget.TextView[contains(@text,'定活宝')]"
CATEGORY_TITLE_HIGH_END = "xpath_//android.widget.TextView[contains(@text,'高端理财')]"

CATEGORY_TITLE_HIGH_END_START = "swipe_xpath_//android.widget.TextView[@text='热门']"
CATEGORY_TITLE_HIGH_END_STOP = "swipe_xpath_//android.widget.TextView[contains(@text,'高端理财')]"

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

        return page

    @robot_log
    def hot_switch_to_high_end_product_list_page(self):
        self.perform_actions(
            CATEGORY_TITLE_HIGH_END_START, CATEGORY_TITLE_HIGH_END_STOP, 'U',
            CATEGORY_TITLE_HIGH_END,
        )

        page = FinanceHighEndPage(self.web_driver)

        return page
