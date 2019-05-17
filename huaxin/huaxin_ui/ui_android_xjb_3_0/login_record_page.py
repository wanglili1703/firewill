# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log


class LoginRecordPage(PageObject):
    def __init__(self, web_driver):
        super(LoginRecordPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('登录记录', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def view_login_records(self, device_id):
        if device_id == '7N2TDM1557021079':
            self.assert_values('荣耀 6', self.get_text('com.shhxzq.xjb:id/tv_login_record_device', 'find_element_by_id'))
        elif device_id == 'ac3997d9':
            self.assert_values('小米手机5', self.get_text('com.shhxzq.xjb:id/tv_login_record_device', 'find_element_by_id'))

        self.assert_values('中国 上海 黄浦区',
                           self.get_text('com.shhxzq.xjb:id/tv_login_record_location', 'find_element_by_id'))

        page = self
        return page
