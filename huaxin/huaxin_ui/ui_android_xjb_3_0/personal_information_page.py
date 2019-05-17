# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.personal_information_email_page
import huaxin_ui.ui_android_xjb_3_0.personal_information_address_page

EMAIL = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/user_email_tv']"
ADDRESS = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/user_address_tv']"
HEADER = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/user_header_icon']"
CAMERA = "xpath_//android.widget.TextView[@text='图库']"
ALBUM = "xpath_//android.widget.TextView[@text='相册']"
PHOTO = "xpath_//android.widget.TextView[@resource-id='com.miui.gallery:id/pick_num_indicator']"
PHOTO_COMPLETE = "xpath_//android.widget.TextView[@text='完成']"
SYSTEM_ALLOW = "xpath_//android.widget.Button[@text='允许']"


class PersonalInformationPage(PageObject):
    def __init__(self, web_driver, device_id=None):
        super(PersonalInformationPage, self).__init__(web_driver, device_id)

    @robot_log
    def verify_page_title(self):
        self.assert_values('个人信息', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def modify_personal_photo(self):
        self.perform_actions(HEADER)

        if self.device_id == 'ac3997d9':
            self.perform_actions(
                # SYSTEM_ALLOW,
                # SYSTEM_ALLOW,
                CAMERA,
                # ALBUM,
                PHOTO,
                PHOTO_COMPLETE)

        page = self
        return page

    @robot_log
    def go_to_email_page(self):
        self.perform_actions(EMAIL)

        page = huaxin_ui.ui_android_xjb_3_0.personal_information_email_page.PersonalInformationEmailPage(
            self.web_driver)
        return page

    @robot_log
    def go_to_address_page(self):
        self.perform_actions(ADDRESS)

        page = huaxin_ui.ui_android_xjb_3_0.personal_information_address_page.PersonalInformationAddessPage(
            self.web_driver)
        return page

    @robot_log
    def verify_personal_information_details(self, email, address):
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='头像']"))
        # self.assert_values(True, self.element_exist("//android.widget.TextView[@text='姓名']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='常用邮箱']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='常用地址']"))
        self.assert_values(email, self.get_text('com.shhxzq.xjb:id/user_email_tv', 'find_element_by_id'))
        self.assert_values(address, self.get_text('com.shhxzq.xjb:id/user_address_tv', 'find_element_by_id'))

        page = self
        return page
