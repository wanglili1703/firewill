# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_3_0.invite_friend_page import InviteFriendPage
from huaxin_ui.ui_android_xjb_3_0.personal_setting_page import PersonalSettingPage
from huaxin_ui.ui_android_xjb_3_0.reservation_code_page import ReservationCodePage
from huaxin_ui.ui_android_xjb_3_0.security_center_page import SecurityCenterPage

IDENTIFIER = "xpath_//android.widget.TextView[@text='个人中心']"
INVITE_FRIEND = "xpath_//android.widget.TextView[@text='邀请好友']"
SECURITY_CENTER = "xpath_//android.widget.TextView[@text='安全中心']"
RESERVATION_CODE = "xpath_//android.widget.TextView[@text='预约码']"
SETTINGS_BUTTON = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"

current_page = []


class PersonalCenterPage(PageObject):
    def __init__(self, web_driver):
        super(PersonalCenterPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_security_center_page(self):
        self.perform_actions(SECURITY_CENTER)
        page = SecurityCenterPage(self.web_driver)

        return page

    @robot_log
    def go_to_personal_setting_page(self):
        self.perform_actions(SETTINGS_BUTTON)
        page = PersonalSettingPage(self.web_driver)

        return page

    @robot_log
    def go_to_invite_friend_page(self):
        self.perform_actions(INVITE_FRIEND)

        page = InviteFriendPage(self.web_driver)

        return page

    @robot_log
    def go_to_reservation_code_page(self):
        self.perform_actions(RESERVATION_CODE)

        page = ReservationCodePage(self.web_driver)

        return page
