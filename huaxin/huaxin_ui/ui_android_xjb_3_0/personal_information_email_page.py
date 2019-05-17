# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.personal_information_page

EMAIL = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/email_address_et']"
CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/bottom_bt']"


class PersonalInformationEmailPage(PageObject):
    def __init__(self, web_driver):
        super(PersonalInformationEmailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('常用邮箱', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def modify_email_address(self, email):
        self.perform_actions(EMAIL, email,
                             CONFIRM)

        page = huaxin_ui.ui_android_xjb_3_0.personal_information_page.PersonalInformationPage(self.web_driver)
        return page
