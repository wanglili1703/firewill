# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.personal_information_page

REGION = "xpathIOS_UIAStaticText_//UIAStaticText[@label='所在地区']/following-sibling::UIAStaticText"
ADDRESS = "xpathIOS_UIATextView_//UIATextView"
CONFIRM = "accId_UIAButton_确定"
SWIPE_BEGIN = "swipe_accId_//"
ADDRESS_COMPLETE = "accId_UIAButton_完成"
SCROLL = "swipe_accId_scroll_1"


class PersonalInformationAddressPage(PageObject):
    def __init__(self, web_driver):
        super(PersonalInformationAddressPage, self).__init__(web_driver)

    @robot_log
    def verify_at_address_page(self):
        self.assert_values('地址', self.get_text("//UIAStaticText[@label='地址']"))

        page = self
        return page

    @robot_log
    def modify_residential_address(self, address):
        self.perform_actions(REGION,
                             SWIPE_BEGIN, SCROLL, 'U',
                             ADDRESS_COMPLETE,
                             ADDRESS, address,
                             CONFIRM)

        page = huaxin_ui.ui_ios_xjb_3_0.personal_information_page.PersonalInformationPage(self.web_driver)
        return page
