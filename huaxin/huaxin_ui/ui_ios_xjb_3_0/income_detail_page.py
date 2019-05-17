# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

current_page = []


class IncomeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(IncomeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_income_detail_page(self, title):
        actual = self.get_text("//UIAButton[@label='%s']" % title)

        self.assert_values(title, actual)
