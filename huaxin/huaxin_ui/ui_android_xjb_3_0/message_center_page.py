# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

import huaxin_ui.ui_android_xjb_3_0.financing_message_page
FINANCING_MASSAGE = "xpath_//android.widget.TextView[@text='理财消息']"


class MessageCenterPage(PageObject):
    def __init__(self, web_driver):
        super(MessageCenterPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('消息中心', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def go_to_financing_message_page(self):
        self.perform_actions(FINANCING_MASSAGE)

        page = huaxin_ui.ui_android_xjb_3_0.financing_message_page.FinancingMessagePage(self.web_driver)
        return page
