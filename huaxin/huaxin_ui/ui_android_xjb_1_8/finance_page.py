# coding: utf-8
from _common.page_object import PageObject

IDENTIFIER = "xpath_//android.widget.TextView[@text='热门']"
HOT_TITLE = "xpath_//android.widget.TextView[@text='热门']"
REGULAR_TITLE = "xpath_//android.widget.TextView[@text='定期']"
HIGH_END_TITLE = "xpath_//android.widget.TextView[@text='高端']"
FUND_TITLE = "xpath_//android.widget.TextView[@text='基金']"
AGREEMENT = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_vip_qualified']"

current_page = []


class FinancePage(PageObject):
    def __init__(self, web_driver):
        super(FinancePage, self).__init__(web_driver)
        self.elements_exist(*current_page)
