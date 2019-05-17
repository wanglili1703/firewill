# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

current_page = []


class MessageDetailPage(PageObject):
    def __init__(self, web_driver):
        super(MessageDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_message_detail_page(self):
        self.assert_values('理财消息', self.get_text("//UIAStaticText[@label='理财消息']"))

        page = self

        return page
