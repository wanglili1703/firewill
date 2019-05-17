# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.personal_information_page

REGION = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/user_area_tv']"
ADDRESS = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/user_street_address_et']"
CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/bottom_bt']"
SWIPE_BEGIN = "swipe_xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/city_lv']"
ADDRESS_COMPLETE = "xpath_//android.widget.TextView[@text='完成']"
SCROLL = "swipe_xpath_//scroll_1"


class PersonalInformationAddessPage(PageObject):
    def __init__(self, web_driver):
        super(PersonalInformationAddessPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('常用地址', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def modify_residential_address(self, address):
        self.perform_actions(REGION,
                             SWIPE_BEGIN, SCROLL, 'U',
                             ADDRESS_COMPLETE,
                             ADDRESS, address,
                             CONFIRM)

        page = huaxin_ui.ui_android_xjb_3_0.personal_information_page.PersonalInformationPage(self.web_driver)
        return page
