# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_2_0.finance_dqb_page import FinanceDqbPage
from huaxin_ui.ui_android_xjb_2_0.finance_high_end_page import FinanceHighEndPage
from huaxin_ui.ui_android_xjb_2_0.finance_hot_page import FinanceHotPage

HOT = "xpath_//android.widget.TextView[@text='热门']"
DQB = "xpath_//android.widget.TextView[@text='定期']"
HIGH_END = "xpath_//android.widget.TextView[@text='高端']"

HOME = "xpath_//android.widget.RelativeLayout[1]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
FUND = "xpath_//android.widget.RelativeLayout[3]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
ASSETS = "xpath_//android.widget.RelativeLayout[5]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
# ASSETS = "xpath_//android.widget.RelativeLayout[4]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"

SEARCH_PRODUCT = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/iv_to_finproduct_search']"
# SEARCH_INPUT = "xpath_//android.widget.EditText[@text='产品名称/简拼']"
SEARCH_INPUT = "xpath_//android.widget.EditText[@text='基金代码/简拼/重仓资产']"

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
