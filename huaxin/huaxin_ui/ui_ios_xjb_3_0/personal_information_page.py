# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.personal_information_email_page
import huaxin_ui.ui_ios_xjb_3_0.personal_information_address_page

# EMAIL = "xpathIOS_UIAStaticText_//UIAStaticText[@label='常用邮箱']/following-sibling::UIAStaticText"
EMAIL = "accId_UIAStaticText_(常用邮箱)"
ADDRESS = "accId_UIAStaticText_(常用地址)"
HEADER = "xpathIOS_UIAStaticText_//UIAStaticText[@label='头像']"
CAMERA = "accId_UIAButton_拍照"
CANCEL = "accId_UIAButton_取消"
ALBUM = "accId_UIAButton_图库"
PHOTO = "axis_IOS_月"
RECENTLY = "accId_UIATableCell_屏幕快照"
PHOTO_COMPLETE = "accId_UIAButton_完成"


class PersonalInformationPage(PageObject):
    def __init__(self, web_driver, device_id=None):
        super(PersonalInformationPage, self).__init__(web_driver, device_id)

    @robot_log
    def verify_at_personal_information_page(self):
        self.assert_values('个人信息', self.get_text("//UIAStaticText[@label='个人信息']"))

        page = self
        return page

    @robot_log
    def modify_personal_photo(self):
        self.perform_actions(HEADER)

        self.perform_actions(
            ALBUM,
            RECENTLY,
            PHOTO,
            PHOTO_COMPLETE)

        page = self
        return page

    @robot_log
    def go_to_email_page(self):
        self.perform_actions(EMAIL)

        page = huaxin_ui.ui_ios_xjb_3_0.personal_information_email_page.PersonalInformationEmailPage(
            self.web_driver)
        return page

    @robot_log
    def go_to_address_page(self):
        self.perform_actions(ADDRESS)

        page = huaxin_ui.ui_ios_xjb_3_0.personal_information_address_page.PersonalInformationAddressPage(
            self.web_driver)
        return page

    @robot_log
    def verify_personal_information_details(self, email, address):
        self.assert_values(True, self.element_exist("//UIAStaticText[@label='头像']"))
        # self.assert_values(True, self.element_exist("//UIAStaticText[@label='姓名']"))
        self.assert_values(email, self.get_text("//UIAStaticText[@label='常用邮箱']/following-sibling::UIAStaticText"))
        self.assert_values(address, self.get_text("//UIAStaticText[@label='常用地址']/following-sibling::UIATextView"))

        page = self
        return page
