# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log


class FinancingMessagePage(PageObject):
    def __init__(self, web_driver):
        super(FinancingMessagePage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('理财消息', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def view_message(self):
        self.assert_values('暂无内容', self.get_text('com.shhxzq.xjb:id/tv_empty_text', 'find_element_by_id'))

        page = self
        return page
