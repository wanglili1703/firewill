# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools

current_page = []


class FinanceDqbHistoryPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceDqbHistoryPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_dhb_history_page(self):
        self.assert_values("历史产品", self.get_text("//UIAStaticText[@label='历史产品']"))
        self.assert_values(True, self.element_exist("(已售罄)", "find_element_by_accessibility_id"))
