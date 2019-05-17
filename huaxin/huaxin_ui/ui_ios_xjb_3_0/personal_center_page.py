# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_3_0.invite_friend_page import InviteFriendPage
from huaxin_ui.ui_ios_xjb_3_0.personal_setting_page import PersonalSettingPage
from huaxin_ui.ui_ios_xjb_3_0.reservation_code_page import ReservationCodePage
from huaxin_ui.ui_ios_xjb_3_0.security_center_page import SecurityCenterPage

IDENTIFIER = "accId_UIAStaticText_个人中心"
INVITE_FRIEND = "axis_IOS_邀请好友"
# SECURITY_CENTER = "accId_UIAStaticText_安全中心"
SECURITY_CENTER = "axis_IOS_安全中心"
RESERVATION_CODE = "axis_IOS_预约码"
SETTINGS_BUTTON = "accId_UIAButton_icon setting"

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
