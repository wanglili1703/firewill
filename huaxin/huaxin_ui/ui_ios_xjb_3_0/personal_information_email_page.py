# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.personal_information_page

EMAIL = "xpathIOS_UIATextView_//UIATextView"
CONFIRM = "accId_UIAButton_确定"


class PersonalInformationEmailPage(PageObject):
    def __init__(self, web_driver):
        super(PersonalInformationEmailPage, self).__init__(web_driver)

    @robot_log
    def verify_at_personal_email_page(self):
        self.assert_values('邮箱', self.get_text("//UIAStaticText[@label='邮箱']"))

        page = self
        return page

    @robot_log
    def modify_email_address(self, email):
        self.perform_actions(EMAIL, email,
                             CONFIRM)

        page = huaxin_ui.ui_ios_xjb_3_0.personal_information_page.PersonalInformationPage(self.web_driver)
        return page
