# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log


class DhbHistoryProductPage(PageObject):
    def __init__(self, web_driver):
        super(DhbHistoryProductPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('历史产品', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_history_product_details(self):
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='产品期限']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='剩余额度']"))

        page = self
        return page
