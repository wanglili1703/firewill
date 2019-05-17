# coding=utf-8
from _common.page_object import PageObject


current_page = []


class FundPageAllFundPage(PageObject):
    def __init__(self, web_driver):
        super(FundPageAllFundPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
