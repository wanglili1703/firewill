# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.message_detail_page

MESSAGE = "xpathIOS_UIAStaticText_//UIAStaticText[@label='理财消息']"
current_page = []


class MessageCenterPage(PageObject):
    def __init__(self, web_driver):
        super(MessageCenterPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def view_message(self):
        self.assert_values('精选活动', self.get_text('(精选活动)', 'find_element_by_accessibility_id'))

        self.open_message()
        page = huaxin_ui.ui_ios_xjb_3_0.message_detail_page.MessageDetailPage(self.web_driver)

        page.verify_at_message_detail_page()

        return page

    @robot_log
    def open_message(self):
        self.perform_actions(MESSAGE)
