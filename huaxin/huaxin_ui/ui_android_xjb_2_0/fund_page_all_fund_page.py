# coding=utf-8
from _common.page_object import PageObject

import huaxin_ui.ui_android_xjb_2_0.fund_page_fund_detail

current_page = []


class FundPageAllFundPage(PageObject):
    def __init__(self, web_driver):
        super(FundPageAllFundPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
