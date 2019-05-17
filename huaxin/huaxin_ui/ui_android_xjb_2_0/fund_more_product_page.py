# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

FUND_PRODUCT_TYPE_ALL = "xpath_//android.widget.TextView[@text='全部']"
FUND_PRODUCT_TYPE_STOCK = "xpath_//android.widget.TextView[@text='股票型']"
FUND_PRODUCT_TYPE_MONETARY = "xpath_//android.widget.TextView[@text='货币型']"
FUND_PRODUCT_TYPE_BOND = "xpath_//android.widget.TextView[@text='债券型']"
FUND_PRODUCT_TYPE_MIXED = "xpath_//android.widget.TextView[@text='混合型']"
FUND_PRODUCT_TYPE_QDII = "xpath_//android.widget.TextView[@text='QDII']"
FUND_PRODUCT_TYPE_OTHER = "xpath_//android.widget.TextView[@text='其他']"

current_page = []


class FundMoreProductPage(PageObject):
    def __init__(self, web_driver):
        super(FundMoreProductPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def view_fund_more_product(self):
        self.perform_actions(
            FUND_PRODUCT_TYPE_ALL,
            FUND_PRODUCT_TYPE_STOCK,
            FUND_PRODUCT_TYPE_MONETARY,
            FUND_PRODUCT_TYPE_BOND,
            FUND_PRODUCT_TYPE_MIXED,
            FUND_PRODUCT_TYPE_QDII,
            FUND_PRODUCT_TYPE_OTHER,
        )
