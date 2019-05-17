# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_3_0.setting_login_password_page import SettingLoginPasswordPage
from huaxin_ui.ui_ios_xjb_3_0.setting_trade_password_page import SettingTradePasswordPage
import huaxin_ui.ui_ios_xjb_3_0.personal_setting_page
import huaxin_ui.ui_ios_xjb_3_0.login_record_page

LOGIN_PASSWORD_BUTTON = "accId_UIAStaticText_登录密码"
TRADE_PASSWORD_BUTTON = "accId_UIAStaticText_交易密码"
LOGIN_METHOD = "accId_UIAStaticText_登录方式"
SWITCH = "xpathIOS_UIASwitch_//UIASwitch"
BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
CONFIRM = "accId_UIAButton_确认"
TRADE_PASSWORD = "xpathIOS_UIATextField_//UIATextField"
LOGIN_RECORD_STOP = "swipe_accId_登录记录"
LOGIN_RECORD = "accId_UIAButton_登录记录"

current_page = []


class SecurityCenterPage(PageObject):
    def __init__(self, web_driver):
        super(SecurityCenterPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_security_center_page(self):
        self.assert_values('安全中心', self.get_text("//UIAStaticText[@label='安全中心']"))

    @robot_log
    def go_to_setting_login_password_page(self):
        self.perform_actions(LOGIN_PASSWORD_BUTTON)
        page = SettingLoginPasswordPage(self.web_driver)

        return page

    @robot_log
    def go_to_setting_trade_password_page(self):
        self.perform_actions(TRADE_PASSWORD_BUTTON)
        page = SettingTradePasswordPage(self.web_driver)

        return page

    # flag = 1: 开启
    # flag = 0: 关闭
    @robot_log
    def change_login_method(self, trade_password=None, flag=1):
        self.perform_actions(LOGIN_METHOD)
        self.assert_values(True, self.element_exist('登录方式', 'find_element_by_accessibility_id'))
        if flag == 0:
            # 关闭短信验证码
            self.perform_actions(SWITCH,
                                 CONFIRM)
        elif flag == 1:
            # 开启短信验证码
            self.perform_actions(SWITCH,
                                 TRADE_PASSWORD, trade_password)

        self.perform_actions(BACK)
        page = self
        return page

    @robot_log
    def back_to_settings_page(self):
        self.perform_actions(BACK)
        page = huaxin_ui.ui_ios_xjb_3_0.personal_setting_page.PersonalSettingPage(self.web_driver)
        return page

    @robot_log
    def go_to_login_record_page(self):
        self.perform_actions("swipe_accId_//", LOGIN_RECORD_STOP, 'U')
        self.perform_actions(LOGIN_RECORD)

        page = huaxin_ui.ui_ios_xjb_3_0.login_record_page.LoginRecordPage(self.web_driver)
        return page