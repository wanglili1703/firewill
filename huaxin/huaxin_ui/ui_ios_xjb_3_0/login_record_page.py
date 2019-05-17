# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log


class LoginRecordPage(PageObject):
    def __init__(self, web_driver):
        super(LoginRecordPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values(True, self.element_exist('登录记录', 'find_element_by_accessibility_id'))

        page = self
        return page

    @robot_log
    def view_login_records(self):
        self.assert_values(True,
                           self.element_exist('(“yaoyanhua”的 iPhone)', 'find_element_by_accessibility_id'))

        page = self
        return page
